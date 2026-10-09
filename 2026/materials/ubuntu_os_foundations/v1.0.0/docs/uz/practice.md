# Ubuntu and OS Foundations — to‘liq ko‘rsatmalar bilan mashqlar

[日本語](../ja/practice.md) · [Русский](../ru/practice.md) · [O‘zbekcha](../uz/practice.md)

> ChatGPT tarjimasi joriy yaponcha manbaga moslashtirilgan. Ona tilida gapiruvchi mutaxassis hali tekshirmagan; baholash shartlari farq qilsa, yaponcha asl matnga tayaning.

Qamrov: Guided Practice P0–P6. Muhit: Ubuntu Server 24.04 LTS.

Tartib: avval har bir P topshirig‘ini o‘qing. O‘zingiz yechib ko‘ring, so‘ng qadamma-qadam yechim bilan amallar va sabablarini solishtiring. Shu ko‘nikmaga tegishli Mission Mni mustaqil bajaring.

## Avval Ubuntuga ulaning

AWS Academy Learner Lab dastlabki sozlamalari tugagach, AWS konsolida CloudShellni oching. CloudShellda o‘z Ubuntu mashq serveringizga ulaning:

```bash
ssh jdu-ubuntu
```

P0–P5ni ulangan Ubuntuda bajaring. P6da CloudShell va Ubuntu amallari uchun joy har bir bosqichda ko‘rsatiladi.

## 0. Umumiy qoidalar

P0–P6 mashq uchun. P0 — OSni kuzatishga bag‘ishlangan boshlang‘ich qadamma-qadam mashq. P1–P6 M1–M6dan boshqa `directory`, `user`, `group`, `service` va `port`lardan foydalanadi. M7 umumlashtiruvchi topshiriq; unga alohida mashq yo‘q.

Har bir Pda avval topshiriq matni, keyin yechim namunasi beriladi. Topshiriqni avval mustaqil bajarish yoki yo‘riqnoma bilan birga ishlash mumkin. P va M alohida baholanadi: Pdagi `PASS` Mni avtomatik `PASS` qilmaydi.

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

Ubuntu tomonidagi baholashni `ssm-user` sifatida bajaring. P6ning CloudShell tomonini CloudShellda tekshiring:

```bash
jdu-check P1
```

Baholash yakuniy holatni tekshiradi. Faqat kuzatish yoki oraliq amal har doim baholanmaydi. Natija o‘qituvchi progress sahifasiga avtomatik yuboriladi. Yuborish ishlamasa ham Ubuntu yoki CloudShelldagi `PASS`/`FAIL` ko‘rinadi.

Faqat boshidan boshlash zarur bo‘lsa `reset` qiling:

```bash
jdu-reset P1
```

## P0 Environment and OS

### O‘rganiladigan ko‘nikmalar

- Ubuntu OS haqidagi ma’lumot bilan Linux `kernel` haqidagi ma’lumotni farqlash.
- Hozirgi `user`, `hostname` va PID 1 `process`ini haqiqiy serverda aniqlash.
- `Command` natijalarini `file`ga yozish, saqlash, tekshirish va topshirish.

### Topshiriq

O‘z Ubuntu mashq serveringizdan oltita qiymatni aniqlang va `~/jdu-lab/p0/observation.env`ga yozing. Bu eski M0 o‘rniga qadamma-qadam P0 mashqidir. Qiymatlarni misoldan yoki boshqa talabadan ko‘chirmang; faqat o‘z serveringizdagi natijalarni oling. Oltita bandni `jdu-check P0` bilan tekshiring.

### Yechim namunasi (qadamma-qadam)

#### 1-bosqich: Server va userni tekshirish

Hujjat boshida aytilganidek, CloudShellda `ssh jdu-ubuntu`ni bajaring. Quyidagi barcha amallar ulangan Ubuntuda bajariladi.

```bash
# Home directoryga o‘ting.
cd ~
# Joriy directoryni ko‘rsating.
pwd
# Joriy user nomini ko‘rsating.
id -un
```

`id -un` natijasi `ssm-user` bo‘lishi kerak. Bu keyin yoziladigan `USER_NAME` qiymati. Keyingi natijalarni o‘zingiz uchun qayd eting.

#### 2-bosqich: OS turi va versiyasini aniqlash

```bash
# OS turi va versiyasini ko‘rsating.
cat /etc/os-release
```

`ID=` qiymatini `OS_ID`, `VERSION_ID=` qiymatini `OS_VERSION_ID` sifatida yozing. Bular `NAME` va `PRETTY_NAME`dan boshqa maydonlar. Agar natijada qo‘shtirnoq bo‘lsa, faqat qiymatni yozing.

#### 3-bosqich: Linux kernel versiyasini aniqlash

```bash
# Linux kernel release raqamini ko‘rsating.
uname -r
```

`-r` `kernel release`ni ko‘rsatadi. Chiqqan butun satrni `KERNEL_RELEASE` sifatida qayd eting. OS versiyasi va `kernel` versiyasi bir xil ma’lumot emas.

#### 4-bosqich: PID 1 process nomini aniqlash

```bash
# PID 1 process nomini ko‘rsating.
cat /proc/1/comm
```

`/proc`da ishlayotgan tizim haqidagi ma’lumotlar mavjud. `1` — `process ID` (PID), `comm` esa shu `process` nomini ko‘rsatadigan `file`. Natijani `PID1_COMM` deb yozing.

#### 5-bosqich: User va hostname qiymatlarini tekshirish

```bash
# Joriy user nomini ko‘rsating.
id -un
# Server hostname qiymatini ko‘rsating.
hostname
```

Birinchi natija `USER_NAME`, ikkinchisi `HOST_NAME`. `Hostname` serverni bildiradi; u `user` nomi yoki natija yuborishga ishlatiladigan Server ID emas.

#### 6-bosqich: Kuzatuv fileini yaratish

```bash
# Home directoryga o‘ting.
cd ~
# P0 ish directorysini yarating.
mkdir -p jdu-lab/p0
# P0 ish directorysiga o‘ting.
cd jdu-lab/p0
# Joriy directoryni ko‘rsating.
pwd
# Kuzatuv fileini tahrirlang.
nano observation.env
```

`nano` ochilgach, quyidagi olti satrni kiriting. Har bir `=` belgisidan o‘ng tomonga o‘z serveringizda aniqlagan qiymatni yozing. Bu `file` mazmuni; uni `command` sifatida bajarmang:

```text
OS_ID=
OS_VERSION_ID=
KERNEL_RELEASE=
PID1_COMM=
USER_NAME=
HOST_NAME=
```

Har bir nom bitta satrda bo‘lsin. `=` atrofida bo‘sh joy va qiymat atrofida qo‘shtirnoq bo‘lmasin. `Ctrl+O` bilan saqlang, `observation.env` nomini `Enter` bilan tasdiqlang, so‘ng `Ctrl+X` bilan chiqing.

#### 7-bosqich: Saqlangan fileni tekshirish

```bash
# Joriy directoryni ko‘rsating.
pwd
# Kuzatuv filei mavjudligi va permissionini tekshiring.
ls -l observation.env
# Yozib olingan oltita maydonni ko‘rsating.
cat observation.env
```

Olti satrning hammasida 1–5-bosqichlarda olingan qiymatlar bo‘lsin. Bo‘sh yoki noto‘g‘ri qiymatni `nano observation.env` bilan tuzatib, qayta saqlang.

#### 8-bosqich: Baholash va topshirish

```bash
# Baholash qaysi user bilan bajarilishini tekshiring.
id -un
# P0 bajarilganini baholang.
jdu-check P0
```

Oltita `PASS` va `6 / 6 checks cleared` P0 tugaganini bildiradi. `FAIL` bo‘lsa, ko‘rsatilgan bandni o‘z serveringizda qayta aniqlang, `file`ni tuzating va baholashni takrorlang.

`RESULT` — topshiriq bahosi, `REPORT` — o‘qituvchiga yuborish natijasi. Yuborish ishlamasa, `file`ni o‘chirmang va mashqni `reset` qilmang. Ulanish hamda ro‘yxatdan o‘tishni tekshirib, yana urinib ko‘ring.

#### 9-bosqich: Keyingi mashqqa o‘tish

```bash
# Keyingi mashqdan oldin home directoryga qayting.
cd ~
```

P1ga o‘ting. CloudShellga qaytmoqchi bo‘lsangizgina `exit`ni bajaring. P0ni birinchi marta bajarishda `reset` kerak emas. Yozuvni o‘chirib qayta boshlash kerak bo‘lsagina Ubuntuda `jdu-reset P0`ni bajaring.

## P1 Shell, path, file, text

### O‘rganiladigan ko‘nikmalar

- `home directory` va ish `directory`sini ajratish.
- `directory` yaratish.
- `file`dan nusxa olish.
- `log`dan kerakli satrlarni saqlash.

### Topshiriq

`~/jdu-lab/p1/inbox`da sozlama `file`i va `log` bor. `~/jdu-lab/p1/practice01` hali tayyor emas, unda keraksiz `.tmp` `file`lar qolgan. Quyidagi holatga keltiring:

1. `practice01` ichida `config`, `logs`, `notes` `directory`larini yarating.
2. `inbox/config/training.conf`ni `practice01/config/training.conf`ga, `inbox/logs/practice.log`ni `practice01/logs/practice.log`ga ko‘chiring. Manba va nusxa mazmunini o‘zgartirmang.
3. `practice01` ostidagi barcha `.tmp` `file`larni o‘chiring. Boshqa `file`larni o‘chirmang.
4. Tayyor `practice01` ichidagi `directory` va `file`larning egasi Ubuntu boshqaruv `user`i `ssm-user` bo‘lsin.
5. Nusxa olingan `log`dagi `WARN` bor satrlarnigina satr raqamisiz `practice01/notes/warnings.txt`ga yozing.
6. Shu `log`ning oxirgi to‘rt satrini asl tartibda `practice01/notes/recent.txt`ga yozing.

Tayyor holatni `jdu-check P1` bilan tekshiring. Olti bandning hammasi `PASS` bo‘lsa, mashq tugaydi.

### Yechim namunasi (qadamma-qadam)

#### 1-bosqich: Home directoryga o‘tish

```bash
# Home directoryga o‘ting.
cd ~
# Joriy directoryni ko‘rsating.
pwd
```

Natija `/home/ssm-user` bo‘lsin.

#### 2-bosqich: P1 directorysiga o‘tish

```bash
# P1 ish directorysiga o‘ting.
cd ~/jdu-lab/p1
# Joriy directoryni ko‘rsating.
pwd
# Asl filelar va tugallanmagan topshirish joyini daraxt shaklida ko‘rsating.
tree
```

`inbox` va hali tugallanmagan `practice01`ni toping.

#### 3-bosqich: Kerakli directorylarni yaratish

```bash
# P1 ish directorysiga o‘ting.
cd ~/jdu-lab/p1
# Config file uchun directory yarating.
mkdir -p practice01/config
# Log uchun directory yarating.
mkdir -p practice01/logs
# Natija filei uchun directory yarating.
mkdir -p practice01/notes
# Yaratilgan tuzilishni ko‘rsating.
tree practice01
```

#### 4-bosqich: Config filedan nusxa olish

Nusxa joylashtiriladigan `directory`ga o‘ting.

```bash
# Config nusxasi joylashgan directoryga o‘ting.
cd ~/jdu-lab/p1/practice01/config
# Joriy directoryni tekshiring.
pwd
# Asl config fileni joriy directoryga nusxalang.
cp ../../inbox/config/training.conf .
# Nusxalangan fileni ko‘rsating.
ls -l
```

`.` hozirgi `directory`ni anglatadi.

#### 5-bosqich: Log filedan nusxa olish

```bash
# Log nusxasi joylashgan directoryga o‘ting.
cd ~/jdu-lab/p1/practice01/logs
# Joriy directoryni tekshiring.
pwd
# Asl logni joriy directoryga nusxalang.
cp ../../inbox/logs/practice.log .
# Nusxalangan fileni ko‘rsating.
ls -l
```

#### 6-bosqich: Vaqtinchalik filelarni topib o‘chirish

`practice01`ga o‘ting va o‘chirishdan oldin tuzilmani ko‘ring:

```bash
# Yakunlash kerak bo‘lgan directoryga o‘ting.
cd ~/jdu-lab/p1/practice01
# Joriy directoryni tekshiring.
pwd
# O‘chirishdan oldingi file tuzilishini ko‘rsating.
tree
```

`staging` ichidan `training.conf.tmp` va `practice.log.tmp`ni toping. So‘ng shu ikki `file`ni shart bilan qidiring:

```bash
# Joriy directory va uning ichidagi faqat .tmp filelarni qidiring.
find . -type f -name '*.tmp' -print
```

`.` — qidirish boshlanadigan joy; `-type f` faqat oddiy `file`larni, `-name '*.tmp'` nomi `.tmp` bilan tugaydiganlarni tanlaydi; `-print` topilgan `path`larni ko‘rsatadi. Qo‘shtirnoq `*.tmp`ni `shell` oldindan kengaytirib yubormasligi uchun kerak. Natijani `tree` bilan solishtiring. Faqat ikki keraksiz `file` ekanini aniqlagach, aynan ularning `path`ini ko‘rsatib o‘chiring:

```bash
# Tekshirilgan ikkita keraksiz vaqtinchalik fileni o‘chiring.
rm staging/training.conf.tmp staging/practice.log.tmp
# O‘chirishdan keyingi tuzilishni tekshiring.
tree
```

Ikki `.tmp` ko‘rinmaydi, lekin `config/training.conf` va `logs/practice.log` saqlanadi.

#### 7-bosqich: WARN bor satrlarni saqlash

Natija yoziladigan `notes`ga o‘ting:

```bash
# Natija filei directorysiga o‘ting.
cd ~/jdu-lab/p1/practice01/notes
# Joriy directoryni tekshiring.
pwd
# Logdagi WARN bor satrlarni ekranda ko‘rsating.
grep 'WARN' ../logs/practice.log
```

Faqat `WARN` bor satrlar ko‘ringanini tekshiring. Endi `>` qo‘shib, shu natijani `file`ga yozing. `>` natijani ekrandan `file`ga yo‘naltiradi; mavjud mazmunni qayta yozadi:

```bash
# WARN satrlarini warnings.txt fileiga saqlang.
grep 'WARN' ../logs/practice.log > warnings.txt
# Saqlangan natijani ko‘rsating.
cat warnings.txt
```

Saqlangan satrlarni oldin ekranda ko‘ringan satrlar bilan solishtiring.

#### 8-bosqich: Oxirgi to‘rt satrni saqlash

```bash
# Natija filei directorysiga o‘ting.
cd ~/jdu-lab/p1/practice01/notes
# Logning oxirgi to‘rt satrini ekranda ko‘rsating.
tail -n 4 ../logs/practice.log
```

Oxirgi to‘rt satr asl tartibda ko‘ringanini tekshiring. So‘ng aynan shu natijani saqlang:

```bash
# Oxirgi to‘rt satrni recent.txt fileiga saqlang.
tail -n 4 ../logs/practice.log > recent.txt
# Saqlangan natijani ko‘rsating.
cat recent.txt
```

Saqlangan to‘rt satrni `cat` bilan tekshiring.

#### 9-bosqich: Barcha natijani tekshirish

```bash
# P1 ish directorysiga qayting.
cd ~/jdu-lab/p1
# Tayyor directory tuzilishini ko‘rsating.
tree practice01
# P1 bajarilganini baholang.
jdu-check P1
```

Barcha 6 band `PASS` bo‘lsa, M1ga o‘ting.

## P2 User, group, permission, setgid

### O‘rganiladigan ko‘nikmalar

- `primary group` va `supplementary group`ni tekshirish.
- Umumiy `directory`ga `group permission` qo‘yish.
- `setgid` yordamida yangi `file`ning `group`ini meros qildirish.

### Topshiriq

`/srv/jdu-practice-share` umumiy `directory`sida yozuvchi va o‘quvchi huquqlarini ajrating. Dastlab `jdupracticeviewer` noto‘g‘ri ravishda `practiceops` `supplementary group`iga kirgan, `jdupracticewriter` esa kirmagan. `Directory` va `GUIDE.txt`ning egasi, `group`i va `permission`i ham tayyor emas.

1. `jdupracticewriter`ni `practiceops` `supplementary group`iga qo‘shing, `jdupracticeviewer`ni undan chiqaring.
2. `/srv/jdu-practice-share` egasi va `group`ini `root:practiceops`, `mode`ini `2775` qiling. Yangi `file`lar `directory group`ini meros qilsin.
3. `GUIDE.txt` egasi va `group`ini `root:practiceops`, `mode`ini `664` qiling.
4. `ssm-user`dan `jdupracticewriter`ga o‘tib, umumiy `directory`da `writer-created.txt` yarating. Yangi `file` `group`i `practiceops` ekanini tekshiring.
5. `ssm-user`ga qaytib, `jdupracticeviewer`ga o‘ting. `GUIDE.txt`ni o‘qish mumkin, lekin umumiy `directory`da yangi `file` yaratish mumkin emasligini tekshiring.

Boshqa `user` bilan amallar tugagach, `ssm-user`ga qayting va `jdu-check P2`ni bajaring. Oltita baho `group` a’zoligi, `directory`, `file`, `group` merosi va o‘quvchi huquqiga tegishli.

### Yechim namunasi (qadamma-qadam)

#### 1-bosqich: Boshqaruv userini tekshirish

```bash
# Home directoryga o‘ting.
cd ~
# Joriy user nomini ko‘rsating.
id -un
# Joriy user ID va tegishli grouplarni ko‘rsating.
id
```

#### 2-bosqich: Boshlang‘ich groupni tekshirish

```bash
# Umumiy group yozuvini ko‘rsating.
getent group practiceops
# Writer user tegishli grouplarni tekshiring.
id jdupracticewriter
# Viewer user tegishli grouplarni tekshiring.
id jdupracticeviewer
```

Dastlab `jdupracticeviewer` `practiceops` a’zosi, `jdupracticewriter` esa a’zo emas.

#### 3-bosqich: Group a’zoligini to‘g‘rilash

```bash
# Home directoryga o‘ting.
cd ~
# Writer userni umumiy groupga qo‘shing.
sudo usermod -aG practiceops jdupracticewriter
# Viewer userni umumiy groupdan chiqaring.
sudo gpasswd -d jdupracticeviewer practiceops
# O‘zgarishdan keyingi umumiy groupni ko‘rsating.
getent group practiceops
# Writer userning group a’zoligini tekshiring.
id jdupracticewriter
# Viewer userning group a’zoligini tekshiring.
id jdupracticeviewer
```

#### 4-bosqich: Umumiy directoryni sozlash

```bash
# /srv directorysiga o‘ting.
cd /srv
# Joriy directoryni ko‘rsating.
pwd
# Umumiy directoryning boshlang‘ich permissionini ko‘rsating.
ls -ld jdu-practice-share
```

O‘zgartirishdan oldin `directory`ning `permission`i, egasi va `group`ini ko‘ring. `ls -ld`dagi `-d` `directory`ning ichidagilarni emas, aynan o‘zini ko‘rsatadi. Avval `permission`, havola sonidan keyin esa ega va `group` chiqadi.

```bash
# Umumiy directory owner va group qiymatini o‘zgartiring.
sudo chown root:practiceops jdu-practice-share
# Owner va group o‘zgarganini tekshiring.
ls -ld jdu-practice-share
# Group merosini o‘z ichiga olgan 2775 permissionni o‘rnating.
sudo chmod 2775 jdu-practice-share
# setgid uchun s belgisi va permission qiymatini tekshiring.
ls -ld jdu-practice-share
```

`chown`dan keyin ega va `group` `root practiceops`, `chmod`dan keyin `permission` `drwxrwsr-x` bo‘lsin. `Group`ning bajarish joyidagi `s` — setgid; shu `directory`da yaratilgan yangi `file` uning `group`ini oladi.

#### 5-bosqich: GUIDE.txtni sozlash

Kerakli `directory`ga o‘ting:

```bash
# Umumiy directoryga o‘ting.
cd /srv/jdu-practice-share
# Joriy directoryni ko‘rsating.
pwd
# GUIDE.txtning boshlang‘ich permission qiymatini ko‘rsating.
ls -l GUIDE.txt
```

Avval `file`ning boshlang‘ich `permission`i, egasi va `group`ini ko‘ring:

```bash
# GUIDE.txt owner va group qiymatlarini o‘zgartiring.
sudo chown root:practiceops GUIDE.txt
# Owner va groupni tekshiring.
ls -l GUIDE.txt
# Owner va groupga o‘qish hamda yozish huquqini bering.
sudo chmod 664 GUIDE.txt
# Filening yakuniy permissionini tekshiring.
ls -l GUIDE.txt
```

Yakuniy natija `root practiceops` va `-rw-rw-r--`. Ega va `group` o‘qib-yozadi, boshqa `user`lar faqat o‘qiydi.

#### 6-bosqich: Writerga o‘tib file yaratish

```bash
# Home directoryga qayting.
cd ~
# Writer user shelliga o‘ting.
sudo su - jdupracticewriter
# Almashgandan keyingi user nomini tekshiring.
id -un
# Almashgandan keyingi grouplarni tekshiring.
id
# Umumiy directoryga o‘ting.
cd /srv/jdu-practice-share
# Joriy directoryni tekshiring.
pwd
# Writer user sifatida file yarating.
printf '%s\n' 'guided writer file' > writer-created.txt
# Yaratilgan filening owner groupini tekshiring.
ls -l writer-created.txt
# Writer user shellidan chiqing.
exit
# Boshqaruvchi userga qaytganingizni tekshiring.
id -un
```

Oxirgi natija `ssm-user` bo‘lsin.

#### 7-bosqich: Viewerning o‘qish va yozishini tekshirish

```bash
# Home directoryga qayting.
cd ~
# Viewer user shelliga o‘ting.
sudo su - jdupracticeviewer
# Almashgandan keyingi user nomini tekshiring.
id -un
# Viewer user tegishli grouplarni tekshiring.
id
# Umumiy directoryga o‘ting.
cd /srv/jdu-practice-share
# Joriy directoryni tekshiring.
pwd
# GUIDE.txtni viewer user sifatida o‘qing.
cat GUIDE.txt
# Yozish rad etilishini tekshiring.
touch viewer-created.txt
# Viewer user shellidan chiqing.
exit
# Boshqaruvchi userga qaytganingizni tekshiring.
id -un
```

`cat` muvaffaqiyatli ishlaydi. `touch` `Permission denied` beradi. Bu kutilgan rad etish.

`jdupracticeviewer` `root` egasi emas va `practiceops`dan chiqarilgan, shuning uchun unga «boshqalar» `permission`i qo‘llanadi. `GUIDE.txt`da bu o‘qishga (`r--`) ruxsat beradi. `Directory`da esa `r-x` bor, lekin yozish (`w`) yo‘q. Yangi `file` yaratish uchun `directory`da yozish va o‘tish (`x`) huquqi kerak; shu sabab `touch` rad etiladi.

#### 8-bosqich: Baholash

```bash
# Home directoryga qayting.
cd ~
# Baholashdan oldin user nomini tekshiring.
id -un
# P2 bajarilganini baholang.
jdu-check P2
```

Barcha 6 band `PASS` bo‘lsa, M2ga o‘ting.

## P3 Process va package

8-bobdan keyin 1–4-bosqichlarda `process`ni tekshirib, `service`ni to‘xtating. 9-bobni o‘qib, 5-bosqichda `package`ni o‘rnating.

### O‘rganiladigan ko‘nikmalar

- `systemd service` va `process` PIDini bog‘lash.
- Main PIDni `ps` bilan tekshirish va kerakli `service`ni to‘xtatish.
- `apt` bilan `package` o‘rnatish.

### Topshiriq

Boshlang‘ich holatda `jdu-p3-process1.service`, `jdu-p3-process2.service` va `jdu-p3-process3.service` ishlayapti. `figlet` `package`i o‘rnatilmagan. A va Bni bajaring.

**Topshiriq A — faqat process2ni to‘xtatish.** `jdu-p3-process2.service` Main PIDini aniqlang va shu PIDdagi `process`ni `ps` bilan tekshiring. `systemctl stop` orqali `service`ni to‘xtating. Faqat `process2` to‘xtasin; `process1` va `process3` ishlashda davom etsin.

**Topshiriq B — package o‘rnatish.** `figlet` ma’lumotini ko‘ring, `apt` bilan o‘rnating va `command`ni bir marta bajaring.

`jdu-check P3` A va Bni bittadan band sifatida baholaydi, jami ikkita. `Command history` yoki yozgan eslatmangiz topshirilmaydi.

### Yechim namunasi (qadamma-qadam)

#### 1-bosqich: Uchta serviceni tekshirish

```bash
# Home directoryga o‘ting.
cd ~
# P3 servicelar ro‘yxatini ko‘rsating.
systemctl list-units --type=service 'jdu-p3-*'
# process1 holatini ko‘rsating.
systemctl status jdu-p3-process1.service --no-pager
# process3 holatini ko‘rsating.
systemctl status jdu-p3-process3.service --no-pager
```

#### 2-bosqich: Process2 Main PIDini o‘qish

```bash
# process2 holati va Main PID qiymatini ko‘rsating.
systemctl status jdu-p3-process2.service
```

`Main PID:` o‘ngidagi raqamni o‘zingiz uchun yozib oling. `Pager` ochilsa, `q` bilan chiqing.

#### 3-bosqich: Yozib olingan PIDdagi processni tekshirish

Masalan, yozib olgan raqam `1234` bo‘lsa, quyidagi `command`da `1234`ni o‘z raqamingizga almashtiring:

```bash
# Yozib olgan PID processini ko‘rsating; 1234 o‘rniga o‘z qiymatingizni qo‘ying.
ps -fp 1234
```

`PID`, `USER` va `CMD`ni tekshiring.

#### 4-bosqich: Process2 serviceni to‘xtatish

```bash
# process2 serviceni to‘xtating.
sudo systemctl stop jdu-p3-process2.service
# process1 ishlayotganini tekshiring.
systemctl is-active jdu-p3-process1.service
# process2 to‘xtaganini tekshiring.
systemctl is-active jdu-p3-process2.service
# process3 ishlayotganini tekshiring.
systemctl is-active jdu-p3-process3.service
```

Tartib bilan `active`, `inactive`, `active` chiqishi kerak.

#### 5-bosqich: Figletni tekshirib o‘rnatish

```bash
# Home directoryga o‘ting.
cd ~
# figlet package ma’lumotini o‘qing.
apt show figlet
# Mavjud packagelar ro‘yxatini yangilang.
sudo apt update
# figletni o‘rnating.
sudo apt install -y figlet
# figlet command joylashuvini tekshiring.
command -v figlet
# figletni bir marta ishga tushiring.
figlet JDU
# P3 bajarilganini baholang.
jdu-check P3
```

`figlet JDU` yozuv chiqarib, o‘zi tugaydi. `jdu-check P3` ikkala topshiriqni bittadan band sifatida baholaydi.

Ikkala band `PASS` bo‘lsa, M3ga o‘ting.

## P4 systemd service

### O‘rganiladigan ko‘nikmalar

- `unit file`ni o‘qish.
- `active` va `enabled` holatlarini alohida sozlash.
- `Unit` sozlamalaridagi `User`, `WorkingDirectory` va `ExecStart`ni o‘qish.

### Topshiriq

`jdu-practice-status.service` `unit file`i tayyor, lekin `service` to‘xtagan va avtomatik ishga tushish o‘chirilgan. `Unit file`ni o‘zgartirmasdan:

1. `User`, `WorkingDirectory` va `ExecStart`ni o‘qing.
2. `Service`ni ishga tushiring va hozir `active` ekanini tekshiring.
3. Avtomatik ishga tushishni yoqing va `enabled` ekanini tekshiring. Bu `active`dan alohida holat.

`jdu-check P4` o‘zgarmagan `unit`ning ishlashi va avtomatik ishga tushishini ikkita bandda baholaydi. Kuzatuv natijasini alohida `file` sifatida topshirmang.

### Yechim namunasi (qadamma-qadam)

#### 1-bosqich: Unit fileni o‘qish

```bash
# Home directoryga o‘ting.
cd ~
# Service unit sozlamasini ko‘rsating.
systemctl cat jdu-practice-status.service
```

`User`, `WorkingDirectory`, `ExecStart`ni tekshiring.

#### 2-bosqich: Dastlabki holatni tekshirish

```bash
# Service hozir ishlayotganini tekshiring.
systemctl is-active jdu-practice-status.service
# Boot paytidagi avtomatik ishga tushish yoqilganini tekshiring.
systemctl is-enabled jdu-practice-status.service
```

#### 3-bosqich: Serviceni start qilish

```bash
# Serviceni hozir ishga tushiring.
sudo systemctl start jdu-practice-status.service
# Servicening joriy holatini tekshiring.
systemctl is-active jdu-practice-status.service
```

#### 4-bosqich: Tizim yoqilganda start qilishni sozlash

```bash
# Boot paytidagi avtomatik ishga tushishni yoqing.
sudo systemctl enable jdu-practice-status.service
# Avtomatik ishga tushish sozlamasini tekshiring.
systemctl is-enabled jdu-practice-status.service
```

#### 5-bosqich: Baholash

```bash
# Home directoryga o‘ting.
cd ~
# P4 bajarilganini baholang.
jdu-check P4
```

Ikkala band `PASS` bo‘lsa, M4ga o‘ting.

## P5 Port, socket, HTTP, journal

### O‘rganiladigan ko‘nikmalar

- `service`, `process` va `listening socket`ni bog‘lash.
- IP address va `port`ni o‘qish.
- HTTP `request` `journal`da qayd etilishini tekshirish.

### Topshiriq

`jdu-practice-web.service` to‘xtagan. `Unit file`ni o‘zgartirmang. Quyidagi bog‘lanishni yarating va tekshiring:

1. `Unit file`dan `service user`, chiqariladigan `file path`, IP address va `port`ni aniqlang. `Service`ni ishga tushiring.
2. `127.0.0.1:8181`da kutayotgan `socket`ni toping. Uning PIDini `service` Main PIDi bilan solishtiring. Barcha manzillarda kutishga o‘zgartirmang.
3. `http://127.0.0.1:8181/`ga `request` yuborib, HTTP 200 va javob mazmunini ko‘ring. `Service user` `/srv/jdu-practice-web/index.txt`ni o‘qiy olishini ham tekshiring.
4. `http://127.0.0.1:8181/p5-check`ga o‘zingiz `request` yuboring. `Service`ning joriy ishga tushishiga tegishli `journal`da `REQUEST path=/p5-check` yozuvi paydo bo‘lsin.
5. `18181` `port`ida `listener` yo‘qligini tekshirib, ishlayotgan `8181` bilan solishtiring.

`jdu-check P5` to‘rtta bandni baholaydi: `socket`, HTTP va `file access`, `request log`i hamda ochiq-yopiq `port`lar farqi.

### Yechim namunasi (qadamma-qadam)

#### 1-bosqich: Unit fileni o‘qish

```bash
# Home directoryga o‘ting.
cd ~
# Web service unit sozlamasini ko‘rsating.
systemctl cat jdu-practice-web.service
```

`127.0.0.1`, `8181`, `jdupracticeweb` va kontent `file`i `path`ini tekshiring.

#### 2-bosqich: Serviceni start qilish

```bash
# Web serviceni hozir ishga tushiring.
sudo systemctl start jdu-practice-web.service
# Service ishlayotganini tekshiring.
systemctl is-active jdu-practice-web.service
```

#### 3-bosqich: Listening socketni tekshirish

```bash
# 8181-portning listening address va PID qiymatini ko‘rsating.
sudo ss -lntp | grep ':8181'
```

`127.0.0.1:8181`ni toping. Shu chiqishda `0.0.0.0:8181` yoki `[::]:8181`da kutish yo‘qligini ham tekshiring. Birinchisi faqat shu `host` ichidan ulanishni, keyingilari barcha manzillarda kutishni bildiradi.

#### 4-bosqich: Socket PID va Main PIDni solishtirish

```bash
# Service holatini ko‘rsating va Main PID raqamini o‘qing.
systemctl status jdu-practice-web.service --no-pager
# 8181-portni tinglayotgan processning pid= qiymatini o‘qing.
sudo ss -lntp | grep ':8181'
```

`systemctl status`dagi `Main PID:` raqamini `ss` natijasining `users:` qatoridagi `pid=` bilan solishtiring. Teng bo‘lsa, `service`ning asosiy `process`i 8181 `port`ida kutmoqda.

#### 5-bosqich: HTTP responseni tekshirish

```bash
# HTTP response header va body qismlarini ko‘rsating.
curl -i http://127.0.0.1:8181/
```

#### 6-bosqich: Service userning o‘qish huquqini tekshirish

Kontent `directory`siga o‘ting:

```bash
# Ochiq file joylashgan directoryga o‘ting.
cd /srv/jdu-practice-web
# Joriy directoryni ko‘rsating.
pwd
# File yo‘lidagi har bir directory permissionini ko‘rsating.
ls -ld /srv /srv/jdu-practice-web
# Ochiq filening owner, group va permission qiymatlarini ko‘rsating.
ls -l index.txt
# Service user tegishli grouplarni ko‘rsating.
id jdupracticeweb
# Service userning login shell qiymatini ko‘rsating.
getent passwd jdupracticeweb
# Fileni service user huquqi bilan faqat shu buyruq uchun o‘qing.
sudo -u jdupracticeweb -- cat index.txt
```

`ls -ld` har bir `directory`ning, `ls -l` esa `index.txt`ning egasi, `group`i va `permission`ini ko‘rsatadi. `File`ni o‘qish uchun uning `read permission`i va har bir yuqori `directory`dan o‘tish (`x`) huquqi kerak. `id` `service user` `group`larini, `getent passwd` uning login `shell`ini ko‘rsatadi.

`sudo -u jdupracticeweb -- cat index.txt` `cat`ni faqat bir marta `jdupracticeweb` huquqi bilan bajaradi. `--` `sudo` opsiyalari tugaganini bildiradi. Mazmun chiqsa, o‘qish mumkin. Bu `service user`ning `shell`i `/usr/sbin/nologin`; shuning uchun interaktiv `su -` ishlatmang.

#### 7-bosqich: Talaba requestini yuborish

```bash
# Ko‘rsatilgan pathga HTTP request yuboring.
curl -i http://127.0.0.1:8181/p5-check
# Servicening so‘nggi journal yozuvlarini ko‘rsating.
sudo journalctl -u jdu-practice-web.service --no-pager -n 20
```

`REQUEST path=/p5-check`ni toping.

#### 8-bosqich: Closed port bilan solishtirish

```bash
# Listening socket yo‘q 18181-portga ulanishni sinang.
curl --max-time 2 http://127.0.0.1:18181/
# 18181-portda listening socket yo‘qligini tekshiring.
sudo ss -lnt | grep ':18181'
```

Ikkalasi ham muvaffaqiyatli chiqmaydi. TCP 18181da kutayotgan `socket` yo‘q.

#### 9-bosqich: Baholash

```bash
# Home directoryga o‘ting.
cd ~
# P5 bajarilganini baholang.
jdu-check P5
```

To‘rttala band `PASS` bo‘lsa, M5ga o‘ting.

## P6 SSH, remote command, scp

### O‘rganiladigan ko‘nikmalar

- CloudShell va Ubuntuni farqlash.
- `scp` bilan `upload` va `download` qilish.
- SSH `remote command`ini bajarish.

### Topshiriq

CloudShellni ulanish boshlanadigan tomon, Ubuntuni esa uzoqdagi tomon deb oling. SSH sozlamasi va `jdu-ubuntu` ulanish nomi tayyor. P6 `file`lari hali mavjud emas.

Uzoqdagi serverda yaratiladigan natija `file`i quyidagi uch satrdan iborat bo‘lsin. `=` o‘ngidagi qiymatlarni taxmin qilib qo‘lda yozmang; haqiqiy `command` natijalaridan oling:

```text
REMOTE_USER=haqiqiy user nomi
REMOTE_HOST=haqiqiy hostname
REMOTE_PATH=haqiqiy home directory
```

1. CloudShelldagi `~/jdu-lab/p6/practice-source.txt`ga faqat `JDU SSH guided transfer` satrini yozing.
2. `scp` bilan uni Ubuntuga `~/jdu-lab/p6/practice-upload.txt` sifatida yuboring. Yuborishdan oldingi va keyingi SHA-256ni solishtiring.
3. CloudShelldan SSH `remote command`ni bajaring. Ubuntu haqidagi haqiqiy uch qiymatni yuqoridagi shaklda `~/jdu-lab/p6/practice-remote-result.txt`ga yozing.
4. Ubuntuga ulanib, `jdu-check P6`ni bajaring. Ubuntu tomonidagi ikki band `PASS` bo‘lsin.
5. Natija `file`ini `scp` bilan CloudShellga `~/jdu-lab/p6/practice-downloaded-result.txt` sifatida qaytaring. Ikkala tomondagi SHA-256ni solishtiring.
6. CloudShellda `jdu-check P6`ni bajaring. CloudShell tomonidagi to‘rt band `PASS` bo‘lsin.

P6 Ubuntu `2/2` va CloudShell `4/4` bo‘lganda tugaydi. O‘qituvchi progress sahifasi ham ikki tomonni alohida ko‘rsatadi.

### Yechim namunasi (qadamma-qadam)

#### 1-bosqich: Ubuntudan CloudShellga qaytish

Ubuntu `prompt`ida bajaring:

```bash
# Ubuntu SSH sessiyasini yakunlab, CloudShellga qayting.
exit
```

CloudShellda qayerda ekaningizni tekshiring:

```bash
# CloudShell home directorysiga o‘ting.
cd ~
# CloudShelldagi joriy directoryni ko‘rsating.
pwd
# CloudShell user nomini ko‘rsating.
id -un
# CloudShell hostname qiymatini ko‘rsating.
hostname
```

#### 2-bosqich: CloudShelldagi ish directorysini yaratish

```bash
# CloudShellda P6 ish directorysini yarating.
mkdir -p ~/jdu-lab/p6
# CloudShelldagi P6 directorysiga o‘ting.
cd ~/jdu-lab/p6
# Joriy directoryni tekshiring.
pwd
```

#### 3-bosqich: Upload manbasi bo‘lgan fileni yaratish

```bash
# Manba filega ko‘rsatilgan bitta satrni yozing.
printf '%s\n' 'JDU SSH guided transfer' > practice-source.txt
# Manba file mazmunini ko‘rsating.
cat practice-source.txt
# Ko‘chirishdan oldingi SHA-256 qiymatini ko‘rsating.
sha256sum practice-source.txt
```

#### 4-bosqich: Ubuntudagi directoryni yaratish

CloudShellda bajaring:

```bash
# SSH orqali Ubuntu tomonidagi P6 directorysini yarating.
ssh jdu-ubuntu 'mkdir -p ~/jdu-lab/p6'
```

#### 5-bosqich: Ubuntuga upload qilish

CloudShell P6 `directory`sidan bajaring:

```bash
# CloudShelldagi P6 directorysiga o‘ting.
cd ~/jdu-lab/p6
# scp yordamida fileni CloudShelldan Ubuntuga yuboring.
scp practice-source.txt jdu-ubuntu:~/jdu-lab/p6/practice-upload.txt
# Ubuntuda qabul qilingan filening SHA-256 qiymatini ko‘rsating.
ssh jdu-ubuntu 'sha256sum ~/jdu-lab/p6/practice-upload.txt'
# CloudShelldagi manba filening SHA-256 qiymatini ko‘rsating.
sha256sum practice-source.txt
```

Ikki SHA-256 qiymati bir xil bo‘lsin.

#### 6-bosqich: SSH remote command bilan natija fileni yaratish

CloudShellda quyidagi bitta `command`ni aynan ko‘rsatilgandek bajaring:

```bash
# Ubuntudagi uchta haqiqiy qiymatni natija fileiga saqlang.
ssh jdu-ubuntu 'cd ~/jdu-lab/p6 && printf "REMOTE_USER=%s\nREMOTE_HOST=%s\nREMOTE_PATH=%s\n" "$(id -un)" "$(hostname)" "$HOME" > practice-remote-result.txt'
```

Mazmunni `remote`da tekshiring:

```bash
# SSH orqali Ubuntudagi natija fileni ko‘rsating.
ssh jdu-ubuntu 'cat ~/jdu-lab/p6/practice-remote-result.txt'
```

#### 7-bosqich: Ubuntu tomonini baholash

Ubuntuga ulanib bajaring:

```bash
# CloudShelldan Ubuntuga ulaning.
ssh jdu-ubuntu
# Ubuntudagi P6 directorysiga o‘ting.
cd ~/jdu-lab/p6
# Ubuntudagi joriy directoryni ko‘rsating.
pwd
# Ko‘chirilgan file va natija fileni tekshiring.
ls -l
# Ubuntu tomonidagi P6ni baholang.
jdu-check P6
# Ubuntu SSH sessiyasini yakunlab, CloudShellga qayting.
exit
```

Ubuntu tomondagi ikkala band `PASS` bo‘lsin.

#### 8-bosqich: Natija fileni download qilish

CloudShellda bajaring:

```bash
# CloudShelldagi P6 directorysiga o‘ting.
cd ~/jdu-lab/p6
# scp yordamida natija fileni Ubuntudan CloudShellga qaytaring.
scp jdu-ubuntu:~/jdu-lab/p6/practice-remote-result.txt practice-downloaded-result.txt
# Yuklab olingan file mazmunini ko‘rsating.
cat practice-downloaded-result.txt
# CloudShelldagi yuklab olingan filening SHA-256 qiymatini ko‘rsating.
sha256sum practice-downloaded-result.txt
# Ubuntudagi manba filening SHA-256 qiymatini ko‘rsating.
ssh jdu-ubuntu 'sha256sum ~/jdu-lab/p6/practice-remote-result.txt'
```

Ikki SHA-256 qiymati bir xil bo‘lsin.

#### 9-bosqich: CloudShell tomonini baholash

```bash
# CloudShelldagi P6 directorysiga o‘ting.
cd ~/jdu-lab/p6
# CloudShell tomonidagi P6ni baholang.
jdu-check P6
```

CloudShell tomondagi to‘rtala band `PASS` bo‘lsa, M6ga o‘ting.

## O‘rganish tartibi

Kitobdagi boblar dars soatlari bilan birma-bir mos emas. Tushungan joyingizdan mashqqa o‘ting, zarur bo‘lsa bobga qayting.

- 1–3-boblar va 4-bobning tahrirlash asoslarini o‘qing. Keyin P0 qadamlari bilan haqiqiy OSni kuzating.
- 4–5-boblarni o‘qib P1, M1ga o‘ting.
- 6–7-boblarni o‘qib P2, M2ga o‘ting.
- 8-bobni o‘qib P3ning 1–4-bosqichlarini bajaring. 9-bobni o‘qib P3ning 5-bosqichini bajaring. Keyin M3ga o‘ting.
- 10-bobdan keyin P4, M4; 11-bobdan keyin P5, M5ga o‘ting.
- 12-bobdan keyin P6, M6ga o‘ting. Avvalgi ko‘nikmalarni birlashtirib M7ni bajaring.

Umumiy tavsiya etilgan tartib:

```text
P0 → P1 → M1 → P2 → M2 → P3 → M3 → P4 → M4
   → P5 → M5 → P6 → M6 → M7 (yakuniy topshiriq)
```

Pda avval mustaqil urinib, keyin yechimga qarashingiz yoki boshidan namuna bo‘yicha ishlashingiz mumkin. M1–M6da P bosqichlariga qaramay, kerakli `command`larni o‘zingiz tanlang. M7da M2, M4 va M5dagi bilimlarni birlashtiring.
