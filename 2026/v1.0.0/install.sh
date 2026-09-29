#!/usr/bin/env bash
set -Eeuo pipefail

VERSION="v1.0.0"
STACK_NAME="jdu-intro-cybersecurity-2026"
INSTANCE_TYPE="t3.micro"
INSTANCE_PROFILE_NAME="LabInstanceProfile"
REGION="${AWS_REGION:-${AWS_DEFAULT_REGION:-}}"
BASE_URL="https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/${VERSION}"
SSH_KEY_PATH="${JDU_SSH_KEY_PATH:-$HOME/.ssh/jdu-intro-cybersecurity-2026}"
PROGRESS_ENDPOINT="${JDU_PROGRESS_ENDPOINT:-}"
REGISTRATION_KEY="${JDU_PROGRESS_REGISTRATION_KEY:-}"
student_state_dir="${JDU_STUDENT_STATE_DIR:-$HOME/.jdu-student}"

usage() {
  printf '%s\n' "Usage: bash install.sh [--region REGION] [--stack-name NAME] [--instance-type t2.micro|t3.micro] [--instance-profile NAME] [--progress-endpoint HTTPS_URL --registration-key KEY]"
}

while (($#)); do
  case "$1" in
    --region) REGION="${2:?Missing region}"; shift 2 ;;
    --stack-name) STACK_NAME="${2:?Missing stack name}"; shift 2 ;;
    --instance-type) INSTANCE_TYPE="${2:?Missing instance type}"; shift 2 ;;
    --instance-profile) INSTANCE_PROFILE_NAME="${2:?Missing instance profile}"; shift 2 ;;
    --progress-endpoint) PROGRESS_ENDPOINT="${2:?Missing endpoint}"; shift 2 ;;
    --registration-key) REGISTRATION_KEY="${2:?Missing registration key}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'ERROR Unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done

for command_name in aws curl sha256sum ssh ssh-keygen base64 sort openssl python3; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'ERROR Required command is missing: %s\n' "$command_name" >&2
    exit 2
  fi
done

if [[ -z "$REGION" ]]; then
  REGION="$(aws configure get region 2>/dev/null || true)"
fi
if [[ -z "$REGION" ]]; then
  printf '%s\n' 'ERROR AWS region is not configured. Use --region.' >&2
  exit 2
fi

case "$INSTANCE_TYPE" in
  t2.micro|t3.micro) ;;
  *) printf 'ERROR Unsupported instance type: %s\n' "$INSTANCE_TYPE" >&2; exit 2 ;;
esac

if [[ ! "$PROGRESS_ENDPOINT" =~ ^https://[^[:space:]]+$ || ! "$REGISTRATION_KEY" =~ ^[0-9a-f]{64}$ ]]; then
  printf '%s\n' 'ERROR Use the complete setup command provided privately by your teacher in Google Classroom. The course endpoint and semester registration key are required.' >&2
  exit 2
fi

export AWS_PAGER=""
work_dir="$(mktemp -d)"
trap 'rm -rf -- "$work_dir"' EXIT

ensure_session_manager_plugin() {
  local minimum_version='1.2.764.0' current_version=''
  if command -v session-manager-plugin >/dev/null 2>&1; then
    current_version="$(session-manager-plugin --version 2>/dev/null | tr -d '[:space:]')"
    if [[ "$current_version" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] && \
       [[ "$(printf '%s\n' "$minimum_version" "$current_version" | sort -V | head -n 1)" == "$minimum_version" ]]; then
      return 0
    fi
    printf 'Updating the AWS Session Manager plugin from %s...\n' "${current_version:-unknown version}"
  fi

  local architecture package_url
  architecture="$(uname -m)"
  case "$architecture" in
    x86_64) package_url="https://s3.amazonaws.com/session-manager-downloads/plugin/latest/linux_64bit/session-manager-plugin.rpm" ;;
    aarch64|arm64) package_url="https://s3.amazonaws.com/session-manager-downloads/plugin/latest/linux_arm64/session-manager-plugin.rpm" ;;
    *) printf 'ERROR Unsupported CloudShell architecture: %s\n' "$architecture" >&2; exit 2 ;;
  esac

  if ! command -v dnf >/dev/null 2>&1 || ! command -v sudo >/dev/null 2>&1; then
    printf '%s\n' 'ERROR Session Manager plugin is missing and automatic CloudShell installation is unavailable.' >&2
    exit 2
  fi
  printf '%s\n' 'Installing the AWS Session Manager plugin in CloudShell...'
  sudo dnf install -y "$package_url" >/dev/null
  command -v session-manager-plugin >/dev/null 2>&1 || {
    printf '%s\n' 'ERROR Session Manager plugin installation failed.' >&2
    exit 2
  }
  current_version="$(session-manager-plugin --version 2>/dev/null | tr -d '[:space:]')"
  if [[ ! "$current_version" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] || \
     [[ "$(printf '%s\n' "$minimum_version" "$current_version" | sort -V | head -n 1)" != "$minimum_version" ]]; then
    printf 'ERROR Session Manager plugin is too old: %s\n' "${current_version:-unknown version}" >&2
    exit 2
  fi
}

prepare_ssh_key() {
  install -d -m 0700 "$HOME/.ssh"
  if [[ -e "$SSH_KEY_PATH.pub" && ! -e "$SSH_KEY_PATH" ]]; then
    printf 'ERROR Public key exists but its private key is missing: %s\n' "$SSH_KEY_PATH" >&2
    exit 2
  fi
  if [[ ! -e "$SSH_KEY_PATH" ]]; then
    printf 'Creating the CloudShell-only SSH key: %s\n' "$SSH_KEY_PATH"
    ssh-keygen -q -t ed25519 -N '' -C 'jdu-intro-cybersecurity-2026-cloudshell' -f "$SSH_KEY_PATH"
  fi
  if [[ ! -e "$SSH_KEY_PATH.pub" ]]; then
    ssh-keygen -y -f "$SSH_KEY_PATH" > "$SSH_KEY_PATH.pub"
  fi
  chmod 0600 "$SSH_KEY_PATH"
  chmod 0644 "$SSH_KEY_PATH.pub"
  if [[ "$(wc -l < "$SSH_KEY_PATH.pub")" -ne 1 ]] || ! grep -Eq '^ssh-ed25519 [A-Za-z0-9+/=]+( .*)?$' "$SSH_KEY_PATH.pub"; then
    printf 'ERROR The SSH public key is not a valid single-line Ed25519 key: %s\n' "$SSH_KEY_PATH.pub" >&2
    exit 2
  fi
}

write_ssh_config() {
  local instance_id="$1" include_line='Include ~/.ssh/config.d/*' config_file config_fragment temporary_file
  config_file="$HOME/.ssh/config"
  config_fragment="$HOME/.ssh/config.d/jdu-intro-cybersecurity-2026.conf"
  install -d -m 0700 "$HOME/.ssh/config.d"
  cat > "$config_fragment" <<EOF
Host jdu-ubuntu
    HostName $instance_id
    User ssm-user
    IdentityFile $SSH_KEY_PATH
    IdentitiesOnly yes
    ProxyCommand sh -c "aws ssm start-session --region $REGION --target %h --document-name AWS-StartSSHSession --parameters portNumber=%p"
    StrictHostKeyChecking accept-new
EOF
  chmod 0600 "$config_fragment"

  if [[ ! -f "$config_file" ]] || ! grep -Fqx "$include_line" "$config_file"; then
    temporary_file="$(mktemp "$HOME/.ssh/config.XXXXXX")"
    printf '%s\n\n' "$include_line" > "$temporary_file"
    if [[ -f "$config_file" ]]; then
      cat "$config_file" >> "$temporary_file"
    fi
    mv -f -- "$temporary_file" "$config_file"
  fi
  chmod 0600 "$config_file"
}

ensure_session_manager_plugin
prepare_ssh_key
student_public_key_base64="$(base64 < "$SSH_KEY_PATH.pub" | tr -d '\r\n')"
progress_endpoint_base64=''
progress_registration_key_base64=''
progress_server_id=''
progress_server_token_base64=''
if [[ -n "$PROGRESS_ENDPOINT" ]]; then
  install -d -m 0700 "$student_state_dir"
  progress_identity_file="$student_state_dir/progress.env"
  if [[ -r "$progress_identity_file" ]]; then
    progress_server_id="$(sed -n 's/^JDU_PROGRESS_SERVER_ID=//p' "$progress_identity_file" | tail -n 1)"
    progress_server_token="$(sed -n 's/^JDU_PROGRESS_SERVER_TOKEN=//p' "$progress_identity_file" | tail -n 1)"
  else
    progress_server_id="srv-$(openssl rand -hex 8)"
    progress_server_token="$(openssl rand -hex 32)"
  fi
  if [[ ! "$progress_server_id" =~ ^[A-Za-z0-9_-]{8,64}$ || ${#progress_server_token} -lt 32 ]]; then
    printf '%s\n' 'ERROR The saved student progress identity is invalid.' >&2
    exit 2
  fi
  printf 'JDU_PROGRESS_ENDPOINT=%s\nJDU_PROGRESS_SERVER_ID=%s\nJDU_PROGRESS_SERVER_TOKEN=%s\n' \
    "$PROGRESS_ENDPOINT" "$progress_server_id" "$progress_server_token" > "$progress_identity_file"
  chmod 0600 "$progress_identity_file"
  progress_endpoint_base64="$(printf '%s' "$PROGRESS_ENDPOINT" | base64 | tr -d '\r\n')"
  progress_registration_key_base64="$(printf '%s' "$REGISTRATION_KEY" | base64 | tr -d '\r\n')"
  progress_server_token_base64="$(printf '%s' "$progress_server_token" | base64 | tr -d '\r\n')"
fi

template_path="$work_dir/lab-environment.json"
checker_path="$work_dir/check-aws-environment.sh"
cloudcheck_path="$work_dir/jdu-cloudcheck"
cloudreset_path="$work_dir/jdu-cloud-reset"
registration_path="$work_dir/register-student.py"
personal_progress_path="$work_dir/jdu-my-progress"
checksums_path="$work_dir/SHA256SUMS"

printf '%s\n' 'Downloading the fixed-version lab files...'
curl -fsSL --retry 3 "$BASE_URL/cloudformation/lab-environment.json" -o "$template_path"
curl -fsSL --retry 3 "$BASE_URL/scripts/check-aws-environment.sh" -o "$checker_path"
curl -fsSL --retry 3 "$BASE_URL/scripts/jdu-cloudcheck" -o "$cloudcheck_path"
curl -fsSL --retry 3 "$BASE_URL/scripts/jdu-cloud-reset" -o "$cloudreset_path"
curl -fsSL --retry 3 "$BASE_URL/scripts/register-student.py" -o "$registration_path"
curl -fsSL --retry 3 "$BASE_URL/scripts/jdu-my-progress" -o "$personal_progress_path"
curl -fsSL --retry 3 "$BASE_URL/SHA256SUMS" -o "$checksums_path"
chmod 0755 "$checker_path"
chmod 0755 "$cloudcheck_path"
chmod 0755 "$cloudreset_path"

verify_download() {
  local published_path="$1" local_path="$2" expected
  expected="$(awk -v path="$published_path" '$2 == path {print $1}' "$checksums_path")"
  if [[ ! "$expected" =~ ^[0-9a-f]{64}$ ]]; then
    printf 'ERROR Missing checksum for %s\n' "$published_path" >&2
    exit 2
  fi
  printf '%s  %s\n' "$expected" "$local_path" | sha256sum --check --status
}

verify_download cloudformation/lab-environment.json "$template_path"
verify_download scripts/check-aws-environment.sh "$checker_path"
verify_download scripts/jdu-cloudcheck "$cloudcheck_path"
verify_download scripts/jdu-cloud-reset "$cloudreset_path"
verify_download scripts/register-student.py "$registration_path"
verify_download scripts/jdu-my-progress "$personal_progress_path"
printf '%s\n' 'PASS Download checksums match.'

install -d -m 0755 "$HOME/.local/bin"
install -m 0755 "$cloudcheck_path" "$HOME/.local/bin/jdu-cloudcheck"
install -m 0755 "$cloudcheck_path" "$HOME/.local/bin/jdu-check"
install -m 0755 "$cloudreset_path" "$HOME/.local/bin/jdu-reset"
"$HOME/.local/bin/jdu-reset" P6
"$HOME/.local/bin/jdu-reset" M6

printf '%s\n' 'Checking AWS login and CloudFormation template...'
aws sts get-caller-identity --region "$REGION" --output json >/dev/null
aws cloudformation validate-template --region "$REGION" --template-body "file://$template_path" >/dev/null

select_lab_availability_zone() {
  local subnet_id existing_zone offered_zone
  aws ec2 describe-instance-type-offerings --region "$REGION" \
    --location-type availability-zone --filters "Name=instance-type,Values=$INSTANCE_TYPE" \
    --query 'InstanceTypeOfferings[].Location' --output text > "$work_dir/offered-zones.txt" || return 1
  aws ec2 describe-availability-zones --region "$REGION" \
    --filters Name=state,Values=available --query 'AvailabilityZones[].ZoneName' \
    --output text > "$work_dir/available-zones.txt" || return 1
  offered_zone="$(python3 - "$work_dir/offered-zones.txt" "$work_dir/available-zones.txt" <<'PY'
import pathlib, sys
offered, available = (set(pathlib.Path(p).read_text().split()) - {'None'} for p in sys.argv[1:])
zones = sorted(offered & available)
if not zones:
    sys.exit('ERROR No available Availability Zone supports the selected instance type.')
print(zones[0])
PY
)" || return 1
  # Preserve an existing subnet's placement during ordinary installer updates.
  subnet_id="$(aws cloudformation describe-stack-resource --region "$REGION" \
    --stack-name "$STACK_NAME" --logical-resource-id PublicSubnet \
    --query 'StackResourceDetail.PhysicalResourceId' --output text 2>/dev/null || true)"
  if [[ "$subnet_id" == subnet-* ]]; then
    existing_zone="$(aws ec2 describe-subnets --region "$REGION" --subnet-ids "$subnet_id" \
      --query 'Subnets[0].AvailabilityZone' --output text)" || return 1
    if ! tr '[:space:]' '\n' < "$work_dir/offered-zones.txt" | grep -Fxq "$existing_zone"; then
      printf 'ERROR Existing subnet zone %s does not support %s. No resources were moved.\n' "$existing_zone" "$INSTANCE_TYPE" >&2
      return 1
    fi
    offered_zone="$existing_zone"
  fi
  printf '%s\n' "$offered_zone"
}
lab_availability_zone="$(select_lab_availability_zone)"
printf 'Selected Availability Zone: %s (%s)\n' "$lab_availability_zone" "$INSTANCE_TYPE"
printf 'Deploying stack %s in %s...\n' "$STACK_NAME" "$REGION"
aws cloudformation deploy \
  --region "$REGION" \
  --stack-name "$STACK_NAME" \
  --template-file "$template_path" \
  --parameter-overrides \
    "InstanceType=$INSTANCE_TYPE" \
    "LabAvailabilityZone=$lab_availability_zone" \
    "InstanceProfileName=$INSTANCE_PROFILE_NAME" \
    "LabVersion=$VERSION" \
    "StudentSshPublicKeyBase64=$student_public_key_base64" \
    "ProgressEndpointBase64=$progress_endpoint_base64" \
    "ProgressRegistrationKeyBase64=$progress_registration_key_base64" \
    "ProgressServerId=$progress_server_id" \
    "ProgressServerTokenBase64=$progress_server_token_base64" \
  --no-fail-on-empty-changeset

printf '%s\n' 'Running the AWS environment acceptance check...'
"$checker_path" --region "$REGION" --stack-name "$STACK_NAME" --wait

instance_id="$(aws cloudformation describe-stacks --region "$REGION" --stack-name "$STACK_NAME" --query "Stacks[0].Outputs[?OutputKey=='InstanceId'].OutputValue | [0]" --output text)"
write_ssh_config "$instance_id"

printf '%s\n' 'Checking SSH through the Session Manager tunnel...'
ssh_ready=false
for attempt in {1..20}; do
  if remote_user="$(ssh -o BatchMode=yes -o ConnectTimeout=15 jdu-ubuntu 'id -un' 2>/dev/null)" && [[ "$remote_user" == 'ssm-user' ]]; then
    ssh_ready=true
    break
  fi
  if ((attempt < 20)); then sleep 6; fi
done
if ! $ssh_ready; then
  printf '%s\n' 'ERROR The instance is online in Systems Manager, but the SSH acceptance check failed.' >&2
  printf '%s\n' 'Run: ssh -vv jdu-ubuntu' >&2
  exit 1
fi

printf '%s\n' 'Checking Ubuntu initialization (this can take several minutes)...'
setup_ready=false
for attempt in {1..40}; do
  if ssh -o BatchMode=yes -o ConnectTimeout=15 jdu-ubuntu \
    'test -f /var/lib/cloud/instance/boot-finished && sudo cloud-init status >/dev/null && sudo grep -Fxq JDU_SETUP_COMPLETE /var/log/cloud-init-output.log'; then
    setup_ready=true
    break
  fi
  if ((attempt < 40)); then sleep 6; fi
done
if ! $setup_ready; then
  printf '%s\n' 'ERROR Ubuntu initialization or initial progress registration did not complete. Ask your teacher; do not recreate the stack yet.' >&2
  exit 1
fi
printf '%s\n' 'PASS Ubuntu initialization is complete.'
if [[ -n "$progress_server_id" ]]; then
  install -m 0755 "$registration_path" "$HOME/.local/bin/jdu-register"
  install -m 0755 "$personal_progress_path" "$HOME/.local/bin/jdu-my-progress"
  JDU_STUDENT_STATE_DIR="$student_state_dir" JDU_INSTANCE_ID="$instance_id" python3 "$registration_path"
fi

printf '\n%s\n' 'PASS The AWS lab environment is ready.'
printf 'Instance ID: %s\n' "$instance_id"
printf 'Private key: %s (keep this file in CloudShell)\n' "$SSH_KEY_PATH"
printf '%s\n' 'Connect to Ubuntu with: ssh jdu-ubuntu'
printf '%s\n' 'Start the fully guided practice with: jdu-check P1'
printf '%s\n' 'Check Mission 6 in CloudShell with: jdu-check M6'
if [[ -n "$progress_server_id" ]]; then
  printf 'Progress server ID: %s\n' "$progress_server_id"
  printf '%s\n' 'Check and automatically report a result from Ubuntu with: jdu-check M1'
fi
printf '%s\n' 'The Security Group still has no inbound TCP 22 rule.'
