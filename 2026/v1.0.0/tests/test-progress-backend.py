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
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": "student@example.test"}), None)["statusCode"] == 401
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": "bad\naddress"}, auth), None)["statusCode"] == 400
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": " Student@Example.test "}, auth), None)["statusCode"] == 200
status = app.handler(event("POST /status", {"server_id": server_id}, auth), None)
assert json.loads(status["body"])["instance_id"] == register_body["instance_id"]
assert json.loads(status["body"])["email_linked"] is True
assert "student@example.test" not in status["body"]
assert fake_ddb.items[f"SERVER#{server_id}"]["studentEmail"]["S"] == "student@example.test"
# Anonymous instance bootstrap cannot erase/change the authenticated email link.
assert app.handler(event("POST /register", register_body, {"X-JDU-Registration-Key": registration_key}), None)["statusCode"] == 200
assert fake_ddb.items[f"SERVER#{server_id}"]["studentEmail"]["S"] == "student@example.test"
assert app.handler(event("POST /link-email", {"server_id": server_id, "student_email": "other@example.test"}, {"Authorization": "Bearer wrong"}), None)["statusCode"] == 401
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
assert "0/8" in partial_dashboard["body"]
assert "P1 6/6" in partial_dashboard["body"]
assert "P6 U2/2 C3/4" in partial_dashboard["body"]
assert "1/6" in partial_dashboard["body"]

m6_cloud["passed"] = 4
assert app.handler(event("POST /submit", m6_cloud, {"Authorization": f"Bearer {server_token}"}), None)["statusCode"] == 200
practice_p6_cloud = {"server_id": server_id, "mission": "P6C", "passed": 4, "total": 4}
assert app.handler(event("POST /submit", practice_p6_cloud, {"Authorization": f"Bearer {server_token}"}), None)["statusCode"] == 200
dashboard = app.handler(event("GET /dashboard", query={"session": session_token}), None)
assert dashboard["statusCode"] == 200
assert server_id in dashboard["body"]
assert "student@example.test" in dashboard["body"]
assert "1/2" in dashboard["body"]
assert "Ubuntu 2/2" in dashboard["body"]
assert "CloudShell 4/4" in dashboard["body"]
assert "M6 6/6" in dashboard["body"]
assert "1/8" in dashboard["body"]
assert "P6 U2/2 C4/4" in dashboard["body"]
assert "2/6" in dashboard["body"]
assert "入力したメールの本人確認は行っていません" in dashboard["body"]
assert app.handler(event("GET /health"), None)["statusCode"] == 200
print("PASS progress backend registration, authentication, submission, session, and dashboard")
