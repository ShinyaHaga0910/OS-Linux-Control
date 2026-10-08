#!/usr/bin/env bash
set -Eeuo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
checker="$root_dir/scripts/check-aws-environment.sh"
mock_bin="$root_dir/tests/mock-bin"
export JDU_STUDENT_USER="$(id -un)"

for script in \
  "$root_dir/install.sh" \
  "$root_dir/scripts/check-aws-environment.sh" \
  "$root_dir/scripts/setup-instance.sh" \
  "$root_dir/scripts/jdu-fixture" \
  "$root_dir/scripts/jdu-labcheck" \
  "$root_dir/scripts/jdu-prepare-student-home" \
  "$root_dir/scripts/jdu-cloudcheck" \
  "$root_dir/scripts/jdu-cloud-reset" \
  "$root_dir/scripts/jdu-progress" \
  "$root_dir/scripts/jdu-process-state" \
  "$root_dir/scripts/update-existing-ubuntu.sh" \
  "$root_dir/scripts/install-my-progress-ubuntu.sh" \
  "$root_dir/tests/test-package-ownership.sh" \
  "$root_dir/tests/test-process-persistence.sh" \
  "$root_dir/teacher/install-teacher.sh" \
  "$root_dir/teacher/scripts/jdu-dashboard" \
  "$root_dir/tests/mock-bin/aws" \
  "$root_dir/tests/mock-bin/systemctl" \
  "$root_dir/tests/mock-bin/dpkg-query" \
  "$root_dir/tests/mock-m6/ssh" \
  "$root_dir/tests/mock-progress/curl" \
  "$root_dir/tests/mock-progress/jdu-progress"; do
  bash -n "$script"
done
python3 - "$root_dir/scripts/jdu-worker" "$root_dir/scripts/jdu-http-service" "$root_dir/teacher/lambda/progress_app.py" "$root_dir/teacher/tools/build-template.py" <<'PY'
import ast
import sys
for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as source:
        ast.parse(source.read(), filename=path)
PY
printf '%s\n' 'PASS shell and Python syntax'
python3 "$root_dir/tests/test-availability-zone.py"

(
  cd "$root_dir"
  sha256sum --check SHA256SUMS >/dev/null
)
printf '%s\n' 'PASS published checksums'

list_output="$(bash "$root_dir/scripts/jdu-labcheck" list)"
[[ "$(grep -c '^M[1-7] ' <<<"$list_output")" -eq 7 ]]
[[ "$(grep -c '^P[0-6] ' <<<"$list_output")" -eq 7 ]]
grep -Fq 'jdu-check' "$root_dir/scripts/jdu-labcheck"
grep -Fq '/usr/local/bin/jdu-check' "$root_dir/scripts/setup-instance.sh"
grep -Fq '/usr/local/bin/jdu-reset' "$root_dir/scripts/setup-instance.sh"
printf '%s\n' 'PASS short student command interface'
python3 "$root_dir/tests/test-p0.py" "$root_dir/scripts/jdu-labcheck"


set +e
wrong_user_output="$(JDU_STUDENT_USER=definitely-not-current bash "$root_dir/scripts/jdu-labcheck" M1 2>&1)"
wrong_user_status=$?
set -e
[[ "$wrong_user_status" -eq 2 ]]
grep -Fq 'jdu-check must be run as definitely-not-current' <<<"$wrong_user_output"
grep -Fq 'Run exit until id -un prints definitely-not-current' <<<"$wrong_user_output"
printf '%s\n' 'PASS wrong-user execution stops with a clear recovery message'

grep -Fq -- '--rotate-registration-key' "$root_dir/teacher/install-teacher.sh"
grep -Fq -- '--progress-endpoint %q --registration-key %q' "$root_dir/teacher/install-teacher.sh"
printf '%s\n' 'PASS teacher command includes the deployed progress configuration'

declare -A expected_counts=(
  [P0]=6 [P1]=6 [P2]=6 [P3]=2 [P4]=2 [P5]=4 [P6]=2
  [M1]=5 [M2]=6 [M3]=2 [M4]=2 [M5]=4 [M6]=2 [M7]=6
)

for mission in P0 P1 P2 P4 P5 P6 M1 M2 M4 M5 M6 M7; do
  test_home="$(mktemp -d)"
  set +e
  output="$(HOME="$test_home" bash "$root_dir/scripts/jdu-labcheck" "$mission" 2>&1)"
  status=$?
  set -e
  [[ "$status" -eq 1 ]]
  grep -Fxq "RESULT    0 / ${expected_counts[$mission]} checks cleared" <<<"$output"
  grep -Fxq 'PASS      0' <<<"$output"
  grep -Fxq "FAIL      ${expected_counts[$mission]}" <<<"$output"
  ! grep -Eq '^PASS[[:space:]]+[PM][1-7]-' <<<"$output"
  rm -rf -- "$test_home"
done
printf '%s\n' 'PASS guided P1-P2/P4-P6 and challenge M1-M2/M4-M7 have zero initial PASS items'

python3 "$root_dir/tests/test-service-two-checks.py" "$root_dir/scripts/jdu-labcheck"

p1_fixture_home="$(mktemp -d)"
mkdir -p "$p1_fixture_home/jdu-lab/p1/practice01/staging"
printf '%s\n' 'temporary guided file' > "$p1_fixture_home/jdu-lab/p1/practice01/staging/training.conf.tmp"
set +e
p1_fixture_initial="$(HOME="$p1_fixture_home" bash "$root_dir/scripts/jdu-labcheck" P1 --no-submit 2>&1)"
p1_fixture_status=$?
set -e
[[ "$p1_fixture_status" -eq 1 ]]
grep -Fxq 'RESULT    0 / 6 checks cleared' <<<"$p1_fixture_initial"
grep -Eq '^FAIL[[:space:]]+P1-FS-04[[:space:]]+' <<<"$p1_fixture_initial"
rm -rf -- "$p1_fixture_home"
printf '%s\n' 'PASS P1 fixture-like initial tree does not pass the ownership check before student work'

m3_test_home="$(mktemp -d)"
mkdir -p "$m3_test_home/jdu-lab/m3"
chmod 0755 "$root_dir/tests/mock-bin/systemctl" "$root_dir/tests/mock-bin/dpkg-query"
set +e
m3_initial="$(PATH="$root_dir/tests/mock-bin:$PATH" HOME="$m3_test_home" bash "$root_dir/scripts/jdu-labcheck" M3 2>&1)"
m3_stopped="$(MOCK_PROCESS2_STOPPED=1 PATH="$root_dir/tests/mock-bin:$PATH" HOME="$m3_test_home" bash "$root_dir/scripts/jdu-labcheck" M3 2>&1)"
m3_wrong="$(MOCK_PROCESS1_STOPPED=1 PATH="$root_dir/tests/mock-bin:$PATH" HOME="$m3_test_home" bash "$root_dir/scripts/jdu-labcheck" M3 2>&1)"
set -e
grep -Fxq 'RESULT    0 / 2 checks cleared' <<<"$m3_initial"
grep -Eq '^PASS[[:space:]]+M3-PROC-01[[:space:]]+Only process2 is stopped$' <<<"$m3_stopped"
grep -Fxq 'RESULT    1 / 2 checks cleared' <<<"$m3_stopped"
grep -Fxq 'RESULT    0 / 2 checks cleared' <<<"$m3_wrong"
rm -rf -- "$m3_test_home"
printf '%s\n' 'PASS M3 starts at zero and requires the exact process outcome'

p3_test_home="$(mktemp -d)"
mkdir -p "$p3_test_home/jdu-lab/p3"
set +e
p3_initial="$(PATH="$root_dir/tests/mock-bin:$PATH" HOME="$p3_test_home" bash "$root_dir/scripts/jdu-labcheck" P3 2>&1)"
p3_stopped="$(MOCK_P3_PROCESS2_STOPPED=1 PATH="$root_dir/tests/mock-bin:$PATH" HOME="$p3_test_home" bash "$root_dir/scripts/jdu-labcheck" P3 2>&1)"
p3_wrong="$(MOCK_P3_PROCESS1_STOPPED=1 PATH="$root_dir/tests/mock-bin:$PATH" HOME="$p3_test_home" bash "$root_dir/scripts/jdu-labcheck" P3 2>&1)"
set -e
grep -Fxq 'RESULT    0 / 2 checks cleared' <<<"$p3_initial"
grep -Eq '^PASS[[:space:]]+P3-PROC-01[[:space:]]+Only guided process2 is stopped$' <<<"$p3_stopped"
grep -Fxq 'RESULT    1 / 2 checks cleared' <<<"$p3_stopped"
grep -Fxq 'RESULT    0 / 2 checks cleared' <<<"$p3_wrong"
rm -rf -- "$p3_test_home"
printf '%s\n' 'PASS P3 starts at zero and requires the exact guided process outcome'

bash "$root_dir/tests/test-package-ownership.sh" "$root_dir/scripts/jdu-labcheck"
bash "$root_dir/tests/test-process-persistence.sh" "$root_dir/scripts/jdu-process-state" "$root_dir/scripts/jdu-fixture" "$root_dir/scripts/setup-instance.sh"

m6_cloud_home="$(mktemp -d)"
m6_cloud_workspace="$m6_cloud_home/jdu-lab/m6"
m6_remote_directory="$m6_cloud_home/remote-m6"
mkdir -p "$m6_cloud_workspace" "$m6_remote_directory"
chmod 0755 "$root_dir/tests/mock-m6/ssh" "$root_dir/tests/mock-progress/curl"
set +e
m6_initial="$(M6_REMOTE_DIR="$m6_remote_directory" JDU_M6_WORKSPACE="$m6_cloud_workspace" PATH="$root_dir/tests/mock-m6:$PATH" HOME="$m6_cloud_home" bash "$root_dir/scripts/jdu-cloudcheck" M6 2>&1)"
set -e
grep -Fxq 'RESULT    0 / 4 checks cleared' <<<"$m6_initial"
printf '%s\n' 'JDU SSH transfer test' > "$m6_cloud_workspace/local-source.txt"
cp "$m6_cloud_workspace/local-source.txt" "$m6_remote_directory/upload.txt"
printf '%s\n' 'REMOTE_USER=ssm-user' 'REMOTE_HOST=mock-host' 'REMOTE_PATH=/home/ssm-user' > "$m6_remote_directory/remote-result.txt"
cp "$m6_remote_directory/remote-result.txt" "$m6_cloud_workspace/downloaded-result.txt"
m6_complete="$(M6_REMOTE_DIR="$m6_remote_directory" JDU_M6_WORKSPACE="$m6_cloud_workspace" PATH="$root_dir/tests/mock-m6:$PATH" HOME="$m6_cloud_home" bash "$root_dir/scripts/jdu-cloudcheck" M6)"
grep -Fxq 'RESULT    4 / 4 checks cleared' <<<"$m6_complete"
grep -Fxq 'PASS      4' <<<"$m6_complete"
printf '%s\n' \
  'JDU_PROGRESS_ENDPOINT=https://example.execute-api.us-east-1.amazonaws.com' \
  'JDU_PROGRESS_SERVER_ID=srv-0123456789abcdef' \
  'JDU_PROGRESS_SERVER_TOKEN=tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt' \
  > "$m6_cloud_home/progress.env"
m6_report_log="$m6_cloud_home/report.log"
m6_reported="$(M6_REMOTE_DIR="$m6_remote_directory" JDU_M6_WORKSPACE="$m6_cloud_workspace" JDU_CLOUD_PROGRESS_CONFIG="$m6_cloud_home/progress.env" MOCK_CURL_LOG="$m6_report_log" PATH="$root_dir/tests/mock-progress:$root_dir/tests/mock-m6:$PATH" HOME="$m6_cloud_home" bash "$root_dir/scripts/jdu-cloudcheck" M6)"
grep -Fq 'REPORT    PASS (server srv-0123456789abcdef, M6-CloudShell)' <<<"$m6_reported"
grep -Fq 'URL=https://example.execute-api.us-east-1.amazonaws.com/submit' "$m6_report_log"
grep -Fq 'Authorization: Bearer tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt' "$m6_report_log"
grep -Fq '"mission":"M6C","passed":4,"total":4' "$m6_report_log"
HOME="$m6_cloud_home" bash "$root_dir/scripts/jdu-cloud-reset" M6 >/dev/null
[[ ! -e "$m6_cloud_workspace/local-source.txt" && ! -e "$m6_cloud_workspace/downloaded-result.txt" ]]
rm -rf -- "$m6_cloud_home"
printf '%s\n' 'PASS M6 CloudShell tasks start at zero, complete, and reset safely'

p6_cloud_home="$(mktemp -d)"
p6_cloud_workspace="$p6_cloud_home/jdu-lab/p6"
p6_remote_directory="$p6_cloud_home/remote-p6"
mkdir -p "$p6_cloud_workspace" "$p6_remote_directory"
set +e
p6_initial="$(P6_REMOTE_DIR="$p6_remote_directory" JDU_P6_WORKSPACE="$p6_cloud_workspace" PATH="$root_dir/tests/mock-m6:$PATH" HOME="$p6_cloud_home" bash "$root_dir/scripts/jdu-cloudcheck" P6 2>&1)"
set -e
grep -Fxq 'RESULT    0 / 4 checks cleared' <<<"$p6_initial"
printf '%s\n' 'JDU SSH guided transfer' > "$p6_cloud_workspace/practice-source.txt"
cp "$p6_cloud_workspace/practice-source.txt" "$p6_remote_directory/practice-upload.txt"
printf '%s\n' 'REMOTE_USER=ssm-user' 'REMOTE_HOST=mock-host' 'REMOTE_PATH=/home/ssm-user' > "$p6_remote_directory/practice-remote-result.txt"
cp "$p6_remote_directory/practice-remote-result.txt" "$p6_cloud_workspace/practice-downloaded-result.txt"
printf '%s\n' \
  'JDU_PROGRESS_ENDPOINT=https://example.execute-api.us-east-1.amazonaws.com' \
  'JDU_PROGRESS_SERVER_ID=srv-0123456789abcdef' \
  'JDU_PROGRESS_SERVER_TOKEN=tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt' \
  > "$p6_cloud_home/progress.env"
p6_report_log="$p6_cloud_home/report.log"
p6_complete="$(P6_REMOTE_DIR="$p6_remote_directory" JDU_P6_WORKSPACE="$p6_cloud_workspace" JDU_CLOUD_PROGRESS_CONFIG="$p6_cloud_home/progress.env" MOCK_CURL_LOG="$p6_report_log" PATH="$root_dir/tests/mock-progress:$root_dir/tests/mock-m6:$PATH" HOME="$p6_cloud_home" bash "$root_dir/scripts/jdu-cloudcheck" P6)"
grep -Fxq 'RESULT    4 / 4 checks cleared' <<<"$p6_complete"
grep -Fq 'REPORT    PASS (server srv-0123456789abcdef, P6-CloudShell)' <<<"$p6_complete"
grep -Fq '"mission":"P6C","passed":4,"total":4' "$p6_report_log"
HOME="$p6_cloud_home" bash "$root_dir/scripts/jdu-cloud-reset" P6 >/dev/null
[[ ! -e "$p6_cloud_workspace/practice-source.txt" && ! -e "$p6_cloud_workspace/practice-downloaded-result.txt" ]]
rm -rf -- "$p6_cloud_home"
printf '%s\n' 'PASS P6 CloudShell guided tasks start at zero, complete, report, and reset safely'

runtime_directory="$(mktemp -d)"
worker_pid=''
http_pid=''
cleanup_runtime_test() {
  [[ -z "$worker_pid" ]] || kill -TERM "$worker_pid" >/dev/null 2>&1 || true
  [[ -z "$http_pid" ]] || kill -TERM "$http_pid" >/dev/null 2>&1 || true
  rm -rf -- "$runtime_directory"
}
trap cleanup_runtime_test EXIT

python3 "$root_dir/scripts/jdu-worker" test-token >"$runtime_directory/worker.log" 2>&1 &
worker_pid=$!
sleep 1
ps -p "$worker_pid" -o args= | grep -Fq 'jdu-worker test-token'
kill -TERM "$worker_pid"
wait "$worker_pid"
worker_pid=''
grep -Fq 'worker stopped: test-token' "$runtime_directory/worker.log"

printf '%s\n' 'JDU-HTTP-FUNCTIONAL' > "$runtime_directory/content.txt"
python3 "$root_dir/scripts/jdu-http-service" --address 127.0.0.1 --port 18081 --content "$runtime_directory/content.txt" >"$runtime_directory/http.log" 2>&1 &
http_pid=$!
for _attempt in {1..20}; do
  if curl -fsS --max-time 1 http://127.0.0.1:18081/ > "$runtime_directory/response.txt" 2>/dev/null; then break; fi
  sleep 0.2
done
grep -Fxq 'JDU-HTTP-FUNCTIONAL' "$runtime_directory/response.txt"
curl -fsS --max-time 1 http://127.0.0.1:18081/m5-check >/dev/null
grep -Fq 'REQUEST path=/m5-check' "$runtime_directory/http.log"
kill -TERM "$http_pid"
wait "$http_pid" 2>/dev/null || true
http_pid=''
printf '%s\n' 'PASS process worker and HTTP service functional tests'

python3 - "$root_dir/cloudformation/lab-environment.json" "$root_dir/scripts/setup-instance.sh" <<'PY'
import hashlib
import json
import sys
with open(sys.argv[1], encoding="utf-8") as source:
    template = json.load(source)
resources = template["Resources"]
required = {
    "LabVpc", "InternetGateway", "GatewayAttachment", "PublicSubnet",
    "PublicRouteTable", "DefaultRoute", "PublicSubnetRouteTableAssociation",
    "LabSecurityGroup", "UbuntuLabInstance",
}
assert required <= resources.keys()
sg = resources["LabSecurityGroup"]["Properties"]
assert sg["SecurityGroupIngress"] == []
instance = resources["UbuntuLabInstance"]["Properties"]
assert "KeyName" not in instance
assert instance["MetadataOptions"]["HttpTokens"] == "required"
assert instance["IamInstanceProfile"] == {"Ref": "InstanceProfileName"}
parameters = template["Parameters"]
assert parameters["LabVersion"]["AllowedValues"] == ["v1.0.0"]
assert parameters["ProgressRegistrationKeyBase64"]["NoEcho"] is True
assert parameters["ProgressServerTokenBase64"]["NoEcho"] is True
user_data = instance["UserData"]["Fn::Base64"]["Fn::Sub"]
with open(sys.argv[2], "rb") as source:
    setup_hash = hashlib.sha256(source.read()).hexdigest()
assert setup_hash in user_data
assert "/2026/lab/scripts/setup-instance.sh" in user_data
assert "/2026/${LabVersion}/" not in user_data
assert template["Outputs"]["ConnectionMethod"]["Value"] == "SSH over AWS Systems Manager Session Manager"
print("PASS CloudFormation structure")
PY

python3 - \
  "$root_dir/install.sh" \
  "$root_dir/scripts/setup-instance.sh" \
  "$root_dir/scripts/jdu-fixture" \
  "$root_dir/scripts/jdu-labcheck" \
  "$root_dir/scripts/jdu-cloudcheck" \
  "$root_dir/MISSION_GUIDE.md" \
  "$root_dir/GUIDED_PRACTICE.md" <<'PY'
import re
import sys
texts = []
for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as source:
        texts.append(source.read())
installer, setup, fixture, checker, cloudchecker, guide, guided = texts
assert 'VERSION="v1.0.0"' in installer
assert '/2026/lab"' in installer
assert '/2026/lab}' in setup
assert 'PROGRESS_ENDPOINT="${JDU_PROGRESS_ENDPOINT:-}"' in installer
assert 'REGISTRATION_KEY="${JDU_PROGRESS_REGISTRATION_KEY:-}"' in installer
assert 'install -m 0755 "$cloudcheck_path" "$HOME/.local/bin/jdu-check"' in installer
assert 'install -m 0755 "$cloudreset_path" "$HOME/.local/bin/jdu-reset"' in installer
assert '"$HOME/.local/bin/jdu-reset" P6' in installer
assert '"$HOME/.local/bin/jdu-reset" M6' in installer
assert '/opt/jdu-lab/bin/jdu-fixture reset all' in setup
assert '/usr/local/bin/jdu-check' in setup
assert '/usr/local/bin/jdu-reset' in setup
assert '/usr/local/bin/jdu-progress' in setup
assert 'verify_download scripts/jdu-my-progress /opt/jdu-lab/bin/jdu-my-progress' in setup
assert 'install -m 0755 /opt/jdu-lab/bin/jdu-my-progress /usr/local/bin/jdu-my-progress' in setup
assert 'jdu-fixture reset all' in setup and 'jdu-progress register' in setup
assert 'required_packages+=(tree)' in setup
assert 'verify_download scripts/jdu-process-state /opt/jdu-lab/bin/jdu-process-state' in setup
assert '/opt/jdu-lab/bin/jdu-process-state install-units' in setup
assert 'jdu-practice-status.service' in setup
assert 'jdu-practice-web.service' in setup
assert 'jdu-practice-final.service' not in setup
assert 'systemd-run' not in fixture
assert 'usermod -aG ops jduviewer' in fixture
assert 'gpasswd -d jduops ops' in fixture
assert 'systemctl is-active --quiet "$unit"' in fixture
for mission in range(1, 8):
    assert f"reset_m{mission}()" in fixture
    assert f"check_m{mission}()" in checker
    assert f"## M{mission} " in guide
for practice in range(0, 7):
    assert f"reset_p{practice}()" in fixture
    assert f"check_p{practice}()" in checker
    assert f"## P{practice} " in guided
assert guided.count("### 課題\n") == 7
assert guided.count("### 解答例（操作手順）\n") == 7
for practice in range(0, 7):
    section = guided.split(f"## P{practice} ", 1)[1].split("\n## ", 1)[0]
    assert section.index("### 課題\n") < section.index("### 解答例（操作手順）\n") < section.index("#### 手順1:")
assert "reset_p7()" not in fixture and "check_p7()" not in checker and "## P7 " not in guided
expected_ids = {
    "P0": {f"P0-OBS-{n:02d}" for n in range(1, 7)},
    "P1": {"P1-FS-01", "P1-FS-02", "P1-FS-03", "P1-FS-04", "P1-TXT-01", "P1-TXT-02"},
    "P2": {"P2-ID-01", "P2-PERM-01", "P2-PERM-02", "P2-PERM-03", "P2-PERM-04", "P2-PERM-05"},
    "P3": {"P3-PROC-01", "P3-APT-01"},
    "P4": {"P4-SVC-01", "P4-SVC-02"},
    "P5": {"P5-SOCK-01", "P5-HTTP-01", "P5-LOG-01", "P5-NEG-01"},
    "P6": {"P6-XFER-01", "P6-REMOTE-01"},
    "M1": {"M1-FS-01", "M1-FS-02", "M1-FS-03", "M1-TXT-01", "M1-TXT-02"},
    "M2": {"M2-ID-01", "M2-PERM-01", "M2-PERM-02", "M2-PERM-03", "M2-PERM-04", "M2-PERM-05"},
    "M3": {"M3-PROC-01", "M3-APT-01"},
    "M4": {"M4-SVC-01", "M4-SVC-02"},
    "M5": {"M5-SOCK-01", "M5-HTTP-01", "M5-LOG-01", "M5-NEG-01"},
    "M6": {"M6-XFER-01", "M6-REMOTE-01"},
    "M7": {"M7-FILE-01", "M7-PERM-01", "M7-SVC-01", "M7-SOCK-01", "M7-HTTP-01", "M7-LOG-01"},
}
for mission, ids in expected_ids.items():
    found = set(re.findall(rf"{mission}-[A-Z]+-[0-9]+", checker))
    assert found == ids, (mission, found, ids)
for suffix in ["-LOCAL-01", "-XFER-01", "-REMOTE-01", "-XFER-02"]:
    assert f'${{check_prefix}}{suffix}' in cloudchecker
assert 'check_prefix=P6' in cloudchecker and 'check_prefix=M6' in cloudchecker and 'report_mission="${mission}C"' in cloudchecker
assert "jdu-web.service" in checker and "jdu-web.service" in fixture and "jdu-web.service" in setup
assert "jdu-status.service" not in checker[checker.index("check_m5()") : checker.index("check_m6()")]
assert "chmod 777" not in fixture
assert "初回構築時に、すべてのMissionは自動で未完成の状態になる" in guide
assert "jdu-checkとjdu-resetは、必ずssm-userで実行する" in guide.replace("`", "")
assert "M6 Ubuntu" in guide and "M6 CloudShell" in guide and "合計`6/6`" in guide
assert "P1 → M1" in guided
for required_command in ["cd ~", "cd /srv", "jdu-check P1", "jdu-check P6", "sudo ss -lntp", "ssh jdu-ubuntu", "scp "]:
    assert required_command in guided
assert "jdu-check M1 --no-submit" in guide
assert 'SUBMIT_PROGRESS=true' in checker
assert '[[ "$mission" == M6 ]] && report_mission=M6U' in checker
assert '[[ "$mission" == P6 ]] && report_mission=P6U' in checker
assert '"$progress_command" submit "$report_mission" "$PASS_COUNT" "$total"' in checker
print("PASS Mission task-to-check and automatic-reset contracts")
PY

python3 - "$root_dir/teacher/cloudformation/progress-server.json" "$root_dir/teacher/lambda/progress_app.py" <<'PY'
import json
import sys
with open(sys.argv[1], encoding="utf-8") as source:
    template = json.load(source)
with open(sys.argv[2], encoding="utf-8") as source:
    lambda_source = source.read()
resources = template["Resources"]
assert not any(value["Type"].startswith("AWS::EC2::") for value in resources.values())
assert resources["ProgressTable"]["Type"] == "AWS::DynamoDB::Table"
assert resources["ProgressTable"]["Properties"]["BillingMode"] == "PAY_PER_REQUEST"
assert resources["ProgressTable"]["Properties"]["TimeToLiveSpecification"]["Enabled"] is True
assert resources["ProgressFunction"]["Properties"]["Code"]["ZipFile"] == lambda_source
assert template["Parameters"]["AdminKeyHash"]["NoEcho"] is True
assert template["Parameters"]["RegistrationKeyHash"]["NoEcho"] is True
route_keys = {value["Properties"]["RouteKey"] for value in resources.values() if value["Type"] == "AWS::ApiGatewayV2::Route"}
assert route_keys == {"POST /register", "POST /status", "POST /link-email", "POST /submit", "POST /admin/session", "GET /dashboard", "GET /health", "POST /student/session", "GET /student/progress"}
assert template["Outputs"]["BaseUrl"]["Value"]["Fn::Sub"].startswith("https://")
assert 'M6U|M6C' in lambda_source
assert 'P[0-6]|P6U|P6C' in lambda_source
assert 'Ubuntu {ubuntu_text}' in lambda_source
assert 'CloudShell {cloud_text}' in lambda_source
assert 'DISPLAY_MISSIONS' in lambda_source
print("PASS teacher CloudFormation uses managed HTTPS without a public EC2 server")
PY

python3 "$root_dir/tests/test-progress-backend.py" "$root_dir/teacher/lambda/progress_app.py"
python3 "$root_dir/tests/test-personal-progress-command.py" "$root_dir/scripts/jdu-my-progress"
bash "$root_dir/tests/test-ubuntu-progress-installer.sh" "$root_dir"
python3 "$root_dir/tests/test-student-registration.py" "$root_dir/scripts/register-student.py"
bash "$root_dir/tests/test-email-upgrade.sh" "$root_dir"
python3 "$root_dir/tests/test-install-registration.py" "$root_dir"
python3 "$root_dir/tests/test-semester-registration-key.py" "$root_dir"

progress_test_dir="$(mktemp -d)"
progress_endpoint='https://example.execute-api.us-east-1.amazonaws.com'
progress_token='tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt'
printf 'JDU_PROGRESS_ENDPOINT_B64=%s\nJDU_PROGRESS_SERVER_ID=%s\nJDU_PROGRESS_SERVER_TOKEN_B64=%s\n' \
  "$(printf '%s' "$progress_endpoint" | base64 | tr -d '\n')" \
  'srv-0123456789abcdef' \
  "$(printf '%s' "$progress_token" | base64 | tr -d '\n')" > "$progress_test_dir/progress.env"
printf '%s' 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr' | base64 | tr -d '\n' > "$progress_test_dir/registration.key.b64"
chmod 0755 "$root_dir/tests/mock-progress/curl"
progress_id="$(JDU_PROGRESS_CONFIG="$progress_test_dir/progress.env" bash "$root_dir/scripts/jdu-progress" id)"
[[ "$progress_id" == 'srv-0123456789abcdef' ]]
MOCK_CURL_LOG="$progress_test_dir/curl.log" \
JDU_PROGRESS_CONFIG="$progress_test_dir/progress.env" \
JDU_PROGRESS_ACCOUNT_ID=123456789012 \
JDU_PROGRESS_INSTANCE_ID=i-0123456789abcdef0 \
JDU_PROGRESS_HOSTNAME=mock-host \
PATH="$root_dir/tests/mock-progress:$PATH" \
bash "$root_dir/scripts/jdu-progress" register "$progress_test_dir/registration.key.b64" >/dev/null
MOCK_CURL_LOG="$progress_test_dir/curl.log" \
JDU_PROGRESS_CONFIG="$progress_test_dir/progress.env" \
JDU_PROGRESS_ACCOUNT_ID=123456789012 \
JDU_PROGRESS_INSTANCE_ID=i-0123456789abcdef0 \
JDU_PROGRESS_HOSTNAME=mock-host \
PATH="$root_dir/tests/mock-progress:$PATH" \
bash "$root_dir/scripts/jdu-progress" submit M5 3 4
grep -Fq "URL=$progress_endpoint/register" "$progress_test_dir/curl.log"
grep -Fq "URL=$progress_endpoint/submit" "$progress_test_dir/curl.log"
grep -Fq 'X-JDU-Registration-Key: rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr' "$progress_test_dir/curl.log"
grep -Fq "Authorization: Bearer $progress_token" "$progress_test_dir/curl.log"
grep -Fq '"mission":"M5","passed":3,"total":4' "$progress_test_dir/curl.log"

printf 'JDU_PROGRESS_ENDPOINT=%s\n' "$progress_endpoint" > "$progress_test_dir/teacher.env"
printf '%s\n' 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' > "$progress_test_dir/admin.key"
dashboard_output="$(MOCK_CURL_LOG="$progress_test_dir/curl.log" MOCK_CURL_RESPONSE='{"url":"https://example.test/dashboard?session=short","expires_in_seconds":1800}' PATH="$root_dir/tests/mock-progress:$PATH" JDU_TEACHER_CONFIG="$progress_test_dir/teacher.env" JDU_TEACHER_ADMIN_KEY="$progress_test_dir/admin.key" bash "$root_dir/teacher/scripts/jdu-dashboard")"
grep -Fq 'https://example.test/dashboard?session=short' <<<"$dashboard_output"
[[ "$dashboard_output" == 'https://example.test/dashboard?session=short' ]]
grep -Fq 'X-JDU-Admin-Key: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' "$progress_test_dir/curl.log"
grep -Fq '\033]8;;%s\033\\%s' "$root_dir/teacher/scripts/jdu-dashboard"
set +e
invalid_dashboard_output="$(MOCK_CURL_LOG="$progress_test_dir/curl.log" MOCK_CURL_RESPONSE='{"url":"http://example.test/dashboard?session=short"}' PATH="$root_dir/tests/mock-progress:$PATH" JDU_TEACHER_CONFIG="$progress_test_dir/teacher.env" JDU_TEACHER_ADMIN_KEY="$progress_test_dir/admin.key" bash "$root_dir/teacher/scripts/jdu-dashboard" 2>&1)"
invalid_dashboard_status=$?
set -e
[[ "$invalid_dashboard_status" -eq 1 ]]
grep -Fq 'invalid dashboard URL' <<<"$invalid_dashboard_output"
rm -rf -- "$progress_test_dir"
printf '%s\n' 'PASS student HTTPS reporting and teacher short-lived dashboard helper'

automatic_test_home="$(mktemp -d)"
automatic_progress_log="$automatic_test_home/progress.log"
chmod 0755 "$root_dir/tests/mock-progress/jdu-progress"
set +e
automatic_output="$(HOME="$automatic_test_home" MOCK_PROGRESS_LOG="$automatic_progress_log" JDU_PROGRESS_COMMAND="$root_dir/tests/mock-progress/jdu-progress" bash "$root_dir/scripts/jdu-labcheck" M1 2>&1)"
automatic_status=$?
set -e
[[ "$automatic_status" -eq 1 ]]
grep -Fxq 'submit M1 0 5' "$automatic_progress_log"
grep -Fq 'REPORT    PASS (server srv-0123456789abcdef)' <<<"$automatic_output"
rm -f -- "$automatic_progress_log"
set +e
HOME="$automatic_test_home" MOCK_PROGRESS_LOG="$automatic_progress_log" JDU_PROGRESS_COMMAND="$root_dir/tests/mock-progress/jdu-progress" bash "$root_dir/scripts/jdu-labcheck" M6 >/dev/null 2>&1
m6_ubuntu_status=$?
set -e
[[ "$m6_ubuntu_status" -eq 1 ]]
grep -Fxq 'submit M6U 0 2' "$automatic_progress_log"
rm -f -- "$automatic_progress_log"
set +e
HOME="$automatic_test_home" MOCK_PROGRESS_LOG="$automatic_progress_log" JDU_PROGRESS_COMMAND="$root_dir/tests/mock-progress/jdu-progress" bash "$root_dir/scripts/jdu-labcheck" P1 >/dev/null 2>&1
p1_report_status=$?
set -e
[[ "$p1_report_status" -eq 1 ]]
grep -Fxq 'submit P1 0 6' "$automatic_progress_log"
rm -f -- "$automatic_progress_log"
set +e
HOME="$automatic_test_home" MOCK_PROGRESS_LOG="$automatic_progress_log" JDU_PROGRESS_COMMAND="$root_dir/tests/mock-progress/jdu-progress" bash "$root_dir/scripts/jdu-labcheck" P6 >/dev/null 2>&1
p6_ubuntu_status=$?
set -e
[[ "$p6_ubuntu_status" -eq 1 ]]
grep -Fxq 'submit P6U 0 2' "$automatic_progress_log"
rm -f -- "$automatic_progress_log"
set +e
HOME="$automatic_test_home" MOCK_PROGRESS_LOG="$automatic_progress_log" JDU_PROGRESS_COMMAND="$root_dir/tests/mock-progress/jdu-progress" bash "$root_dir/scripts/jdu-labcheck" M1 --no-submit >/dev/null 2>&1
no_submit_status=$?
set -e
[[ "$no_submit_status" -eq 1 && ! -e "$automatic_progress_log" ]]
rm -rf -- "$automatic_test_home"
printf '%s\n' 'PASS jdu-check reports P and M results, maps both SSH Ubuntu sides, and honors --no-submit'

chmod 0755 "$mock_bin/aws" "$checker"
pass_output="$(PATH="$mock_bin:$PATH" "$checker" --region us-east-1 --stack-name test-stack)"
grep -q '^Required checks: 22 PASS, 0 FAIL, 0 ERROR$' <<<"$pass_output"
set +e
fail_output="$(MOCK_BAD_SG=1 PATH="$mock_bin:$PATH" "$checker" --region us-east-1 --stack-name test-stack 2>&1)"
fail_status=$?
set -e
[[ "$fail_status" -eq 1 ]]
grep -q '^FAIL  Security group has no inbound rules' <<<"$fail_output"
printf '%s\n' 'PASS AWS acceptance checker positive and negative tests'

printf '%s\n' 'ALL TESTS PASSED'
