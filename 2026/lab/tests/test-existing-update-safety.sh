#!/usr/bin/env bash
set -Eeuo pipefail

root_dir="${1:?Lab root is required}"
scratch="$(mktemp -d)"
trap 'rm -rf -- "$scratch"' EXIT

set +e
teacher_output="$(HOME="$scratch" bash "$root_dir/teacher/update-existing-teacher.sh" --region us-east-1 2>&1)"
teacher_status=$?
student_output="$(HOME="$scratch" bash "$root_dir/scripts/update-existing-cloudshell.sh" --region us-east-1 2>&1)"
student_status=$?
set -e
[[ "$teacher_status" -eq 2 && "$teacher_output" == *'Original teacher configuration and both keys are required'* ]]
[[ "$student_status" -eq 2 && "$student_output" == *'Existing student registration is missing'* ]]

! grep -Eq '^[[:space:]]*aws[[:space:]]+cloudformation[[:space:]]+(deploy|delete-stack)' "$root_dir/scripts/update-existing-cloudshell.sh"
! grep -Eq '^[[:space:]]*aws[[:space:]]+cloudformation[[:space:]]+delete-stack' "$root_dir/teacher/update-existing-teacher.sh"
! grep -Eq '^[[:space:]]*.*(jdu-reset|--rotate-registration-key)' "$root_dir/scripts/update-existing-cloudshell.sh" "$root_dir/teacher/update-existing-teacher.sh"
grep -Fq 'sha256sum --check --status' "$root_dir/scripts/update-existing-cloudshell.sh"
grep -Fq 'sha256sum --check --status' "$root_dir/teacher/update-existing-teacher.sh"
printf '%s\n' 'PASS existing-environment updater refuses missing state and has no create/delete/reset/rotation path'
