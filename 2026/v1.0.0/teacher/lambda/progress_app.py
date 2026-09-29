import base64
import hashlib
import hmac
import html
import json
import os
import re
import secrets
import time
from datetime import datetime, timezone
from urllib.parse import quote

import boto3


TABLE_NAME = os.environ["TABLE_NAME"]
ADMIN_KEY_HASH = os.environ["ADMIN_KEY_HASH"]
REGISTRATION_KEY_HASH = os.environ["REGISTRATION_KEY_HASH"]
SESSION_TTL_SECONDS = int(os.environ.get("SESSION_TTL_SECONDS", "1800"))
DDB = boto3.client("dynamodb")
SERVER_ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,64}$")
MISSION_RE = re.compile(r"^(?:M[0-7]|M6U|M6C|P[1-6]|P6U|P6C)$")


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def response(status, body, content_type="application/json; charset=utf-8"):
    if not isinstance(body, str):
        body = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": content_type,
            "Cache-Control": "no-store",
            "Referrer-Policy": "no-referrer",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
        },
        "body": body,
    }


def header(event, name):
    wanted = name.lower()
    for key, value in (event.get("headers") or {}).items():
        if key.lower() == wanted:
            return value or ""
    return ""


def parse_body(event):
    raw = event.get("body") or ""
    if event.get("isBase64Encoded"):
        raw = base64.b64decode(raw).decode("utf-8")
    if len(raw.encode("utf-8")) > 16384:
        raise ValueError("request body is too large")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("JSON object required")
    return value


def valid_secret(candidate, expected_hash):
    return bool(candidate) and hmac.compare_digest(digest(candidate), expected_hash)


def text_field(body, name, maximum=128):
    value = body.get(name, "")
    if not isinstance(value, str) or len(value) > maximum:
        raise ValueError(f"invalid {name}")
    return value


def register(event):
    if not valid_secret(header(event, "X-JDU-Registration-Key"), REGISTRATION_KEY_HASH):
        return response(401, {"error": "unauthorized"})
    try:
        body = parse_body(event)
        server_id = text_field(body, "server_id", 64)
        token = text_field(body, "server_token", 256)
        if not SERVER_ID_RE.fullmatch(server_id) or len(token) < 32:
            raise ValueError("invalid server credentials")
        fields = {
            "hostname": text_field(body, "hostname"),
            "accountId": text_field(body, "account_id"),
            "instanceId": text_field(body, "instance_id"),
            "labVersion": text_field(body, "lab_version", 32),
        }
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return response(400, {"error": "invalid request"})

    stamp = now_iso()
    values = {
        ":kind": {"S": "server"},
        ":serverId": {"S": server_id},
        ":tokenHash": {"S": digest(token)},
        ":createdAt": {"S": stamp},
        ":updatedAt": {"S": stamp},
        ":empty": {"M": {}},
    }
    names = {"#kind": "kind"}
    assignments = [
        "#kind=:kind",
        "serverId=:serverId",
        "tokenHash=:tokenHash",
        "createdAt=if_not_exists(createdAt,:createdAt)",
        "updatedAt=:updatedAt",
        "missions=if_not_exists(missions,:empty)",
    ]
    for field_name, value in fields.items():
        values[f":{field_name}"] = {"S": value}
        assignments.append(f"{field_name}=:{field_name}")
    try:
        DDB.update_item(
            TableName=TABLE_NAME,
            Key={"pk": {"S": f"SERVER#{server_id}"}},
            UpdateExpression="SET " + ", ".join(assignments),
            ConditionExpression="attribute_not_exists(pk) OR tokenHash=:tokenHash",
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=values,
        )
    except DDB.exceptions.ConditionalCheckFailedException:
        return response(409, {"error": "server id is already registered"})
    return response(200, {"ok": True, "server_id": server_id})


def registration_status(event):
    try:
        server_id = text_field(parse_body(event), "server_id", 64)
        if not SERVER_ID_RE.fullmatch(server_id):
            raise ValueError("invalid server id")
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return response(400, {"error": "invalid request"})
    authorization = header(event, "Authorization")
    token = authorization[7:] if authorization.startswith("Bearer ") else ""
    item = DDB.get_item(TableName=TABLE_NAME, Key={"pk": {"S": f"SERVER#{server_id}"}}, ConsistentRead=True).get("Item")
    if not item or not valid_secret(token, item.get("tokenHash", {}).get("S", "")):
        return response(401, {"error": "unauthorized"})
    return response(200, {
        "ok": True,
        "registered": True,
        "server_id": server_id,
        "instance_id": item.get("instanceId", {}).get("S", ""),
        "email_linked": bool(item.get("studentEmail", {}).get("S", "")),
    })


def link_email(event):
    try:
        body = parse_body(event)
        server_id = text_field(body, "server_id", 64)
        email = text_field(body, "student_email", 254).strip().lower()
        if not SERVER_ID_RE.fullmatch(server_id) or not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+", email):
            raise ValueError("invalid registration")
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return response(400, {"error": "invalid request"})
    authorization = header(event, "Authorization")
    token = authorization[7:] if authorization.startswith("Bearer ") else ""
    item = DDB.get_item(TableName=TABLE_NAME, Key={"pk": {"S": f"SERVER#{server_id}"}}, ConsistentRead=True).get("Item")
    if not item or not valid_secret(token, item.get("tokenHash", {}).get("S", "")):
        return response(401, {"error": "unauthorized"})
    DDB.update_item(
        TableName=TABLE_NAME, Key={"pk": {"S": f"SERVER#{server_id}"}},
        UpdateExpression="SET studentEmail=:studentEmail, updatedAt=:updatedAt",
        ExpressionAttributeValues={":studentEmail": {"S": email}, ":updatedAt": {"S": now_iso()}},
    )
    return response(200, {"ok": True})


def submit(event):
    try:
        body = parse_body(event)
        server_id = text_field(body, "server_id", 64)
        mission = text_field(body, "mission", 8).upper()
        passed = body.get("passed")
        total = body.get("total")
        if not SERVER_ID_RE.fullmatch(server_id) or not MISSION_RE.fullmatch(mission):
            raise ValueError("invalid id")
        if isinstance(passed, bool) or isinstance(total, bool) or not isinstance(passed, int) or not isinstance(total, int):
            raise ValueError("invalid score")
        if passed < 0 or total < 1 or passed > total or total > 50:
            raise ValueError("invalid score")
        metadata = {
            "hostname": text_field(body, "hostname"),
            "accountId": text_field(body, "account_id"),
            "instanceId": text_field(body, "instance_id"),
            "labVersion": text_field(body, "lab_version", 32),
        }
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return response(400, {"error": "invalid request"})

    token_header = header(event, "Authorization")
    token = token_header[7:] if token_header.startswith("Bearer ") else ""
    item = DDB.get_item(TableName=TABLE_NAME, Key={"pk": {"S": f"SERVER#{server_id}"}}, ConsistentRead=True).get("Item")
    if not item or not valid_secret(token, item.get("tokenHash", {}).get("S", "")):
        return response(401, {"error": "unauthorized"})

    stamp = now_iso()
    mission_value = {
        "M": {
            "passed": {"N": str(passed)},
            "total": {"N": str(total)},
            "complete": {"BOOL": passed == total},
            "checkedAt": {"S": stamp},
        }
    }
    values = {":mission": mission_value, ":updatedAt": {"S": stamp}}
    assignments = ["missions.#mission=:mission", "updatedAt=:updatedAt"]
    for field_name, value in metadata.items():
        if value:
            values[f":{field_name}"] = {"S": value}
            assignments.append(f"{field_name}=:{field_name}")
    DDB.update_item(
        TableName=TABLE_NAME,
        Key={"pk": {"S": f"SERVER#{server_id}"}},
        UpdateExpression="SET " + ", ".join(assignments),
        ExpressionAttributeNames={"#mission": mission},
        ExpressionAttributeValues=values,
    )
    return response(200, {"ok": True, "server_id": server_id, "mission": mission})


def create_session(event):
    if not valid_secret(header(event, "X-JDU-Admin-Key"), ADMIN_KEY_HASH):
        return response(401, {"error": "unauthorized"})
    token = secrets.token_urlsafe(32)
    expires_at = int(time.time()) + SESSION_TTL_SECONDS
    DDB.put_item(
        TableName=TABLE_NAME,
        Item={
            "pk": {"S": f"SESSION#{digest(token)}"},
            "kind": {"S": "session"},
            "role": {"S": "teacher"},
            "createdAt": {"S": now_iso()},
            "expiresAt": {"N": str(expires_at)},
        },
    )
    context = event.get("requestContext") or {}
    domain = context.get("domainName", "")
    stage = context.get("stage", "$default")
    prefix = "" if stage == "$default" else f"/{stage}"
    url = f"https://{domain}{prefix}/dashboard?session={quote(token)}"
    return response(200, {"url": url, "expires_in_seconds": SESSION_TTL_SECONDS})


def create_student_session(event):
    try:
        server_id = text_field(parse_body(event), "server_id", 64)
        if not SERVER_ID_RE.fullmatch(server_id):
            raise ValueError("invalid server id")
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return response(400, {"error": "invalid request"})
    authorization = header(event, "Authorization")
    server_token = authorization[7:] if authorization.startswith("Bearer ") else ""
    server = DDB.get_item(TableName=TABLE_NAME, Key={"pk": {"S": f"SERVER#{server_id}"}}, ConsistentRead=True).get("Item")
    if not server or not valid_secret(server_token, attr_s(server, "tokenHash")):
        return response(401, {"error": "unauthorized"})
    token = secrets.token_urlsafe(32)
    lifetime = min(900, SESSION_TTL_SECONDS)
    DDB.put_item(TableName=TABLE_NAME, Item={
        "pk": {"S": f"STUDENT_SESSION#{digest(token)}"},
        "kind": {"S": "student_session"},
        "role": {"S": "student"},
        "serverId": {"S": server_id},
        "serverTokenHash": {"S": attr_s(server, "tokenHash")},
        "createdAt": {"S": now_iso()},
        "expiresAt": {"N": str(int(time.time()) + lifetime)},
    })
    context = event.get("requestContext") or {}
    stage = context.get("stage", "$default")
    prefix = "" if stage == "$default" else f"/{stage}"
    url = f"https://{context.get('domainName', '')}{prefix}/student/progress?session={quote(token)}"
    return response(200, {"url": url, "expires_in_seconds": lifetime})


def scan_servers():
    items = []
    start_key = None
    while True:
        request = {
            "TableName": TABLE_NAME,
            "FilterExpression": "begins_with(pk,:prefix)",
            "ExpressionAttributeValues": {":prefix": {"S": "SERVER#"}},
        }
        if start_key:
            request["ExclusiveStartKey"] = start_key
        result = DDB.scan(**request)
        items.extend(result.get("Items", []))
        start_key = result.get("LastEvaluatedKey")
        if not start_key:
            return items


def attr_s(item, key):
    return item.get(key, {}).get("S", "")


def mission_score(missions, name):
    score = missions.get(name, {}).get("M")
    if not score:
        return None
    return {
        "passed": int(score.get("passed", {}).get("N", "0")),
        "total": int(score.get("total", {}).get("N", "0")),
        "complete": score.get("complete", {}).get("BOOL") is True,
        "checked_at": score.get("checkedAt", {}).get("S", ""),
    }


DISPLAY_MISSIONS = [("M0", "M0")]
for number in range(1, 7):
    DISPLAY_MISSIONS.extend([(f"T{number}", f"P{number}"), (f"M{number}", f"M{number}")])
DISPLAY_MISSIONS.append(("M7", "M7"))


def standard_mission_cell(name, score):
    if not score:
        return f'<td class="missing">{name}<br>—</td>'
    css = "done" if score["complete"] else "partial"
    return f'<td class="{css}">{name}<br>{score["passed"]}/{score["total"]}</td>'


def paired_mission_cell(missions, stored_name, display_name):
    ubuntu = mission_score(missions, f"{stored_name}U")
    cloud = mission_score(missions, f"{stored_name}C")
    if not ubuntu and not cloud:
        return f'<td class="missing">{display_name}<br>—</td>'
    passed = (ubuntu or {}).get("passed", 0) + (cloud or {}).get("passed", 0)
    ubuntu_text = f'{ubuntu["passed"]}/{ubuntu["total"]}' if ubuntu else "—/2"
    cloud_text = f'{cloud["passed"]}/{cloud["total"]}' if cloud else "—/4"
    complete = bool(ubuntu and cloud and ubuntu["complete"] and cloud["complete"])
    css = "done" if complete else "partial"
    return (
        f'<td class="{css}"><strong>{display_name} {passed}/6</strong><br>'
        f'<small>Ubuntu {ubuntu_text}<br>CloudShell {cloud_text}</small></td>'
    )


def dashboard(event, personal=False):
    token = (event.get("queryStringParameters") or {}).get("session", "")
    if not token:
        return response(401, "Session URL is required.", "text/plain; charset=utf-8")
    namespace = "STUDENT_SESSION" if personal else "SESSION"
    item = DDB.get_item(TableName=TABLE_NAME, Key={"pk": {"S": f"{namespace}#{digest(token)}"}}, ConsistentRead=True).get("Item")
    expires_at = int(item.get("expiresAt", {}).get("N", "0")) if item else 0
    if expires_at <= int(time.time()):
        command = "jdu-my-progress" if personal else "jdu-dashboard"
        return response(401, f"This URL is invalid or expired. Run {command} again in CloudShell.", "text/plain; charset=utf-8")

    if personal:
        server_id = attr_s(item, "serverId")
        requested_id = (event.get("queryStringParameters") or {}).get("server_id", server_id)
        if attr_s(item, "role") != "student" or not SERVER_ID_RE.fullmatch(server_id) or requested_id != server_id:
            return response(403, {"error": "forbidden"})
        server = DDB.get_item(TableName=TABLE_NAME, Key={"pk": {"S": f"SERVER#{server_id}"}}, ConsistentRead=True).get("Item")
        if not server or not hmac.compare_digest(attr_s(server, "tokenHash"), attr_s(item, "serverTokenHash")):
            return response(401, {"error": "session no longer valid"})
        servers = [server]
    else:
        # Existing teacher sessions predating the explicit role remain valid in
        # the teacher-only namespace until their original expiry.
        if attr_s(item, "kind") != "session" or attr_s(item, "role") not in {"", "teacher"}:
            return response(403, {"error": "forbidden"})
        servers = scan_servers()

    rows = []
    for server in servers:
        missions = server.get("missions", {}).get("M", {})
        cells = [
            paired_mission_cell(missions, stored_name, display_name)
            if stored_name in {"P6", "M6"}
            else standard_mission_cell(display_name, mission_score(missions, stored_name))
            for display_name, stored_name in DISPLAY_MISSIONS
        ]
        rows.append((attr_s(server, "serverId"), f"<tr><th scope=row><strong>{('自分のサーバー' if personal else html.escape(attr_s(server, 'studentEmail')) or 'メール未登録')}</strong><br><small>{html.escape(attr_s(server, 'serverId'))}</small><br><span>{html.escape(attr_s(server, 'hostname'))}</span><br><small>{html.escape(attr_s(server, 'instanceId'))}</small></th>{''.join(cells)}<td>{html.escape(attr_s(server, 'updatedAt'))}</td></tr>"))
    rows.sort(key=lambda pair: pair[0])
    body_rows = "".join(row for _, row in rows) or '<tr><td colspan="16">まだ進捗報告はありません。</td></tr>'
    page = f"""<!doctype html><html lang=ja><head><meta charset=utf-8><meta name=viewport content=\"width=device-width,initial-scale=1\"><meta http-equiv=refresh content=30><title>JDU Linux Lab Progress</title><style>body{{font-family:system-ui,sans-serif;margin:24px;background:#f4f6f8;color:#18212b}}h1{{font-size:1.35rem}}p{{color:#52606d}}.wrap{{overflow:auto;background:white;border:1px solid #d9e2ec;border-radius:10px}}table{{border-collapse:separate;border-spacing:0;width:100%;min-width:1500px}}th,td{{padding:10px;border-bottom:1px solid #e6eaf0;text-align:center}}th:first-child{{text-align:left;position:sticky;left:0;min-width:220px}}tbody th{{background:white;z-index:1}}thead th:first-child{{z-index:3}}thead th{{background:#edf2f7;position:sticky;top:0;z-index:2}}td span,small{{color:#66788a}}.done{{background:#e5f7ea;color:#176b32}}.partial{{background:#fff3d6;color:#815500}}.missing{{color:#8997a5}}footer{{margin-top:12px;font-size:.85rem;color:#66788a}}</style></head><body><h1>JDU Linux Lab 進捗</h1><p>T1～T6（練習）とM0～M7（課題）の最新結果です。Tの送信コマンドはPを使います（例：T1 → jdu-check P1）。30秒ごとに更新します。</p><div class=wrap role=region aria-label="課題の進捗一覧" tabindex=0><table><thead><tr><th scope=col>学生メール / サーバー</th>{''.join(f'<th scope=col>{name}</th>' for name, _ in DISPLAY_MISSIONS)}<th scope=col>最終送信 (UTC)</th></tr></thead><tbody>{body_rows}</tbody></table></div><footer>閲覧URLは一定時間で失効します。登録メールは教員の進捗確認に使用します。入力したメールの本人確認は行っていません。</footer></body></html>"""
    if personal:
        page = page.replace("JDU Linux Lab 進捗", "JDU Linux Lab 自分の進捗").replace("学生メール / サーバー", "自分のサーバー")
        page = page.replace("<footer>閲覧URLは一定時間で失効します。登録メールは教員の進捗確認に使用します。入力したメールの本人確認は行っていません。</footer>", "<footer>読み取り専用のページです。閲覧URLは15分以内に失効します。URLを他の人へ共有せず、共有PCでは利用後にページを閉じてください。再発行：CloudShellで jdu-my-progress。</footer>")
    return response(200, page, "text/html; charset=utf-8")


def handler(event, context):
    route = event.get("routeKey", "")
    try:
        if route == "POST /register":
            return register(event)
        if route == "POST /status":
            return registration_status(event)
        if route == "POST /link-email":
            return link_email(event)
        if route == "POST /submit":
            return submit(event)
        if route == "POST /admin/session":
            return create_session(event)
        if route == "POST /student/session":
            return create_student_session(event)
        if route == "GET /student/progress":
            return dashboard(event, personal=True)
        if route == "GET /dashboard":
            return dashboard(event)
        if route == "GET /health":
            return response(200, {"ok": True})
        return response(404, {"error": "not found"})
    except Exception as exc:
        print(f"request failed: {type(exc).__name__}: {exc}")
        return response(500, {"error": "internal error"})
