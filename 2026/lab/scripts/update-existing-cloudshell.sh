#!/usr/bin/env bash
set -Eeuo pipefail

# Update CloudShell helpers and the existing Ubuntu host; never deploy a stack.
region=''
stack_name='jdu-intro-cybersecurity-2026'
ssh_host='jdu-ubuntu'
change_email=false
state_dir="${JDU_STUDENT_STATE_DIR:-$HOME/.jdu-student}"
base_url="${JDU_UPDATE_BASE_URL:-https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab}"

usage() {
  printf '%s\n' 'Usage: bash update-existing-cloudshell.sh --region REGION [--stack-name NAME] [--ssh-host HOST] [--change-email]'
}

while (($#)); do
  case "$1" in
    --region) region="${2:?Missing region}"; shift 2 ;;
    --stack-name) stack_name="${2:?Missing stack name}"; shift 2 ;;
    --ssh-host) ssh_host="${2:?Missing SSH host}"; shift 2 ;;
    --change-email) change_email=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
done
if [[ ! "$region" =~ ^[a-z]{2}(-gov)?-[a-z]+-[0-9]+$ || ! "$stack_name" =~ ^[A-Za-z][A-Za-z0-9-]{0,127}$ || ! "$ssh_host" =~ ^[A-Za-z0-9_-]+$ ]]; then
  printf '%s\n' 'ERROR Region, stack name, or SSH host is invalid.' >&2
  exit 2
fi
config="$state_dir/progress.env"
if [[ ! -s "$config" ]]; then
  printf '%s\n' 'ERROR Existing student registration is missing. Do not run the initial installer again.' >&2
  exit 2
fi
for tool in aws ssh curl sha256sum awk mktemp install base64 sed; do
  command -v "$tool" >/dev/null 2>&1 || { printf 'ERROR Missing command: %s\n' "$tool" >&2; exit 2; }
done
server_id="$(sed -n 's/^JDU_PROGRESS_SERVER_ID=//p' "$config" | tail -n 1)"
endpoint="$(sed -n 's/^JDU_PROGRESS_ENDPOINT=//p' "$config" | tail -n 1)"
token="$(sed -n 's/^JDU_PROGRESS_SERVER_TOKEN=//p' "$config" | tail -n 1)"
if [[ ! "$server_id" =~ ^[A-Za-z0-9_-]{8,64}$ || ! "$endpoint" =~ ^https://[^[:space:]]+$ || ${#token} -lt 32 ]]; then
  printf '%s\n' 'ERROR Saved student registration is incomplete. Nothing was changed.' >&2
  exit 2
fi
unset token
stack_status="$(aws cloudformation describe-stacks --region "$region" --stack-name "$stack_name" --query 'Stacks[0].StackStatus' --output text 2>/dev/null)" || {
  printf '%s\n' 'ERROR The existing student stack was not found. No new stack was created.' >&2
  exit 2
}
if [[ "$stack_status" != CREATE_COMPLETE && "$stack_status" != UPDATE_COMPLETE ]]; then
  printf 'ERROR Student stack is %s, not ready for an ordinary update.\n' "$stack_status" >&2
  exit 2
fi
instance_id="$(aws cloudformation describe-stacks --region "$region" --stack-name "$stack_name" --query "Stacks[0].Outputs[?OutputKey=='InstanceId'].OutputValue | [0]" --output text)"
ssh_target="$(ssh -G "$ssh_host" | awk '$1 == "hostname" {print $2; exit}')"
if [[ ! "$instance_id" =~ ^i-[0-9a-f]+$ || "$ssh_target" != "$instance_id" ]]; then
  printf '%s\n' 'ERROR SSH host does not point to the existing student stack. Nothing was changed.' >&2
  exit 2
fi
remote_identity="$(ssh -o BatchMode=yes -o ConnectTimeout=20 "$ssh_host" \
  'test "$(id -un)" = ssm-user && test -r /etc/jdu-lab/progress.env && printf "%s\n" "$(sed -n "s/^JDU_PROGRESS_SERVER_ID=//p" /etc/jdu-lab/progress.env)" "$(sed -n "s/^JDU_PROGRESS_ENDPOINT_B64=//p" /etc/jdu-lab/progress.env | base64 -d)"')" || {
  printf '%s\n' 'ERROR Cannot read the existing Ubuntu registration. Nothing was changed.' >&2
  exit 2
}
remote_server_id="${remote_identity%%$'\n'*}"
remote_endpoint="${remote_identity#*$'\n'}"
if [[ "$remote_server_id" != "$server_id" || "$remote_endpoint" != "$endpoint" ]]; then
  printf '%s\n' 'ERROR CloudShell and Ubuntu registration do not match. Nothing was changed.' >&2
  exit 2
fi

work_dir="$(mktemp -d)"
trap 'rm -rf -- "$work_dir"' EXIT
curl -fsSL --retry 3 --connect-timeout 10 "$base_url/SHA256SUMS" -o "$work_dir/SHA256SUMS"
for script_name in jdu-cloudcheck jdu-cloud-reset register-student.py jdu-my-progress update-existing-ubuntu.sh; do
  curl -fsSL --retry 3 --connect-timeout 10 "$base_url/scripts/$script_name" -o "$work_dir/$script_name"
  expected="$(awk -v path="scripts/$script_name" '$2 == path {print $1}' "$work_dir/SHA256SUMS")"
  if [[ ! "$expected" =~ ^[0-9a-f]{64}$ ]] || ! printf '%s  %s\n' "$expected" "$work_dir/$script_name" | sha256sum --check --status; then
    printf 'ERROR Download verification failed for %s. No scripts were installed.\n' "$script_name" >&2
    exit 1
  fi
done

# The Ubuntu updater changes commands and boot units, not exercise files or registration.
ssh -o BatchMode=yes -o ConnectTimeout=20 "$ssh_host" bash -s < "$work_dir/update-existing-ubuntu.sh"
install -d -m 0755 "$HOME/.local/bin"
install -m 0755 "$work_dir/jdu-cloudcheck" "$HOME/.local/bin/jdu-cloudcheck"
install -m 0755 "$work_dir/jdu-cloudcheck" "$HOME/.local/bin/jdu-check"
install -m 0755 "$work_dir/jdu-cloud-reset" "$HOME/.local/bin/jdu-reset"
install -m 0755 "$work_dir/register-student.py" "$HOME/.local/bin/jdu-register"
install -m 0755 "$work_dir/jdu-my-progress" "$HOME/.local/bin/jdu-my-progress"
printf '%s\n' 'PASS CloudShell and Ubuntu tools updated without recreating or resetting the stack.'

if $change_email || [[ ! -s "$state_dir/student-email.txt" ]]; then
  printf '%s\n' 'Enter and confirm your university email in this CloudShell.'
  JDU_STUDENT_STATE_DIR="$state_dir" JDU_INSTANCE_ID="$instance_id" "$HOME/.local/bin/jdu-register" --change-email
else
  printf '%s\n' 'Saved email was kept. To correct it later, run jdu-register --change-email.'
fi
