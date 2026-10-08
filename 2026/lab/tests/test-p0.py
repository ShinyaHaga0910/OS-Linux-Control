import os
import subprocess
import sys
import tempfile
from pathlib import Path

checker = Path(sys.argv[1]).resolve()
def output(*args):
    return subprocess.check_output(args, text=True).strip()
release = dict(line.split("=", 1) for line in Path("/etc/os-release").read_text().splitlines() if "=" in line)
values = {
    "OS_ID": release["ID"].strip('"'),
    "OS_VERSION_ID": release["VERSION_ID"].strip('"'),
    "KERNEL_RELEASE": output("uname", "-r"),
    "PID1_COMM": Path("/proc/1/comm").read_text().strip(),
    "USER_NAME": output("id", "-un"),
    "HOST_NAME": output("hostname"),
}
with tempfile.TemporaryDirectory(prefix="jdu-p0-") as home:
    env = dict(os.environ, HOME=home, JDU_STUDENT_USER=values["USER_NAME"])
    record = Path(home) / "jdu-lab/p0/observation.env"
    record.parent.mkdir(parents=True)
    content = "".join(f"{key}={value}\n" for key, value in values.items())
    record.write_text(content)
    def check(mission, passed):
        result = subprocess.run(["bash", str(checker), mission, "--no-submit"], env=env, text=True, capture_output=True)
        assert result.returncode == (0 if passed == 6 else 1), result.stdout + result.stderr
        assert f"{passed} / 6 checks cleared" in result.stdout, result.stdout
    check("P0", 6)
    check("M0", 6)
    record.write_text(content.replace("OS_ID=" + values["OS_ID"], "OS_ID=wrong"))
    check("P0", 5)
    record.unlink()
    legacy = record.parent.parent / "m0/observation.env"
    legacy.parent.mkdir()
    legacy.write_text(content)
    # An initialized/reset P0 must not revive old M0 evidence.
    check("P0", 0)
    record.parent.rmdir()
    check("P0", 0)
    record.parent.mkdir()
    record.write_text(content)
    check("P0", 6)
print("PASS P0 live observations, incorrect value, M0 alias, and canonical p0 path")
