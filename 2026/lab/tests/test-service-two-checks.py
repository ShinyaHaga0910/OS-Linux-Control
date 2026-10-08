"""Verify P4/M4 state transitions without changing host systemd units."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


checker = Path(sys.argv[1]).resolve()
with tempfile.TemporaryDirectory(prefix="jdu-service-state-") as directory:
    root = Path(directory)
    bin_dir = root / "bin"
    bin_dir.mkdir()
    for name, body in {
        "cat": """#!/bin/sh
case "$1" in
  /opt/jdu-lab/fixtures/?4/*.sha256) printf 'unchanged\n' ;;
  *) exec /bin/cat "$@" ;;
esac
""",
        "sha256sum": """#!/bin/sh
case "$1" in
  /opt/jdu-lab/fixtures/?4/*.service) printf 'unchanged  %s\n' "$1" ;;
  /etc/systemd/system/jdu-*.service)
    if [ "${MOCK_CHANGED:-0}" = 1 ]; then printf 'changed  %s\n' "$1";
    else printf 'unchanged  %s\n' "$1"; fi ;;
  *) exec /usr/bin/sha256sum "$@" ;;
esac
""",
        "systemctl": """#!/bin/sh
case "$1" in
  is-active) printf '%s\n' "${MOCK_ACTIVE:-inactive}" ;;
  is-enabled) printf '%s\n' "${MOCK_ENABLED:-disabled}" ;;
  *) exit 2 ;;
esac
""",
    }.items():
        path = bin_dir / name
        path.write_text(body)
        path.chmod(0o755)

    for mission in ("P4", "M4"):
        for active, enabled, changed, expected in (
            ("inactive", "disabled", "0", 0),
            ("active", "disabled", "0", 1),
            ("active", "enabled", "0", 2),
            ("active", "enabled", "1", 0),
        ):
            env = dict(os.environ)
            env.update(
                HOME=str(root),
                JDU_STUDENT_USER=subprocess.check_output(["id", "-un"], text=True).strip(),
                PATH=f"{bin_dir}:{env['PATH']}",
                MOCK_ACTIVE=active,
                MOCK_ENABLED=enabled,
                MOCK_CHANGED=changed,
            )
            result = subprocess.run(
                ["bash", str(checker), mission, "--no-submit"],
                env=env,
                capture_output=True,
                text=True,
            )
            assert f"RESULT    {expected} / 2 checks cleared" in result.stdout, result.stdout + result.stderr
            assert result.returncode == (0 if expected == 2 else 1), result.stdout + result.stderr

print("PASS P4/M4 start, enable, and changed-unit outcomes use two checks")
