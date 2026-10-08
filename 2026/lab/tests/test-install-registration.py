"""Exercise installer completion gates and generated teacher commands without AWS."""
from pathlib import Path
import os
import shlex
import subprocess
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
student = (root / "install.sh").read_text()
tail = student[student.index("printf '%s\\n' 'Checking Ubuntu initialization") :]
with tempfile.TemporaryDirectory() as temporary:
    home = Path(temporary)
    (home / ".local/bin").mkdir(parents=True)
    helper = home / "register-student.py"
    helper.write_text("# test fixture\n")
    prelude = '''set -Eeuo pipefail
ssh() { [[ "${TEST_SETUP:-success}" == success ]]; }
sleep() { :; }
python3() { echo REGISTRATION_ATTEMPTED; [[ "${TEST_LINK:-success}" == success ]]; }
progress_server_id=srv-test1234
instance_id=i-test
student_state_dir="$HOME/.jdu-student"
registration_path="$HOME/register-student.py"
personal_progress_path="$HOME/register-student.py"
SSH_KEY_PATH="$HOME/key"
'''
    for setup, link, expected in [("success", "success", 0), ("failure", "success", 1), ("success", "failure", 1)]:
        result = subprocess.run(["bash", "-c", prelude + tail], env={**os.environ, "HOME": str(home), "TEST_SETUP": setup, "TEST_LINK": link}, capture_output=True, text=True)
        assert result.returncode == expected, result.stderr
        assert ("PASS The AWS lab environment is ready." in result.stdout) == (expected == 0)
        assert ("REGISTRATION_ATTEMPTED" in result.stdout) == (setup == "success")

teacher = (root / "teacher/install-teacher.sh").read_text()
command_printer = teacher[teacher.index('student_setup_command="$(') :]
env = {**os.environ, "BASE_URL": "https://raw.example.test/lab", "REGION": "us-east-1", "endpoint": "https://new.example.test", "registration_key_value": "f" * 64}
with tempfile.TemporaryDirectory() as command_state:
    printed = subprocess.check_output(["bash", "-c", command_printer], env={**env, "state_dir": command_state}, text=True)
    command_file = Path(command_state) / "student-setup-command.txt"
    assert command_file.stat().st_mode & 0o777 == 0o600
    assert command_file.read_text().strip() == printed.splitlines()[0]
arguments = shlex.split(printed.splitlines()[0].split("&&", 1)[1])
assert arguments[arguments.index("--progress-endpoint") + 1] == env["endpoint"]
assert arguments[arguments.index("--registration-key") + 1] == env["registration_key_value"]
assert "admin" not in printed
print("PASS installer initialization/registration failure gates and actual teacher endpoint handoff")
