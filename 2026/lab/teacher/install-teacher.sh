#!/usr/bin/env bash
set -Eeuo pipefail

VERSION="v1.0.0"
STACK_NAME="jdu-linux-progress-2026-v140"
ROLE_NAME="LabRole"
REGION="${AWS_REGION:-${AWS_DEFAULT_REGION:-}}"
BASE_URL="https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab"
state_dir="${JDU_TEACHER_STATE_DIR:-$HOME/.jdu-teacher}"
ROTATE_REGISTRATION_KEY=false
# Fingerprint of the retired publicly distributed key; never accept it again.
RETIRED_REGISTRATION_HASH="a3e404ef200f59946a59d8f6f0295fef25c0e0fd46a6112848501b31b12d217d"

usage() {
  printf '%s\n' 'Usage: bash install-teacher.sh [--region REGION] [--stack-name NAME] [--role-name LabRole] [--rotate-registration-key]'
}

while (($#)); do
  case "$1" in
    --region) REGION="${2:?Missing region}"; shift 2 ;;
    --stack-name) STACK_NAME="${2:?Missing stack name}"; shift 2 ;;
    --role-name) ROLE_NAME="${2:?Missing role name}"; shift 2 ;;
    --rotate-registration-key) ROTATE_REGISTRATION_KEY=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'ERROR Unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done

for command_name in aws curl sha256sum openssl python3; do
  command -v "$command_name" >/dev/null 2>&1 || {
    printf 'ERROR Required command is missing: %s\n' "$command_name" >&2
    exit 2
  }
done

if [[ -z "$REGION" ]]; then
  REGION="$(aws configure get region 2>/dev/null || true)"
fi
if [[ -z "$REGION" ]]; then
  printf '%s\n' 'ERROR AWS region is not configured. Use --region.' >&2
  exit 2
fi
if [[ ! "$ROLE_NAME" =~ ^[A-Za-z0-9+=,.@_-]+$ ]]; then
  printf '%s\n' 'ERROR Invalid Lambda role name.' >&2
  exit 2
fi

export AWS_PAGER=""
stack_status=''
if stack_status="$(aws cloudformation describe-stacks --region "$REGION" --stack-name "$STACK_NAME" --query 'Stacks[0].StackStatus' --output text 2>&1)"; then
  :
elif [[ "$stack_status" == *ValidationError* && "$stack_status" == *'does not exist'* ]]; then
  stack_status='NOT_FOUND'
else
  printf 'ERROR Could not inspect the teacher stack before handling keys: %s\n' "$stack_status" >&2
  exit 2
fi

umask 077
install -d -m 0700 "$state_dir"
admin_key_file="$state_dir/admin.key"
registration_key_file="$state_dir/registration.key"
config_file="$state_dir/progress.env"
pending_key_file="$state_dir/registration.pending.key"

if [[ -s "$config_file" ]]; then
  if [[ "$stack_status" == NOT_FOUND ]]; then
    printf '%s\n' 'ERROR Saved teacher configuration exists, but the matching AWS stack does not. Do not recreate it during a routine update.' >&2
    exit 2
  fi
  saved_stack="$(sed -n 's/^JDU_PROGRESS_STACK=//p' "$config_file" | tail -n 1)"
  if [[ "$saved_stack" != "$STACK_NAME" ]]; then
    printf '%s\n' 'ERROR This teacher key directory belongs to another stack. Use the original key directory for the requested stack.' >&2
    exit 2
  fi
fi
if [[ "$stack_status" != NOT_FOUND && ! -s "$config_file" ]]; then
  printf '%s\n' 'ERROR The existing teacher stack has no saved configuration in this directory. Restore the original teacher key directory before updating.' >&2
  exit 2
fi
if [[ "$stack_status" != NOT_FOUND && ! -s "$admin_key_file" ]]; then
  printf '%s\n' 'ERROR The existing teacher stack has no saved admin key in this directory. Restore the original key before updating.' >&2
  exit 2
fi
if [[ "$stack_status" != NOT_FOUND && ! -s "$registration_key_file" && "$ROTATE_REGISTRATION_KEY" == false ]]; then
  printf '%s\n' 'ERROR The existing teacher stack has no saved registration key in this directory. Restore the original key before updating.' >&2
  exit 2
fi
if [[ ! -s "$admin_key_file" ]]; then
  openssl rand -hex 32 > "$admin_key_file"
fi
registration_key_value=''
if [[ "$ROTATE_REGISTRATION_KEY" == false && -s "$registration_key_file" ]]; then
  registration_key_value="$(tr -d '\r\n' < "$registration_key_file")"
  if [[ -n "${JDU_PROGRESS_REGISTRATION_KEY:-}" && "$JDU_PROGRESS_REGISTRATION_KEY" != "$registration_key_value" ]]; then
    printf '%s\n' 'ERROR The supplied registration key differs from the saved key. Use --rotate-registration-key only if rotation is intended.' >&2
    exit 2
  fi
  if [[ -s "$pending_key_file" && "$(tr -d '\r\n' < "$pending_key_file")" != "$registration_key_value" ]]; then
    printf '%s\n' 'ERROR A pending registration key differs from the saved key. Resolve the pending update before continuing.' >&2
    exit 2
  fi
else
  registration_key_value="${JDU_PROGRESS_REGISTRATION_KEY:-}"
  if [[ -z "$registration_key_value" && -s "$pending_key_file" && "$ROTATE_REGISTRATION_KEY" == false ]]; then
    registration_key_value="$(tr -d '\r\n' < "$pending_key_file")"
  fi
fi
candidate_hash="$(printf '%s' "$registration_key_value" | sha256sum | awk '{print $1}')"
if [[ "$candidate_hash" == "$RETIRED_REGISTRATION_HASH" ]]; then
  printf '%s\n' 'ERROR The saved registration key was publicly distributed and is retired. No automatic rotation is performed; use --rotate-registration-key only after approving a key change.' >&2
  exit 2
fi
if [[ -z "$registration_key_value" ]]; then
  registration_key_value="$(openssl rand -hex 32)"
fi
if [[ ! "$registration_key_value" =~ ^[0-9a-f]{64}$ ]]; then
  printf '%s\n' 'ERROR The registration key must be 64 lowercase hexadecimal characters.' >&2
  exit 2
fi
printf '%s\n' "$registration_key_value" > "$pending_key_file"
chmod 0600 "$admin_key_file" "$pending_key_file"

admin_hash="$(tr -d '\r\n' < "$admin_key_file" | sha256sum | awk '{print $1}')"
registration_hash="$(printf '%s' "$registration_key_value" | sha256sum | awk '{print $1}')"

work_dir="$(mktemp -d)"
trap 'rm -rf -- "$work_dir"' EXIT
template_path="$work_dir/progress-server.json"
dashboard_path="$work_dir/jdu-dashboard"
checksums_path="$work_dir/SHA256SUMS"

printf '%s\n' 'Downloading the fixed-version teacher files...'
curl -fsSL --retry 3 "$BASE_URL/teacher/cloudformation/progress-server.json" -o "$template_path"
curl -fsSL --retry 3 "$BASE_URL/teacher/scripts/jdu-dashboard" -o "$dashboard_path"
curl -fsSL --retry 3 "$BASE_URL/SHA256SUMS" -o "$checksums_path"

verify_download() {
  local published_path="$1" local_path="$2" expected
  expected="$(awk -v path="$published_path" '$2 == path {print $1}' "$checksums_path")"
  if [[ ! "$expected" =~ ^[0-9a-f]{64}$ ]]; then
    printf 'ERROR Missing checksum for %s\n' "$published_path" >&2
    exit 2
  fi
  printf '%s  %s\n' "$expected" "$local_path" | sha256sum --check --status
}

verify_download teacher/cloudformation/progress-server.json "$template_path"
verify_download teacher/scripts/jdu-dashboard "$dashboard_path"
printf '%s\n' 'PASS Download checksums match.'

aws sts get-caller-identity --region "$REGION" --output json >/dev/null
aws cloudformation validate-template --region "$REGION" --template-body "file://$template_path" >/dev/null
printf 'Deploying teacher progress stack %s in %s...\n' "$STACK_NAME" "$REGION"
aws cloudformation deploy \
  --region "$REGION" \
  --stack-name "$STACK_NAME" \
  --template-file "$template_path" \
  --parameter-overrides \
    "LambdaExecutionRoleName=$ROLE_NAME" \
    "AdminKeyHash=$admin_hash" \
    "RegistrationKeyHash=$registration_hash" \
  --no-fail-on-empty-changeset

# Commit the new private key only after AWS confirms a successful update.
mv -- "$pending_key_file" "$registration_key_file"
chmod 0600 "$registration_key_file"

endpoint="$(aws cloudformation describe-stacks \
  --region "$REGION" \
  --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?OutputKey=='BaseUrl'].OutputValue | [0]" \
  --output text)"
if [[ ! "$endpoint" =~ ^https://[^[:space:]]+$ ]]; then
  printf '%s\n' 'ERROR CloudFormation did not return the HTTPS endpoint.' >&2
  exit 1
fi

install -d -m 0755 "$HOME/.local/bin"
install -m 0755 "$dashboard_path" "$HOME/.local/bin/jdu-dashboard"
printf 'JDU_PROGRESS_ENDPOINT=%s\nJDU_PROGRESS_REGION=%s\nJDU_PROGRESS_STACK=%s\n' \
  "$endpoint" "$REGION" "$STACK_NAME" > "$config_file"
chmod 0600 "$config_file"

health_ready=false
for attempt in {1..12}; do
  if curl -fsS --max-time 10 "${endpoint%/}/health" >/dev/null; then
    health_ready=true
    break
  fi
  if ((attempt < 12)); then sleep 5; fi
done
if ! $health_ready; then
  printf '%s\n' 'ERROR The stack completed, but the HTTPS health check failed.' >&2
  exit 1
fi

printf '\n%s\n' 'PASS The teacher progress server is ready.'
printf 'HTTPS endpoint: %s\n' "$endpoint"
printf '%s\n' 'Dashboard: jdu-dashboard'
printf '%s\n' 'Keep admin.key private to the teacher. Share the semester setup command only through the enrolled Google Classroom course.'
printf '\n%s\n' 'Private student setup command (do not publish on GitHub):'
student_setup_command="$(printf 'curl -fsSL %q -o /tmp/jdu-install.sh && bash /tmp/jdu-install.sh --region %q --progress-endpoint %q --registration-key %q\n' \
  "$BASE_URL/install.sh" "$REGION" "$endpoint" "$registration_key_value")"
printf '%s\n' "$student_setup_command" > "$state_dir/student-setup-command.txt"
chmod 0600 "$state_dir/student-setup-command.txt"
printf '%s\n' "$student_setup_command"
printf '%s\n' 'Saved privately to ~/.jdu-teacher/student-setup-command.txt. Copy it only into Google Classroom.'
