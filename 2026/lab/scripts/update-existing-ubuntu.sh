#!/usr/bin/env bash
set -Eeuo pipefail

# Update an existing course Ubuntu host without resetting student work.
if [[ "$(id -un)" != ssm-user ]]; then
  printf '%s\n' 'ERROR Run this on the course Ubuntu host as ssm-user.' >&2
  exit 2
fi
if [[ ! -d /opt/jdu-lab/fixtures/p3 || ! -d /opt/jdu-lab/fixtures/m3 || ! -f /etc/jdu-lab/progress.env ]]; then
  printf '%s\n' 'ERROR This is not an initialized JDU course Ubuntu host.' >&2
  exit 2
fi
for command_name in curl sha256sum awk install mktemp sudo systemctl; do
  command -v "$command_name" >/dev/null 2>&1 || {
    printf 'ERROR Required command is unavailable: %s\n' "$command_name" >&2
    exit 2
  }
done

base_url="${JDU_UPDATE_BASE_URL:-https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab}"
download_dir="$(mktemp -d)"
trap 'rm -rf -- "$download_dir"' EXIT
curl -fsSL --retry 3 --connect-timeout 10 "$base_url/SHA256SUMS" -o "$download_dir/SHA256SUMS"

for script_name in jdu-labcheck jdu-fixture jdu-process-state jdu-my-progress; do
  curl -fsSL --retry 3 --connect-timeout 10 "$base_url/scripts/$script_name" -o "$download_dir/$script_name"
  expected="$(awk -v path="scripts/$script_name" '$2 == path {print $1}' "$download_dir/SHA256SUMS")"
  [[ "$expected" =~ ^[0-9a-f]{64}$ ]] || {
    printf 'ERROR Missing checksum for %s. No scripts were installed.\n' "$script_name" >&2
    exit 1
  }
  printf '%s  %s\n' "$expected" "$download_dir/$script_name" | sha256sum --check --status || {
    printf 'ERROR Checksum mismatch for %s. No scripts were installed.\n' "$script_name" >&2
    exit 1
  }
done

for script_name in jdu-labcheck jdu-fixture jdu-process-state jdu-my-progress; do
  sudo install -o root -g root -m 0755 "$download_dir/$script_name" "/opt/jdu-lab/bin/$script_name"
done
sudo install -o root -g root -m 0755 "$download_dir/jdu-my-progress" /usr/local/bin/jdu-my-progress
sudo /opt/jdu-lab/bin/jdu-process-state upgrade

printf '%s\n' 'PASS Ubuntu tools and P3/M3 boot units are updated without resetting exercise files.'
for mission in P3 M3; do
  if [[ -f "/var/lib/jdu-lab/stopped/$mission-needs-review" ]]; then
    printf 'REVIEW %s had an ambiguous old process state. If you have not completed it, run jdu-reset %s before starting.\n' "$mission" "$mission"
  fi
done
printf '%s\n' 'Run jdu-check P0, P3, M3, P4, and M4 as needed. Their current results are not changed until checked.'
printf '%s\n' 'Run jdu-my-progress to open the saved teacher service. The endpoint and credentials were not changed.'
