#!/usr/bin/env bash
set -Eeuo pipefail

checker="$1"
test_dir="$(mktemp -d)"
trap 'rm -rf -- "$test_dir"' EXIT
mkdir -p "$test_dir/bin" "$test_dir/package"
printf '#!/bin/sh\nexit 0\n' > "$test_dir/package/real-command"
chmod 0755 "$test_dir/package/real-command"
ln -s "$test_dir/package/real-command" "$test_dir/bin/public-command"

cat > "$test_dir/bin/dpkg-query" <<'MOCK'
#!/bin/sh
case "$1" in
  -W)
    if [ "${MOCK_MISSING:-0}" = 1 ]; then exit 1; fi
    printf 'install ok installed:2.2.5-3'
    ;;
  -S)
    printf '%s: %s\n' "${MOCK_OWNER:-figlet}" "$3"
    ;;
  *) exit 2 ;;
esac
MOCK
chmod 0755 "$test_dir/bin/dpkg-query"
export PATH="$test_dir/bin:$PATH"

# Source only the pure helper; do not execute the student-facing checker.
source <(sed -n '/^package_command_owned_by() {/,/^}/p' "$checker")
package_command_owned_by figlet "$test_dir/bin/public-command"
MOCK_OWNER=cmatrix package_command_owned_by cmatrix "$test_dir/bin/public-command"
if MOCK_OWNER=other-package package_command_owned_by figlet "$test_dir/bin/public-command"; then exit 1; fi
if MOCK_MISSING=1 package_command_owned_by figlet "$test_dir/bin/public-command"; then exit 1; fi
rm "$test_dir/bin/public-command"
ln -s "$test_dir/package/absent" "$test_dir/bin/public-command"
if package_command_owned_by figlet "$test_dir/bin/public-command"; then exit 1; fi

grep -Fq 'package_command_owned_by figlet /usr/bin/figlet' "$checker"
grep -Fq 'package_command_owned_by cmatrix /usr/bin/cmatrix' "$checker"
printf '%s\n' 'PASS P3/M3 package checks resolve alternatives links and reject missing or wrong owners'
