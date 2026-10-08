#!/usr/bin/env bash
set -Eeuo pipefail

helper="$1"
fixture="$2"
setup="$3"
test_dir="$(mktemp -d)"
trap 'rm -rf -- "$test_dir"' EXIT
mkdir -p "$test_dir/bin"
cat > "$test_dir/bin/systemctl" <<'MOCK'
#!/bin/sh
case "$1" in
  is-system-running) printf '%s\n' "${MOCK_SYSTEM_STATE:-running}" ;;
  start) printf '%s\n' "$2" >> "$MOCK_START_LOG" ;;
  *) exit 2 ;;
esac
MOCK
chmod 0755 "$test_dir/bin/systemctl"
export PATH="$test_dir/bin:$PATH"
export JDU_PROCESS_STATE_DIR="$test_dir/state"
export MOCK_START_LOG="$test_dir/started"

bash "$helper" stop P3
[[ -f "$JDU_PROCESS_STATE_DIR/P3-process2" ]]
bash "$helper" resume
[[ "$(wc -l < "$MOCK_START_LOG")" -eq 5 ]]
! grep -Fq 'jdu-p3-process2.service' "$MOCK_START_LOG"
grep -Fq 'jdu-m3-process2.service' "$MOCK_START_LOG"

bash "$helper" start P3
[[ ! -e "$JDU_PROCESS_STATE_DIR/P3-process2" ]]
: > "$MOCK_START_LOG"
bash "$helper" resume
[[ "$(wc -l < "$MOCK_START_LOG")" -eq 6 ]]

touch "$JDU_PROCESS_STATE_DIR/P3-needs-review"
: > "$MOCK_START_LOG"
bash "$helper" resume
[[ "$(wc -l < "$MOCK_START_LOG")" -eq 3 ]]
! grep -Fq 'jdu-p3-' "$MOCK_START_LOG"
rm "$JDU_PROCESS_STATE_DIR/P3-needs-review"

MOCK_SYSTEM_STATE=stopping bash "$helper" stop M3
[[ ! -e "$JDU_PROCESS_STATE_DIR/M3-process2" ]]
SERVICE_RESULT=exit-code bash "$helper" stop M3
[[ ! -e "$JDU_PROCESS_STATE_DIR/M3-process2" ]]
grep -Fq 'jdu-process-state install-units' "$setup"
grep -Fq 'rm -f -- /var/lib/jdu-lab/stopped/P3-process2' "$fixture"
grep -Fq 'rm -f -- /var/lib/jdu-lab/stopped/M3-process2' "$fixture"
grep -Fq 'WantedBy=multi-user.target' "$helper"
printf '%s\n' 'PASS P3/M3 reboot resume preserves completed stops and reset can clear markers'
