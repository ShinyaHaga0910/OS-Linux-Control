# Ubuntu va OS asoslari: atamalar va commandlar jadvali

[日本語](../ja/reference.md) · [Русский](../ru/reference.md) · [O‘zbekcha](../uz/reference.md)

Qamrov: Ubuntu Server 24.04 LTS / ochiq Lab v1.0.0. Bu yodlash uchun jadval emas. Maqsadga mos `command`ni toping, kerakli `option` va tekshirish usulini kitobdan qayta o‘qing.

## Atamalar

| Atama | O‘zbekcha izoh |
| --- | --- |
| OS (operating system) | Apparat qismlarini boshqarib, `process`, `file`, kirish nazorati va aloqa kabi umumiy imkoniyatlarni beradigan asosiy tizim. |
| `kernel` | Ishlayotgan `OS`ning markazi; CPU, xotira, qurilma, `process`, `file` va tarmoqni boshqaradi. |
| `user space` | `shell`, `command` va `service` kabi odatdagi `program`lar `kernel`dan ajratilgan holda ishlaydigan makon. |
| `distribution` | Linux `kernel`i, vositalar, `package`lar, boshlang‘ich sozlamalar va yangilash siyosati birlashtirilgan tizim. Ubuntu bunga misol. |
| CLI (command-line interface) | Ko‘rsatma va natija matn orqali almashiladigan boshqarish usuli. |
| `terminal` | Matn kiritish va natijani ko‘rsatish oynasi yoki interaktiv ulanish muhiti. |
| `shell` | Kiritilgan matnni talqin qilib `command`ni bajaradigan `program`. Bu muhitda asosan Bash ishlatiladi. |
| `file` | Mazmuni va `metadata`si bo‘lgan asosiy saqlash birligi. |
| `directory` | `file` va boshqa `directory` nomlarini obyektlarga bog‘lab, iyerarxiya hosil qiladigan maxsus `file`. |
| `path` | `directory`lar iyerarxiyasidan o‘tib obyekt manzilini bildiradigan matn. |
| `owner` | `file` yoki `directory` `metadata`sida egasi sifatida yozilgan `user`. |
| `primary group` | Har bir `user`ga bitta asosiy a’zolik sifatida biriktiriladigan `group`. |
| `supplementary group` | Umumiy resurslardan foydalanish kabi maqsadlar uchun qo‘shimcha a’zolik. |
| `permission` | `owner`, `group` va `others` uchun o‘qish (`r`), yozish (`w`), bajarish (`x`) huquqlari. |
| `program` | Saqlash qurilmasidagi bajariladigan ko‘rsatmalar va tegishli `file`lar. |
| `process` | Xotiraga yuklanib bajarilayotgan `program`; o‘z PIDi va bajarish huquqlariga ega. |
| `package` | Dastur `file`lari, versiya, bog‘liqlik va o‘rnatish tartibini jamlaydigan tarqatish birligi. |
| `service` | Tizim boshqaradigan, fonda davomli imkoniyat beradigan `program` va uning boshqaruv birligi. |
| `unit` | `systemd` `service` va boshqa resurslarni boshqaradigan sozlama birligi. |
| `socket` | `process` `kernel`ning tarmoq aloqasi imkoniyatidan foydalanadigan kirish-chiqish nuqtasi. |
| `listen` | `socket` `client`ning ulanish `request`ini qabul qilishga tayyor holat. |
| `loopback` | Aloqani o‘sha `host` ichiga qaytaradigan virtual tarmoq `interface`i; IPv4da `127.0.0.1` misol. |
| `port` | Bir `host` ichidagi turli aloqa nuqtalarini farqlaydigan raqam. |
| `log` | `program` yoki `OS` ishi, xatosi va holat o‘zgarishi haqidagi yozuv. |
| `local` | SSH/SCP ulanishi yoki uzatishini boshlaydigan muhit; bu mashqda AWS CloudShell. |
| `remote` | SSH/SCP ulanishi yoki uzatilishi manzili; bu mashqda Ubuntu EC2. |
| `authentication` | Ulanayotgan tomon da’vo qilgan hisobning haqiqiy egasi ekanini tekshirish. |
| `authorization` | Tekshirilgan tomon muayyan resurs bilan nima qila olishini hal qilish. |

## Bilish zarur bo‘lgan commandlar

| Maqsad | `command` va kerakli `option` | Xavf yoki noto‘g‘ri talqin | Keyingi tekshiruv |
| --- | --- | --- | --- |
| Hozirgi joy | `pwd` | Faqat `prompt` matniga qarab joyni taxmin qilmang. | Chiqqan `path`ni `hostname` va `user` bilan solishtiring. |
| Joyni o‘zgartirish | `cd PATH`, `cd ..`, `cd ~` | `relative path` joriy `directory`ga bog‘liq. | `pwd` |
| Ro‘yxat | `ls -la`, `ls -ld DIR` | `-l DIR` ichidagi obyektlarni, `-ld DIR` `directory`ning o‘zini ko‘rsatadi. | Kerak bo‘lsa `stat` yoki `tree`. |
| Iyerarxiya | `tree PATH` | Tuzilishni ko‘rsatadi, lekin mazmun va `permission`ni to‘liq bermaydi. | `ls -l` bilan birga ishlating. |
| Directory yaratish | `mkdir -p PATH` | Noto‘g‘ri iyerarxiyani yaratib qo‘ymang. | `tree`, `ls -ld` |
| Nusxa olish | `cp SOURCE DEST` | Manba va manzil tartibini adashtirmang; eski `file` ustidan yozib qo‘yishingiz mumkin. | `cat`, `sha256sum` |
| Ko‘chirish yoki nomlash | `mv SOURCE DEST` | Manzildagi mavjud `file` ustidan yozish xavfi bor. | `ls` |
| O‘chirish | `rm FILE` | GUI “savatchasi” yo‘q. Bu mashqda `rm -rf`ni ishlatmang. | Oldin `pwd` va `ls` bilan maqsadni, keyin uning yo‘qligini tekshiring. |
| Tahrirlash | `nano FILE` | To‘g‘ri `file`ni saqlaganingizni va saqlamasdan chiqib ketmaganingizni tekshiring. | `Ctrl+O`, `Enter`, `Ctrl+X`; keyin `cat`. |
| Mazmunni ko‘rish | `cat FILE`, `less FILE` | Ikkilik yoki juda katta `file`ni ehtiyotsiz `cat` qilmang. | `less`dan `q` bilan chiqing. |
| Qidirish | `grep [-F] PATTERN FILE` | `-n` satr raqamini qo‘shadi; talab qilinmasa ishlatmang. | Mos satrlar va `exit status`ni ko‘ring. |
| Oxirgi satrlar | `tail -n N FILE` | Bu `-n` satrlar sonini bildiradi; `grep -n`dan farq qiladi. | Satrlar soni va tartibini tekshiring. |
| Chiqishni saqlash | `>`, `>>` | `>` eskisini bo‘shatib, ustidan yozadi. Kirish `file`i bilan bir xil manzilni bermang. | `cat`, `wc -l` |
| Commandlarni ulash | `\|` | Faqat `stdout` uzatiladi; `stderr` odatda o‘tmaydi. | Ulamasdan oldin har bir `command`ni alohida sinang. |
| User/group | `id [USER]`, `groups [USER]` | Ro‘yxatdagi hisob bilan ochiq `session` huquqlarini farqlang. | Yangi `session`da `id` bajaring. |
| Account ma’lumoti | `getent passwd USER`, `getent group GROUP` | `group` ro‘yxatida uni `primary group` qilgan `user` ko‘rinmasligi mumkin. | `id USER` bilan tekshiring. |
| Userni almashtirish | `sudo su - USER`, `exit` | `shell`lar ichma-ich ochiladi; mashq hisoblarida `sudo` huquqi yo‘q. | Har safar `id -un` va `pwd`. |
| Bitta commandni boshqa user sifatida bajarish | `sudo -u USER -- COMMAND` | `root` uchun muvaffaqiyat maqsad `user` uchun ham ruxsat borligini isbotlamaydi. | Darhol `echo $?`. |
| Groupga qo‘shish | `usermod -aG GROUP USER` | `-a`siz `-G` eski `supplementary group`lardan chiqarishi mumkin. | `id USER` va yangi `session`. |
| Groupdan chiqarish | `gpasswd -d USER GROUP` | `user` va `group` argumentlari tartibini adashtirmang. | `id USER` |
| Egasi/groupni o‘zgartirish | `chown OWNER:GROUP PATH` | `-R` bilan kutilmagan obyektlar ham o‘zgarishi mumkin. | `stat -c '%U:%G %a %n'` |
| Modeni o‘zgartirish | `chmod MODE PATH` | O‘ylamasdan `777` qo‘ymang; `x` `file` va `directory`da turlicha. | `stat` va boshqa `user` nomidan `test`. |
| Processlar ro‘yxati | `ps -e -o ...`, `ps -p PID -o ...` | Kitobdagi PID misolini aynan ko‘chirmang. | `user`, `command` nomi va PIDni solishtiring. |
| Signal yuborish | `kill -TERM PID` | PID o‘zgaruvchisi bo‘sh, `0`, manfiy yoki `1` emasligini tekshiring. PID uchun `pkill` ishlatmang. | `ps` yoki `service` holatida to‘xtaganini ko‘ring. |
| Package ma’lumoti va o‘rnatish | `apt show NAME`, `sudo apt update`, `sudo apt install NAME` | `apt update` ro‘yxatni, `apt upgrade` o‘rnatilgan `package`larni yangilaydi. Mashqdan tashqari butun tizimni yangilamang. | `command -v`, `dpkg-query` |
| Service sozlamasi | `systemctl cat UNIT` | Mashq `unit file`ini bevosita tahrirlamang. | `User`, `WorkingDirectory`, `ExecStart`ni o‘qing. |
| Service holati | `systemctl status/start/stop` | `active` bo‘lish barcha funksiyalar ishlashini isbotlamaydi. | `is-active`, MainPID, `curl` bilan tekshiring. |
| Avtomatik boshlanish | `systemctl enable/disable UNIT` | Hozir boshlash (`start`/`stop`) va keyingi yuklanish (`enable`/`disable`) boshqa amallar. | `is-enabled` |
| Main PID | `systemctl status UNIT` | `Main PID:` qatoridagi joriy raqamni o‘qing; to‘xtagan `service` uchun ko‘rinmasligi mumkin. | `ps -fp PID` |
| Socket holati | `sudo ss -lntp` | Manzil, `port` va `process` PIDini birgalikda tekshiring. | `service` Main PIDi bilan solishtiring. |
| HTTP aloqa | `curl -i URL`, zarur bo‘lsa `--max-time` | TCP ulanishi, HTTP `status code` va `response body` mazmuni alohida tekshiruvlar. | `status line`, mazmun va `exit status`. |
| Journal log | `sudo journalctl -u UNIT --no-pager -n N` | Eski ishga tushish `log`larini hozirgi `log` bilan adashtirmang. | Kerakli `request path` yozilganini toping. |
| SSH ulanishi | `ssh HOST`, `ssh HOST 'COMMAND'` | SSH `host alias` va DNS `hostname`ni, `local`/`remote` o‘zgaruvchi kengayishini, `private key` himoyasini farqlang. | Ulangach `id -un`, `hostname`, `pwd`. |
| SCP file uzatish | `scp SOURCE DEST` | Manba va manzilni almashtirmang; mavjud `file` ustidan yozish xavfi bor. | Ikki muhitda `sha256sum`, `remote`da `stat`. |

## Commandni qanday o‘qish kerak

`Command`ni nom, `option` va obyektga ajrating. Masalan, `tail -n 4 practice.log`da `tail` — bajariladigan `program`, `-n 4` — satrlar sonini belgilovchi `option` va qiymat, `practice.log` esa o‘qiladigan `file`. Bo‘sh joy bilan ajratilgan qismlarni tartib bilan o‘qing. Qo‘llanmadagi katta harfli `FILE`, `PATH` va `N` — tushuntirish uchun belgi; bajarishda ularni haqiqiy nom, `path` yoki raqamga almashtiring.

`Option` `command` ishini o‘zgartiradi. Qisqa shakl ko‘pincha `-u` kabi bitta harf, uzun shakl esa `--user` kabi ikki chiziqdan keyingi so‘zdir. Har bir `command`da ikkala shakl ham bo‘lmaydi. `find -name` bir chiziqdan keyin so‘z ishlatadi. Inglizcha ma’nodan taxmin qiling, lekin aniq vazifani o‘sha `command` yordamidan tekshiring.

### Inglizcha so‘zlar bilan eslab qolish

Quyidagi inglizcha so‘zlar eslashga yordam beradi; hammasi tarixiy rasmiy qisqartma deb qaralmaydi. `find` va `tail` oddiy inglizcha so‘zlar.

| Command | Inglizcha ishora | Vazifasi |
| --- | --- | --- |
| `pwd` | print working directory | Hozirgi ish `directory`sini ko‘rsatadi. |
| `cd` | change directory | Ish `directory`sini o‘zgartiradi. |
| `ls` | list | Nomlar ro‘yxatini ko‘rsatadi. |
| `mkdir` | make directory | `Directory` yaratadi. |
| `cp` | copy | Avval manba, keyin manzil ko‘rsatib nusxa oladi. |
| `mv` | move | Ko‘chiradi yoki shu `directory` ichida nomini o‘zgartiradi. |
| `rm` | remove | Belgilangan `file`ni o‘chiradi. |
| `cat` | concatenate | `File`lar mazmunini birlashtirib ko‘rsatadi; bitta `file` bilan ham ishlaydi. |
| `tree` | tree | `Directory` tuzilmasini daraxt ko‘rinishida ko‘rsatadi. |
| `find` | find | `Directory`larni kezib, shart bo‘yicha obyekt qidiradi. |
| `grep` | global / regular expression / print (`g/re/p`) | `File` ichidagi satrlarni qidiradi; `find` esa nomlarni qidiradi. |
| `tail` | tail | `File` oxirini ko‘rsatadi. |
| `id` | identity / identifier | `User` va `group` identifikatorlarini ko‘rsatadi. |
| `chown` | change owner | Egani o‘zgartiradi. |
| `chmod` | change mode | `Permission mode`ni o‘zgartiradi. |
| `ssh` | Secure Shell | Boshqa kompyuterga himoyalangan ulanish yaratadi. |

### id -un qismlarini o‘qish

`id` `option`siz UID, GID va `group`larni ko‘rsatadi. Quyidagilarni solishtiring:

```bash
id
id -u
id -u -n
id -un
```

`-u` `--user`ga mos keladi va faqat joriy `effective UID`ni chiqaradi. `-n` `--name`ga mos keladi: raqam o‘rniga nom chiqadi. Shu bois `id -u -n` va `id -un` bir xil; bizning Ubuntuga ulanganda `ssm-user`ni ko‘rsatadi.

**Faqat `id -n` yetarli emas:** qaysi ID nomga aylanishini belgilang. `-n`ni `-u`, `-g` yoki `-G` bilan qo‘shing. `id -gn` joriy `effective group` nomini, `id -Gn` barcha `group` nomlarini ko‘rsatadi. Inglizcha ishoradan tashqari, `option`lar birga ishlash shartini ham tekshiring.

### Bir xil harf turli commandlarda turlicha

| Misol | Option ma’nosi | Natija |
| --- | --- | --- |
| `id -un` | `-u` — user, `-n` — name | Joriy `effective user` nomi. |
| `grep -n 'WARN' practice.log` | `-n` — `--line-number` | Mos satr oldiga satr raqami. |
| `tail -n 4 practice.log` | `-n` — `--lines`, `4` — son | Oxirgi to‘rt satr. |
| `ls -la` | `-l` — uzun shakl, `-a` — hammasi | Yashirin `file`lar bilan batafsil ro‘yxat. |
| `mkdir -p logs/archive` | `-p` — `--parents` | Kerakli yuqori `directory`larni ham yaratadi. |
| `grep -F 'WARN' practice.log` | `-F` — `--fixed-strings` | `Regular expression` emas, oddiy matn qidiradi. |
| `chown -R USER DIR` | `-R` — `--recursive` | `Directory` ichidagilarning ham egasini o‘zgartiradi. |

Qisqa `option`lar ba’zan `id -un` kabi birlashtiriladi, lekin har doim emas. Qiymat oladigan `tail -n 4` va so‘zli `find -name`ni ko‘rsatilgan shaklda yozing.

### Natijani saqlash belgisi option emas

```bash
grep 'WARN' ../logs/practice.log
grep 'WARN' ../logs/practice.log > warnings.txt
```

Birinchisi ekranga chiqaradi. Ikkinchisidagi `>` — `shell`ning `stdout`ni `warnings.txt`ga yo‘naltirish belgisi; u `grep` `option`i emas. `cat warnings.txt` bilan natijani ko‘ring. `>>` `file` oxiriga qo‘shadi.

## findni bosqichma-bosqich o‘qish

`tree` butun tuzilmani ko‘rsatadi, `find` esa shartlar bilan natijani toraytiradi. P1da avval `tree` bilan tuzilmani, keyin `find` bilan `.tmp` `file`larni ko‘ring; aniq `path`lar tekshirilgach, `rm` bilan o‘chiring.

### Boshlanish joyi, shart va chiqishni ajratish

```bash
find . -type f -name '*.tmp' -print
```

Buni «hozirgi joy va ichidagi obyektlarni kezib, nomi `.tmp` bilan tugaydigan oddiy `file`larning `path`ini chiqarish» deb o‘qing.

| Qism | Ma’nosi | Eslatma |
| --- | --- | --- |
| `find` | Qidirish `command`i. | find — topish. |
| `.` | Boshlanish joyi. | Hozirgi `directory` va osti. |
| `-type f` | Faqat oddiy `file`. | type — tur; `directory` uchun `-type d`. |
| `-name '*.tmp'` | Nom `pattern`ga mos. | `File` mazmunini qidirmaydi. |
| `-print` | Topilgan `path`ni chiqarish. | Qog‘ozga chop etish emas. |

`-type` va `-name` — shartlar, `-print` — amal. Operator ko‘rsatilmagan ketma-ket shartlar odatda «ikkalasi ham» (AND) bo‘ladi. Shuning uchun `-type f` bo‘lsa, nomi mos `directory` chiqmaydi. Oddiy `find` `-print`siz ham `path`larni ko‘rsatadi; bu yerda amal aniq yozilgan.

### Shartlarni bittadan qo‘shish

P1da satrlarni birma-bir bajaring va natijani solishtiring:

```bash
cd ~/jdu-lab/p1/practice01
find . -print
find . -type f -print
find . -type f -name '*.tmp' -print
```

Avval barcha obyektlar, keyin faqat `file`lar, oxirida nomi `.tmp` bilan tugaydigan `file`lar ko‘rinadi. O‘chirishdan oldin ikkita `path` chiqadi (tartib o‘zgarishi mumkin):

```text
./staging/training.conf.tmp
./staging/practice.log.tmp
```

Agar 6-bosqichda allaqachon o‘chirgan bo‘lsangiz, hech narsa chiqmasligi normal. Shu misol uchungina topshiriqni `reset` qilmang.

### Nega qo‘shtirnoq ishlatiladi

`'*.tmp'`dagi `*` nol yoki undan ko‘p belgiga mos keladi. Qo‘shtirnoq `shell` bu `pattern`ni joriy `directory` nomlariga oldindan kengaytirishiga yo‘l qo‘ymaydi. `find` uni o‘zgarmagan holda olib, har qatlamdagi nom bilan solishtiradi. Qo‘shtirnoqsiz `find` ishga tushmasdan oldin argument o‘zgarishi mumkin.

`-name` faqat obyekt nomini, yuqori `directory`larsiz tekshiradi. To‘liq `path` uchun `-path` ishlatiladi. Bu `regular expression` emas, `file name pattern`dir.

### Kerak bo‘lganda boshqa shartlar

| Belgilash | Inglizcha ishora | Ma’nosi |
| --- | --- | --- |
| `-type d` | directory | Faqat `directory`lar. |
| `-iname '*.log'` | case-insensitive name | Katta-kichik harfni farqlamaydi. |
| `-path './staging/*'` | path | To‘liq `path`ga `pattern`. |
| `-maxdepth 2` | maximum depth | Boshlanish joyi 0; 2-darajagacha yuradi. |
| `-mindepth 1` | minimum depth | Boshlanish joyini natijaga qo‘shmaydi. |
| `-empty` | empty | Bo‘sh `file` yoki `directory`. |
| `-user ssm-user` | user | Ko‘rsatilgan `owner`ga tegishli obyekt. |

Chuqurlik chegarasini boshlanish joyidan keyin yozish o‘qishni osonlashtiradi. Ikki darajagacha oddiy `file`lar misoli:

```bash
find . -maxdepth 2 -type f -print
```

### Qidirish va o‘chirishni ajratish

P1da `find` faqat qidirib ko‘rsatadi. Natijani tekshirgach, `rm`ga aniq `path`larni bering:

```bash
rm staging/training.conf.tmp staging/practice.log.tmp
tree
find . -type f -name '*.tmp' -print
```

`tree` bilan tuzilmani ko‘ring; oxirgi `find` `.tmp` topmasin. `find -delete` va `find -exec` kabi o‘zgartiruvchi amallar ham bor, ammo natijani tushunmaguncha qidirish bilan o‘chirishni ajrating.

## grep yordamida file ichidagi satrlarni qidirish

`grep` `pattern`ga mos satrlarni chiqaradi. Nomi Unix `ed` muharriridagi `g/re/p` (global / regular expression / print) yozuvidan kelgan. `find` `file`ning nomi yoki turini, `grep` uning mazmunidagi satrlarni qidiradi.

```bash
grep 'WARN' ../logs/practice.log
```

`grep` — `command`, `'WARN'` — `pattern`, `../logs/practice.log` — o‘qiladigan `file`. Odatda katta-kichik harf farqlanadi, `pattern` `basic regular expression` sifatida talqin qilinadi. Bu yerda `WARN` bor satrning barchasi chiqadi, faqat so‘zning o‘zi emas.

| Option | Uzun shakl | Ma’nosi |
| --- | --- | --- |
| `-n` | `--line-number` | Mos satr oldiga asl raqamini qo‘shadi. |
| `-i` | `--ignore-case` | Katta-kichik harfni farqlamaydi. |
| `-F` | `--fixed-strings` | `Regular expression` emas, oddiy matn. |
| `-v` | `--invert-match` | Mos kelmagan satrlarni chiqaradi. |
| `-c` | `--count` | Mos kelgan satrlar soni; so‘z takrorlari soni emas. |

`grep -n 'WARN' ../logs/practice.log` satr raqamini qo‘shadi. P1/M1da asl satrlar raqamsiz kerak bo‘lsa, saqlashda `-n` ishlatmang. `grep -F` oddiy matnni izlaydi.

### Avval ko‘rish, keyin saqlash

```bash
grep 'WARN' ../logs/practice.log
grep 'WARN' ../logs/practice.log > warnings.txt
cat warnings.txt
```

Avval ekranda to‘g‘ri satrlar ekanini ko‘ring, so‘ng natijani `file`ga yozib, `cat` bilan qayta o‘qing. `>` bilan ekranga natija chiqmasa ham, `file`ga yozilgan bo‘lsa normal. `grep`ning odatiy `exit status`lari: 0 — mos satr bor, 1 — yo‘q, 2 — xato. Mos satr yo‘qligini `file`ni o‘qish xatosidan farqlang.

## tail yordamida file oxirini o‘qish

Inglizcha `tail` — «dum, oxir». `tail FILE` `option`siz oxirgi o‘n satrni ko‘rsatadi; `file` qisqaroq bo‘lsa, mavjud satrlar chiqadi. Bu `log`dagi so‘nggi hodisalar uchun qulay.

```bash
tail -n 4 ../logs/practice.log
```

`-n 4` ko‘rsatiladigan satrlar soni, `../logs/practice.log` o‘qiladigan `file`. Bu `--lines`ga mos, `grep -n`dagi satr raqami emas.

| Option | Uzun shakl | Ma’nosi |
| --- | --- | --- |
| `-n 4` | `--lines=4` | Oxirgi to‘rt satr. |
| `-n 5` | `--lines=5` | Oxirgi besh satr. |
| `-f` | `--follow` | Yangi qo‘shilgan satrlarni ham ko‘rsatishda davom etadi. |

`tail` satrlarni teskari tartibga aylantirmaydi. Oxirgi satrlarni asl tartibda chiqaradi: P1da to‘rt, M1da besh satr.

### Avval ko‘rish, keyin saqlash

```bash
tail -n 4 ../logs/practice.log
tail -n 4 ../logs/practice.log > recent.txt
cat recent.txt
```

Birinchi bajarishda satrlar soni va tartibini ko‘ring, keyin saqlang. P1dagi `recent.txt` oxirgi to‘rt satrga teng bo‘lsin. `tail -f FILE` yangi yozuvlarni kutadi; `Ctrl+C` bilan chiqing. Topshiriq `file`i uchun tugaydigan `tail -n N FILE`ni ishlating.

## Tushunarsiz optionni tekshirish

```bash
id --help
find --help
man find
help cd
```

`--help` ko‘p tashqi `command`larga qisqa yordam beradi, `man` batafsil qo‘llanma, `help` esa Bash ichki `command`larini tushuntiradi. `man`dan `q` bilan chiqing. Labda `man` o‘rnatilmagan bo‘lsa, `--help`, `help` yoki rasmiy hujjatlardan foydalaning:

- [GNU Coreutils: id](https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html)
- [GNU Grep](https://www.gnu.org/software/grep/manual/grep.html)
- [GNU Coreutils: tail](https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html)
- [GNU Findutils](https://www.gnu.org/software/findutils/manual/html_mono/find.html)

Tartib: (1) `command` vazifasi, (2) `option` ma’nosi, (3) undan keyingi qiymat, (4) amal bajariladigan obyekt. AIdan maslahat olsangiz ham, `find . -type f -name '*.tmp' -print`ni qismlarga ajratib tushuntirishini so‘rang va `--help` bilan tekshiring.

## Darsda ishlatiladi, lekin yodlash shart emas

`uname -r`, `hostname`, `find`, `touch`, `stat`, `namei -l`, `test -r/-w`, `echo $?`, `printf`, `command -v`, `dpkg-query`, `dpkg -S`, `sha256sum`, `readlink`, `tr`, `/proc/PID/`.

Maqsad va natijani o‘qishni kitobdan tekshiring. Zarur bo‘lsa `man`, `help` yoki shu jadvalga qayting.

## Keyingi bo‘limlarda ko‘riladigan commandlar

`ip`, `ping`, `dig`, `tcpdump`, `mount`, `df`, `psql`. Bu kitob faqat aloqasini ko‘rsatadi; batafsil sozlash tarmoq, saqlash, DNS va ma’lumotlar bazasi bo‘limlarida o‘rganiladi.

## Bu kitobga kirmaydigan mavzular

`kernel`ni yaratish va `debug` qilish; CPU ko‘rsatmalarining ichki bajarilishi; xotira sahifalarini almashtirish algoritmi; disk I/O rejalashtiruvchisini boshqarish; `file system` yaratish yoki bo‘limlarni o‘zgartirish; tashqi `host` `port`larini `scan` qilish; SSH `server` sozlamasini o‘zgartirish.
