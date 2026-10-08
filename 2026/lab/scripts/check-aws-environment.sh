#!/usr/bin/env bash
set -u

STACK_NAME="jdu-intro-cybersecurity-2026"
REGION="${AWS_REGION:-${AWS_DEFAULT_REGION:-}}"
WAIT=false
PASS_COUNT=0
FAIL_COUNT=0
ERROR_COUNT=0

usage() {
  printf '%s\n' "Usage: check-aws-environment.sh [--region REGION] [--stack-name NAME] [--wait]"
}

while (($#)); do
  case "$1" in
    --region) REGION="${2:?Missing region}"; shift 2 ;;
    --stack-name) STACK_NAME="${2:?Missing stack name}"; shift 2 ;;
    --wait) WAIT=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'ERROR Unknown option: %s\n' "$1" >&2; exit 2 ;;
  esac
done

pass() { PASS_COUNT=$((PASS_COUNT + 1)); printf 'PASS  %s\n' "$1"; }
fail() { FAIL_COUNT=$((FAIL_COUNT + 1)); printf 'FAIL  %s\n' "$1"; }
error() { ERROR_COUNT=$((ERROR_COUNT + 1)); printf 'ERROR %s\n' "$1"; }
check_equal() {
  local label="$1" actual="$2" expected="$3"
  if [[ "$actual" == "$expected" ]]; then pass "$label"; else fail "$label (expected $expected; observed ${actual:-empty})"; fi
}
stack_output() {
  local key="$1"
  aws cloudformation describe-stacks --region "$REGION" --stack-name "$STACK_NAME" \
    --query "Stacks[0].Outputs[?OutputKey=='${key}'].OutputValue | [0]" --output text 2>/dev/null
}

export AWS_PAGER=""
if ! command -v aws >/dev/null 2>&1; then
  error 'AWS CLI is not available'
  exit 2
fi
if [[ -z "$REGION" ]]; then
  REGION="$(aws configure get region 2>/dev/null || true)"
fi
if [[ -z "$REGION" ]]; then
  error 'AWS region is not configured'
  exit 2
fi
if ! aws sts get-caller-identity --region "$REGION" --output json >/dev/null 2>&1; then
  error 'AWS credentials are not active'
  exit 2
fi

stack_status="$(aws cloudformation describe-stacks --region "$REGION" --stack-name "$STACK_NAME" --query 'Stacks[0].StackStatus' --output text 2>/dev/null || true)"
case "$stack_status" in
  CREATE_COMPLETE|UPDATE_COMPLETE) pass "CloudFormation stack is complete ($stack_status)" ;;
  '') error "CloudFormation stack cannot be read: $STACK_NAME" ;;
  *) fail "CloudFormation stack is not complete ($stack_status)" ;;
esac

instance_id="$(stack_output InstanceId || true)"
vpc_id="$(stack_output VpcId || true)"
subnet_id="$(stack_output PublicSubnetId || true)"
route_table_id="$(stack_output RouteTableId || true)"
security_group_id="$(stack_output SecurityGroupId || true)"
profile_name="$(stack_output InstanceProfileName || true)"
connection_method="$(stack_output ConnectionMethod || true)"
student_ssh_user="$(stack_output StudentSshUser || true)"

for pair in "InstanceId:$instance_id" "VpcId:$vpc_id" "PublicSubnetId:$subnet_id" "RouteTableId:$route_table_id" "SecurityGroupId:$security_group_id" "InstanceProfileName:$profile_name" "ConnectionMethod:$connection_method" "StudentSshUser:$student_ssh_user"; do
  label="${pair%%:*}"; value="${pair#*:}"
  if [[ -n "$value" && "$value" != "None" ]]; then pass "Stack output exists: $label"; else error "Stack output is missing: $label"; fi
done

if ((ERROR_COUNT == 0)); then
  vpc_cidr="$(aws ec2 describe-vpcs --region "$REGION" --vpc-ids "$vpc_id" --query 'Vpcs[0].CidrBlock' --output text 2>/dev/null || true)"
  subnet_cidr="$(aws ec2 describe-subnets --region "$REGION" --subnet-ids "$subnet_id" --query 'Subnets[0].CidrBlock' --output text 2>/dev/null || true)"
  map_public="$(aws ec2 describe-subnets --region "$REGION" --subnet-ids "$subnet_id" --query 'Subnets[0].MapPublicIpOnLaunch' --output text 2>/dev/null || true)"
  default_gateway="$(aws ec2 describe-route-tables --region "$REGION" --route-table-ids "$route_table_id" --query "RouteTables[0].Routes[?DestinationCidrBlock=='0.0.0.0/0' && State=='active'].GatewayId | [0]" --output text 2>/dev/null || true)"
  ingress_count="$(aws ec2 describe-security-groups --region "$REGION" --group-ids "$security_group_id" --query 'length(SecurityGroups[0].IpPermissions)' --output text 2>/dev/null || true)"
  instance_state="$(aws ec2 describe-instances --region "$REGION" --instance-ids "$instance_id" --query 'Reservations[0].Instances[0].State.Name' --output text 2>/dev/null || true)"
  public_ip="$(aws ec2 describe-instances --region "$REGION" --instance-ids "$instance_id" --query 'Reservations[0].Instances[0].PublicIpAddress' --output text 2>/dev/null || true)"
  http_tokens="$(aws ec2 describe-instances --region "$REGION" --instance-ids "$instance_id" --query 'Reservations[0].Instances[0].MetadataOptions.HttpTokens' --output text 2>/dev/null || true)"
  profile_arn="$(aws ec2 describe-instances --region "$REGION" --instance-ids "$instance_id" --query 'Reservations[0].Instances[0].IamInstanceProfile.Arn' --output text 2>/dev/null || true)"
  course_tag="$(aws ec2 describe-instances --region "$REGION" --instance-ids "$instance_id" --query "Reservations[0].Instances[0].Tags[?Key=='JDUCourse'].Value | [0]" --output text 2>/dev/null || true)"

  check_equal 'VPC CIDR is isolated for the course' "$vpc_cidr" '10.20.0.0/16'
  check_equal 'Public subnet CIDR is correct' "$subnet_cidr" '10.20.10.0/24'
  check_equal 'Public subnet assigns a public IPv4 address' "${map_public,,}" 'true'
  if [[ "$default_gateway" == igw-* ]]; then pass 'Default route uses an Internet Gateway'; else fail "Default route does not use an Internet Gateway (observed ${default_gateway:-empty})"; fi
  check_equal 'Security group has no inbound rules' "$ingress_count" '0'
  check_equal 'Ubuntu instance is running' "$instance_state" 'running'
  if [[ -n "$public_ip" && "$public_ip" != "None" ]]; then pass 'Instance has outbound Internet connectivity through a public IPv4 address'; else fail 'Instance has no public IPv4 address'; fi
  check_equal 'IMDSv2 tokens are required' "$http_tokens" 'required'
  if [[ "$profile_arn" == */"$profile_name" ]]; then pass 'Expected instance profile is attached'; else fail "Expected instance profile is not attached (observed ${profile_arn:-empty})"; fi
  check_equal 'Course ownership tag is present' "$course_tag" 'Introduction_CyberSecurity'
  check_equal 'Connection method is SSH over Session Manager' "$connection_method" 'SSH over AWS Systems Manager Session Manager'
  check_equal 'SSH user is ssm-user' "$student_ssh_user" 'ssm-user'

  attempts=1
  if $WAIT; then attempts=40; fi
  ssm_status=""
  for ((attempt=1; attempt<=attempts; attempt++)); do
    ssm_status="$(aws ssm describe-instance-information --region "$REGION" --filters "Key=InstanceIds,Values=$instance_id" --query 'InstanceInformationList[0].PingStatus' --output text 2>/dev/null || true)"
    [[ "$ssm_status" == "Online" ]] && break
    if ((attempt < attempts)); then sleep 15; fi
  done
  check_equal 'Instance is online in Systems Manager' "$ssm_status" 'Online'
fi

printf 'Required checks: %d PASS, %d FAIL, %d ERROR\n' "$PASS_COUNT" "$FAIL_COUNT" "$ERROR_COUNT"
if ((ERROR_COUNT > 0)); then exit 2; fi
if ((FAIL_COUNT > 0)); then exit 1; fi
exit 0
