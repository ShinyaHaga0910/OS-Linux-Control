# Ubuntu and OS Foundations — 自力課題 Mission Guide

対象: Mission 1～7
環境: Ubuntu Server 24.04 LTS
進め方: 授業回ではなく、学生ごとの進度でMissionを進める。

この文書は、commandを自分で選ぶ課題M1～M7である。完全なcommand手順が必要な場合は、先に[GUIDED_PRACTICE.md](GUIDED_PRACTICE.md)のP0～P6を実施する。

PとMは別のresourceを使う。Pを完了しても、対応するMはPASSにならない。推奨順序は`P0 → P1 → M1 → P2 → M2 → … → P6 → M6 → M7`である。旧M0は手順付き練習P0へ移した。統合課題M7には対応するPを設けない。

## 最初にUbuntuへ接続する

AWS Academy Learner Labのセットアップを完了してから、AWSコンソールでCloudShellを開く。CloudShellで次のcommandを実行し、自分のUbuntu演習サーバーへ接続する。

```bash
ssh jdu-ubuntu
```

接続後、Ubuntuで次を実行する。

```bash
id -un
```

`ssm-user`と表示されることを確認する。この文書のUbuntu側の操作は、この接続先で実行する。CloudShellで操作する課題では、課題中の指示に従って`exit`でCloudShellへ戻る。

## 共通操作

初回構築時に、すべてのMissionは自動で未完成の状態になる。最初にresetする必要はない。

### 実行user

Ubuntuへ接続した直後の管理userは`ssm-user`である。次のcommandで確認する。

```bash
id -un
```

`jdu-check`と`jdu-reset`は、必ず`ssm-user`で実行する。別のuserで実行すると、`ssm-user`へ戻る方法を表示して終了する。

演習用userは`jduops`、`jduviewer`、`jduwriter`である。`ssm-user`から演習用userへ切り替える例を示す。

```bash
sudo su - jduops
id
```

元の`ssm-user`へ戻る。

```bash
exit
id -un
```

この演習で切り替えるuserのうち、Passwordなしで`sudo`を使えるのは`ssm-user`だけである。例えば、`jduwriter`から`jduviewer`へ直接切り替えない。一度`exit`で`ssm-user`へ戻り、そこから`sudo su - jduviewer`を実行する。

`jduapp`、`jduweb`、`jdufinal`、`jduworker`はservice専用userである。Login shellは`nologin`であり、`su -`による対話loginは行わない。必要な確認は`ssm-user`から`sudo -u USER COMMAND`で1 commandだけ実行する。

現在のMissionを確認する。

```bash
jdu-check M1
```

教員のprogress serverが設定されている場合、現在の結果は自動送信される。全問PASSする前でも送信される。

`RESULT`はUbuntu上の課題判定である。`REPORT`はHTTPS送信の成否である。送信に失敗しても、課題のPASS/FAILは変わらない。自分の匿名server IDは次で確認できる。

```bash
jdu-progress id
```

通信を一時的に行わず、local判定だけを実行する場合は次を使う。

```bash
jdu-check M1 --no-submit
```

最初からやり直す場合だけ、そのMissionをresetする。

```bash
jdu-reset M1
```

reset直後は、すべての課題が`FAIL`になる。これは正常である。LabCheckは状態を修正しない。

## M1 Shell, path, file, and text

### 目的

相対pathと絶対pathを区別する。Directoryとfileを作る。Fileをコピーする。Logから必要な行を取り出す。

### 初期状態

`~/jdu-lab/m1/inbox`に素材がある。`case01`は未完成であり、`staging`に不要な`.tmp` fileがある。

### 課題

1. 次のdirectory treeを作る。

```text
~/jdu-lab/m1/case01/
├── config/
├── logs/
└── notes/
```

2. `inbox/config/app.conf`を`case01/config/app.conf`へコピーする。
3. `inbox/logs/incident.log`を`case01/logs/incident.log`へコピーする。
4. コピーした2 fileの内容を変更しない。
5. `case01`の中から`.tmp` fileをすべて除く。
6. `incident.log`から`ERROR`を含む完全な行だけを取り出し、`notes/errors.txt`へ保存する。行番号を付けない。
7. `incident.log`の最後の5行を順序を変えず、`notes/recent.txt`へ保存する。

### 判定

5項目を判定する。Directory、source file、`.tmp`、`errors.txt`、`recent.txt`がそれぞれ判定に対応する。

```bash
jdu-check M1
```

確認候補: `pwd`, `ls`, `tree`, `mkdir`, `cp`, `rm`, `find`, `grep`, `tail`

## M2 User, group, permission, and sudo

### 目的

User、primary group、supplementary groupを区別する。共有directoryへgroup accessとsetgidを設定する。

### 初期状態

`jduops`、`jduviewer`、`ops`は存在する。初期状態では、`jduviewer`だけがsupplementary group `ops`に誤って所属している。`jduops`は`ops`に所属していない。`/srv/jdu-share`と`README.txt`のowner、group、modeは未完成である。

### 課題

1. `jduops`をsupplementary group `ops`へ追加する。
2. `jduviewer`をsupplementary group `ops`から削除する。
3. `/srv/jdu-share`を`root:ops`にする。
4. `/srv/jdu-share`をmode `2775`にする。setgidを使う。world-writableにしない。
5. `/srv/jdu-share/README.txt`を`root:ops`、mode `664`にする。
6. `ssm-user`から`sudo su - jduops`で切り替える。共有directoryにfileを作る。新しいfileのgroupが`ops`になることも確認する。
7. `jduviewer`が`README.txt`を読めることを確認する。
8. `jduviewer`が共有directoryにfileを作れないことを確認する。

`jduops`での確認後は`exit`で`ssm-user`へ戻る。次に`sudo su - jduviewer`で切り替える。`jduviewer`での確認後も`exit`で戻る。最後に`id -un`が`ssm-user`であることを確認してから`jdu-check M2`を実行する。

### 判定

6課題を判定する。Group membership、directory owner/group、directory mode、sample file、group継承、viewer accessが対応する。

```bash
jdu-check M2
```

確認候補: `id`, `groups`, `getent passwd`, `getent group`, `stat`, `namei`, `chown`, `chmod`, `usermod`, `sudo -u`

禁止: `chmod 777`

## M3 Process and package

第8・9章と練習P3の両部分を終えてから取り組む。第10章では、サービスの起動と自動起動を詳しく学ぶ。

### 目的

Serviceとprocessを対応させる。PIDを指定してsignalを送る。Ubuntu packageを調査し、installする。

### 初期状態

`jdu-m3-process1.service`、`jdu-m3-process2.service`、`jdu-m3-process3.service`が通常のsystemd unitとして動いている。`cmatrix`は未installである。初期状態を確認するには、次を使う。

```bash
systemctl list-units --type=service 'jdu-m3-*'
systemctl status jdu-m3-process1.service jdu-m3-process2.service jdu-m3-process3.service
```

### 課題A: process2だけを停止する

1. `jdu-m3-process2.service`のMain PIDを調べる。
2. `ps`で同じPIDのprocessを確認する。
3. そのPIDだけへ`TERM`を送る。
4. `process2`が停止し、`process1`と`process3`が動いていることを確認する。

広い条件の`pkill`、`killall`、signal `KILL`は使わない。

### 課題B: cmatrixをinstallする

1. Package情報を確認する。
2. `apt`で`cmatrix`をinstallする。
3. Commandを実行する。終了は`Ctrl+C`とする。
4. Packageのversionと、`/usr/bin/cmatrix`を提供するpackageを確認する。

### 判定

2課題を判定する。課題A全体で1件、課題B全体で1件である。提出fileはない。

```bash
jdu-check M3
```

確認候補: `systemctl status`, `systemctl show`, `ps`, `kill`, `apt show`, `apt install`, `dpkg-query`, `command -v`, `dpkg -S`

## M4 systemd service

### 目的

Unit file、service、processの関係を確認する。Activeとenabledを区別する。

### 初期状態

教師が用意した`jdu-status.service`はloaded、inactive、disabledである。Unit fileは完成済みである。

### 課題

1. `systemctl cat jdu-status.service`で`User`、`WorkingDirectory`、`ExecStart`を読む。
2. Unit fileを変更せず、serviceをstartする。
3. Boot時にstartするようenableする。
4. Activeとenabledを別々に確認する。
5. Main PIDを調べ、実際のprocessと対応させる。
6. Processのuser、command line、working directoryがunitの指定と一致することを確認する。

### 判定

3課題を判定する。Active、enabled、変更されていないunitと実processの対応がそれぞれ課題になる。提出fileはない。

```bash
jdu-check M4
```

確認候補: `systemctl cat`, `systemctl start`, `systemctl enable`, `systemctl is-active`, `systemctl is-enabled`, `systemctl show`, `ps`, `/proc/PID/cmdline`, `/proc/PID/cwd`

## M5 Port, socket, and log

### 目的

Service、process、socket、IP address、port、HTTP、journalを一つの実行状態として関連付ける。

### 初期状態

教師が用意した`jdu-web.service`はloaded、inactive、disabledである。Unit fileとcontent fileは完成済みである。TCP 8081にはlistenerがない。

### 課題

1. Unit fileの`User`、`ExecStart`、address、port、content pathを読む。
2. Unit fileを変更せず、`jdu-web.service`をstartする。
3. `127.0.0.1:8081`で通信を待ち受けているsocketを確認する。この状態をlistener（待受socket）という。

```bash
sudo ss -lntp | grep ':8081'
```

4. `ss`の`users:`欄にあるPIDと、serviceのMain PIDを比較する。

```bash
systemctl show --property MainPID --value jdu-web.service
```
5. `0.0.0.0:8081`や`[::]:8081`でlistenしていないことを確認する。
6. `http://127.0.0.1:8081/`へrequestを送り、HTTP responseを確認する。
7. Service user `jduweb`がcontent fileを読めることを確認する。`jduweb`はlogin用userではないため、`su - jduweb`は使わない。実際のread可否は次で確認する。`0`はread可能、`1`はread不可を表す。

```bash
sudo -u jduweb -- test -r /srv/jdu-web/index.txt
echo $?
```

Userとgroupは`getent passwd jduweb`と`id jduweb`で確認する。Fileと親directoryのpermissionは`stat`と`namei -l /srv/jdu-web/index.txt`で確認する。
8. `http://127.0.0.1:8081/m5-check`へrequestを送る。
9. 現在のservice起動に対応するjournalで`REQUEST path=/m5-check`を確認する。
10. TCP 18081にlistenerがなく、HTTP requestが失敗することを確認する。

### 判定

4課題を判定する。ListenerとPID、HTTPとfile access、学生が送ったrequestのlog、open portとclosed portの比較が対応する。LabCheckが送る`/` requestは、学生の`/m5-check`を代行しない。

```bash
jdu-check M5
```

確認候補: `systemctl cat`, `systemctl start`, `systemctl show`, `sudo ss -lntp`, `curl`, `sudo -u`, `sudo journalctl`

## M6 SSH and remote operation

### 目的

CloudShellをlocal、Ubuntuをremoteとして区別する。SSH remote commandと`scp`のupload、downloadを使う。

### 初期状態

SSH鍵、alias `jdu-ubuntu`、Session Manager tunnelは構築済みである。これらは課題点に含めない。CloudShellとUbuntuのMission fileは存在しない。

### 課題

1. CloudShellで`id -un`、`hostname`、`pwd`を確認する。
2. `ssh jdu-ubuntu`またはSSH remote commandで、Ubuntu側の同じ3項目を確認する。
3. CloudShellの`~/jdu-lab/m6/local-source.txt`へ、次の一行だけを書く。

```text
JDU SSH transfer test
```

4. `scp`で、Ubuntuの`~/jdu-lab/m6/upload.txt`へuploadする。
5. SSH remote commandを使い、Ubuntuに`~/jdu-lab/m6/remote-result.txt`を作る。値を手入力しない。

```text
REMOTE_USER=<Ubuntuで取得したuser>
REMOTE_HOST=<Ubuntuで取得したhostname>
REMOTE_PATH=<Ubuntuで取得したhome directory>
```

6. `scp`で、Ubuntuの`remote-result.txt`をCloudShellの`~/jdu-lab/m6/downloaded-result.txt`へdownloadする。
7. Upload元と先、download元と先を`sha256sum`で比較する。

### 判定

Ubuntu側は2課題を判定する。UbuntuへSSHで入った状態で実行する。この結果はDashboardの`M6 Ubuntu`へ送られる。

```bash
jdu-check M6
```

CloudShell側は4課題を判定する。Ubuntuから`exit`してCloudShellへ戻った後に実行する。この結果はDashboardの`M6 CloudShell`へ送られる。

```bash
jdu-check M6
```

DashboardのM6欄は、Ubuntu `2/2`、CloudShell `4/4`、合計`6/6`を別々に表示する。M6のMission完了は両方が全件PASSになった時点である。どちらか一方だけを再実行しても、もう一方の最新結果は保持される。

両方で全件`PASS`にする。秘密鍵を表示、提出、移動しない。SSH service、SSH設定、`authorized_keys`を変更しない。

確認候補: `ssh`, `scp`, `sha256sum`, `id`, `hostname`, `pwd`, `printf`

## M7 Integrated Ubuntu check

### 目的

M2、M4、M5の知識を、新しいserviceへ自力で適用する。新しいcommandは追加しない。

### 初期状態

- 教師配布の`jdu-final.service`はloaded、inactive、disabledである。
- `/srv/jdu-final`と`index.txt`は存在しない。
- `jduwriter`と`jduviewer`は`finalops`に所属していない。

### 課題

1. `systemctl cat jdu-final.service`で`User`、`WorkingDirectory`、`ExecStart`を読む。
2. `/srv/jdu-final`を`root:finalops`、mode `2775`で作る。
3. `/srv/jdu-final/index.txt`を作る。内容は`/etc/jdu-lab/final-marker`と同じ一行にする。
4. `index.txt`を`root:finalops`、mode `664`にする。
5. `jduwriter`を`finalops`へ追加する。`jduviewer`は追加しない。
6. Writerがcontentを更新でき、viewerが更新できないことを確認する。
7. Unit fileを変更せず、serviceをstartしてenableする。
8. Serviceが`jdufinal`で動き、`127.0.0.1:8090`だけでlistenすることを確認する。
9. HTTP responseがstatus 200で、指定markerを返すことを確認する。
10. `http://127.0.0.1:8090/m7-check`へrequestを送る。
11. 現在のservice起動に対応するjournalで`REQUEST path=/m7-check`を確認する。

Userを切り替える場合は、`ssm-user`から`sudo su - jduwriter`または`sudo su - jduviewer`を使う。各確認後は`exit`で`ssm-user`へ戻る。最後に`id -un`を確認してから`jdu-check M7`を実行する。

### 判定

6課題を判定する。File構成、writer/viewer、service、socket、HTTP、journalが対応する。Unit file、SSH設定、LabCheckを変更しない。

```bash
jdu-check M7
```

確認候補: `id`, `getent`, `stat`, `chown`, `chmod`, `systemctl`, `ps`, `sudo ss -lntp`, `curl`, `sudo journalctl`

## 安全上の禁止事項

- `chmod 777`を使わない。
- `/etc/ssh/sshd_config`を変更しない。
- `ssh.service`を停止しない。
- `killall`または広い条件の`pkill`を使わない。
- 秘密鍵を表示、提出、Gitへ追加しない。
- 外部hostへscanまたはlogin試行をしない。
