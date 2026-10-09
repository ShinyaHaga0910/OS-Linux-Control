# Mavjud Lab muhitini yangilash (stackni o‘chirmasdan)

[日本語](UPDATE_EXISTING.md) · [Русский](UPDATE_EXISTING.ru.md) · [O‘zbekcha](UPDATE_EXISTING.uz.md)

Bu yo‘riqnoma o‘qituvchi va talabalar uchun Lab muhiti allaqachon yaratilgan guruhga mo‘ljallangan. CloudFormation `stack`ni o‘chirish shart emas. Talabaning EC2 muhiti ham qayta yaratilmaydi. Yangi `stack` bilan dastlabki o‘rnatish faqat yangi talabalar uchun sinovda yoki keyingi o‘quv yilida kerak bo‘ladi.

`Stack` o‘chirilsa, o‘qituvchi tomondagi progress yozuvlari, talabalarning mashq natijalari va ulanish ma’lumotlari yo‘qolishi mumkin. Ushbu yangilanishda bunday amal kerak emas. Avval o‘qituvchi o‘z `stack`ini yangilaydi, keyin har bir talaba o‘z CloudShell muhitida yangilashni bajaradi. Boshlashdan oldin ishlatilayotgan AWS account va regionni tekshiring. Ishlab turgan asosiy muhitga qo‘llash haqida o‘qituvchi alohida qaror qiladi.

## 1. O‘qituvchi: mavjud `stack`ni saqlangan `key` bilan yangilash

Buyruqlarni o‘qituvchi Labini dastlab sozlagan CloudShell muhitida bajaring. Unda `~/.jdu-teacher/progress.env`, `admin.key` va `registration.key` saqlangan bo‘lishi kerak. `Key` qiymatlarini ko‘rsatmang va boshqalarga yubormang.

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/teacher/update-existing-teacher.sh -o /tmp/jdu-update-existing-teacher.sh
printf '%s  %s\n' 'cc6cf61fbb2db3457fd70ce60e8c80733be566e7fc72ec91d827faea3611af3a' '/tmp/jdu-update-existing-teacher.sh' | sha256sum --check
bash /tmp/jdu-update-existing-teacher.sh --region us-east-1
```

Saqlangan `stack` topilmasa, `script` to‘xtaydi. U `key` qiymatlarini qayta yaratmaydi yoki almashtirmaydi; o‘sha CloudFormation `stack`ni yangilaydi. Muvaffaqiyatli yakunlangach, `jdu-dashboard`ni ishga tushiring va yangi ko‘rish URLi orqali sahifani tekshiring. Bu URLni boshqalarga yubormang.

```bash
jdu-dashboard
```

## 2. Talaba: CloudShell va mavjud Ubuntuni yangilash

O‘qituvchi yangilashni tugatgach, har bir talaba buyruqlarni **dastlabki o‘rnatishda ishlatgan CloudShell** muhitida bajaradi. Ularni `ssh jdu-ubuntu` orqali Ubuntu ichiga kirgandan keyin bajarmang.

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/scripts/update-existing-cloudshell.sh -o /tmp/jdu-update-existing-cloudshell.sh
printf '%s  %s\n' '890a92f55ce9183fb10eee8c76ba2c32a03d283edb8deac626fec0f3b96b9087' '/tmp/jdu-update-existing-cloudshell.sh' | sha256sum --check
bash /tmp/jdu-update-existing-cloudshell.sh --region us-east-1
```

`Script` avval mavjud talaba `stack`i, SSH ulanish manzili hamda CloudShell va Ubuntudagi ro‘yxatdan o‘tish ma’lumotlari bir muhitga tegishli ekanini tekshiradi. Keyin yuklab olingan `file`larning SHA-256 qiymatini solishtiradi va CloudShelldagi yordamchi `command`lar hamda Ubuntudagi topshiriqni tekshirish `command`larini yangilaydi. Talaba uchun CloudFormation qayta ishga tushirilmaydi. Mashq `file`lari, Server ID, token, SSH `key` va progress yuboriladigan manzil qayta o‘rnatilmaydi.

Email hali ro‘yxatdan o‘tmagan bo‘lsa, `@jdu.uz` bilan tugaydigan manzilni kiriting, ekranda ko‘rsatilgan manzilni tekshiring va `Yes` deb tasdiqlang. Email avval ro‘yxatdan o‘tgan bo‘lsa, u saqlanadi. Faqat manzilini tuzatishi kerak bo‘lgan talabalar yangilashdan keyin CloudShellda quyidagini bajaradi:

```bash
jdu-register --change-email
```

Yangilashdan so‘ng Ubuntuga ulanib, faqat kerakli topshiriqlarni qayta tekshiring. `jdu-check` natijani avtomatik ravishda o‘qituvchi tomoniga yuboradi. `jdu-my-progress` shaxsiy ko‘rish URLini bitta qatorda chiqaradi. URLni boshqalarga yubormang.

```bash
ssh jdu-ubuntu
command -v jdu-my-progress
jdu-check P0
jdu-my-progress
```

P3 yoki M3 uchun `REVIEW` ko‘rinsa, `script` to‘xtatilgan `process`larning eski holatini xavfsiz aniqlay olmagan bo‘ladi. Bajarilgan mashqlar avtomatik ravishda `reset` qilinmaydi. Faqat tugallanmagan topshiriq uchun Ubuntuda `jdu-reset P3` yoki `jdu-reset M3`ni bajaring.

## Bajarilmaydigan amallar

- O‘qituvchi yoki talabaning mavjud CloudFormation `stack`ini o‘chirish.
- Talabalarga dastlabki `install.sh`ni qayta ishga tushirishni buyurish.
- Oddiy yangilash paytida o‘qituvchining ro‘yxatdan o‘tkazish `key`ini almashtirish.
- Barcha talabalardan emailni qayta kiritishni talab qilish. Faqat kiritilmagan yoki noto‘g‘ri manzilni tuzating.

Dastlabki o‘rnatish ish boshlanishidan oldin `ROLLBACK_COMPLETE` holatida tugagan bo‘lsa, alohida tiklash tartibi kerak. Buni ishlayotgan guruhning Lab muhitini yangilash bilan aralashtirmang.
