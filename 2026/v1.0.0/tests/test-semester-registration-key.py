"""Test random private key creation, reuse, rotation and migration without AWS."""
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

root = Path(sys.argv[1])
teacher = (root / "teacher/install-teacher.sh").read_text()
key_logic = teacher[teacher.index('export AWS_PAGER='):teacher.index('work_dir="$(mktemp')]
fixture_key = "d" * 64
fixture_retired_hash = hashlib.sha256(fixture_key.encode()).hexdigest()
with tempfile.TemporaryDirectory() as temporary:
    state = Path(temporary)
    env = {**os.environ, "state_dir": temporary, "ROTATE_REGISTRATION_KEY": "false",
           "RETIRED_REGISTRATION_HASH": fixture_retired_hash, "JDU_PROGRESS_REGISTRATION_KEY": ""}
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
    assert prepare(ROTATE_REGISTRATION_KEY="true").returncode == 0
    rotated = (state / "registration.pending.key").read_text().strip()
    assert rotated != new_key
    # Until AWS succeeds, the committed key and admin key remain unchanged.
    assert (state / "registration.key").read_text().strip() == new_key
    assert (state / "admin.key").read_text() == admin
    (state / "registration.pending.key").unlink()
    (state / "registration.key").write_text(fixture_key)
    assert prepare().returncode == 0
    assert (state / "registration.pending.key").read_text().strip() != fixture_key
    assert prepare(JDU_PROGRESS_REGISTRATION_KEY=fixture_key).returncode == 2

student = (root / "install.sh").read_text()
guard = student[student.index('if [[ ! "$PROGRESS_ENDPOINT"'):student.index('export AWS_PAGER=')]
empty = subprocess.run(["bash", "-c", guard], env={**os.environ, "PROGRESS_ENDPOINT": "", "REGISTRATION_KEY": ""}, capture_output=True, text=True)
assert empty.returncode == 2 and "Google Classroom" in empty.stderr
print("PASS private semester key generation, reuse, rotation, legacy retirement and missing-key rejection")
