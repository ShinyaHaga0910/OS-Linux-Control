#!/usr/bin/env bash
set -Eeuo pipefail

root_dir="$1"
test_dir="$(mktemp -d)"
trap 'rm -rf -- "$test_dir"' EXIT
mkdir -p "$test_dir/bin" "$test_dir/install"

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
  */scripts/jdu-my-progress) cp "$JDU_TEST_SOURCE/scripts/jdu-my-progress" "$destination" ;;
  *) exit 99 ;;
esac
if [[ "${JDU_TEST_TAMPER:-0}" == 1 && "$source_url" == */scripts/jdu-my-progress ]]; then
  printf '%s\n' '# tampered' >> "$destination"
fi
MOCK_CURL
cat > "$test_dir/bin/sudo" <<'MOCK_SUDO'
#!/usr/bin/env bash
exec "$@"
MOCK_SUDO
chmod 0755 "$test_dir/bin/curl" "$test_dir/bin/sudo"

export JDU_TEST_SOURCE="$root_dir" JDU_UBUNTU_PROGRESS_CONFIG="$test_dir/progress.env"
export JDU_UBUNTU_INSTALL_DIR="$test_dir/install" PATH="$test_dir/bin:$PATH"
set +e
missing_output="$(bash "$root_dir/scripts/install-my-progress-ubuntu.sh" 2>&1)"
missing_status=$?
set -e
[[ "$missing_status" -eq 2 ]]
grep -Fq 'registration is not readable' <<< "$missing_output"
[[ ! -e "$test_dir/install/jdu-my-progress" ]]

printf '%s\n' 'JDU_PROGRESS_ENDPOINT_B64=example' > "$test_dir/progress.env"
bash "$root_dir/scripts/install-my-progress-ubuntu.sh" >/dev/null
cmp "$root_dir/scripts/jdu-my-progress" "$test_dir/install/jdu-my-progress"

printf '%s\n' '# original installed command' >> "$test_dir/install/jdu-my-progress"
set +e
JDU_TEST_TAMPER=1 bash "$root_dir/scripts/install-my-progress-ubuntu.sh" >/dev/null 2>&1
tampered_status=$?
set -e
[[ "$tampered_status" -ne 0 ]]
grep -Fq '# original installed command' "$test_dir/install/jdu-my-progress"
printf '%s\n' 'PASS Ubuntu personal progress installer checks state and hashes without resetting the lab'
