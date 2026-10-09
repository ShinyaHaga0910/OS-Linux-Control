# Ubuntu and OS Foundations — to‘liq ko‘rsatmalar bilan mashqlar

[日本語](../ja/practice.md) · [Русский](../ru/practice.md) · [O‘zbekcha](../uz/practice.md)

> Bu tarjimada amaldagi P0–P6 savollari va qadamlari hali aks etmagan. Lab tekshiradigan amaldagi talablar uchun OS-Linux-Control repositorysidagi yaponcha joriy nusxadan foydalaning.

Qamrov: Guided Practice P1–P6. Muhit: Ubuntu Server 24.04 LTS. Har bir P mashqidan keyin shu ko‘nikma bilan Mission Mni mustaqil bajaring.

## 0. Umumiy qoidalar

P1–P6 mashq uchun. Ular M1–M6dan boshqa `directory`, `user`, `group`, `service` va `port`lardan foydalanadi. M7 umumlashtiruvchi topshiriq; unga alohida qadamma-qadam mashq yo‘q.

Ubuntuda quyidagini bajaring. Natija `ssm-user` bo‘lsin:

```bash
id -un
```

Boshqa `user` ko‘rinsa, bir marta `exit` qiling va qayta tekshiring:

```bash
exit
id -un
```

Har bir bosqich boshida ish `directory`siga o‘ting. O‘tgach `pwd` bilan joyni tekshiring.

Baholash:

```bash
jdu-check P1
```

Faqat boshidan boshlash zarur bo‘lsa `reset` qiling:

```bash
jdu-reset P1
```

## P1 Shell, path, file, text

### O‘rganiladigan ko‘nikmalar

- `home directory` va ish `directory`sini ajratish.
- `directory` yaratish.
- `file`dan nusxa olish.
- `log`dan kerakli satrlarni saqlash.

### 1-bosqich: Home directoryga o‘tish

```bash
cd ~
pwd
```

Natija `/home/ssm-user` bo‘lsin.

### 2-bosqich: P1 directorysiga o‘tish

```bash
cd ~/jdu-lab/p1
pwd
tree
```

`inbox` va hali tugallanmagan `practice01`ni toping.

### 3-bosqich: Kerakli directorylarni yaratish

```bash
cd ~/jdu-lab/p1
mkdir -p practice01/config
mkdir -p practice01/logs
mkdir -p practice01/notes
tree practice01
```

### 4-bosqich: Config filedan nusxa olish

Nusxa joylashtiriladigan `directory`ga o‘ting.

```bash
cd ~/jdu-lab/p1/practice01/config
pwd
cp ../../inbox/config/training.conf .
ls -l
```

`.` hozirgi `directory`ni anglatadi.

### 5-bosqich: Log filedan nusxa olish

```bash
cd ~/jdu-lab/p1/practice01/logs
pwd
cp ../../inbox/logs/practice.log .
ls -l
```

### 6-bosqich: Vaqtinchalik filelarni topib o‘chirish

`practice01`ga o‘ting:

```bash
cd ~/jdu-lab/p1/practice01
pwd
find . -type f -name '*.tmp' -print
find . -type f -name '*.tmp' -delete
find . -type f -name '*.tmp' -print
```

Oxirgi `command` hech narsa chiqarmasligi kerak.

### 7-bosqich: WARN bor satrlarni saqlash

Natija yoziladigan `notes`ga o‘ting:

```bash
cd ~/jdu-lab/p1/practice01/notes
pwd
grep 'WARN' ../logs/practice.log > warnings.txt
cat warnings.txt
```

### 8-bosqich: Oxirgi to‘rt satrni saqlash

```bash
cd ~/jdu-lab/p1/practice01/notes
tail -n 4 ../logs/practice.log > recent.txt
cat recent.txt
```

### 9-bosqich: Barcha natijani tekshirish

```bash
cd ~/jdu-lab/p1
tree practice01
stat -c '%U:%G %a %n' practice01 practice01/config/training.conf practice01/logs/practice.log practice01/notes/warnings.txt practice01/notes/recent.txt
jdu-check P1
```

Barcha 6 band `PASS` bo‘lsa, M1ga o‘ting.

## P2 User, group, permission, setgid

### O‘rganiladigan ko‘nikmalar

- `primary group` va `supplementary group`ni tekshirish.
- Umumiy `directory`ga `group permission` qo‘yish.
- `setgid` yordamida yangi `file`ning `group`ini meros qildirish.

### 1-bosqich: Boshqaruv userini tekshirish

```bash
cd ~
id -un
id
```

### 2-bosqich: Boshlang‘ich groupni tekshirish

```bash
getent group practiceops
id jdupracticewriter
id jdupracticeviewer
```

Dastlab `jdupracticeviewer` `practiceops` a’zosi, `jdupracticewriter` esa a’zo emas.

### 3-bosqich: Group a’zoligini to‘g‘rilash

```bash
cd ~
sudo usermod -aG practiceops jdupracticewriter
sudo gpasswd -d jdupracticeviewer practiceops
getent group practiceops
id jdupracticewriter
id jdupracticeviewer
```

### 4-bosqich: Umumiy directoryni sozlash

```bash
cd /srv
pwd
sudo chown root:practiceops jdu-practice-share
sudo chmod 2775 jdu-practice-share
stat -c '%U:%G %a %n' jdu-practice-share
```

### 5-bosqich: GUIDE.txtni sozlash

Kerakli `directory`ga o‘ting:

```bash
cd /srv/jdu-practice-share
pwd
sudo chown root:practiceops GUIDE.txt
sudo chmod 664 GUIDE.txt
stat -c '%U:%G %a %n' GUIDE.txt
```

### 6-bosqich: Writerga o‘tib file yaratish

```bash
cd ~
sudo su - jdupracticewriter
id -un
id
cd /srv/jdu-practice-share
pwd
printf '%s\n' 'guided writer file' > writer-created.txt
ls -l writer-created.txt
exit
id -un
```

Oxirgi natija `ssm-user` bo‘lsin.

### 7-bosqich: Viewerning o‘qish va yozishini tekshirish

```bash
cd ~
sudo su - jdupracticeviewer
id -un
id
cd /srv/jdu-practice-share
pwd
cat GUIDE.txt
touch viewer-created.txt
exit
id -un
```

`cat` muvaffaqiyatli ishlaydi. `touch` `Permission denied` beradi. Bu kutilgan rad etish.

### 8-bosqich: Baholash

```bash
cd ~
id -un
jdu-check P2
```

Barcha 6 band `PASS` bo‘lsa, M2ga o‘ting.

## P3 Process va package

8-bobdan keyin 1–4-bosqichlar orqali `process`ni tekshirib to‘xtating. 9-bobni o‘qib, 5–6-bosqichlar orqali `package`ni o‘rnating. Ikkala qism tugagach `jdu-check P3`ni bajaring.

### O‘rganiladigan ko‘nikmalar

- `systemd service` va `process` PIDini bog‘lash.
- Aniq PIDga `TERM signal` yuborish.
- `apt` bilan `package` o‘rnatish.

### 1-bosqich: Uchta serviceni tekshirish

```bash
cd ~
systemctl list-units --type=service 'jdu-p3-*'
systemctl status jdu-p3-process1.service --no-pager
systemctl status jdu-p3-process2.service --no-pager
systemctl status jdu-p3-process3.service --no-pager
```

### 2-bosqich: Process2 Main PIDini ko‘rsatish

```bash
systemctl show --property MainPID --value jdu-p3-process2.service
```

### 3-bosqich: PIDni shell o‘zgaruvchisida saqlash

```bash
P3_PID=$(systemctl show --property MainPID --value jdu-p3-process2.service)
printf '%s\n' "$P3_PID"
ps -fp "$P3_PID"
```

### 4-bosqich: Faqat process2ga TERM yuborish

```bash
sudo kill -TERM "$P3_PID"
systemctl is-active jdu-p3-process1.service
systemctl is-active jdu-p3-process2.service
systemctl is-active jdu-p3-process3.service
```

Tartib bilan `active`, `inactive`, `active` chiqishi kerak.

### 5-bosqich: Figletni tekshirib o‘rnatish

```bash
cd ~
apt show figlet
sudo apt update
sudo apt install -y figlet
command -v figlet
figlet JDU
```

### 6-bosqich: Package va command mosligini ko‘rish

```bash
dpkg-query -W -f='${Status} ${Version}\n' figlet
dpkg -S /usr/bin/figlet
jdu-check P3
```

Ikkala band `PASS` bo‘lsa, M3ga o‘ting.

## P4 systemd service

### O‘rganiladigan ko‘nikmalar

- `unit file`ni o‘qish.
- `active` va `enabled` holatlarini alohida sozlash.
- Main PID va haqiqiy `process`ni bog‘lash.

### 1-bosqich: Unit fileni o‘qish

```bash
cd ~
systemctl cat jdu-practice-status.service
```

`User`, `WorkingDirectory`, `ExecStart`ni tekshiring.

### 2-bosqich: Dastlabki holatni tekshirish

```bash
systemctl is-active jdu-practice-status.service
systemctl is-enabled jdu-practice-status.service
```

### 3-bosqich: Serviceni start qilish

```bash
sudo systemctl start jdu-practice-status.service
systemctl is-active jdu-practice-status.service
```

### 4-bosqich: Tizim yoqilganda start qilishni sozlash

```bash
sudo systemctl enable jdu-practice-status.service
systemctl is-enabled jdu-practice-status.service
```

### 5-bosqich: Main PID va processni tekshirish

```bash
P4_PID=$(systemctl show --property MainPID --value jdu-practice-status.service)
printf '%s\n' "$P4_PID"
ps -fp "$P4_PID"
sudo cat "/proc/$P4_PID/cmdline" | tr '\0' ' '
printf '\n'
sudo readlink -f "/proc/$P4_PID/cwd"
```

### 6-bosqich: Baholash

```bash
cd ~
jdu-check P4
```

Uchala band `PASS` bo‘lsa, M4ga o‘ting.

## P5 Port, socket, HTTP, journal

### O‘rganiladigan ko‘nikmalar

- `service`, `process` va `listening socket`ni bog‘lash.
- IP address va `port`ni o‘qish.
- HTTP `request` `journal`da qayd etilishini tekshirish.

### 1-bosqich: Unit fileni o‘qish

```bash
cd ~
systemctl cat jdu-practice-web.service
```

`127.0.0.1`, `8181`, `jdupracticeweb` va kontent `file`i `path`ini tekshiring.

### 2-bosqich: Serviceni start qilish

```bash
sudo systemctl start jdu-practice-web.service
systemctl is-active jdu-practice-web.service
```

### 3-bosqich: Listening socketni tekshirish

```bash
sudo ss -lntp | grep ':8181'
```

`127.0.0.1:8181`ni toping. Shu chiqishda `0.0.0.0:8181` yoki `[::]:8181`da kutish yo‘qligini ham tekshiring. Birinchisi faqat shu `host` ichidan ulanishni, keyingilari barcha manzillarda kutishni bildiradi.

### 4-bosqich: Socket PID va Main PIDni solishtirish

```bash
systemctl show --property MainPID --value jdu-practice-web.service
sudo ss -lntp | grep ':8181'
```

Ikki PID bir xil bo‘lishi kerak.

### 5-bosqich: HTTP responseni tekshirish

```bash
curl -i http://127.0.0.1:8181/
```

### 6-bosqich: Service userning o‘qish huquqini tekshirish

Kontent `directory`siga o‘ting:

```bash
cd /srv/jdu-practice-web
pwd
stat -c '%U:%G %a %n' index.txt
namei -l /srv/jdu-practice-web/index.txt
id jdupracticeweb
sudo -u jdupracticeweb -- test -r index.txt
echo $?
```

Oxirgi qiymat `0` bo‘lsa, o‘qish mumkin.

### 7-bosqich: Talaba requestini yuborish

```bash
curl -i http://127.0.0.1:8181/p5-check
sudo journalctl -u jdu-practice-web.service --no-pager -n 20
```

`REQUEST path=/p5-check`ni toping.

### 8-bosqich: Closed port bilan solishtirish

```bash
curl --max-time 2 http://127.0.0.1:18181/
sudo ss -lnt | grep ':18181'
```

Ikkalasi ham muvaffaqiyatli chiqmaydi. TCP 18181da kutayotgan `socket` yo‘q.

### 9-bosqich: Baholash

```bash
cd ~
jdu-check P5
```

To‘rttala band `PASS` bo‘lsa, M5ga o‘ting.

## P6 SSH, remote command, scp

### O‘rganiladigan ko‘nikmalar

- CloudShell va Ubuntuni farqlash.
- `scp` bilan `upload` va `download` qilish.
- SSH `remote command`ini bajarish.

### 1-bosqich: Ubuntudan CloudShellga qaytish

Ubuntu `prompt`ida bajaring:

```bash
exit
```

CloudShellda qayerda ekaningizni tekshiring:

```bash
cd ~
pwd
id -un
hostname
```

### 2-bosqich: CloudShelldagi ish directorysini yaratish

```bash
mkdir -p ~/jdu-lab/p6
cd ~/jdu-lab/p6
pwd
```

### 3-bosqich: Upload manbasi bo‘lgan fileni yaratish

```bash
printf '%s\n' 'JDU SSH guided transfer' > practice-source.txt
cat practice-source.txt
sha256sum practice-source.txt
```

### 4-bosqich: Ubuntudagi directoryni yaratish

CloudShellda bajaring:

```bash
ssh jdu-ubuntu 'mkdir -p ~/jdu-lab/p6'
```

### 5-bosqich: Ubuntuga upload qilish

CloudShell P6 `directory`sidan bajaring:

```bash
cd ~/jdu-lab/p6
scp practice-source.txt jdu-ubuntu:~/jdu-lab/p6/practice-upload.txt
ssh jdu-ubuntu 'sha256sum ~/jdu-lab/p6/practice-upload.txt'
sha256sum practice-source.txt
```

Ikki SHA-256 qiymati bir xil bo‘lsin.

### 6-bosqich: SSH remote command bilan natija fileni yaratish

CloudShellda quyidagi bitta `command`ni aynan ko‘rsatilgandek bajaring:

```bash
ssh jdu-ubuntu 'cd ~/jdu-lab/p6 && printf "REMOTE_USER=%s\nREMOTE_HOST=%s\nREMOTE_PATH=%s\n" "$(id -un)" "$(hostname)" "$HOME" > practice-remote-result.txt'
```

Mazmunni `remote`da tekshiring:

```bash
ssh jdu-ubuntu 'cat ~/jdu-lab/p6/practice-remote-result.txt'
```

### 7-bosqich: Ubuntu tomonini baholash

Ubuntuga ulanib bajaring:

```bash
ssh jdu-ubuntu
cd ~/jdu-lab/p6
pwd
ls -l
jdu-check P6
exit
```

Ubuntu tomondagi ikkala band `PASS` bo‘lsin.

### 8-bosqich: Natija fileni download qilish

CloudShellda bajaring:

```bash
cd ~/jdu-lab/p6
scp jdu-ubuntu:~/jdu-lab/p6/practice-remote-result.txt practice-downloaded-result.txt
cat practice-downloaded-result.txt
sha256sum practice-downloaded-result.txt
ssh jdu-ubuntu 'sha256sum ~/jdu-lab/p6/practice-remote-result.txt'
```

Ikki SHA-256 qiymati bir xil bo‘lsin.

### 9-bosqich: CloudShell tomonini baholash

```bash
cd ~/jdu-lab/p6
jdu-check P6
```

CloudShell tomondagi to‘rtala band `PASS` bo‘lsa, M6ga o‘ting.

## O‘rganish tartibi

Kitobdagi boblar dars soatlari bilan birma-bir mos emas. Tushungan joyingizdan mashqqa o‘ting, zarur bo‘lsa bobga qayting.

- 1–3-boblar va 4-bobning tahrirlash asoslarini o‘qing. Keyin M0da haqiqiy `OS`ni kuzating.
- 4–5-boblarni o‘qib P1, M1ga o‘ting.
- 6–7-boblarni o‘qib P2, M2ga o‘ting.
- 8-bobni o‘qib P3ning 1–4-bosqichlarini bajaring. 9-bobni o‘qib P3ning 5–6-bosqichlarini bajaring. Keyin M3ga o‘ting.
- 10-bobdan keyin P4, M4; 11-bobdan keyin P5, M5ga o‘ting.
- 12-bobdan keyin P6, M6ga o‘ting. Avvalgi ko‘nikmalarni birlashtirib M7ni bajaring.

Umumiy tavsiya etilgan tartib:

```text
P1 → M1 → P2 → M2 → P3 → M3 → P4 → M4
   → P5 → M5 → P6 → M6 → M7 (yakuniy topshiriq)
```

Pda ko‘rsatilgan `command`larga qarab ishlang. M1–M6da Pdagi `command`larga qaramasdan, keraklisini o‘zingiz tanlang. M7da M2, M4 va M5dagi bilimlarni birlashtiring.
