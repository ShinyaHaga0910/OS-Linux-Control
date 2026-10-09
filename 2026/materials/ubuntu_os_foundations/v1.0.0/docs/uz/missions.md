# Ubuntu and OS Foundations — mustaqil topshiriqlar: Mission Guide

[日本語](../ja/missions.md) · [Русский](../ru/missions.md) · [O‘zbekcha](../uz/missions.md)

> ChatGPT tarjimasi joriy yaponcha manbaga moslashtirilgan. Ona tilida gapiruvchi mutaxassis hali tekshirmagan; baholash shartlari farq qilsa, yaponcha asl matnga tayaning.

Qamrov: Mission 1–7. Muhit: Ubuntu Server 24.04 LTS. Har bir talaba Missionlarni o‘z sur’atida bajaradi; ular dars soatlariga birma-bir bog‘lanmagan.

Bu hujjat `command`ni talaba o‘zi tanlaydigan M1–M7 topshiriqlaridir. To‘liq, qadamma-qadam ko‘rsatma kerak bo‘lsa, avval [P0–P6 mashqlarini](practice.md) bajaring.

P va M alohida resurslardan foydalanadi. P tugagani tegishli M avtomatik `PASS` bo‘lishini anglatmaydi. Tavsiya etilgan tartib: `P0 → P1 → M1 → P2 → M2 → … → P6 → M6 → M7`. Eski M0 qadamma-qadam P0 mashqiga ko‘chirildi. Yakuniy M7 uchun alohida P yo‘q.

## Avval Ubuntuga ulaning

AWS Academy Learner Lab dastlabki sozlamalari tugagach, AWS konsolida CloudShellni oching. O‘z Ubuntu mashq serveringizga quyidagicha ulaning:

```bash
ssh jdu-ubuntu
```

Ulangach, Ubuntuda `user` nomini tekshiring:

```bash
id -un
```

Natija `ssm-user` bo‘lishi kerak. Ushbu hujjatdagi Ubuntu amallarini ulangan serverda bajaring. CloudShell kerak bo‘ladigan topshiriqda `exit` bilan unga qayting.

## Umumiy amallar

Muhit ilk yaratilganda barcha Missionlar tugallanmagan holatda bo‘ladi. Avval `reset` qilish shart emas.

### Amallarni bajaradigan user

Ubuntuga ulangandan keyingi boshqaruv `user`i — `ssm-user`. Tekshiring:

```bash
id -un
```

`jdu-check` va `jdu-reset`ni faqat `ssm-user` sifatida bajaring. Boshqa `user` ishlatsa, dastur `ssm-user`ga qaytish usulini ko‘rsatib tugaydi.

Mashq uchun `jduops`, `jduviewer`, `jduwriter` hisoblari bor. `ssm-user`dan ulardan biriga o‘tish misoli:

```bash
sudo su - jduops
id
```

Asl `ssm-user`ga qayting:

```bash
exit
id -un
```

Bu yerda almashtiriladigan `user`lardan faqat `ssm-user` parolsiz `sudo` ishlata oladi. Masalan, `jduwriter`dan bevosita `jduviewer`ga o‘tmang. Avval `exit` bilan `ssm-user`ga qayting, keyin `sudo su - jduviewer`ni bajaring.

`jduapp`, `jduweb`, `jdufinal`, `jduworker` faqat `service` uchun mo‘ljallangan `user`lardir. Ularning login `shell`i `nologin`; `su -` bilan interaktiv login qilmang. Kerakli tekshiruvni `ssm-user`dan `sudo -u USER COMMAND` shaklida bitta `command` sifatida bajaring.

Hozirgi Missionni tekshiring:

```bash
jdu-check M1
```

O‘qituvchining progress `server`i sozlangan bo‘lsa, natija avtomatik yuboriladi. Barcha savollar `PASS` bo‘lishini kutmaydi.

`RESULT` — Ubuntudagi topshiriq natijasi. `REPORT` — HTTPS yuborish natijasi. Yuborish xatosi Missionning `PASS`/`FAIL` holatini o‘zgartirmaydi. Anonim `server ID`ni quyidagicha ko‘ring:

```bash
jdu-progress id
```

Faqat `local` tekshiruvni bajarib, hozircha natija yubormaslik uchun:

```bash
jdu-check M1 --no-submit
```

Missionni boshidan boshlash zarur bo‘lsagina uni `reset` qiling:

```bash
jdu-reset M1
```

`reset`dan darhol keyin barcha bandlar `FAIL` bo‘ladi. Bu kutilgan holat. LabCheck holatni o‘zi tuzatmaydi.

## M1 Shell, path, file, and text

### Maqsad

`relative path` va `absolute path`ni farqlash; `directory` va `file` yaratish; `file`dan nusxa olish; `log`dan kerakli satrlarni ajratish.

### Boshlang‘ich holat

Materiallar `~/jdu-lab/m1/inbox`da. `case01` hali tayyor emas; `staging`da ortiqcha `.tmp` `file` bor.

### Topshiriq

1. Quyidagi `directory tree`ni yarating:

```text
~/jdu-lab/m1/case01/
├── config/
├── logs/
└── notes/
```

2. `inbox/config/app.conf`dan `case01/config/app.conf`ga nusxa oling.
3. `inbox/logs/incident.log`dan `case01/logs/incident.log`ga nusxa oling.
4. Nusxa olingan ikkala `file` mazmunini o‘zgartirmang.
5. `case01` ichidagi barcha `.tmp` `file`larni olib tashlang.
6. `incident.log`dagi `ERROR` bor to‘liq satrlarnigina `notes/errors.txt`ga yozing. Satr raqami qo‘shmang.
7. `incident.log`ning oxirgi besh satrini tartibini o‘zgartirmay `notes/recent.txt`ga yozing.

### Tekshiruv

Beshta natija tekshiriladi: `directory`, manba `file`lar, `.tmp`, `errors.txt`, `recent.txt`.

```bash
jdu-check M1
```

Foydali `command`lar: `pwd`, `ls`, `tree`, `mkdir`, `cp`, `rm`, `find`, `grep`, `tail`.

## M2 User, group, permission, and sudo

### Maqsad

`user`, `primary group`, `supplementary group`ni farqlash; umumiy `directory`ga `group permission` va `setgid` qo‘yish.

### Boshlang‘ich holat

`jduops`, `jduviewer` va `ops` oldindan bor. Dastlab faqat `jduviewer` noto‘g‘ri ravishda `ops` `supplementary group`iga kirgan. `jduops` esa `ops`da emas. `/srv/jdu-share` va `README.txt`ning egasi, `group`i va `mode`i tayyor emas.

### Topshiriq

1. `jduops`ni `ops` `supplementary group`iga qo‘shing.
2. `jduviewer`ni `ops` `supplementary group`idan chiqaring.
3. `/srv/jdu-share` egasi va `group`ini `root:ops` qiling.
4. `/srv/jdu-share` `mode`ini `2775` qiling; `setgid` ishlating. Hammaga yozish huquqini bermang.
5. `/srv/jdu-share/README.txt`ni `root:ops`, `mode 664` qiling.
6. `ssm-user`dan `sudo su - jduops` orqali o‘ting. Umumiy `directory`da `file` yarating. Yangi `file` `group`i `ops` bo‘lganini tekshiring.
7. `jduviewer` `README.txt`ni o‘qiy olishini tekshiring.
8. `jduviewer` umumiy `directory`da yangi `file` yarata olmasligini tekshiring.

`jduops`dagi tekshiruvdan keyin `exit` bilan `ssm-user`ga qayting. So‘ng `sudo su - jduviewer` orqali o‘ting. `jduviewer` tekshiruvidan keyin ham `exit` qiling. Oxirida `id -un` natijasi `ssm-user` ekanini tekshirib, keyin `jdu-check M2`ni bajaring.

### Tekshiruv

Oltita natija tekshiriladi: `group` a’zoligi, `directory` egasi/`group`i, `directory mode`, namunaviy `file`, `group` merosi va `viewer` huquqi.

```bash
jdu-check M2
```

Foydali `command`lar: `id`, `groups`, `getent passwd`, `getent group`, `stat`, `namei`, `chown`, `chmod`, `usermod`, `sudo -u`.

Taqiqlanadi: `chmod 777`.

## M3 Process and package

8- va 9-boblarni hamda P3 mashqining ikkala qismini tugatgach bajaring. 10-bobda `service`ni boshlash va avtomatik boshlash batafsil ko‘riladi.

### Maqsad

`service` va `process`ni bog‘lash, kerakli `service`ni to‘xtatish; Ubuntu `package`ini tekshirib o‘rnatish.

### Boshlang‘ich holat

`jdu-m3-process1.service`, `jdu-m3-process2.service`, `jdu-m3-process3.service` odatdagi `systemd unit`lari sifatida ishlamoqda. `cmatrix` o‘rnatilmagan. Boshlang‘ich holatni tekshirish:

```bash
systemctl list-units --type=service 'jdu-m3-*'
systemctl status jdu-m3-process1.service jdu-m3-process2.service jdu-m3-process3.service
```

### Topshiriq A: faqat process2ni to‘xtatish

1. `jdu-m3-process2.service` Main PIDini topib, o‘zingiz uchun yozib oling.
2. Shu PIDdagi `process`ni `ps` bilan tekshiring.
3. Tegishli `service`ni to‘xtating.
4. `process2` to‘xtagan, `process1` va `process3` ishlayotganini tekshiring.

Yozib olgan PIDdagi `process`ni bevosita to‘xtatmang. `systemd` boshqaradigan `service`ni to‘xtating.

### Topshiriq B: cmatrixni o‘rnatish

1. `package` ma’lumotini ko‘ring.
2. `apt` bilan `cmatrix`ni o‘rnating.
3. `command`ni ishga tushiring; `Ctrl+C` bilan chiqing.

### Tekshiruv

Ikki natija: A topshirig‘i uchun bitta, B topshirig‘i uchun bitta. Topshiriladigan `file` yo‘q.

```bash
jdu-check M3
```

Foydali `command`lar: `systemctl status`, `systemctl stop`, `systemctl is-active`, `ps`, `apt show`, `apt install`, `command -v`.

## M4 systemd service

### Maqsad

`unit file` sozlamalarini o‘qish; `active` va `enabled`ni farqlash.

### Boshlang‘ich holat

O‘qituvchi tayyorlagan `jdu-status.service` `loaded`, `inactive`, `disabled` holatida. `unit file` tayyor.

### Topshiriq

1. `systemctl cat jdu-status.service` yordamida `User`, `WorkingDirectory`, `ExecStart`ni o‘qing.
2. `unit file`ni o‘zgartirmay `service`ni `start` qiling.
3. Tizim yoqilganda avtomatik `start` bo‘ladigan qilib `enable` qiling.
4. `active` va `enabled` holatlarini alohida tekshiring.

### Tekshiruv

Ikki natija: o‘zgarmagan `unit`ning ishlashi (`active`) va avtomatik ishga tushishi (`enabled`). Topshiriladigan `file` yo‘q.

```bash
jdu-check M4
```

Foydali: `systemctl cat`, `systemctl start`, `systemctl enable`, `systemctl is-active`, `systemctl is-enabled`.

## M5 Port, socket, and log

### Maqsad

`service`, `process`, `socket`, IP address, `port`, HTTP va `journal`ni bitta ishlayotgan tizimning qismlari sifatida bog‘lash.

### Boshlang‘ich holat

O‘qituvchi tayyorlagan `jdu-web.service` `loaded`, `inactive`, `disabled` holatida. `unit file` va kontent `file`i tayyor. TCP 8081da `listener` yo‘q.

### Topshiriq

1. `unit file`dagi `User`, `ExecStart`, manzil, `port` va kontent `path`ini o‘qing.
2. `unit file`ni o‘zgartirmay `jdu-web.service`ni `start` qiling.
3. `127.0.0.1:8081`da aloqa kutayotgan `socket`ni toping. Bu holat `listener` (kutayotgan `socket`) deyiladi.
4. `socket`ga tegishli `process` PIDini `service` Main PIDi bilan solishtiring.

5. `0.0.0.0:8081` yoki `[::]:8081`da kutmayotganini tekshiring.
6. `http://127.0.0.1:8081/`ga `request` yuborib, HTTP `response`ni tekshiring.
7. `service user` `jduweb` kontent `file`ini o‘qiy olishini tekshiring. `file` va unga olib boruvchi yuqori `directory`larning `permission`ini ham ko‘ring.

8. `http://127.0.0.1:8081/m5-check`ga `request` yuboring.
9. Hozirgi `service` ishga tushgan davrga tegishli `journal`da `REQUEST path=/m5-check`ni toping.
10. TCP 18081da `listener` yo‘qligini va HTTP `request` muvaffaqiyatsiz bo‘lishini tekshiring.

### Tekshiruv

To‘rtta natija: `listener` va PID; HTTP va `file permission`; talaba yuborgan `request` `log`i; ochiq va yopiq `port`ni solishtirish. LabCheckning `/` `request`i talabaning `/m5-check` `request`i o‘rnini bosmaydi.

```bash
jdu-check M5
```

## M6 SSH and remote operation

### Maqsad

CloudShellni `local`, Ubuntuni `remote` deb farqlash; SSH `remote command`i va `scp` bilan `upload`/`download` qilish.

### Boshlang‘ich holat

SSH kaliti, `jdu-ubuntu` aliasi va Session Manager `tunnel`i tayyor. Ular topshiriq balliga kirmaydi. CloudShell va Ubuntuda Mission `file`lari hali yo‘q.

### Topshiriq

1. CloudShellda `id -un`, `hostname`, `pwd`ni tekshiring.
2. `ssh jdu-ubuntu` yoki SSH `remote command` orqali Ubuntudagi shu uch qiymatni tekshiring.
3. CloudShelldagi `~/jdu-lab/m6/local-source.txt`ga faqat quyidagi bitta satrni yozing:

```text
JDU SSH transfer test
```

4. `scp` bilan Ubuntudagi `~/jdu-lab/m6/upload.txt`ga `upload` qiling.
5. SSH `remote command` bilan Ubuntuda `~/jdu-lab/m6/remote-result.txt` yarating. Qiymatlarni qo‘lda yozmang.

```text
REMOTE_USER=<Ubuntuda aniqlangan user>
REMOTE_HOST=<Ubuntuda aniqlangan hostname>
REMOTE_PATH=<Ubuntuda aniqlangan home directory>
```

6. `scp` bilan Ubuntudagi `remote-result.txt`ni CloudShelldagi `~/jdu-lab/m6/downloaded-result.txt`ga `download` qiling.
7. `upload` manbasi va manzili, `download` manbasi va manzilini `sha256sum` bilan solishtiring.

### Tekshiruv

Ubuntu tomonida ikki topshiriq baholanadi. SSH orqali Ubuntuga kirib bajaring. Natija Dashboarddagi `M6 Ubuntu`ga yuboriladi.

```bash
jdu-check M6
```

CloudShell tomonida to‘rt topshiriq baholanadi. `exit` bilan Ubuntudan CloudShellga qaytgach bajaring. Natija Dashboarddagi `M6 CloudShell`ga yuboriladi.

```bash
jdu-check M6
```

Dashboard M6 qatorida Ubuntu `2/2`, CloudShell `4/4`, jami `6/6`ni alohida ko‘rsatadi. Ikkala tomonda ham hammasi `PASS` bo‘lgandagina M6 tugaydi. Bir tomonni qayta tekshirish boshqa tomondagi oxirgi natijani o‘chirmaydi.

Ikkala tomonni to‘liq `PASS` qiling. `private key`ni ko‘rsatmang, topshirmang, ko‘chirmang. SSH `service`i, SSH sozlamasi va `authorized_keys`ni o‘zgartirmang.

Foydali: `ssh`, `scp`, `sha256sum`, `id`, `hostname`, `pwd`, `printf`.

## M7 Integrated Ubuntu check

### Maqsad

M2, M4, M5dagi bilimlarni yangi `service`ga mustaqil qo‘llash. Yangi `command` kiritilmaydi.

### Boshlang‘ich holat

- O‘qituvchi bergan `jdu-final.service` `loaded`, `inactive`, `disabled` holatida.
- `/srv/jdu-final` va `index.txt` hali yo‘q.
- `jduwriter` va `jduviewer` `finalops` a’zosi emas.

### Topshiriq

1. `systemctl cat jdu-final.service` orqali `User`, `WorkingDirectory`, `ExecStart`ni o‘qing.
2. `/srv/jdu-final`ni `root:finalops`, `mode 2775` qilib yarating.
3. `/srv/jdu-final/index.txt` yarating. Mazmuni `/etc/jdu-lab/final-marker`dagi bir satr bilan aynan bir xil bo‘lsin.
4. `index.txt`ni `root:finalops`, `mode 664` qiling.
5. `jduwriter`ni `finalops`ga qo‘shing. `jduviewer`ni qo‘shmang.
6. `writer` kontentni o‘zgartira olishini, `viewer` esa o‘zgartira olmasligini tekshiring.
7. `unit file`ni o‘zgartirmay `service`ni `start` va `enable` qiling.
8. `service` `jdufinal` nomidan ishlashi va faqat `127.0.0.1:8090`da kutishini tekshiring.
9. HTTP `response status` `200` bo‘lib, kerakli `marker`ni qaytarishini tekshiring.
10. `http://127.0.0.1:8090/m7-check`ga `request` yuboring.
11. Hozirgi `service` ishga tushgan davrga tegishli `journal`dan `REQUEST path=/m7-check`ni toping.

`user`ni almashtirish kerak bo‘lsa, `ssm-user`dan `sudo su - jduwriter` yoki `sudo su - jduviewer`ni bajaring. Har tekshiruvdan keyin `exit` bilan `ssm-user`ga qayting. Oxirida `id -un`ni tekshirib, keyin `jdu-check M7`ni bajaring.

### Tekshiruv

Oltita natija: `file`lar tuzilishi, `writer`/`viewer` huquqlari, `service`, `socket`, HTTP va `journal`. `unit file`, SSH sozlamasi va LabCheckni o‘zgartirmang.

```bash
jdu-check M7
```

Foydali: `id`, `getent`, `stat`, `chown`, `chmod`, `systemctl`, `ps`, `sudo ss -lntp`, `curl`, `sudo journalctl`.

## Xavfsizlik uchun taqiqlangan amallar

- `chmod 777`ni ishlatmang.
- `/etc/ssh/sshd_config`ni o‘zgartirmang.
- `ssh.service`ni to‘xtatmang.
- `killall` yoki keng qamrovli `pkill`ni ishlatmang.
- `private key`ni ko‘rsatmang, topshirmang va Gitga qo‘shmang.
- Tashqi `host`larni `scan` qilmang yoki ularga login qilishga urinmang.
