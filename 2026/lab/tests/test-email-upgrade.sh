#!/usr/bin/env bash
set -Eeuo pipefail

root_dir="$1"
test_dir="$(mktemp -d)"
trap 'rm -rf -- "$test_dir"' EXIT
mkdir -p "$test_dir/bin" "$test_dir/home/.jdu-student"

update_command="$(awk '
  /^古い環境で`jdu-register/ { found=1; next }
  found && /^```bash$/ { block=1; next }
  block && /^```$/ { exit }
  block { print }
' "$root_dir/setup/student-registration.ja.md")"
[[ "$update_command" == *'scripts/register-student.py'* ]]
[[ "$update_command" == *'sha256sum --check --status'* ]]
[[ "$update_command" == *'--change-email'* ]]

cat > "$test_dir/bin/curl" <<'MOCK_CURL'
#!/usr/bin/env bash
set -Eeuo pipefail
destination=''
source_url=''
while (($#)); do
  case "$1" in
    -o) destination="$2"; shift 2 ;;
    -*) shift ;;
    *) source_url="$1"; shift ;;
  esac
done
case "$source_url" in
  */SHA256SUMS) cp "$JDU_TEST_SOURCE/SHA256SUMS" "$destination" ;;
  */scripts/register-student.py)
    cp "$JDU_TEST_SOURCE/scripts/register-student.py" "$destination"
    if [[ "${JDU_TEST_TAMPER:-0}" == 1 ]]; then
      printf '%s\n' '# tampered download' >> "$destination"
    fi ;;
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
printf '%s\n' 'JDU_PROGRESS_ENDPOINT=https://example.test' > "$HOME/.jdu-student/progress.env"
bash -c "$update_command" >/dev/null
cmp "$root_dir/scripts/register-student.py" "$HOME/.local/bin/jdu-register"
grep -Fq -- '--change-email' "$test_dir/python.log"

printf '%s\n' '# keep existing installation' >> "$HOME/.local/bin/jdu-register"
rm -f "$test_dir/python.log"
set +e
JDU_TEST_TAMPER=1 bash -c "$update_command" >/dev/null 2>&1
tampered_status=$?
set -e
[[ "$tampered_status" -ne 0 ]]
[[ ! -e "$test_dir/python.log" ]]
grep -Fq '# keep existing installation' "$HOME/.local/bin/jdu-register"
printf '%s\n' 'PASS documented jdu-register upgrade verifies SHA-256 before replacing an old installation'
