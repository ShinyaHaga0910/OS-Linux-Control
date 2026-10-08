#!/usr/bin/env python3
"""Link a classroom email without placing personal data in EC2 or CloudFormation."""
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

EMAIL_RE = re.compile(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+")
REQUIRED_DOMAIN = "@jdu.uz"


def valid_email(email):
    return len(email) <= 254 and bool(EMAIL_RE.fullmatch(email)) and email.endswith(REQUIRED_DOMAIN)


def request(endpoint, route, body, headers):
    req = Request(endpoint.rstrip("/") + route, data=json.dumps(body).encode(),
                  headers={"Content-Type": "application/json", **headers}, method="POST")
    with urlopen(req, timeout=20) as result:
        return json.load(result)


def prompt_email():
    if not sys.stdin.isatty():
        raise ValueError("Run this command interactively in CloudShell to enter your email.")
    while True:
        email = input("Enter your university email (visible): ").strip().lower()
        if not email:
            print("Email is required.")
            continue
        if not valid_email(email):
            print("Use your @jdu.uz email.")
            continue
        if input(f"Confirm {email}? Type Yes: ").strip() == "Yes":
            return email
        print("Not confirmed. Enter the email again.")


def main():
    if any(arg not in {"--change-email"} for arg in sys.argv[1:]):
        raise ValueError("Run jdu-register [--change-email].")
    state = Path(os.environ.get("JDU_STUDENT_STATE_DIR", str(Path.home() / ".jdu-student")))
    config = dict(line.split("=", 1) for line in (state / "progress.env").read_text().splitlines() if "=" in line)
    endpoint = config["JDU_PROGRESS_ENDPOINT"]
    server_id = config["JDU_PROGRESS_SERVER_ID"]
    token = config["JDU_PROGRESS_SERVER_TOKEN"]
    if not endpoint.startswith("https://"):
        raise ValueError("A valid teacher HTTPS endpoint is required.")
    auth = {"Authorization": "Bearer " + token}
    # Read back the existing record before prompting: catches an old/unavailable teacher API.
    status = request(endpoint, "/status", {"server_id": server_id}, auth)
    if not status.get("registered") or status.get("server_id") != server_id:
        raise ValueError("Progress registration could not be verified.")
    instance_id = os.environ.get("JDU_INSTANCE_ID", status.get("instance_id", ""))
    if not instance_id or status.get("instance_id") != instance_id:
        raise ValueError("The teacher record does not match this EC2 instance.")
    email_file = state / "student-email.txt"
    email = email_file.read_text().strip() if email_file.exists() and "--change-email" not in sys.argv else ""
    if email and not valid_email(email):
        print("The saved email does not end in @jdu.uz. Please enter your JDU email address.")
        email = ""
    if not email:
        email = prompt_email()
    if not valid_email(email):
        raise ValueError("A valid @jdu.uz email address is required.")
    result = request(endpoint, "/link-email", {"server_id": server_id, "student_email": email}, auth)
    if not result.get("ok"):
        raise ValueError("Email linking failed.")
    status = request(endpoint, "/status", {"server_id": server_id}, auth)
    if not (status.get("registered") and status.get("email_linked") and
            status.get("server_id") == server_id and status.get("instance_id") == instance_id):
        raise ValueError("The teacher did not confirm the registration.")
    with open(email_file, "w", opener=lambda name, flags: os.open(name, flags, 0o600)) as saved:
        saved.write(email + "\n")
    email_file.chmod(0o600)
    print("PASS Teacher registration, EC2 identity, and email link confirmed.")
    print("You do not need to submit your Server ID in Google Classroom.")


if __name__ == "__main__":
    try:
        main()
    except HTTPError as exc:
        print(f"ERROR Teacher registration service returned HTTP {exc.code}. Ask your teacher to update/check the progress stack, then run jdu-register in this CloudShell.", file=sys.stderr)
        sys.exit(1)
    except (URLError, OSError, ValueError, KeyError, EOFError) as exc:
        print(f"ERROR Registration could not be completed ({type(exc).__name__}). No completion is claimed. Ask your teacher, then run jdu-register in this CloudShell.", file=sys.stderr)
        sys.exit(1)
