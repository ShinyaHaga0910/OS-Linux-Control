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


def standard_mission_cell(name, score):
    if not score:
        return f'<td class="missing">{name}<br>—</td>'
    css = "done" if score["complete"] else "partial"
    return f'<td class="{css}">{name}<br>{score["passed"]}/{score["total"]}</td>'


def m6_mission_cell(missions):
    ubuntu = mission_score(missions, "M6U")
    cloud = mission_score(missions, "M6C")
    if not ubuntu and not cloud:
        return '<td class="missing m6">M6<br>—</td>'
    passed = (ubuntu or {}).get("passed", 0) + (cloud or {}).get("passed", 0)
    ubuntu_text = f'{ubuntu["passed"]}/{ubuntu["total"]}' if ubuntu else "—/2"
    cloud_text = f'{cloud["passed"]}/{cloud["total"]}' if cloud else "—/4"
    complete = bool(ubuntu and cloud and ubuntu["complete"] and cloud["complete"])
    css = "done" if complete else "partial"
    return (
        f'<td class="{css} m6"><strong>M6 {passed}/6</strong><br>'
        f'<small>Ubuntu {ubuntu_text}<br>CloudShell {cloud_text}</small></td>'
    )


def paired_complete(missions, prefix):
    ubuntu = mission_score(missions, f"{prefix}U")
    cloud = mission_score(missions, f"{prefix}C")
    return bool(ubuntu and cloud and ubuntu["complete"] and cloud["complete"])


def guided_progress_cell(missions):
    completed = sum(
        1
        for name in ["P1", "P2", "P3", "P4", "P5"]
        if (mission_score(missions, name) or {}).get("complete")
    )
    if paired_complete(missions, "P6"):
        completed += 1
    parts = []
    for name in ["P1", "P2", "P3", "P4", "P5"]:
        score = mission_score(missions, name)
        parts.append(f'{name} {score["passed"]}/{score["total"]}' if score else f"{name} —")
    ubuntu = mission_score(missions, "P6U")
    cloud = mission_score(missions, "P6C")
    ubuntu_text = f'{ubuntu["passed"]}/{ubuntu["total"]}' if ubuntu else "—/2"
    cloud_text = f'{cloud["passed"]}/{cloud["total"]}' if cloud else "—/4"
    parts.append(f"P6 U{ubuntu_text} C{cloud_text}")
    css = "done" if completed == 6 else ("partial" if any(mission_score(missions, name) for name in ["P1", "P2", "P3", "P4", "P5", "P6U", "P6C"]) else "missing")
    return f'<td class="{css} guided"><strong>{completed}/6</strong><br><small>{"<br>".join(parts)}</small></td>'


def dashboard(event):
    token = (event.get("queryStringParameters") or {}).get("session", "")
    if not token:
        return response(401, "Session URL is required.", "text/plain; charset=utf-8")
    item = DDB.get_item(TableName=TABLE_NAME, Key={"pk": {"S": f"SESSION#{digest(token)}"}}, ConsistentRead=True).get("Item")
    expires_at = int(item.get("expiresAt", {}).get("N", "0")) if item else 0
    if expires_at <= int(time.time()):
        return response(401, "This dashboard URL has expired. Run jdu-dashboard again in CloudShell.", "text/plain; charset=utf-8")

    rows = []
    for server in scan_servers():
        missions = server.get("missions", {}).get("M", {})
        completed = sum(
            1
            for name in ["M0", "M1", "M2", "M3", "M4", "M5", "M7"]
            if (mission_score(missions, name) or {}).get("complete")
        )
        if paired_complete(missions, "M6"):
            completed += 1
        cells = [standard_mission_cell(f"M{i}", mission_score(missions, f"M{i}")) for i in range(6)]
        cells.append(m6_mission_cell(missions))
        cells.append(standard_mission_cell("M7", mission_score(missions, "M7")))
        guided_cell = guided_progress_cell(missions)
        rows.append((attr_s(server, "serverId"), f"<tr><td><strong>{html.escape(attr_s(server, 'studentEmail')) or 'メール未登録'}</strong><br><small>{html.escape(attr_s(server, 'serverId'))}</small><br><span>{html.escape(attr_s(server, 'hostname'))}</span><br><small>{html.escape(attr_s(server, 'instanceId'))}</small></td>{guided_cell}<td><strong>{completed}/8</strong><div class=bar><i style=\"width:{completed * 12.5}%\"></i></div></td>{''.join(cells)}<td>{html.escape(attr_s(server, 'updatedAt'))}</td></tr>"))
    rows.sort(key=lambda pair: pair[0])
    body_rows = "".join(row for _, row in rows) or '<tr><td colspan="12">まだ進捗報告はありません。</td></tr>'
    page = f"""<!doctype html><html lang=ja><head><meta charset=utf-8><meta name=viewport content=\"width=device-width,initial-scale=1\"><meta http-equiv=refresh content=30><title>JDU Linux Lab Progress</title><style>body{{font-family:system-ui,sans-serif;margin:24px;background:#f4f6f8;color:#18212b}}h1{{font-size:1.35rem}}p{{color:#52606d}}.wrap{{overflow:auto;background:white;border:1px solid #d9e2ec;border-radius:10px}}table{{border-collapse:collapse;width:100%;min-width:1250px}}th,td{{padding:10px;border-bottom:1px solid #e6eaf0;text-align:center}}th:first-child,td:first-child{{text-align:left}}th{{background:#edf2f7;position:sticky;top:0}}td span,small{{color:#66788a}}.guided{{min-width:145px;text-align:left}}.done{{background:#e5f7ea;color:#176b32}}.partial{{background:#fff3d6;color:#815500}}.missing{{color:#8997a5}}.bar{{height:8px;background:#e4e9ee;border-radius:8px;margin-top:6px}}.bar i{{display:block;height:100%;background:#238636;border-radius:8px}}footer{{margin-top:12px;font-size:.85rem;color:#66788a}}</style></head><body><h1>JDU Linux Lab 進捗</h1><p>完全手順付き演習P1～P6と、自力課題M0～M7の最新結果です。30秒ごとに更新します。</p><div class=wrap><table><thead><tr><th>Student email / Server</th><th>Guided P1–P6</th><th>Challenge</th>{''.join(f'<th>M{i}</th>' for i in range(8))}<th>Last report (UTC)</th></tr></thead><tbody>{body_rows}</tbody></table></div><footer>閲覧URLは一定時間で失効します。登録メールは教員の進捗確認に使用します。入力したメールの本人確認は行っていません。</footer></body></html>"""
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
        if route == "GET /dashboard":
            return dashboard(event)
        if route == "GET /health":
            return response(200, {"ok": True})
        return response(404, {"error": "not found"})
    except Exception as exc:
        print(f"request failed: {type(exc).__name__}: {exc}")
        return response(500, {"error": "internal error"})
