import hashlib
import importlib.util
import json
import os
import sys
import types
from urllib.parse import parse_qs, urlparse


class ConditionalCheckFailedException(Exception):
    pass


class FakeDDB:
    exceptions = types.SimpleNamespace(ConditionalCheckFailedException=ConditionalCheckFailedException)

    def __init__(self):
        self.items = {}

    def put_item(self, TableName, Item):
        self.items[Item["pk"]["S"]] = Item

    def get_item(self, TableName, Key, ConsistentRead=False):
        item = self.items.get(Key["pk"]["S"])
        return {"Item": item} if item else {}

    def scan(self, **kwargs):
        return {"Items": [item for key, item in self.items.items() if key.startswith("SERVER#")]}

    def update_item(self, TableName, Key, UpdateExpression, ExpressionAttributeValues, ExpressionAttributeNames=None, ConditionExpression=None):
        key = Key["pk"]["S"]
        item = self.items.get(key)
        if ConditionExpression and item and item["tokenHash"] != ExpressionAttributeValues[":tokenHash"]:
            raise ConditionalCheckFailedException()
        if item is None:
            item = {"pk": {"S": key}, "missions": {"M": {}}}
            self.items[key] = item
        if ExpressionAttributeNames and "#mission" in ExpressionAttributeNames:
            item["missions"]["M"][ExpressionAttributeNames["#mission"]] = ExpressionAttributeValues[":mission"]
        for name, value in ExpressionAttributeValues.items():
            field = name[1:]
            if field not in {"mission", "empty"}:
                item[field] = value


fake_ddb = FakeDDB()
fake_boto3 = types.ModuleType("boto3")
fake_boto3.client = lambda name: fake_ddb
sys.modules["boto3"] = fake_boto3

admin_key = "a" * 64
registration_key = "r" * 64
os.environ.update(
    TABLE_NAME="test-table",
    ADMIN_KEY_HASH=hashlib.sha256(admin_key.encode()).hexdigest(),
    REGISTRATION_KEY_HASH=hashlib.sha256(registration_key.encode()).hexdigest(),
    SESSION_TTL_SECONDS="1800",
)

source_path = sys.argv[1]
spec = importlib.util.spec_from_file_location("progress_app", source_path)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


def event(route, body=None, headers=None, query=None):
    return {
        "routeKey": route,
        "body": json.dumps(body) if body is not None else None,
        "headers": headers or {},
        "queryStringParameters": query,
        "requestContext": {"domainName": "abc.execute-api.us-east-1.amazonaws.com", "stage": "$default"},
    }


server_id = "srv-0123456789abcdef"
server_token = "t" * 64
register_body = {
    "server_id": server_id,
    "server_token": server_token,
    "hostname": "ip-10-20-10-10",
    "account_id": "123456789012",
    "instance_id": "i-0123456789abcdef0",
    "lab_version": "v1.0.0",
}
assert app.handler(event("POST /register", register_body), None)["statusCode"] == 401
registered = app.handler(event("POST /register", register_body, {"X-JDU-Registration-Key": registration_key}), None)
assert registered["statusCode"] == 200
auth = {"Authorization": f"Bearer {server_token}"}
assert app.handler(event("POST /status", {"server_id": server_id}), None)["statusCode"] == 401
status = app.handler(event("POST /status", {"server_id": server_id}, auth), None)
assert json.loads(status["body"])["email_linked"] is False
assert "tokenHash" not in status["body"] and server_token not in status["body"]
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": "student@jdu.uz"}), None)["statusCode"] == 401
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": "bad\naddress"}, auth), None)["statusCode"] == 400
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": ""}, auth), None)["statusCode"] == 400
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": "student@example.test"}, auth), None)["statusCode"] == 400
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": "student@jdu.uz.evil"}, auth), None)["statusCode"] == 400
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": " Student@JDU.UZ "}, auth), None)["statusCode"] == 200
status = app.handler(event("POST /status", {"server_id": server_id}, auth), None)
assert json.loads(status["body"])["instance_id"] == register_body["instance_id"]
assert json.loads(status["body"])["email_linked"] is True
assert "student@jdu.uz" not in status["body"]
assert fake_ddb.items[f"SERVER#{server_id}"]["studentEmail"]["S"] == "student@jdu.uz"
# Anonymous instance bootstrap cannot erase/change the authenticated email link.
assert app.handler(event("POST /register", register_body, {"X-JDU-Registration-Key": registration_key}), None)["statusCode"] == 200
assert fake_ddb.items[f"SERVER#{server_id}"]["studentEmail"]["S"] == "student@jdu.uz"
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": "other@jdu.uz"}, {"Authorization": "Bearer wrong"}), None)["statusCode"] == 401
assert app.handler(
    event("POST /submit", {"server_id": server_id, "mission": "P7", "passed": 1, "total": 1}, {"Authorization": f"Bearer {server_token}"}),
    None,
)["statusCode"] == 400

submit_body = dict(register_body)
submit_body.pop("server_token")
submit_body.update(mission="M3", passed=1, total=2)
assert app.handler(event("POST /submit", submit_body, {"Authorization": "Bearer wrong"}), None)["statusCode"] == 401
submitted = app.handler(event("POST /submit", submit_body, {"Authorization": f"Bearer {server_token}"}), None)
assert submitted["statusCode"] == 200

for practice_body in [
    {"server_id": server_id, "mission": "P0", "passed": 6, "total": 6},
    {"server_id": server_id, "mission": "P1", "passed": 6, "total": 6},
    {"server_id": server_id, "mission": "P6U", "passed": 2, "total": 2},
    {"server_id": server_id, "mission": "P6C", "passed": 3, "total": 4},
]:
    assert app.handler(event("POST /submit", practice_body, {"Authorization": f"Bearer {server_token}"}), None)["statusCode"] == 200

m6_ubuntu = {
    "server_id": server_id,
    "mission": "M6U",
    "passed": 2,
    "total": 2,
}
m6_cloud = {
    "server_id": server_id,
    "mission": "M6C",
    "passed": 3,
    "total": 4,
}
assert app.handler(event("POST /submit", m6_ubuntu, {"Authorization": f"Bearer {server_token}"}), None)["statusCode"] == 200
assert app.handler(event("POST /submit", m6_cloud, {"Authorization": f"Bearer {server_token}"}), None)["statusCode"] == 200
stored_server = fake_ddb.items[f"SERVER#{server_id}"]
assert stored_server["hostname"]["S"] == register_body["hostname"]

session_response = app.handler(event("POST /admin/session", {}, {"X-JDU-Admin-Key": admin_key}), None)
assert session_response["statusCode"] == 200
session_url = json.loads(session_response["body"])["url"]
session_token = parse_qs(urlparse(session_url).query)["session"][0]
partial_dashboard = app.handler(event("GET /dashboard", query={"session": session_token}), None)
assert "Ubuntu 2/2" in partial_dashboard["body"]
assert "CloudShell 3/4" in partial_dashboard["body"]
assert "M6 5/6" in partial_dashboard["body"]
assert '<td class="done">P1<br>6/6</td>' in partial_dashboard["body"]
assert '<td class="partial"><strong>P6 5/6</strong>' in partial_dashboard["body"]
assert "Guided P1" not in partial_dashboard["body"] and "Challenge" not in partial_dashboard["body"]
expected_headers = ["P0", "P1", "M1", "P2", "M2", "P3", "M3", "P4", "M4", "P5", "M5", "P6", "M6", "M7"]
actual_headers = app.re.findall(r'<th scope=col>([PM][0-9])</th>', partial_dashboard["body"])
assert actual_headers == expected_headers
assert '<td class="done">P0<br>6/6</td>' in partial_dashboard["body"]
# Existing stored M0 reports remain visible under P0 until a new submission.
legacy_score = stored_server["missions"]["M"].pop("P0")
stored_server["missions"]["M"]["M0"] = legacy_score
legacy_dashboard = app.handler(event("GET /dashboard", query={"session": session_token}), None)
assert '<td class="done">P0<br>6/6</td>' in legacy_dashboard["body"]
legacy_body = {"server_id": server_id, "mission": "M0", "passed": 4, "total": 6}
assert app.handler(event("POST /submit", legacy_body, {"Authorization": f"Bearer {server_token}"}), None)["statusCode"] == 200
assert app.mission_score(stored_server["missions"]["M"], "P0")["passed"] == 4


m6_cloud["passed"] = 4
assert app.handler(event("POST /submit", m6_cloud, {"Authorization": f"Bearer {server_token}"}), None)["statusCode"] == 200
practice_p6_cloud = {"server_id": server_id, "mission": "P6C", "passed": 4, "total": 4}
assert app.handler(event("POST /submit", practice_p6_cloud, {"Authorization": f"Bearer {server_token}"}), None)["statusCode"] == 200
dashboard = app.handler(event("GET /dashboard", query={"session": session_token}), None)
assert dashboard["statusCode"] == 200
assert server_id in dashboard["body"]
assert "student@jdu.uz" in dashboard["body"]
assert "学生メール / Server ID" in dashboard["body"]
assert "自分のサーバー" not in dashboard["body"]
assert register_body["hostname"] not in dashboard["body"]
assert register_body["instance_id"] not in dashboard["body"]
assert "1/2" in dashboard["body"]
assert "Ubuntu 2/2" in dashboard["body"]
assert "CloudShell 4/4" in dashboard["body"]
assert "M6 6/6" in dashboard["body"]
assert '<td class="done"><strong>P6 6/6</strong>' in dashboard["body"]
assert '<td class="missing">P2<br>—</td>' in dashboard["body"]
assert "入力したメールの本人確認は行っていません" in dashboard["body"]
assert app.handler(event("GET /health"), None)["statusCode"] == 200
previous_m3_score = stored_server["missions"]["M"]["M3"].copy()
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": "updated@jdu.uz"}, auth), None)["statusCode"] == 200
assert stored_server["studentEmail"]["S"] == "updated@jdu.uz"
assert stored_server["missions"]["M"]["M3"] == previous_m3_score
updated_dashboard = app.handler(event("GET /dashboard", query={"session": session_token}), None)
assert "updated@jdu.uz" in updated_dashboard["body"]
assert "student@jdu.uz" not in updated_dashboard["body"]
print("PASS progress backend registration, authentication, submission, session, and dashboard")

# Student links are server-bound and must never become teacher credentials.
assert app.handler(event("POST /student/session", {"server_id": server_id}), None)["statusCode"] == 401
assert app.handler(event("POST /student/session", {"server_id": "srv-other1234"}, auth), None)["statusCode"] == 401
personal_session = app.handler(event("POST /student/session", {"server_id": server_id}, auth), None)
assert personal_session["statusCode"] == 200
personal_payload = json.loads(personal_session["body"])
assert personal_payload["expires_in_seconds"] == 900
assert server_token not in personal_payload["url"]
personal_token = parse_qs(urlparse(personal_payload["url"]).query)["session"][0]
other_record = {"pk": {"S": "SERVER#srv-other1234"}, "kind": {"S": "server"},
                "serverId": {"S": "srv-other1234"}, "studentEmail": {"S": "other@example.test"}, "missions": {"M": {}}}
fake_ddb.put_item(TableName="test-table", Item=other_record)
def forbidden_scan(**kwargs):
    raise AssertionError("Personal progress must not scan other students")
original_scan = fake_ddb.scan
fake_ddb.scan = forbidden_scan
personal_view = app.handler(event("GET /student/progress", query={"session": personal_token}), None)
assert personal_view["statusCode"] == 200
assert "P1" in personal_view["body"] and "M6 6/6" in personal_view["body"]
assert "登録メール / Server ID" in personal_view["body"]
assert "updated@jdu.uz" in personal_view["body"]
assert "自分のサーバー" not in personal_view["body"]
assert register_body["hostname"] not in personal_view["body"]
assert register_body["instance_id"] not in personal_view["body"]
assert app.re.findall(r'<th scope=col>([PM][0-9])</th>', personal_view["body"]) == expected_headers
for view in [personal_view, partial_dashboard]:
    assert not app.re.search(r'\bT[0-6]\b', view["body"])
    assert not app.re.search(r'\bM0\b', view["body"])

assert "other@example.test" not in personal_view["body"] and "srv-other1234" not in personal_view["body"]
assert "student@jdu.uz" not in personal_view["body"]
assert "tokenHash" not in personal_view["body"] and server_token not in personal_view["body"]
assert app.handler(event("GET /student/progress", query={"session": personal_token, "server_id": "srv-other1234"}), None)["statusCode"] == 403
assert app.handler(event("GET /dashboard", query={"session": personal_token}), None)["statusCode"] == 401
assert app.handler(event("GET /student/progress", query={"session": session_token}), None)["statusCode"] == 401
assert app.handler(event("GET /student/progress"), None)["statusCode"] == 401
assert app.handler(event("POST /submit", submit_body, {"Authorization": "Bearer " + personal_token}), None)["statusCode"] == 401
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": "evil@jdu.uz"}, {"Authorization": "Bearer " + personal_token}), None)["statusCode"] == 401
assert app.handler(event("POST /admin/session", {}, {"X-JDU-Admin-Key": personal_token}), None)["statusCode"] == 401
session_record = fake_ddb.items["STUDENT_SESSION#" + app.digest(personal_token)]
session_record["expiresAt"] = {"N": str(int(app.time.time()) - 1)}
assert app.handler(event("GET /student/progress", query={"session": personal_token}), None)["statusCode"] == 401
session_record["expiresAt"] = {"N": str(int(app.time.time()) + 900)}
session_record["serverTokenHash"] = {"S": "changed-token-hash"}
assert app.handler(event("GET /student/progress", query={"session": personal_token}), None)["statusCode"] == 401
fake_ddb.scan = original_scan
assert app.handler(event("GET /dashboard", query={"session": session_token}), None)["statusCode"] == 200
print("PASS personal progress isolation, read-only scope, expiry, and credential revocation")

app.REGISTRATION_KEY_HASH = hashlib.sha256(("n" * 64).encode()).hexdigest()
assert app.handler(event("POST /register", register_body, {"X-JDU-Registration-Key": registration_key}), None)["statusCode"] == 401
assert app.handler(event("POST /register", register_body, {"X-JDU-Registration-Key": "n" * 64}), None)["statusCode"] == 200
assert app.handler(event("POST /status", {"server_id": server_id}, auth), None)["statusCode"] == 200
assert app.handler(event("POST /submit", submit_body, auth), None)["statusCode"] == 200
assert app.handler(event("POST /student/session", {"server_id": server_id}, auth), None)["statusCode"] == 200
assert app.handler(event("POST /admin/session", {}, {"X-JDU-Admin-Key": admin_key}), None)["statusCode"] == 200
print("PASS retired registration key rejected while existing submission and viewing remain available")
