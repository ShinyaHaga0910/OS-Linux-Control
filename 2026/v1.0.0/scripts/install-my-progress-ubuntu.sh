#!/usr/bin/env bash
set -Eeuo pipefail

# Add only the personal progress command to an existing Ubuntu lab.
progress_config="${JDU_UBUNTU_PROGRESS_CONFIG:-/etc/jdu-lab/progress.env}"
install_dir="${JDU_UBUNTU_INSTALL_DIR:-/usr/local/bin}"
if [[ ! -r "$progress_config" ]]; then
  printf '%s\n' 'ERROR Ubuntu progress registration is not readable.' \
    'Run this on the course Ubuntu host as ssm-user, or ask your teacher to check the lab registration.' >&2
  exit 2
fi
for command in curl sha256sum awk install mktemp python3; do
  if ! command -v "$command" >/dev/null 2>&1; then
    printf 'ERROR Required command is unavailable: %s\n' "$command" >&2
    exit 2
  fi
done
if (( EUID != 0 )) && ! command -v sudo >/dev/null 2>&1; then
  printf '%s\n' 'ERROR sudo is required to install this command.' >&2
  exit 2
fi

base_url="https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/v1.0.0"
download_dir="$(mktemp -d)"
trap 'rm -rf -- "$download_dir"' EXIT
curl -fsSL --retry 3 --connect-timeout 10 "$base_url/scripts/jdu-my-progress" -o "$download_dir/jdu-my-progress"
curl -fsSL --retry 3 --connect-timeout 10 "$base_url/SHA256SUMS" -o "$download_dir/SHA256SUMS"
expected_hash="$(awk '$2 == "scripts/jdu-my-progress" {print $1}' "$download_dir/SHA256SUMS")"
if [[ ! "$expected_hash" =~ ^[0-9a-f]{64}$ ]]; then
  printf '%s\n' 'ERROR Personal progress checksum is missing or invalid.' >&2
  exit 1
fi
printf '%s  %s\n' "$expected_hash" "$download_dir/jdu-my-progress" | sha256sum --check --status

if (( EUID == 0 )); then
  install -m 0755 "$download_dir/jdu-my-progress" "$install_dir/jdu-my-progress"
else
  sudo install -m 0755 "$download_dir/jdu-my-progress" "$install_dir/jdu-my-progress"
fi
printf '%s\n' 'PASS jdu-my-progress is installed on Ubuntu. Run jdu-my-progress to open your personal dashboard.'
