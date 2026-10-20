#!/usr/bin/env python3
"""Recover a registration from an existing Ubuntu host without deploying a stack."""
import argparse
import base64
import getpass
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class RecoveryError(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def run(args, source=None):
    result = subprocess.run(args, input=source, text=True, capture_output=True, timeout=90)
    if result.returncode:
        raise RecoveryError("AWS/SSH check failed. Check the running Lab, region, stack and SSH connection. No completion is claimed.")
    return result.stdout


def aws(region, *args):
    return json.loads(run(["aws", *args, "--region", region, "--output", "json", "--no-cli-pager"]))


def api(endpoint, route, body, headers):
    req = Request(endpoint + route, data=json.dumps(body).encode(), method="POST",
                  headers={"Content-Type": "application/json", **headers})
    # Never forward a student's token or the semester key through a redirect.
    with build_opener(NoRedirect()).open(req, timeout=20) as result:
        return json.load(result)


def config(text):
    result = {}
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if not sep or key in result:
            raise RecoveryError("Invalid or duplicate registration fields. Ask your teacher.")
        result[key] = value
    return result


REMOTE_READ = """from pathlib import Path
import json
p=Path('/etc/jdu-lab/progress.env')
print(json.dumps({'config':p.read_text(),'hostname':__import__('socket').gethostname(),
 'version':Path('/etc/jdu-lab/version').read_text().strip()}))
"""


def validate_status(status, server_id, instance_id):
    if not (isinstance(status, dict) and status.get("registered") and status.get("server_id") == server_id
            and status.get("instance_id") == instance_id):
        raise RecoveryError("Teacher registration does not match the existing EC2. Ask your teacher; nothing is overwritten.")


def save_state(state, values):
    if state.is_symlink() or (state / "progress.env").is_symlink():
        raise RecoveryError("Registration path is a symbolic link. Ask your teacher.")
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    state.chmod(0o700)
    target = state / "progress.env"
    if target.exists():
        with tempfile.NamedTemporaryFile(prefix="progress.env.backup-", dir=state, delete=False) as backup:
            backup_path = Path(backup.name)
        shutil.copyfile(target, backup_path)
        backup_path.chmod(0o600)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=state, delete=False) as saved:
        temporary = Path(saved.name)
        saved.write("".join(f"{key}={value}\n" for key, value in values.items()))
    try:
        temporary.chmod(0o600)
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def recover(args):
    endpoint = args.progress_endpoint.rstrip("/")
    url = urlsplit(endpoint)
    if (url.scheme != "https" or not url.hostname or url.username or url.password
            or url.query or url.fragment or any(c.isspace() for c in endpoint)):
        raise RecoveryError("Use the teacher's HTTPS endpoint without a session URL.")
    if not re.fullmatch(r"[a-z]{2}(?:-gov)?-[a-z]+-[0-9]+", args.region):
        raise RecoveryError("Invalid AWS region.")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]{0,127}", args.stack_name):
        raise RecoveryError("Invalid stack name.")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.ssh_host):
        raise RecoveryError("Invalid SSH host.")
    state = Path(os.environ.get("JDU_STUDENT_STATE_DIR", str(Path.home() / ".jdu-student")))
    if state.is_symlink() or (state / "progress.env").is_symlink():
        raise RecoveryError("Registration path is a symbolic link. Ask your teacher.")
    stack = aws(args.region, "cloudformation", "describe-stacks", "--stack-name", args.stack_name)["Stacks"][0]
    if stack["StackStatus"] not in {"CREATE_COMPLETE", "UPDATE_COMPLETE"}:
        raise RecoveryError("The existing stack is not ready. No stack is created or changed.")
    outputs = {v["OutputKey"]: v["OutputValue"] for v in stack.get("Outputs", [])}
    instance_id = outputs.get("InstanceId", "")
    if not re.fullmatch(r"i-[0-9a-f]+", instance_id):
        raise RecoveryError("Existing EC2 output not found.")
    ssh_config = dict(line.split(None, 1) for line in run(["ssh", "-G", args.ssh_host]).splitlines()
                      if line.startswith(("hostname ", "user ")))
    if ssh_config.get("hostname") != instance_id or ssh_config.get("user") != "ssm-user":
        raise RecoveryError("SSH does not point to this stack's EC2 as ssm-user.")
    account_id = aws(args.region, "sts", "get-caller-identity")["Account"]
    remote = json.loads(run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20",
                             args.ssh_host, "python3 -"], REMOTE_READ))
    raw = config(remote["config"])
    server_id = raw.get("JDU_PROGRESS_SERVER_ID", "")
    token = base64.b64decode(raw.get("JDU_PROGRESS_SERVER_TOKEN_B64", ""), validate=True).decode()
    remote_endpoint = base64.b64decode(raw.get("JDU_PROGRESS_ENDPOINT_B64", ""), validate=True).decode().rstrip("/")
    if (not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", server_id) or not 32 <= len(token) <= 256
            or any(c.isspace() for c in token) or remote_endpoint != endpoint):
        raise RecoveryError("Ubuntu registration is incomplete or points to another endpoint. Ask your teacher.")
    parameters = {p["ParameterKey"]: p.get("ParameterValue", "") for p in stack.get("Parameters", [])}
    if parameters.get("ProgressServerId") not in {None, "", "****", server_id}:
        raise RecoveryError("Ubuntu Server ID differs from the stack. Ask your teacher.")
    target = state / "progress.env"
    local = config(target.read_text()) if target.exists() else {}
    if local.get("JDU_PROGRESS_SERVER_ID") not in {None, "", server_id}:
        raise RecoveryError("CloudShell belongs to another Server ID. Ask your teacher; nothing is overwritten.")
    if local.get("JDU_PROGRESS_ENDPOINT", "").rstrip("/") not in {"", endpoint}:
        raise RecoveryError("CloudShell points to another teacher endpoint. Ask your teacher.")
    auth = {"Authorization": "Bearer " + token}
    try:
        status = api(endpoint, "/status", {"server_id": server_id}, auth)
    except HTTPError as exc:
        if exc.code != 401:
            raise
        if not sys.stdin.isatty():
            raise RecoveryError("Run interactively in CloudShell to enter the registration key without echo.")
        print("Existing registration was not accepted. A teacher registration key is required.")
        key = getpass.getpass("Semester registration key (hidden): ").strip()
        if not re.fullmatch(r"[0-9a-f]{64}", key):
            raise RecoveryError("Invalid registration key format.")
        try:
            reply = api(endpoint, "/register", {
                "server_id": server_id, "server_token": token,
                "account_id": account_id, "instance_id": instance_id,
                "hostname": remote["hostname"], "lab_version": remote["version"],
            }, {"X-JDU-Registration-Key": key})
        except HTTPError as conflict:
            if conflict.code == 409:
                raise RecoveryError("Server ID already has another token. Teacher review is required; no token or score was overwritten.") from None
            raise
        finally:
            key = ""
        if not isinstance(reply, dict) or not reply.get("ok") or reply.get("server_id") != server_id:
            raise RecoveryError("Server registration was not confirmed.")
        status = api(endpoint, "/status", {"server_id": server_id}, auth)
    validate_status(status, server_id, instance_id)
    values = {"JDU_PROGRESS_ENDPOINT": endpoint, "JDU_PROGRESS_SERVER_ID": server_id,
              "JDU_PROGRESS_SERVER_TOKEN": token}
    if local != values:
        save_state(state, values)
        print("PASS CloudShell registration recovered from the existing Ubuntu; previous local config backed up when present.")
    else:
        print("PASS Existing CloudShell and Ubuntu registration already match.")
    print("PASS Teacher registration and existing EC2 identity confirmed.")
    print("Next: run the existing-environment updater with --change-email, then resubmit completed checks.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region", required=True)
    parser.add_argument("--progress-endpoint", required=True)
    parser.add_argument("--stack-name", default="jdu-intro-cybersecurity-2026")
    parser.add_argument("--ssh-host", default="jdu-ubuntu")
    args = parser.parse_args()
    try:
        recover(args)
    except HTTPError as exc:
        print(f"ERROR Teacher API returned HTTP {exc.code}. Ask your teacher to check the endpoint, routes and registration. No completion is claimed.", file=sys.stderr)
        return 1
    except (RecoveryError, URLError, OSError, ValueError, KeyError, IndexError,
            subprocess.TimeoutExpired, EOFError) as exc:
        # Do not print exceptions containing URLs, API response bodies or config values.
        message = str(exc) if isinstance(exc, RecoveryError) else type(exc).__name__
        print(f"ERROR Recovery stopped: {message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
