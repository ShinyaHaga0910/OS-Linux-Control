#!/usr/bin/env bash
set -Eeuo pipefail

VERSION="${1:-v1.0.0}"
case "$VERSION" in
  v1.0.0) ;;
  *) printf 'ERROR Unsupported lab version: %s\n' "$VERSION" >&2; exit 2 ;;
esac

BASE_URL="${JDU_BASE_URL:-https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/${VERSION}}"
install -d -m 0755 /opt/jdu-lab/bin /opt/jdu-lab/fixtures/m1/source/config /opt/jdu-lab/fixtures/m1/source/logs /opt/jdu-lab/fixtures/m1/source/notes
install -d -m 0755 /opt/jdu-lab/fixtures/m3 /opt/jdu-lab/fixtures/m4 /opt/jdu-lab/fixtures/m5 /opt/jdu-lab/fixtures/m7
install -d -m 0755 /opt/jdu-lab/fixtures/p1/source/config /opt/jdu-lab/fixtures/p1/source/logs /opt/jdu-lab/fixtures/p1/source/notes
install -d -m 0755 /opt/jdu-lab/fixtures/p3 /opt/jdu-lab/fixtures/p4 /opt/jdu-lab/fixtures/p5
install -d -m 0755 /var/lib/jdu-lab/progress /etc/jdu-lab

curl -fsSL --retry 5 --retry-delay 5 "$BASE_URL/SHA256SUMS" -o /tmp/jdu-SHA256SUMS
curl -fsSL --retry 5 --retry-delay 5 "$BASE_URL/scripts/jdu-labcheck" -o /opt/jdu-lab/bin/jdu-labcheck
curl -fsSL --retry 5 --retry-delay 5 "$BASE_URL/scripts/jdu-fixture" -o /opt/jdu-lab/bin/jdu-fixture
curl -fsSL --retry 5 --retry-delay 5 "$BASE_URL/scripts/jdu-prepare-student-home" -o /opt/jdu-lab/bin/jdu-prepare-student-home
curl -fsSL --retry 5 --retry-delay 5 "$BASE_URL/scripts/jdu-worker" -o /opt/jdu-lab/bin/jdu-worker
curl -fsSL --retry 5 --retry-delay 5 "$BASE_URL/scripts/jdu-http-service" -o /opt/jdu-lab/bin/jdu-http-service
curl -fsSL --retry 5 --retry-delay 5 "$BASE_URL/scripts/jdu-progress" -o /opt/jdu-lab/bin/jdu-progress
curl -fsSL --retry 5 --retry-delay 5 "$BASE_URL/scripts/jdu-my-progress" -o /opt/jdu-lab/bin/jdu-my-progress

verify_download() {
  local published_path="$1" local_path="$2" expected
  expected="$(awk -v path="$published_path" '$2 == path {print $1}' /tmp/jdu-SHA256SUMS)"
  [[ "$expected" =~ ^[0-9a-f]{64}$ ]] || return 1
  printf '%s  %s\n' "$expected" "$local_path" | sha256sum --check --status
}
verify_download scripts/jdu-labcheck /opt/jdu-lab/bin/jdu-labcheck
verify_download scripts/jdu-fixture /opt/jdu-lab/bin/jdu-fixture
verify_download scripts/jdu-prepare-student-home /opt/jdu-lab/bin/jdu-prepare-student-home
verify_download scripts/jdu-worker /opt/jdu-lab/bin/jdu-worker
verify_download scripts/jdu-http-service /opt/jdu-lab/bin/jdu-http-service
verify_download scripts/jdu-progress /opt/jdu-lab/bin/jdu-progress
verify_download scripts/jdu-my-progress /opt/jdu-lab/bin/jdu-my-progress
rm -f -- /tmp/jdu-SHA256SUMS

chmod 0755 /opt/jdu-lab/bin/jdu-labcheck /opt/jdu-lab/bin/jdu-fixture /opt/jdu-lab/bin/jdu-prepare-student-home /opt/jdu-lab/bin/jdu-worker /opt/jdu-lab/bin/jdu-http-service /opt/jdu-lab/bin/jdu-progress /opt/jdu-lab/bin/jdu-my-progress
ln -sfn /opt/jdu-lab/bin/jdu-labcheck /usr/local/bin/jdu-labcheck
ln -sfn /opt/jdu-lab/bin/jdu-fixture /usr/local/bin/jdu-fixture
ln -sfn /opt/jdu-lab/bin/jdu-labcheck /usr/local/bin/jdu-check
ln -sfn /opt/jdu-lab/bin/jdu-fixture /usr/local/bin/jdu-reset
ln -sfn /opt/jdu-lab/bin/jdu-progress /usr/local/bin/jdu-progress
install -m 0755 /opt/jdu-lab/bin/jdu-my-progress /usr/local/bin/jdu-my-progress
ln -sfn /opt/jdu-lab/bin/jdu-prepare-student-home /usr/local/sbin/jdu-prepare-student-home
rm -f -- /opt/jdu-lab/bin/jdu-probe /usr/local/bin/jdu-probe

required_packages=()
command -v sshd >/dev/null 2>&1 || required_packages+=(openssh-server)
command -v tree >/dev/null 2>&1 || required_packages+=(tree)
if ((${#required_packages[@]} > 0)); then
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq "${required_packages[@]}"
fi
command -v tree >/dev/null 2>&1 || { printf '%s\n' 'ERROR tree installation failed.' >&2; exit 1; }
systemctl enable --now ssh.service

if ! getent passwd ssm-user >/dev/null; then
  useradd --create-home --shell /bin/bash ssm-user
fi
usermod -aG sudo ssm-user
if [[ -f /etc/jdu-lab/progress.env ]]; then
  chown root:ssm-user /etc/jdu-lab/progress.env
  chmod 0640 /etc/jdu-lab/progress.env
fi
install -d -m 0750 /etc/sudoers.d
printf '%s\n' 'ssm-user ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ssm-user
chmod 0440 /etc/sudoers.d/ssm-user

if ! getent passwd jduapp >/dev/null; then
  useradd --system --home-dir /srv/jdu-status --shell /usr/sbin/nologin jduapp
fi
if ! getent passwd jduweb >/dev/null; then
  useradd --system --home-dir /srv/jdu-web --shell /usr/sbin/nologin jduweb
fi
if ! getent passwd jdufinal >/dev/null; then
  useradd --system --home-dir /srv/jdu-final --shell /usr/sbin/nologin jdufinal
fi
if ! getent passwd jdupracticeapp >/dev/null; then
  useradd --system --home-dir /srv/jdu-practice-status --shell /usr/sbin/nologin jdupracticeapp
fi
if ! getent passwd jdupracticeweb >/dev/null; then
  useradd --system --home-dir /srv/jdu-practice-web --shell /usr/sbin/nologin jdupracticeweb
fi

marker_seed="$(tr -d '-' < /etc/machine-id | cut -c1-8)"
printf 'JDU-STATUS-%s\n' "$marker_seed" > /etc/jdu-lab/status-marker
printf 'JDU-WEB-%s\n' "$marker_seed" > /etc/jdu-lab/web-marker
printf 'JDU-FINAL-%s\n' "$marker_seed" > /etc/jdu-lab/final-marker
printf 'JDU-PRACTICE-STATUS-%s\n' "$marker_seed" > /etc/jdu-lab/practice-status-marker
printf 'JDU-PRACTICE-WEB-%s\n' "$marker_seed" > /etc/jdu-lab/practice-web-marker
chmod 0644 /etc/jdu-lab/status-marker /etc/jdu-lab/web-marker /etc/jdu-lab/final-marker \
  /etc/jdu-lab/practice-status-marker /etc/jdu-lab/practice-web-marker

for process_number in 1 2 3; do
  cat > "/opt/jdu-lab/fixtures/m3/jdu-m3-process${process_number}.service" <<UNIT
[Unit]
Description=JDU M3 process${process_number} for process and signal practice

[Service]
Type=simple
User=jduworker
ExecStart=/opt/jdu-lab/bin/jdu-worker process${process_number}
Restart=no
UNIT
  chmod 0444 "/opt/jdu-lab/fixtures/m3/jdu-m3-process${process_number}.service"
done

for process_number in 1 2 3; do
  cat > "/opt/jdu-lab/fixtures/p3/jdu-p3-process${process_number}.service" <<UNIT
[Unit]
Description=JDU P3 guided process${process_number}

[Service]
Type=simple
User=jdupracticeworker
ExecStart=/opt/jdu-lab/bin/jdu-worker guided-process${process_number}
Restart=no
UNIT
  chmod 0444 "/opt/jdu-lab/fixtures/p3/jdu-p3-process${process_number}.service"
done

install -d -o root -g root -m 0755 /srv/jdu-status
cp /etc/jdu-lab/status-marker /srv/jdu-status/index.txt
chown root:root /srv/jdu-status/index.txt
chmod 0644 /srv/jdu-status/index.txt

cat > /opt/jdu-lab/fixtures/m4/jdu-status.service <<'UNIT'
[Unit]
Description=JDU status service for systemd, port, and log practice
After=network.target

[Service]
Type=simple
User=jduapp
WorkingDirectory=/srv/jdu-status
ExecStart=/opt/jdu-lab/bin/jdu-http-service --address 127.0.0.1 --port 8080 --content /srv/jdu-status/index.txt
Restart=on-failure

[Install]
WantedBy=multi-user.target
UNIT
chmod 0444 /opt/jdu-lab/fixtures/m4/jdu-status.service
sha256sum /opt/jdu-lab/fixtures/m4/jdu-status.service | awk '{print $1}' > /opt/jdu-lab/fixtures/m4/jdu-status.service.sha256
chmod 0444 /opt/jdu-lab/fixtures/m4/jdu-status.service.sha256

cat > /opt/jdu-lab/fixtures/p4/jdu-practice-status.service <<'UNIT'
[Unit]
Description=JDU guided status service
After=network.target

[Service]
Type=simple
User=jdupracticeapp
WorkingDirectory=/srv/jdu-practice-status
ExecStart=/opt/jdu-lab/bin/jdu-http-service --address 127.0.0.1 --port 8180 --content /srv/jdu-practice-status/index.txt
Restart=on-failure

[Install]
WantedBy=multi-user.target
UNIT
chmod 0444 /opt/jdu-lab/fixtures/p4/jdu-practice-status.service
sha256sum /opt/jdu-lab/fixtures/p4/jdu-practice-status.service | awk '{print $1}' > /opt/jdu-lab/fixtures/p4/jdu-practice-status.service.sha256
chmod 0444 /opt/jdu-lab/fixtures/p4/jdu-practice-status.service.sha256

cat > /opt/jdu-lab/fixtures/m5/jdu-web.service <<'UNIT'
[Unit]
Description=JDU web service for socket, HTTP, and journal practice
After=network.target

[Service]
Type=simple
User=jduweb
WorkingDirectory=/srv/jdu-web
ExecStart=/opt/jdu-lab/bin/jdu-http-service --address 127.0.0.1 --port 8081 --content /srv/jdu-web/index.txt
Restart=on-failure

[Install]
WantedBy=multi-user.target
UNIT
chmod 0444 /opt/jdu-lab/fixtures/m5/jdu-web.service
sha256sum /opt/jdu-lab/fixtures/m5/jdu-web.service | awk '{print $1}' > /opt/jdu-lab/fixtures/m5/jdu-web.service.sha256
chmod 0444 /opt/jdu-lab/fixtures/m5/jdu-web.service.sha256

cat > /opt/jdu-lab/fixtures/p5/jdu-practice-web.service <<'UNIT'
[Unit]
Description=JDU guided web service
After=network.target

[Service]
Type=simple
User=jdupracticeweb
WorkingDirectory=/srv/jdu-practice-web
ExecStart=/opt/jdu-lab/bin/jdu-http-service --address 127.0.0.1 --port 8181 --content /srv/jdu-practice-web/index.txt
Restart=on-failure

[Install]
WantedBy=multi-user.target
UNIT
chmod 0444 /opt/jdu-lab/fixtures/p5/jdu-practice-web.service
sha256sum /opt/jdu-lab/fixtures/p5/jdu-practice-web.service | awk '{print $1}' > /opt/jdu-lab/fixtures/p5/jdu-practice-web.service.sha256
chmod 0444 /opt/jdu-lab/fixtures/p5/jdu-practice-web.service.sha256

cat > /opt/jdu-lab/fixtures/m7/jdu-final.service <<'UNIT'
[Unit]
Description=JDU final integrated Ubuntu service
After=network.target

[Service]
Type=simple
User=jdufinal
WorkingDirectory=/srv/jdu-final
ExecStart=/opt/jdu-lab/bin/jdu-http-service --address 127.0.0.1 --port 8090 --content /srv/jdu-final/index.txt
Restart=on-failure

[Install]
WantedBy=multi-user.target
UNIT
chmod 0444 /opt/jdu-lab/fixtures/m7/jdu-final.service
sha256sum /opt/jdu-lab/fixtures/m7/jdu-final.service | awk '{print $1}' > /opt/jdu-lab/fixtures/m7/jdu-final.service.sha256
chmod 0444 /opt/jdu-lab/fixtures/m7/jdu-final.service.sha256

cat > /etc/systemd/system/jdu-student-home.service <<'UNIT'
[Unit]
Description=Prepare the JDU workspace for the Session Manager student user
ConditionPathExists=/home/ssm-user

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/jdu-prepare-student-home ssm-user
UNIT

cat > /etc/systemd/system/jdu-student-home.path <<'UNIT'
[Unit]
Description=Watch for the Session Manager student home

[Path]
PathExists=/home/ssm-user
Unit=jdu-student-home.service

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now jdu-student-home.path
if getent passwd ssm-user >/dev/null; then
  /usr/local/sbin/jdu-prepare-student-home ssm-user
fi

printf '%s\n' 'mode=training' 'course=Introduction_CyberSecurity' > /opt/jdu-lab/fixtures/m1/source/config/app.conf
printf '%s\n' \
  '2026-09-01T08:00:00Z INFO service started' \
  '2026-09-01T08:03:00Z WARN retry requested' \
  '2026-09-01T08:05:00Z ERROR permission denied for report.txt' \
  '2026-09-01T08:06:00Z INFO request completed' \
  '2026-09-01T08:08:00Z ERROR configuration key is missing' \
  '2026-09-01T08:10:00Z INFO service stopped' > /opt/jdu-lab/fixtures/m1/source/logs/incident.log
printf '%s\n' 'Preserve the source files. Build the required case01 tree in your home directory.' > /opt/jdu-lab/fixtures/m1/source/notes/instructions.txt
sha256sum /opt/jdu-lab/fixtures/m1/source/config/app.conf /opt/jdu-lab/fixtures/m1/source/logs/incident.log /opt/jdu-lab/fixtures/m1/source/notes/instructions.txt > /opt/jdu-lab/fixtures/m1/SHA256SUMS
printf '%s\n' 'mode=guided-practice' 'course=Introduction_CyberSecurity' > /opt/jdu-lab/fixtures/p1/source/config/training.conf
printf '%s\n' \
  '2026-09-02T09:00:00Z INFO guided service started' \
  '2026-09-02T09:02:00Z WARN storage usage reached 70 percent' \
  '2026-09-02T09:04:00Z INFO request accepted' \
  '2026-09-02T09:06:00Z WARN response time exceeded target' \
  '2026-09-02T09:08:00Z INFO guided service stopped' > /opt/jdu-lab/fixtures/p1/source/logs/practice.log
printf '%s\n' 'Follow the guided steps. Build practice01 without changing the source files.' > /opt/jdu-lab/fixtures/p1/source/notes/instructions.txt
sha256sum /opt/jdu-lab/fixtures/p1/source/config/training.conf /opt/jdu-lab/fixtures/p1/source/logs/practice.log /opt/jdu-lab/fixtures/p1/source/notes/instructions.txt > /opt/jdu-lab/fixtures/p1/SHA256SUMS
chmod -R a-w /opt/jdu-lab/fixtures

printf '%s\n' "$VERSION" > /etc/jdu-lab/version
printf '%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > /etc/jdu-lab/installed-at-utc
chmod 0644 /etc/jdu-lab/version /etc/jdu-lab/installed-at-utc

if command -v snap >/dev/null 2>&1 && snap list amazon-ssm-agent >/dev/null 2>&1; then
  snap start amazon-ssm-agent >/dev/null 2>&1 || true
elif systemctl list-unit-files amazon-ssm-agent.service >/dev/null 2>&1; then
  systemctl enable --now amazon-ssm-agent.service >/dev/null 2>&1 || true
fi

sha256sum /etc/ssh/sshd_config > /etc/jdu-lab/ssh-baseline.sha256
sha256sum /opt/jdu-lab/bin/jdu-labcheck > /etc/jdu-lab/checker-baseline.sha256
chmod 0444 /etc/jdu-lab/ssh-baseline.sha256 /etc/jdu-lab/checker-baseline.sha256

/opt/jdu-lab/bin/jdu-fixture reset all >/var/log/jdu-fixture-initial-reset.log

if [[ -s /etc/jdu-lab/progress-registration-key.b64 ]]; then
  if /opt/jdu-lab/bin/jdu-progress register /etc/jdu-lab/progress-registration-key.b64 >/var/log/jdu-progress-registration.log 2>&1; then
    rm -f -- /etc/jdu-lab/progress-registration-key.b64
  else
    printf '%s\n' 'JDU_PROGRESS_REGISTRATION_FAILED' >&2
    exit 1
  fi
fi

printf '%s\n' 'JDU_SETUP_COMPLETE'
