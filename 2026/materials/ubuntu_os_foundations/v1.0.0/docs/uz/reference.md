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
| Package ma’lumoti va o‘rnatish | `apt show NAME`, `sudo apt update`, `sudo apt install NAME` | `apt update` ro‘yxatni, `apt upgrade` o‘rnatilgan `package`larni yangilaydi. Mashq shartidan tashqari butun tizimni o‘zgartirmang. | `command -v`, `dpkg-query` |
| Service sozlamasi | `systemctl cat UNIT` | Mashq `unit file`ini bevosita tahrirlamang. | `User`, `WorkingDirectory`, `ExecStart`ni o‘qing. |
| Service holati | `systemctl status/start/stop` | `active` bo‘lish barcha funksiyalar ishlashini isbotlamaydi. | `is-active`, MainPID, `curl` bilan tekshiring. |
| Avtomatik boshlanish | `systemctl enable/disable UNIT` | Hozir boshlash (`start`/`stop`) va keyingi yuklanish (`enable`/`disable`) boshqa amallar. | `is-enabled` |
| Main PID | `systemctl show -p MainPID --value UNIT` | PID `0`, bo‘sh yoki avvalgi ishlashdan qolgan qiymat emasligini tekshiring. | `ps -p PID` |
| Socket holati | `sudo ss -lntp` | Manzil, `port` va `process` PIDini birgalikda tekshiring. | `service` Main PIDi bilan solishtiring. |
| HTTP aloqa | `curl -i URL`, zarur bo‘lsa `--max-time` | TCP ulanishi, HTTP `status code` va `response body` mazmuni alohida tekshiruvlar. | `status line`, mazmun va `exit status`. |
| Journal log | `sudo journalctl -u UNIT --no-pager -n N` | Eski ishga tushish `log`larini hozirgi `log` bilan adashtirmang. | Kerakli `request path` yozilganini toping. |
| SSH ulanishi | `ssh HOST`, `ssh HOST 'COMMAND'` | SSH `host alias` va DNS `hostname`ni, `local`/`remote` o‘zgaruvchi kengayishini, `private key` himoyasini farqlang. | Ulangach `id -un`, `hostname`, `pwd`. |
| SCP file uzatish | `scp SOURCE DEST` | Manba va manzilni almashtirmang; mavjud `file` ustidan yozish xavfi bor. | Ikki muhitda `sha256sum`, `remote`da `stat`. |

## Darsda ishlatiladi, lekin yodlash shart emas

`uname -r`, `hostname`, `find`, `touch`, `stat`, `namei -l`, `test -r/-w`, `echo $?`, `printf`, `command -v`, `dpkg-query`, `dpkg -S`, `sha256sum`, `readlink`, `tr`, `/proc/PID/`.

Maqsad va natijani o‘qishni kitobdan tekshiring. Zarur bo‘lsa `man`, `help` yoki shu jadvalga qayting.

## Keyingi bo‘limlarda ko‘riladigan commandlar

`ip`, `ping`, `dig`, `tcpdump`, `mount`, `df`, `psql`. Bu kitob faqat aloqasini ko‘rsatadi; batafsil sozlash tarmoq, saqlash, DNS va ma’lumotlar bazasi bo‘limlarida o‘rganiladi.

## Bu kitobga kirmaydigan mavzular

`kernel`ni yaratish va `debug` qilish; CPU ko‘rsatmalarining ichki bajarilishi; xotira sahifalarini almashtirish algoritmi; disk I/O rejalashtiruvchisini boshqarish; `file system` yaratish yoki bo‘limlarni o‘zgartirish; tashqi `host` `port`larini `scan` qilish; SSH `server` sozlamasini o‘zgartirish.
