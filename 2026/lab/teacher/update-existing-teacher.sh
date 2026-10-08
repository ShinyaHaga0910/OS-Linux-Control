#!/usr/bin/env bash
set -Eeuo pipefail

# Update only an existing teacher stack. Never create a stack or rotate keys here.
region=''
state_dir="${JDU_TEACHER_STATE_DIR:-$HOME/.jdu-teacher}"
base_url="${JDU_UPDATE_BASE_URL:-https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab}"

usage() {
  printf '%s\n' 'Usage: bash update-existing-teacher.sh --region REGION'
}

while (($#)); do
  case "$1" in
    --region) region="${2:?Missing region}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
done
if [[ ! "$region" =~ ^[a-z]{2}(-gov)?-[a-z]+-[0-9]+$ ]]; then
  printf '%s\n' 'ERROR Specify the existing stack region with --region.' >&2
  exit 2
fi
config="$state_dir/progress.env"
if [[ ! -s "$config" || ! -s "$state_dir/admin.key" || ! -s "$state_dir/registration.key" ]]; then
  printf '%s\n' 'ERROR Original teacher configuration and both keys are required. Nothing was changed.' >&2
  exit 2
fi
stack_name="$(sed -n 's/^JDU_PROGRESS_STACK=//p' "$config" | tail -n 1)"
if [[ ! "$stack_name" =~ ^[A-Za-z][A-Za-z0-9-]{0,127}$ ]]; then
  printf '%s\n' 'ERROR The saved teacher stack name is invalid. Nothing was changed.' >&2
  exit 2
fi
for tool in aws curl sha256sum awk mktemp; do
  command -v "$tool" >/dev/null 2>&1 || { printf 'ERROR Missing command: %s\n' "$tool" >&2; exit 2; }
done
stack_status="$(aws cloudformation describe-stacks --region "$region" --stack-name "$stack_name" --query 'Stacks[0].StackStatus' --output text 2>/dev/null)" || {
  printf '%s\n' 'ERROR The saved teacher stack was not found. No new stack was created.' >&2
  exit 2
}
if [[ "$stack_status" != CREATE_COMPLETE && "$stack_status" != UPDATE_COMPLETE ]]; then
  printf 'ERROR Teacher stack is %s, not ready for an ordinary update.\n' "$stack_status" >&2
  exit 2
fi

work_dir="$(mktemp -d)"
trap 'rm -rf -- "$work_dir"' EXIT
curl -fsSL --retry 3 --connect-timeout 10 "$base_url/SHA256SUMS" -o "$work_dir/SHA256SUMS"
curl -fsSL --retry 3 --connect-timeout 10 "$base_url/teacher/install-teacher.sh" -o "$work_dir/install-teacher.sh"
expected="$(awk '$2 == "teacher/install-teacher.sh" {print $1}' "$work_dir/SHA256SUMS")"
if [[ ! "$expected" =~ ^[0-9a-f]{64}$ ]] || ! printf '%s  %s\n' "$expected" "$work_dir/install-teacher.sh" | sha256sum --check --status; then
  printf '%s\n' 'ERROR Teacher installer checksum verification failed. Nothing was changed.' >&2
  exit 1
fi

printf 'Updating existing teacher stack %s in %s without rotating keys...\n' "$stack_name" "$region"
JDU_TEACHER_STATE_DIR="$state_dir" bash "$work_dir/install-teacher.sh" --region "$region" --stack-name "$stack_name"
final_status="$(aws cloudformation describe-stacks --region "$region" --stack-name "$stack_name" --query 'Stacks[0].StackStatus' --output text)"
if [[ "$final_status" != CREATE_COMPLETE && "$final_status" != UPDATE_COMPLETE ]]; then
  printf 'ERROR Teacher stack ended in %s.\n' "$final_status" >&2
  exit 1
fi
printf '%s\n' 'PASS Existing teacher stack updated; saved keys were reused.'
