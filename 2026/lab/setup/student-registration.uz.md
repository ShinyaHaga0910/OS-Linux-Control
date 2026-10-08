# Dastlabki sozlash va topshiriqlarni tekshirish tizimida ro‘yxatdan o‘tish

[Tilni tanlash](README.md) · [日本語](student-registration.ja.md) · [Русский](student-registration.ru.md)

**O‘qituvchi bergan command’ni bajaring va shaxsiy progress dashboard’ingizni oching — shunda dastlabki ro‘yxatdan o‘tish tugaydi.** Siz mashqlar uchun server yaratasiz va uni Google Classroom’da ishlatadigan email manzilingiz bilan o‘qituvchining topshiriqlarni tekshirish tizimida bog‘laysiz. P0 mashqi ro‘yxatdan o‘tgandan keyin bajariladi.

Bu qo‘llanma birinchi marta sozlayotgan talabalar uchun. Agar topshiriqlarni bajarishni boshlagan bo‘lsangiz, setup command’ni qayta bajarmang; «Muammo yuz bersa» bo‘limiga qarang.

## 1. Learner Lab’ni ishga tushiring

Agar hali AWS Academy’da ro‘yxatdan o‘tmagan bo‘lsangiz, avval [ro‘yxatdan o‘tish va login qo‘llanmasini](https://github.com/ShinyaHaga0910/Introduction-CyberSecurity/blob/main/orientation/aws-academy/README.md) bajaring.

O‘qituvchi ko‘rsatgan Learner Lab’ni oching va `Start Lab` tugmasini bosing. AWS indikatori yashil bo‘lgach, `AWS` orqali AWS console’ni oching.

## 2. CloudShell’ni oching

AWS console’da o‘qituvchi ko‘rsatgan region’ni tanlang va CloudShell’ni oching. Command kiritish mumkin bo‘lguncha kuting.

Keyingi barcha amallar **CloudShell’da** bajariladi. Ushbu qo‘llanmada Ubuntu server’ga login qilish shart emas.

## 3. O‘qituvchi bergan command’ni bajaring

Google Classroom’da **joriy semestr uchun setup command**’ni oching. Uni to‘liq nusxalang, CloudShell’ga joylang va Enter tugmasini bosing.

O‘qituvchi tizimining endpoint’i va dastlabki registration key shu command ichida berilgan. Ularni o‘zingiz o‘zgartirishingiz shart emas. Haqiqiy command’ni Google Classroom’dan oling.

Setup mashqlar uchun server yaratadi, Ubuntu’ni dastlabki sozlaydi va server’ni o‘qituvchi tizimida ro‘yxatdan o‘tkazadi. Jarayon tugashini kuting; ayni command’ni boshqa oynada bir vaqtda bajarmang.

## 4. Email manzilingizni kiriting

Jarayon davomida quyidagi so‘rov chiqadi:

```text
Classroom email (visible):
```

**Google Classroom’da ishlatadigan `@jdu.uz` bilan tugaydigan shaxsiy email manzilingizni** kiriting va Enter tugmasini bosing. Manzil ekranda ko‘rinadi; bo‘sh kiritish yoki boshqa domain bilan davom etib bo‘lmaydi. Ko‘rsatilgan manzilni tekshiring, so‘ng `Yes` deb yozib Enter bosing. Xato bo‘lsa, faqat Enter bosib, manzilni qayta kiriting. Parol kerak emas. Email ko‘ringan ekran rasmini ulashmang.

O‘qituvchi shu email orqali server’ingiz va topshiriqlardagi progress’ingizni siz bilan bog‘laydi. Server ID’ni Google Classroom’ga alohida topshirish shart emas. Bu amal email egasini tasdiqlamaydi, shuning uchun manzilni xatosiz kiriting.

## 5. Setup muvaffaqiyatli tugaganini tekshiring

Quyidagi ikkala xabar ham chiqishi kerak:

```text
PASS Teacher registration, EC2 identity, and email link confirmed.
PASS The AWS lab environment is ready.
```

Birinchi xabar server ro‘yxatdan o‘tganini va email bog‘langanini, ikkinchisi mashqlar muhiti tayyorligini bildiradi. Error chiqsa yoki xabarlardan biri bo‘lmasa, setup hali tugamagan.

## 6. Shaxsiy dashboard’ingizni oching

CloudShell’da bajaring. `ssh jdu-ubuntu` orqali Ubuntu server’ga kirgandan keyin ham shu command’ni bajarishingiz mumkin. Yangi setup paytida u Ubuntu’ga avtomatik o‘rnatiladi:

```bash
jdu-my-progress
```

Chiqqan link’ni bosing. Agar link bosilmasa, HTTPS URL’ni nusxalab browser’da oching. CloudShell yoki SSH orqali ulangan Ubuntu sizning kompyuteringizdagi browser’ni avtomatik ocha olmaydi. Bu **sizning shaxsiy progress dashboard’ingiz**. Sahifa o‘qituvchi tizimida taqdim etiladi va unda faqat sizning natijalaringiz ko‘rinadi. Dashboard uchun alohida server yaratish kerak emas.

P0–P6 va M1–M7 bo‘yicha progress’ni ko‘rishingiz mumkin. Dastlab natijalar hali yuborilmaganligi sababli bo‘sh kataklar yoki «—» normal holatdir. Sarlavhada ro‘yxatdan o‘tgan email va Server ID ko‘rsatiladi. Sahifaning yuqori qismidagi tugmalar orqali yapon, o‘zbek yoki rus tilini tanlashingiz mumkin. Hostname va EC2 instance ID ko‘rsatilmaydi.

URL 15 daqiqa amal qiladi. Muddati tugasa, CloudShell yoki Ubuntu’da `jdu-my-progress`’ni yana bajaring va yangi URL’ni oching. Kompyuteringizga certificate o‘rnatish shart emas.

Avval yaratilgan Ubuntu server’da `jdu-my-progress: command not found` chiqsa, **SSH orqali Ubuntu’ga kirgandan keyin** quyidagilarni bir marta bajaring:

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/scripts/install-my-progress-ubuntu.sh -o /tmp/jdu-install-my-progress-ubuntu.sh
bash /tmp/jdu-install-my-progress-ubuntu.sh
jdu-my-progress
```

Topshiriqlar va natijalar reset qilinmaydi. Chiqqan URL’ni browser’da oching va boshqalarga yubormang. Ubuntu registration ma’lumotlari o‘qilmasa, `ssm-user` sifatida kirganingizni tekshiring va o‘qituvchiga murojaat qiling.

## Yakuniy tekshiruv

- Setup muvaffaqiyatini bildiruvchi ikkala `PASS` xabari chiqdi.
- Shaxsiy progress dashboard ochildi.

Ikkalasini tekshirganingizdan so‘ng dastlabki ro‘yxatdan o‘tish tugaydi. Keyin [P0 qo‘llanmasiga](../GUIDED_PRACTICE.md#p0-environment-and-os) o‘ting. Ro‘yxatdan o‘tishning o‘zi P0 bajarilganini anglatmaydi.

## Muammo yuz bersa

| Holat | CloudShell’da bajariladigan amal |
| --- | --- |
| Email kiritilmadi yoki noto‘g‘ri kiritildi | Quyidagi email’ni qayta ro‘yxatdan o‘tkazish command’ini o‘sha CloudShell’da bajaring |
| Registration holatini qayta tekshirmoqchisiz | `jdu-register`’ni bajaring |
| Dashboard URL muddati tugadi | `jdu-my-progress`’ni bajaring |
| Setup yoki registration xato bilan tugadi | Qaysi bosqichda to‘xtaganini va error’ni o‘qituvchiga ayting. Stack’ni o‘zingizcha o‘chirmang |

Command ichidagi registration key, private key, authentication token va shaxsiy dashboard URL’ni ommaga chiqarmang yoki boshqalarga bermang. Umumiy kompyuterda ishlagandan keyin dashboard sahifasini yoping.

### Faqat email’ni qayta ro‘yxatdan o‘tkazish

Dastlabki setup command’ini qayta ishga tushirmang. Quyidagi command’ni **dastlabki sozlashda ishlatilgan CloudShell**’da bajaring. Bu faqat email’ni o‘zgartiradi. Mashq server’i va topshiriqlar qayta tiklanmaydi.

```bash
jdu-register --change-email
```

`@jdu.uz` bilan tugaydigan email’ni kiriting va `Yes` bilan tasdiqlang. `PASS Teacher registration, EC2 identity, and email link confirmed.` chiqsa, ish tugadi. Registration ma’lumotlari topilmasa, to‘g‘ri CloudShell’ni tekshiring va o‘qituvchiga murojaat qiling.

Eski muhitda `jdu-register` topilmasa yoki `--change-email` qo‘llab-quvvatlanmasa, o‘sha CloudShell’da quyidagi command’larni bajaring. Yangi versiya o‘rnatilishidan oldin SHA-256 tekshiriladi. Tekshiruv muvaffaqiyatsiz bo‘lsa, eski tool almashtirilmaydi.

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/scripts/register-student.py -o /tmp/jdu-register-new && \
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/SHA256SUMS -o /tmp/jdu-register-checksums && \
awk '$2 == "scripts/register-student.py" {print $1 "  /tmp/jdu-register-new"}' /tmp/jdu-register-checksums | sha256sum --check --status && \
install -D -m 0755 /tmp/jdu-register-new "$HOME/.local/bin/jdu-register" && \
"$HOME/.local/bin/jdu-register" --change-email
```

## O‘qituvchining oldindan tayyorgarligi

Command’ni talabalarga berishdan oldin [o‘qituvchi qo‘llanmasi](../teacher/README.md) bo‘yicha tekshirish va progress server’ini tayyorlang yoki yangilang. Yaratilgan joriy semestr command’ini Google Classroom’da tarqating. Ro‘yxatdan o‘tgach, email va Server ID bog‘lanishini o‘qituvchi `jdu-dashboard` orqali tekshirishi mumkin.
