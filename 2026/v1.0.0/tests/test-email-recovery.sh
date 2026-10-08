#!/usr/bin/env bash
set -Eeuo pipefail

root_dir="$1"
test_dir="$(mktemp -d)"
trap 'rm -rf -- "$test_dir"' EXIT
mkdir -p "$test_dir/bin" "$test_dir/home/.jdu-student"

cat > "$test_dir/bin/curl" <<'MOCK_CURL'
#!/usr/bin/env bash
set -Eeuo pipefail
destination=''
source_url=''
while (($#)); do
  case "$1" in
    -o) destination="$2"; shift 2 ;;
    --retry|--connect-timeout) shift 2 ;;
    -*) shift ;;
    *) source_url="$1"; shift ;;
  esac
done
case "$source_url" in
  */SHA256SUMS) cp "$JDU_TEST_SOURCE/SHA256SUMS" "$destination" ;;
  */scripts/register-student.py) cp "$JDU_TEST_SOURCE/scripts/register-student.py" "$destination" ;;
  *) exit 99 ;;
esac
MOCK_CURL
cat > "$test_dir/bin/python3" <<'MOCK_PYTHON'
#!/usr/bin/env bash
printf '%s\n' "$*" > "$JDU_TEST_PYTHON_LOG"
MOCK_PYTHON
chmod 0755 "$test_dir/bin/curl" "$test_dir/bin/python3"

export HOME="$test_dir/home" JDU_TEST_SOURCE="$root_dir" JDU_TEST_PYTHON_LOG="$test_dir/python.log"
export PATH="$test_dir/bin:$PATH"
set +e
missing_output="$(bash "$root_dir/scripts/recover-student-email.sh" 2>&1)"
missing_status=$?
set -e
[[ "$missing_status" -eq 2 ]]
grep -Fq 'Registration state was not found' <<<"$missing_output"
[[ ! -e "$HOME/.local/bin/jdu-register" ]]

printf '%s\n' 'JDU_PROGRESS_ENDPOINT=https://example.test' > "$HOME/.jdu-student/progress.env"
bash "$root_dir/scripts/recover-student-email.sh" >/dev/null
cmp "$root_dir/scripts/register-student.py" "$HOME/.local/bin/jdu-register"
grep -Fq -- '--change-email' "$test_dir/python.log"

printf '%s\n' '# tampered' >> "$HOME/.local/bin/jdu-register"
# A bad download must not replace the installed helper or invoke registration.
cat > "$test_dir/bin/curl" <<'MOCK_BAD_CURL'
#!/usr/bin/env bash
set -Eeuo pipefail
destination=''
source_url=''
while (($#)); do
  case "$1" in
    -o) destination="$2"; shift 2 ;;
    --retry|--connect-timeout) shift 2 ;;
    -*) shift ;;
    *) source_url="$1"; shift ;;
  esac
done
case "$source_url" in
  */SHA256SUMS) cp "$JDU_TEST_SOURCE/SHA256SUMS" "$destination" ;;
  */scripts/register-student.py) cp "$JDU_TEST_SOURCE/scripts/register-student.py" "$destination"; printf '%s\n' '# tampered' >> "$destination" ;;
  *) exit 99 ;;
esac
MOCK_BAD_CURL
chmod 0755 "$test_dir/bin/curl"
rm -f "$test_dir/python.log"
set +e
bash "$root_dir/scripts/recover-student-email.sh" >/dev/null 2>&1
tampered_status=$?
set -e
[[ "$tampered_status" -ne 0 ]]
[[ ! -e "$test_dir/python.log" ]]
grep -Fq '# tampered' "$HOME/.local/bin/jdu-register"
printf '%s\n' 'PASS email-only recovery rejects missing state and tampered downloads, without resetting the lab'
