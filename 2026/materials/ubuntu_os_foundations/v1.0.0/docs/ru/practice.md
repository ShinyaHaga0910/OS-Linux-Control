# Основы Ubuntu и ОС — пошаговые упражнения

[日本語](../ja/practice.md) · [Русский](../ru/practice.md) · [O‘zbekcha](../uz/practice.md)

> Этот перевод пока не отражает действующие формулировки и шаги P0–P6. Для заданий, которые проверяет Lab, используйте актуальную японскую версию в репозитории OS-Linux-Control.

Упражнения: P1–P6.

Среда: Ubuntu Server 24.04 LTS.
После каждого P самостоятельно решайте Mission M, используя те же навыки.

## 0. Общие правила

P1–P6 предназначены для тренировки. Они используют другие каталоги, учётные записи, группы, службы и порты, чем M1–M6. M7 — итоговое задание, поэтому отдельной пошаговой практики для него нет.

В Ubuntu выполните команду и убедитесь, что показано `ssm-user`:

```bash
id -un
```

Если показано другое имя, один раз выполните `exit` и проверьте снова:

```bash
exit
id -un
```

Перед каждым действием переходите в указанный рабочий каталог, затем подтверждайте текущее место через `pwd`.

Запуск проверки:

```bash
jdu-check P1
```

Сброс нужен только для начала упражнения заново:

```bash
jdu-reset P1
```

## P1. Оболочка, путь, файл и текст

### Что изучаем

- Различие между домашним и рабочим каталогами.
- Создание каталогов.
- Копирование файлов.
- Сохранение нужных строк из журнала.

### Шаг 1. Перейдите в домашний каталог

```bash
cd ~
pwd
```

Убедитесь, что показано `/home/ssm-user`.

### Шаг 2. Перейдите в каталог P1

```bash
cd ~/jdu-lab/p1
pwd
tree
```

Найдите `inbox` и незавершённый `practice01`.

### Шаг 3. Создайте нужные каталоги

```bash
cd ~/jdu-lab/p1
mkdir -p practice01/config
mkdir -p practice01/logs
mkdir -p practice01/notes
tree practice01
```

### Шаг 4. Скопируйте файл настройки

Сначала перейдите в каталог назначения:

```bash
cd ~/jdu-lab/p1/practice01/config
pwd
cp ../../inbox/config/training.conf .
ls -l
```

`.` означает текущий каталог.

### Шаг 5. Скопируйте файл журнала

```bash
cd ~/jdu-lab/p1/practice01/logs
pwd
cp ../../inbox/logs/practice.log .
ls -l
```

### Шаг 6. Найдите и удалите временные файлы

Перейдите в `practice01`:

```bash
cd ~/jdu-lab/p1/practice01
pwd
find . -type f -name '*.tmp' -print
find . -type f -name '*.tmp' -delete
find . -type f -name '*.tmp' -print
```

Последняя команда ничего не должна вывести.

### Шаг 7. Сохраните строки WARN

Перейдите в каталог результата `notes`:

```bash
cd ~/jdu-lab/p1/practice01/notes
pwd
grep 'WARN' ../logs/practice.log > warnings.txt
cat warnings.txt
```

### Шаг 8. Сохраните последние четыре строки

```bash
cd ~/jdu-lab/p1/practice01/notes
tail -n 4 ../logs/practice.log > recent.txt
cat recent.txt
```

### Шаг 9. Проверьте результат целиком

```bash
cd ~/jdu-lab/p1
tree practice01
stat -c '%U:%G %a %n' practice01 practice01/config/training.conf practice01/logs/practice.log practice01/notes/warnings.txt practice01/notes/recent.txt
jdu-check P1
```

Когда все шесть пунктов покажут PASS, переходите к M1.

## P2. Пользователи, группы, права и setgid

### Что изучаем

- Проверка основной и дополнительных групп.
- Настройка групповых прав на общий каталог.
- Наследование группы новым файлом с помощью setgid.

### Шаг 1. Проверьте управляющего пользователя

```bash
cd ~
id -un
id
```

### Шаг 2. Проверьте начальное членство в группе

```bash
getent group practiceops
id jdupracticewriter
id jdupracticeviewer
```

Изначально `jdupracticeviewer` входит в `practiceops`, а `jdupracticewriter` — нет.

### Шаг 3. Исправьте членство

```bash
cd ~
sudo usermod -aG practiceops jdupracticewriter
sudo gpasswd -d jdupracticeviewer practiceops
getent group practiceops
id jdupracticewriter
id jdupracticeviewer
```

### Шаг 4. Настройте общий каталог

```bash
cd /srv
pwd
sudo chown root:practiceops jdu-practice-share
sudo chmod 2775 jdu-practice-share
stat -c '%U:%G %a %n' jdu-practice-share
```

### Шаг 5. Настройте GUIDE.txt

Перейдите в каталог файла:

```bash
cd /srv/jdu-practice-share
pwd
sudo chown root:practiceops GUIDE.txt
sudo chmod 664 GUIDE.txt
stat -c '%U:%G %a %n' GUIDE.txt
```

### Шаг 6. Переключитесь на writer и создайте файл

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

В конце должно появиться `ssm-user`.

### Шаг 7. Проверьте чтение и запись под viewer

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

`cat` должен сработать, а `touch` — завершиться сообщением `Permission denied`. Это ожидаемый отказ.

### Шаг 8. Запустите проверку

```bash
cd ~
id -un
jdu-check P2
```

Когда все шесть пунктов покажут PASS, переходите к M2.

## P3. Процесс и пакет

После главы 8 выполните шаги 1–4: изучите и остановите процесс. Затем прочитайте главу 9 и выполните шаги 5–6: установите пакет. Только после обеих частей запускайте `jdu-check P3`.

### Что изучаем

- Сопоставление службы systemd с PID процесса.
- Отправка сигнала TERM определённому PID.
- Установка пакета через `apt`.

### Шаг 1. Проверьте три службы

```bash
cd ~
systemctl list-units --type=service 'jdu-p3-*'
systemctl status jdu-p3-process1.service --no-pager
systemctl status jdu-p3-process2.service --no-pager
systemctl status jdu-p3-process3.service --no-pager
```

### Шаг 2. Покажите Main PID процесса 2

```bash
systemctl show --property MainPID --value jdu-p3-process2.service
```

### Шаг 3. Сохраните PID в переменной оболочки

```bash
P3_PID=$(systemctl show --property MainPID --value jdu-p3-process2.service)
printf '%s\n' "$P3_PID"
ps -fp "$P3_PID"
```

### Шаг 4. Отправьте TERM только процессу 2

```bash
sudo kill -TERM "$P3_PID"
systemctl is-active jdu-p3-process1.service
systemctl is-active jdu-p3-process2.service
systemctl is-active jdu-p3-process3.service
```

Результаты по порядку: `active`, `inactive`, `active`.

### Шаг 5. Изучите и установите figlet

```bash
cd ~
apt show figlet
sudo apt update
sudo apt install -y figlet
command -v figlet
figlet JDU
```

### Шаг 6. Сопоставьте пакет и команду

```bash
dpkg-query -W -f='${Status} ${Version}\n' figlet
dpkg -S /usr/bin/figlet
jdu-check P3
```

Когда оба пункта покажут PASS, переходите к M3.

## P4. Служба systemd

### Что изучаем

- Чтение файла юнита.
- Раздельная настройка `active` и `enabled`.
- Сопоставление Main PID с настоящим процессом.

### Шаг 1. Прочитайте файл юнита

```bash
cd ~
systemctl cat jdu-practice-status.service
```

Найдите `User`, `WorkingDirectory`, `ExecStart`.

### Шаг 2. Проверьте начальное состояние

```bash
systemctl is-active jdu-practice-status.service
systemctl is-enabled jdu-practice-status.service
```

### Шаг 3. Запустите службу

```bash
sudo systemctl start jdu-practice-status.service
systemctl is-active jdu-practice-status.service
```

### Шаг 4. Включите автозапуск при загрузке

```bash
sudo systemctl enable jdu-practice-status.service
systemctl is-enabled jdu-practice-status.service
```

### Шаг 5. Проверьте Main PID и процесс

```bash
P4_PID=$(systemctl show --property MainPID --value jdu-practice-status.service)
printf '%s\n' "$P4_PID"
ps -fp "$P4_PID"
sudo cat "/proc/$P4_PID/cmdline" | tr '\0' ' '
printf '\n'
sudo readlink -f "/proc/$P4_PID/cwd"
```

### Шаг 6. Запустите проверку

```bash
cd ~
jdu-check P4
```

Когда все три пункта покажут PASS, переходите к M4.

## P5. Порт, сокет, HTTP и журнал

### Что изучаем

- Связь службы, процесса и ожидающего сокета.
- Чтение IP-адреса и порта.
- Проверка записи HTTP-запроса в журнале.

### Шаг 1. Прочитайте юнит

```bash
cd ~
systemctl cat jdu-practice-web.service
```

Найдите `127.0.0.1`, `8181`, `jdupracticeweb` и путь к файлу содержимого.

### Шаг 2. Запустите службу

```bash
sudo systemctl start jdu-practice-web.service
systemctl is-active jdu-practice-web.service
```

### Шаг 3. Проверьте ожидающий сокет

```bash
sudo ss -lntp | grep ':8181'
```

Найдите `127.0.0.1:8181`. Убедитесь, что нет ожидания на `0.0.0.0:8181` или `[::]:8181`. Первый адрес принимает соединения лишь внутри данного хоста, два последних обозначали бы ожидание на всех адресах.

### Шаг 4. Сравните PID сокета и Main PID

```bash
systemctl show --property MainPID --value jdu-practice-web.service
sudo ss -lntp | grep ':8181'
```

Проверьте совпадение двух PID.

### Шаг 5. Проверьте HTTP-ответ

```bash
curl -i http://127.0.0.1:8181/
```

### Шаг 6. Проверьте чтение от имени пользователя службы

Перейдите в каталог содержимого:

```bash
cd /srv/jdu-practice-web
pwd
stat -c '%U:%G %a %n' index.txt
namei -l /srv/jdu-practice-web/index.txt
id jdupracticeweb
sudo -u jdupracticeweb -- test -r index.txt
echo $?
```

Последнее значение `0` означает разрешённое чтение.

### Шаг 7. Отправьте запрос для студента

```bash
curl -i http://127.0.0.1:8181/p5-check
sudo journalctl -u jdu-practice-web.service --no-pager -n 20
```

Найдите `REQUEST path=/p5-check`.

### Шаг 8. Сравните с закрытым портом

```bash
curl --max-time 2 http://127.0.0.1:18181/
sudo ss -lnt | grep ':18181'
```

Ни одна команда не покажет успешное соединение или ожидающий сокет: TCP-порт 18181 закрыт.

### Шаг 9. Запустите проверку

```bash
cd ~
jdu-check P5
```

Когда все четыре пункта покажут PASS, переходите к M5.

## P6. SSH, удалённая команда и scp

### Что изучаем

- Различие между CloudShell и Ubuntu.
- Загрузка и скачивание файлов через `scp`.
- Выполнение удалённой команды SSH.

### Шаг 1. Вернитесь из Ubuntu в CloudShell

В приглашении Ubuntu выполните:

```bash
exit
```

Затем в CloudShell проверьте среду:

```bash
cd ~
pwd
id -un
hostname
```

### Шаг 2. Создайте рабочий каталог в CloudShell

```bash
mkdir -p ~/jdu-lab/p6
cd ~/jdu-lab/p6
pwd
```

### Шаг 3. Создайте файл для отправки

```bash
printf '%s\n' 'JDU SSH guided transfer' > practice-source.txt
cat practice-source.txt
sha256sum practice-source.txt
```

### Шаг 4. Создайте каталог в Ubuntu

Выполните из CloudShell:

```bash
ssh jdu-ubuntu 'mkdir -p ~/jdu-lab/p6'
```

### Шаг 5. Загрузите файл в Ubuntu

Выполните из каталога P6 в CloudShell:

```bash
cd ~/jdu-lab/p6
scp practice-source.txt jdu-ubuntu:~/jdu-lab/p6/practice-upload.txt
ssh jdu-ubuntu 'sha256sum ~/jdu-lab/p6/practice-upload.txt'
sha256sum practice-source.txt
```

Убедитесь, что два значения SHA-256 совпадают.

### Шаг 6. Создайте файл результата удалённой командой

Из CloudShell выполните следующую одну команду без изменений:

```bash
ssh jdu-ubuntu 'cd ~/jdu-lab/p6 && printf "REMOTE_USER=%s\nREMOTE_HOST=%s\nREMOTE_PATH=%s\n" "$(id -un)" "$(hostname)" "$HOME" > practice-remote-result.txt'
```

Посмотрите содержимое на удалённой стороне:

```bash
ssh jdu-ubuntu 'cat ~/jdu-lab/p6/practice-remote-result.txt'
```

### Шаг 7. Проверьте сторону Ubuntu

Подключитесь к Ubuntu:

```bash
ssh jdu-ubuntu
cd ~/jdu-lab/p6
pwd
ls -l
jdu-check P6
exit
```

Два пункта Ubuntu должны показать PASS.

### Шаг 8. Скачайте файл результата

Выполните в CloudShell:

```bash
cd ~/jdu-lab/p6
scp jdu-ubuntu:~/jdu-lab/p6/practice-remote-result.txt practice-downloaded-result.txt
cat practice-downloaded-result.txt
sha256sum practice-downloaded-result.txt
ssh jdu-ubuntu 'sha256sum ~/jdu-lab/p6/practice-remote-result.txt'
```

Проверьте совпадение двух значений SHA-256.

### Шаг 9. Проверьте сторону CloudShell

```bash
cd ~/jdu-lab/p6
jdu-check P6
```

После PASS всех четырёх пунктов CloudShell переходите к M6.

## Порядок обучения

Номера глав не соответствуют занятиям один к одному. Переходите к упражнениям по мере понимания и при необходимости возвращайтесь к объяснениям.

- Прочитайте главы 1–3 и начало главы 4 о редактировании; затем наблюдайте реальную ОС в M0.
- После глав 4 и 5 выполните P1 и M1.
- После глав 6 и 7 выполните P2 и M2.
- После главы 8 выполните шаги 1–4 P3. После главы 9 — шаги 5–6 P3, затем M3.
- После главы 10 выполните P4 и M4; после главы 11 — P5 и M5.
- После главы 12 выполните P6 и M6, затем объедините изученное в M7.

Рекомендуемая последовательность всей практики:

```text
P1 → M1 → P2 → M2 → P3 → M3 → P4 → M4
   → P5 → M5 → P6 → M6 → M7 (итоговое задание)
```

В P можно следовать написанным командам. В M1–M6 выбирайте команды самостоятельно, не подсматривая шаги P. В M7 объединяются навыки M2, M4 и M5.
