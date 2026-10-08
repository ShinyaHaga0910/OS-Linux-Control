"""Test initial key creation, default preservation and explicit rotation without AWS."""
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

root = Path(sys.argv[1])
teacher = (root / "teacher/install-teacher.sh").read_text()
stack_lookup = teacher[teacher.index('export AWS_PAGER='):teacher.index('umask 077')]
key_logic = teacher[teacher.index('umask 077'):teacher.index('work_dir="$(mktemp')]
fixture_key = "d" * 64
fixture_retired_hash = hashlib.sha256(fixture_key.encode()).hexdigest()
def inspect_stack(response, status):
    script = ('set -Eeuo pipefail\n'
              'aws() { printf "%s\\n" "$MOCK_AWS_RESPONSE"; return "$MOCK_AWS_STATUS"; }\n'
              + stack_lookup + 'printf "STACK_STATUS=%s\\n" "$stack_status"\n')
    return subprocess.run(["bash", "-c", script], env={**os.environ, "REGION": "us-east-1",
                          "STACK_NAME": "test", "MOCK_AWS_RESPONSE": response,
                          "MOCK_AWS_STATUS": str(status)}, capture_output=True, text=True)
assert "STACK_STATUS=UPDATE_COMPLETE" in inspect_stack("UPDATE_COMPLETE", 0).stdout
assert "STACK_STATUS=NOT_FOUND" in inspect_stack(
    "An error occurred (ValidationError): Stack with id test does not exist", 255).stdout
assert inspect_stack("An error occurred (AccessDenied): denied", 255).returncode == 2
with tempfile.TemporaryDirectory() as temporary:
    state = Path(temporary)
    env = {**os.environ, "state_dir": temporary, "ROTATE_REGISTRATION_KEY": "false",
           "RETIRED_REGISTRATION_HASH": fixture_retired_hash, "JDU_PROGRESS_REGISTRATION_KEY": "",
           "STACK_NAME": "test", "stack_status": "NOT_FOUND"}
    def prepare(**overrides):
        return subprocess.run(["bash", "-c", "set -Eeuo pipefail\n" + key_logic], env={**env, **overrides}, capture_output=True, text=True)
    assert prepare().returncode == 0
    new_key = (state / "registration.pending.key").read_text().strip()
    assert re.fullmatch("[0-9a-f]{64}", new_key) and new_key != fixture_key
    assert (state / "registration.pending.key").stat().st_mode & 0o777 == 0o600
    (state / "registration.pending.key").rename(state / "registration.key")
    admin = (state / "admin.key").read_text()
    assert prepare().returncode == 0
    assert (state / "registration.pending.key").read_text().strip() == new_key
    (state / "progress.env").write_text("JDU_PROGRESS_STACK=test\n")
    assert prepare(stack_status="UPDATE_COMPLETE").returncode == 0
    assert (state / "registration.pending.key").read_text().strip() == new_key
    assert (state / "admin.key").read_text() == admin
    (state / "progress.env").unlink()
    (state / "registration.pending.key").write_text("e" * 64)
    pending_mismatch = prepare()
    assert pending_mismatch.returncode == 2 and "pending registration key differs" in pending_mismatch.stderr
    assert (state / "registration.key").read_text().strip() == new_key
    (state / "registration.pending.key").unlink()
    supplied_mismatch = prepare(JDU_PROGRESS_REGISTRATION_KEY="e" * 64)
    assert supplied_mismatch.returncode == 2 and "supplied registration key differs" in supplied_mismatch.stderr
    assert not (state / "registration.pending.key").exists()
    assert prepare(JDU_PROGRESS_REGISTRATION_KEY=new_key).returncode == 0
    assert prepare(ROTATE_REGISTRATION_KEY="true").returncode == 0
    rotated = (state / "registration.pending.key").read_text().strip()
    assert rotated != new_key
    # Until AWS succeeds, the committed key and admin key remain unchanged.
    assert (state / "registration.key").read_text().strip() == new_key
    assert (state / "admin.key").read_text() == admin
    (state / "registration.pending.key").unlink()
    (state / "registration.key").write_text(fixture_key)
    retired = prepare()
    assert retired.returncode == 2 and "No automatic rotation" in retired.stderr
    assert not (state / "registration.pending.key").exists()
    assert (state / "registration.key").read_text().strip() == fixture_key
    assert prepare(JDU_PROGRESS_REGISTRATION_KEY=fixture_key).returncode == 2
    assert prepare(ROTATE_REGISTRATION_KEY="true").returncode == 0
    assert (state / "registration.pending.key").read_text().strip() != fixture_key
    (state / "registration.pending.key").unlink()
    (state / "progress.env").write_text("JDU_PROGRESS_STACK=test\n")
    (state / "registration.key").unlink()
    missing_registration = prepare(stack_status="UPDATE_COMPLETE")
    assert missing_registration.returncode == 2 and "no saved registration key" in missing_registration.stderr, missing_registration.stderr
    assert not (state / "registration.pending.key").exists()
    (state / "registration.key").write_text(new_key)
    (state / "admin.key").unlink()
    missing_admin = prepare(stack_status="UPDATE_COMPLETE")
    assert missing_admin.returncode == 2 and "no saved admin key" in missing_admin.stderr, missing_admin.stderr
with tempfile.TemporaryDirectory() as temporary:
    env = {**os.environ, "state_dir": temporary, "ROTATE_REGISTRATION_KEY": "false",
           "JDU_PROGRESS_REGISTRATION_KEY": "", "STACK_NAME": "test",
           "stack_status": "UPDATE_COMPLETE", "RETIRED_REGISTRATION_HASH": fixture_retired_hash}
    missing_keys = subprocess.run(["bash", "-c", "set -Eeuo pipefail\n" + key_logic],
                                  env=env, capture_output=True, text=True)
    assert missing_keys.returncode == 2 and "no saved configuration" in missing_keys.stderr
    (Path(temporary) / "progress.env").write_text("JDU_PROGRESS_STACK=other\n")
    wrong_stack = subprocess.run(["bash", "-c", "set -Eeuo pipefail\n" + key_logic],
                                 env=env, capture_output=True, text=True)
    assert wrong_stack.returncode == 2 and "belongs to another stack" in wrong_stack.stderr
    (Path(temporary) / "progress.env").write_text("JDU_PROGRESS_STACK=test\n")
    missing_admin = subprocess.run(["bash", "-c", "set -Eeuo pipefail\n" + key_logic],
                                   env=env, capture_output=True, text=True)
    assert missing_admin.returncode == 2 and "existing teacher stack has no saved admin key" in missing_admin.stderr
    assert not (Path(temporary) / "admin.key").exists()

student = (root / "install.sh").read_text()
guard = student[student.index('if [[ ! "$PROGRESS_ENDPOINT"'):student.index('export AWS_PAGER=')]
empty = subprocess.run(["bash", "-c", guard], env={**os.environ, "PROGRESS_ENDPOINT": "", "REGISTRATION_KEY": ""}, capture_output=True, text=True)
assert empty.returncode == 2 and "Google Classroom" in empty.stderr
print("PASS initial key generation, preservation, explicit rotation and missing-key rejection")
