#!/usr/bin/env bash
set -Eeuo pipefail

# Run only in the original student's CloudShell. This does not deploy or reset a lab.
base_url="https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/v1.0.0"
state_dir="${JDU_STUDENT_STATE_DIR:-$HOME/.jdu-student}"
if [[ ! -s "$state_dir/progress.env" ]]; then
  printf '%s\n' 'ERROR Registration state was not found in this CloudShell.' \
    'Open the original CloudShell used for setup. If it is unavailable, ask your teacher; do not rerun the full installer.' >&2
  exit 2
fi

for command in curl sha256sum python3 awk install mktemp; do
  if ! command -v "$command" >/dev/null 2>&1; then
    printf 'ERROR Required command is unavailable: %s\n' "$command" >&2
    exit 2
  fi
done

download_dir="$(mktemp -d)"
trap 'rm -rf -- "$download_dir"' EXIT
curl -fsSL --retry 3 --connect-timeout 10 "$base_url/scripts/register-student.py" -o "$download_dir/register-student.py"
curl -fsSL --retry 3 --connect-timeout 10 "$base_url/SHA256SUMS" -o "$download_dir/SHA256SUMS"
expected_hash="$(awk '$2 == "scripts/register-student.py" {print $1}' "$download_dir/SHA256SUMS")"
if [[ ! "$expected_hash" =~ ^[0-9a-f]{64}$ ]]; then
  printf '%s\n' 'ERROR Registration script checksum is missing or invalid.' >&2
  exit 1
fi
printf '%s  %s\n' "$expected_hash" "$download_dir/register-student.py" | sha256sum --check --status

install -d -m 0755 "$HOME/.local/bin"
install -m 0755 "$download_dir/register-student.py" "$HOME/.local/bin/jdu-register"
printf '%s\n' 'Registration tool updated. Enter your Google Classroom email below.'
JDU_STUDENT_STATE_DIR="$state_dir" python3 "$HOME/.local/bin/jdu-register" --change-email
