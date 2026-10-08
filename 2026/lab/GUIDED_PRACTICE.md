# Ubuntu and OS Foundations — 練習課題と解答例

対象: 練習課題P0～P6

環境: Ubuntu Server 24.04 LTS

進め方: まず各Pの「課題」を読む。自分で試した後、「解答例」の手順で操作と考え方を確認する。同じ技能を使うMission Mは自力で解く。

## 最初にUbuntuへ接続する

AWS Academy Learner Labのセットアップを完了してから、AWSコンソールでCloudShellを開く。CloudShellで次を実行して、自分のUbuntu演習サーバーへ接続する。

```bash
ssh jdu-ubuntu
```

P0～P5は、接続先のUbuntuで進める。CloudShell側の操作が必要なP6では、手順中に実行場所を示す。

## 0. 共通ルール

P0～P6は練習用である。P0はOSの観察を手順付きで行う導入練習である。M1～M6とは別のdirectory、user、group、service、portを使う。M7は統合課題であるため、対応する練習課題を設けない。

各Pには、最初に問題文、その後に解答例を置く。問題文だけを読んで解いてもよい。解答例の手順を見ながら進めてもよい。PとMの採点対象は別であり、PのPASSはMのPASSにならない。

Ubuntuで次を実行する。表示が`ssm-user`であることを確認する。

```bash
id -un
```

別のuser名が表示された場合は、`exit`を1回実行する。もう一度確認する。

```bash
exit
id -un
```

各手順では、最初に作業directoryへ移動する。移動後に`pwd`で現在地を確認する。

Ubuntu側の判定は、`ssm-user`で次の形で実行する。P6のCloudShell側の判定は、その環境で実行する。

```bash
jdu-check P1
```

判定は課題の完成状態を調べる。観察しただけの操作や途中の操作は、判定項目に含まれない場合がある。判定結果は設定済みの教員用進捗画面へ自動送信される。送信できなくても、UbuntuまたはCloudShell上のPASS/FAILは確認できる。

最初からやり直す場合だけresetする。

```bash
jdu-reset P1
```

## P0 Environment and OS

### 学ぶこと

- UbuntuというOSとLinux kernelの情報を区別する。
- 現在のユーザー、ホスト名、PID 1のプロセスを実機で確認する。
- コマンドの結果をファイルへ記録し、保存・確認・提出する。

### 課題

自分のUbuntu演習サーバーから6項目を調べ、`~/jdu-lab/p0/observation.env`へ記録する。以前のM0を、手順付き練習P0に変更したものである。値は以下の例や他の学生からコピーせず、自分のサーバーの表示を使う。6項目を`jdu-check P0`で確認する。

### 解答例（操作手順）

#### 手順1: 接続先とユーザーを確認する

この資料の冒頭のとおり、CloudShellで`ssh jdu-ubuntu`を実行する。以下の手順はすべて接続先のUbuntuで行う。

```bash
cd ~
pwd
id -un
```

`id -un`の表示が`ssm-user`であることを確認する。これが後で記録する`USER_NAME`である。以降の表示はメモしておく。

#### 手順2: OSの種類とバージョンを確認する

```bash
cat /etc/os-release
```

`ID=`の値を`OS_ID`、`VERSION_ID=`の値を`OS_VERSION_ID`としてメモする。`NAME`や`PRETTY_NAME`とは異なる項目である。表示に引用符がある場合は、値だけを記録し、引用符は付けない。

#### 手順3: Linux kernelのバージョンを確認する

```bash
uname -r
```

`-r`はkernelのreleaseを表示する指定である。表示された文字列全体を`KERNEL_RELEASE`としてメモする。OSのバージョンとkernelのバージョンは別の情報である。

#### 手順4: PID 1のプロセス名を確認する

```bash
cat /proc/1/comm
```

`/proc`には実行中のシステムの情報が公開されている。`1`はプロセス番号（PID）、`comm`はそのプロセスの名前を確認するファイルである。表示を`PID1_COMM`としてメモする。

#### 手順5: ユーザー名とホスト名を確認する

```bash
id -un
hostname
```

1つ目を`USER_NAME`、2つ目を`HOST_NAME`としてメモする。ホスト名はサーバーを識別する名前であり、ユーザー名や提出用Server IDとは別である。

#### 手順6: 記録用ファイルを作成する

```bash
cd ~
mkdir -p jdu-lab/p0
cd jdu-lab/p0
pwd
nano observation.env
```

`nano`が開いたら、次の6行を入力し、それぞれの`=`の右にメモした値を入れる。この枠は編集するファイルの内容であり、コマンドとして実行しない。

```text
OS_ID=
OS_VERSION_ID=
KERNEL_RELEASE=
PID1_COMM=
USER_NAME=
HOST_NAME=
```

各項目を1行にし、項目名や`=`の前後に空白を入れない。値に引用符は付けない。`Ctrl+O`で保存し、ファイル名が`observation.env`であることを確認して`Enter`を押す。`Ctrl+X`でエディタを閉じる。

#### 手順7: 保存した内容を確認する

```bash
pwd
ls -l observation.env
cat observation.env
```

6行すべてに値があり、手順1～5の出力と一致するか確認する。空欄や誤記があれば`nano observation.env`で修正し、再び保存する。

#### 手順8: 判定・提出する

```bash
id -un
jdu-check P0
```

6件すべてが`PASS`、結果が`6 / 6 checks cleared`になればP0の記録は完成である。`FAIL`なら指摘された項目の実機情報を再確認し、ファイルを修正して再実行する。何度でも実行できる。

`RESULT`は課題の判定、`REPORT`は教員サーバーへの送信結果である。送信に失敗した場合はファイルを消したりresetしたりせず、通信・登録の状態を確認して再実行する。

#### 手順9: 次の練習へ進む

```bash
cd ~
```

P1へ進む。CloudShellへ戻りたい場合だけ`exit`を実行する。初回のP0ではreset不要である。P0の記録を消してやり直す場合だけ、Ubuntuで`jdu-reset P0`を実行する。

## P1 Shell、path、file、text

### 学ぶこと

- Home directoryと作業directoryを区別する。
- Directoryを作る。
- Fileをコピーする。
- Logから必要な行を保存する。

### 課題

`~/jdu-lab/p1/inbox`に設定ファイルとログがある。`~/jdu-lab/p1/practice01`は未完成で、不要な`.tmp`ファイルが残っている。次の状態に仕上げる。

1. `practice01`の下に`config`、`logs`、`notes`の3つのディレクトリを作る。
2. `inbox/config/training.conf`を`practice01/config/training.conf`へ、`inbox/logs/practice.log`を`practice01/logs/practice.log`へコピーする。元ファイルとコピーの内容を変えない。
3. `practice01`以下の`.tmp`ファイルをすべて削除する。それ以外のファイルは消さない。
4. 完成した`practice01`以下のディレクトリとファイルの所有者を、Ubuntuの管理ユーザー`ssm-user`にする。
5. コピーしたログから`WARN`を含む行だけを、行番号を付けずに`practice01/notes/warnings.txt`へ保存する。
6. 同じログの最後の4行を、元の順序で`practice01/notes/recent.txt`へ保存する。

完成状態を`jdu-check P1`で判定する。6項目すべてがPASSなら終了する。

### 解答例（操作手順）

#### 手順1: Home directoryへ移動する

```bash
cd ~
pwd
```

表示が`/home/ssm-user`であることを確認する。

#### 手順2: P1 directoryへ移動する

```bash
cd ~/jdu-lab/p1
pwd
tree
```

`inbox`と、未完成の`practice01`を確認する。

#### 手順3: 必要なdirectoryを作る

```bash
cd ~/jdu-lab/p1
mkdir -p practice01/config
mkdir -p practice01/logs
mkdir -p practice01/notes
tree practice01
```

#### 手順4: Config fileをコピーする

コピー先のdirectoryへ移動する。

```bash
cd ~/jdu-lab/p1/practice01/config
pwd
cp ../../inbox/config/training.conf .
ls -l
```

`.`は現在のdirectoryを表す。

#### 手順5: Log fileをコピーする

```bash
cd ~/jdu-lab/p1/practice01/logs
pwd
cp ../../inbox/logs/practice.log .
ls -l
```

#### 手順6: 一時fileを確認して削除する

`practice01`へ移動し、削除前の構成を確認する。

```bash
cd ~/jdu-lab/p1/practice01
pwd
tree
```

`tree`の表示から、`staging`の中にある`training.conf.tmp`と`practice.log.tmp`を探す。次に、同じ2つのfileを`find`で検索する。

```bash
find . -type f -name '*.tmp' -print
```

`.`は現在のdirectoryから探す指定、`-type f`は通常のfileだけを対象にする条件、`-name '*.tmp'`は名前が`.tmp`で終わる条件、`-print`は一致したパスを表示する指示である。`'*.tmp'`を引用符で囲む理由を含め、詳しい読み方は巻末の参照資料で説明する。

`./staging/training.conf.tmp`と`./staging/practice.log.tmp`が表示されることを確認する。表示順は問わない。検索結果と`tree`の構成を照合したら、この2つの不要なfileを`rm`で削除する。

```bash
rm staging/training.conf.tmp staging/practice.log.tmp
tree
```

削除後の`tree`で、2つの`.tmp`ファイルが表示されないことを確認する。コピーした`config/training.conf`と`logs/practice.log`が残っていることも確認する。

#### 手順7: WARN行を確認して保存する

出力先の`notes`へ移動する。まず、`grep`の結果を画面で確認する。

```bash
cd ~/jdu-lab/p1/practice01/notes
pwd
grep 'WARN' ../logs/practice.log
```

`WARN`を含む行だけが表示されることを確認する。次に、同じcommandに`>`を追加して、結果を`warnings.txt`へ保存する。`>`は出力先を画面からfileへ変更し、同名のfileがあれば内容を上書きする。

```bash
grep 'WARN' ../logs/practice.log > warnings.txt
cat warnings.txt
```

`cat`で、先ほど画面に表示された行が保存されていることを確認する。

#### 手順8: 最後の4行を確認して保存する

まず、`tail`の結果を画面で確認する。

```bash
cd ~/jdu-lab/p1/practice01/notes
tail -n 4 ../logs/practice.log
```

ログの最後の4行が、元の順序で表示されることを確認する。次に、`>`を追加して結果を`recent.txt`へ保存する。

```bash
tail -n 4 ../logs/practice.log > recent.txt
cat recent.txt
```

`cat`で、先ほど画面に表示された4行が保存されていることを確認する。

#### 手順9: 全体を確認する

```bash
cd ~/jdu-lab/p1
tree practice01
jdu-check P1
```

全6件がPASSになったら、M1へ進む。

## P2 User、group、permission、setgid

### 学ぶこと

- Primary groupとsupplementary groupを確認する。
- 共有directoryへgroup permissionを設定する。
- setgidで新しいfileのgroupを継承する。

### 課題

共有ディレクトリ`/srv/jdu-practice-share`を、書き込み担当者と閲覧担当者で使い分ける。初期状態では、`jdupracticeviewer`が補助グループ`practiceops`に入っており、書き込み担当の`jdupracticewriter`は入っていない。ディレクトリと`GUIDE.txt`の所有者・グループ・権限も未完成である。

1. `jdupracticewriter`を補助グループ`practiceops`に追加し、`jdupracticeviewer`をそのグループから削除する。
2. `/srv/jdu-practice-share`の所有者とグループを`root:practiceops`、権限を`2775`にする。新しいファイルが共有グループを引き継ぐようにする。
3. `GUIDE.txt`の所有者とグループを`root:practiceops`、権限を`664`にする。
4. `ssm-user`から`jdupracticewriter`へ切り替えて、共有ディレクトリに`writer-created.txt`を作る。新しいファイルのグループが`practiceops`であることを確認する。
5. `ssm-user`に戻り、`jdupracticeviewer`へ切り替える。`GUIDE.txt`は読めるが、共有ディレクトリに新しいファイルは作れないことを確認する。

異なるユーザーでの操作を終えたら`ssm-user`へ戻り、`jdu-check P2`を実行する。グループ所属、ディレクトリ、ファイル、作成時のグループ継承、閲覧担当者のアクセスを計6項目で判定する。

### 解答例（操作手順）

#### 手順1: 管理userを確認する

```bash
cd ~
id -un
id
```

#### 手順2: 初期groupを確認する

```bash
getent group practiceops
id jdupracticewriter
id jdupracticeviewer
```

初期状態では`jdupracticeviewer`が`practiceops`に入り、`jdupracticewriter`が入っていない。

#### 手順3: Group membershipを修正する

```bash
cd ~
sudo usermod -aG practiceops jdupracticewriter
sudo gpasswd -d jdupracticeviewer practiceops
getent group practiceops
id jdupracticewriter
id jdupracticeviewer
```

#### 手順4: 共有directoryを設定する

```bash
cd /srv
pwd
ls -ld jdu-practice-share
```

変更前の権限・所有者・所有グループを確認する。`ls -l`は詳細表示、`-d`はディレクトリの中身ではなくディレクトリ自体を表示する指定である。表示の先頭が権限、その後のリンク数に続く2列が所有者と所有グループである。

```bash
sudo chown root:practiceops jdu-practice-share
ls -ld jdu-practice-share
sudo chmod 2775 jdu-practice-share
ls -ld jdu-practice-share
```

`chown`の後は所有者・所有グループが`root practiceops`、`chmod`の後は権限が`drwxrwsr-x`になることを確認する。グループの実行権限の位置にある`s`はsetgidを表し、このディレクトリ内に作るファイルが所有グループを引き継ぐ。

#### 手順5: GUIDE.txtを設定する

対象directoryへ移動する。

```bash
cd /srv/jdu-practice-share
pwd
ls -l GUIDE.txt
```

変更前のファイルの権限・所有者・所有グループを確認してから設定する。

```bash
sudo chown root:practiceops GUIDE.txt
ls -l GUIDE.txt
sudo chmod 664 GUIDE.txt
ls -l GUIDE.txt
```

所有者・所有グループが`root practiceops`、権限が`-rw-rw-r--`になることを確認する。所有者と所有グループには読み書き、その他のユーザーには読み取りだけを許可している。

#### 手順6: Writerへ切り替えてfileを作る

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

最後に`ssm-user`と表示されることを確認する。

#### 手順7: Viewerのreadとwriteを確認する

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

`cat`は成功する。`touch`は`Permission denied`になる。これは想定した失敗である。

`jdupracticeviewer`は所有者の`root`ではなく、手順3で`practiceops`からも外したため、「その他のユーザー」の権限が適用される。`GUIDE.txt`はその他のユーザーにも読み取り権限（`r--`）があるので、`cat`で読める。一方、共有ディレクトリのその他のユーザーの権限は`r-x`で、書き込み権限（`w`）がない。新しいファイルを作るには、そのファイルを置くディレクトリへの書き込み権限と実行権限が必要なので、`touch`による作成は拒否される。

#### 手順8: 採点する

```bash
cd ~
id -un
jdu-check P2
```

全6件がPASSになったら、M2へ進む。

## P3 Processとpackage

第8章を読んだら手順1～4でプロセスを確認・停止する。続いて第9章を読み、手順5でパッケージを導入する。

### 学ぶこと

- systemd serviceとprocessのPIDを対応させる。
- Main PIDを`ps`で照合し、対象のserviceを停止する。
- `apt`でpackageをinstallする。

### 課題

初期状態で`jdu-p3-process1.service`、`jdu-p3-process2.service`、`jdu-p3-process3.service`が動いている。`figlet`は未インストールである。次のAとBの両方を完了する。

**課題A - process2だけを停止する。** `jdu-p3-process2.service`のMain PIDを調べ、そのPIDのプロセスを`ps`で確かめる。対象のserviceを`systemctl stop`で停止する。`process2`だけが停止し、`process1`と`process3`は動いたままにする。

**課題B - パッケージを導入する。** `figlet`のパッケージ情報を調べ、`apt`でインストールする。コマンドを1回実行する。

`jdu-check P3`でAとBを各1項目、計2項目として判定する。調査時のコマンド履歴やメモは提出しない。

### 解答例（操作手順）

#### 手順1: 3 serviceを確認する

```bash
cd ~
systemctl list-units --type=service 'jdu-p3-*'
systemctl status jdu-p3-process1.service --no-pager
systemctl status jdu-p3-process3.service --no-pager
```

#### 手順2: Process2のMain PIDを読む

```bash
systemctl status jdu-p3-process2.service
```

`Main PID:`の右に出る番号を手元にメモする。ページャーが開いた場合は`q`で終了する。

#### 手順3: メモしたPIDのprocessを見る

例えば、メモした番号が`1234`なら次のように入力する。`1234`を自分の画面の番号に置き換える。

```bash
ps -fp 1234
```

`PID`、`USER`、`CMD`を確認する。

#### 手順4: Process2のserviceを停止する

```bash
sudo systemctl stop jdu-p3-process2.service
systemctl is-active jdu-p3-process1.service
systemctl is-active jdu-p3-process2.service
systemctl is-active jdu-p3-process3.service
```

順に`active`、`inactive`、`active`になる。

#### 手順5: figletを調査してinstallする

```bash
cd ~
apt show figlet
sudo apt update
sudo apt install -y figlet
command -v figlet
figlet JDU
jdu-check P3
```

`figlet JDU`は文字を表示した後、自動で終了してプロンプトへ戻る。`jdu-check P3`は課題A・Bを各1件として判定する。

全2件がPASSになったら、M3へ進む。

## P4 systemd service

### 学ぶこと

- Unit fileを読む。
- Activeとenabledを別々に設定する。
- `User`、`WorkingDirectory`、`ExecStart`をunitの設定として読む。

### 課題

`jdu-practice-status.service`のユニットファイルは完成しているが、サービスは停止中で、自動起動も無効である。ユニットファイルを変更せずに次を行う。

1. ユニットファイルの`User`、`WorkingDirectory`、`ExecStart`を調べる。
2. サービスを起動し、現在の状態が`active`であることを確認する。
3. 起動時の自動実行を有効にし、`enabled`であることを確認する。`active`と`enabled`は別の状態として調べる。
`jdu-check P4`は、変更されていないユニットの稼働状態と自動起動を計2項目で判定する。観察結果を別ファイルへ提出する必要はない。

### 解答例（操作手順）

#### 手順1: Unit fileを読む

```bash
cd ~
systemctl cat jdu-practice-status.service
```

`User`、`WorkingDirectory`、`ExecStart`を確認する。

#### 手順2: 初期状態を確認する

```bash
systemctl is-active jdu-practice-status.service
systemctl is-enabled jdu-practice-status.service
```

#### 手順3: Serviceをstartする

```bash
sudo systemctl start jdu-practice-status.service
systemctl is-active jdu-practice-status.service
```

#### 手順4: Boot時にstartするよう設定する

```bash
sudo systemctl enable jdu-practice-status.service
systemctl is-enabled jdu-practice-status.service
```

#### 手順5: 採点する

```bash
cd ~
jdu-check P4
```

全2件がPASSになったら、M4へ進む。

## P5 Port、socket、HTTP、journal

### 学ぶこと

- Service、process、listening socketを対応させる。
- IP addressとportを読む。
- HTTP requestがjournalへ記録されることを確認する。

### 課題

`jdu-practice-web.service`は停止中である。ユニットファイルを変更せず、次の一連のつながりを完成させる。

1. ユニットファイルから、実行ユーザー、公開するファイルのパス、待受IPアドレスとポート番号を調べる。サービスを起動する。
2. `127.0.0.1:8181`で待ち受けているソケットを見つける。そのソケットのPIDがサービスのMain PIDと同じであることを確かめる。全アドレスでの待受には変更しない。
3. `http://127.0.0.1:8181/`へリクエストを送り、HTTP 200と本文を確認する。サービスの実行ユーザーが`/srv/jdu-practice-web/index.txt`を読めることも確かめる。
4. `http://127.0.0.1:8181/p5-check`へ自分でリクエストを送り、現在のサービスのシステムジャーナルに`REQUEST path=/p5-check`が記録される状態にする。
5. ポート`18181`には待受がないことを調べ、接続できる`8181`との違いを確認する。

`jdu-check P5`は、ソケット、HTTPとファイルアクセス、指定リクエストのログ、開いているポートと閉じているポートの比較を計4項目で判定する。

### 解答例（操作手順）

#### 手順1: Unit fileを読む

```bash
cd ~
systemctl cat jdu-practice-web.service
```

`127.0.0.1`、`8181`、`jdupracticeweb`、content fileのpathを確認する。

#### 手順2: Serviceをstartする

```bash
sudo systemctl start jdu-practice-web.service
systemctl is-active jdu-practice-web.service
```

#### 手順3: Listening socketを確認する

```bash
sudo ss -lntp | grep ':8181'
```

`127.0.0.1:8181`を確認する。同じ出力で`0.0.0.0:8181`や`[::]:8181`の待受がないことも確認する。前者はこのホスト内からの接続だけを受け付ける。後者は全アドレスでの待受を表す。

#### 手順4: Socket PIDとMain PIDを比較する

```bash
# サービスの状態を表示し、Main PIDの数字を読む。
systemctl status jdu-practice-web.service --no-pager
# 8181番ポートで待ち受けるプロセスのpid=を読む。
sudo ss -lntp | grep ':8181'
```

`systemctl status`の`Main PID:`と、`ss`の`users:`欄にある`pid=`の数字が同じであることを確認する。同じなら、このサービスの主プロセスが8181番ポートで待ち受けている。

#### 手順5: HTTP responseを確認する

```bash
curl -i http://127.0.0.1:8181/
```

#### 手順6: Service userのread権限を確認する

Content directoryへ移動する。

```bash
cd /srv/jdu-practice-web
pwd
ls -ld /srv /srv/jdu-practice-web
ls -l index.txt
id jdupracticeweb
getent passwd jdupracticeweb
sudo -u jdupracticeweb -- cat index.txt
```

`ls -ld`は各directory自身の権限を、`ls -l`は`index.txt`の所有者・group・権限を表示する。ファイルを読むには、ファイルのread権限に加え、そこへ至る各directoryを通過するためのexecute権限も必要である。`id`ではサービス用ユーザーのgroupを、`getent passwd`ではログインシェルを確認する。

`sudo -u jdupracticeweb -- cat index.txt`は、`jdupracticeweb`の権限で`cat index.txt`を**一回だけ**実行する。`--`は`sudo`のオプションの終わりを示す。内容が表示されれば、そのユーザーはファイルを読めている。`jdupracticeweb`のログインシェルは`/usr/sbin/nologin`なので、通常の`su -`で対話ログインするのではなく、この方法で確認する。

#### 手順7: 学生用requestを送る

```bash
curl -i http://127.0.0.1:8181/p5-check
sudo journalctl -u jdu-practice-web.service --no-pager -n 20
```

`REQUEST path=/p5-check`を確認する。

#### 手順8: Closed portと比較する

```bash
curl --max-time 2 http://127.0.0.1:18181/
sudo ss -lnt | grep ':18181'
```

どちらも成功しない。TCP 18181は待ち受けられていない。

#### 手順9: 採点する

```bash
cd ~
jdu-check P5
```

全4件がPASSになったら、M5へ進む。

## P6 SSH、remote command、scp

### 学ぶこと

- CloudShellとUbuntuを区別する。
- `scp`でuploadとdownloadを行う。
- SSH remote commandを実行する。

### 課題

CloudShellを接続元、Ubuntuを接続先として作業する。SSHの接続設定と`jdu-ubuntu`という接続名は準備済みである。P6の転送ファイルはまだない。

リモートで作る結果ファイルは、次の3行の形式にする。右辺は実際のコマンド出力を使い、推測して手入力しない。

```text
REMOTE_USER=実際のユーザー名
REMOTE_HOST=実際のホスト名
REMOTE_PATH=実際のホームディレクトリ
```

1. CloudShellの`~/jdu-lab/p6/practice-source.txt`へ、`JDU SSH guided transfer`の1行だけを書き込む。
2. `scp`でそのファイルをUbuntuの`~/jdu-lab/p6/practice-upload.txt`へ送る。転送前後のSHA-256が同じことを確認する。
3. CloudShellからSSHでUbuntu上のコマンドを実行し、Ubuntuの`~/jdu-lab/p6/practice-remote-result.txt`へ、実際のリモートユーザー・ホスト名・ホームディレクトリを上の形式で保存する。
4. Ubuntuへ接続して`jdu-check P6`を実行する。Ubuntu側の2項目がPASSになることを確認する。
5. 結果ファイルを`scp`でCloudShellの`~/jdu-lab/p6/practice-downloaded-result.txt`へ戻す。両側のSHA-256が同じことを確認する。
6. CloudShellで`jdu-check P6`を実行する。CloudShell側の4項目がPASSになることを確認する。

P6はUbuntu側`2/2`とCloudShell側`4/4`の両方が揃って完了する。教員用進捗画面でも両側を区別して表示する。

### 解答例（操作手順）

#### 手順1: UbuntuからCloudShellへ戻る

Ubuntuのpromptで実行する。

```bash
exit
```

CloudShellで現在地を確認する。

```bash
cd ~
pwd
id -un
hostname
```

#### 手順2: CloudShell側の作業directoryを作る

```bash
mkdir -p ~/jdu-lab/p6
cd ~/jdu-lab/p6
pwd
```

#### 手順3: Upload元fileを作る

```bash
printf '%s\n' 'JDU SSH guided transfer' > practice-source.txt
cat practice-source.txt
sha256sum practice-source.txt
```

#### 手順4: Ubuntu側のdirectoryを作る

CloudShellで実行する。

```bash
ssh jdu-ubuntu 'mkdir -p ~/jdu-lab/p6'
```

#### 手順5: Ubuntuへuploadする

CloudShellのP6 directoryにいる状態で実行する。

```bash
cd ~/jdu-lab/p6
scp practice-source.txt jdu-ubuntu:~/jdu-lab/p6/practice-upload.txt
ssh jdu-ubuntu 'sha256sum ~/jdu-lab/p6/practice-upload.txt'
sha256sum practice-source.txt
```

2つのSHA-256が同じであることを確認する。

#### 手順6: SSH remote commandで結果fileを作る

CloudShellで、次の1 commandをそのまま実行する。

```bash
ssh jdu-ubuntu 'cd ~/jdu-lab/p6 && printf "REMOTE_USER=%s\nREMOTE_HOST=%s\nREMOTE_PATH=%s\n" "$(id -un)" "$(hostname)" "$HOME" > practice-remote-result.txt'
```

内容をremoteで確認する。

```bash
ssh jdu-ubuntu 'cat ~/jdu-lab/p6/practice-remote-result.txt'
```

#### 手順7: Ubuntu側を採点する

Ubuntuへ接続する。

```bash
ssh jdu-ubuntu
cd ~/jdu-lab/p6
pwd
ls -l
jdu-check P6
exit
```

Ubuntu側2件がPASSになる。

#### 手順8: Result fileをdownloadする

CloudShellで実行する。

```bash
cd ~/jdu-lab/p6
scp jdu-ubuntu:~/jdu-lab/p6/practice-remote-result.txt practice-downloaded-result.txt
cat practice-downloaded-result.txt
sha256sum practice-downloaded-result.txt
ssh jdu-ubuntu 'sha256sum ~/jdu-lab/p6/practice-remote-result.txt'
```

2つのSHA-256が同じであることを確認する。

#### 手順9: CloudShell側を採点する

```bash
cd ~/jdu-lab/p6
jdu-check P6
```

CloudShell側4件がPASSになったら、M6へ進む。

## 学習順序

教科書の章は授業回数と一対一ではない。理解した範囲から演習へ進み、必要なら章へ戻る。

- 第1～3章と第4章の編集の基本を読む。その後、P0の手順で実機のOSを観察する。
- 第4・5章を読んでP1、M1へ進む。
- 第6・7章を読んでP2、M2へ進む。
- 第8章を読んでP3手順1～4を行う。第9章を読んでP3手順5～6を行い、最後にM3へ進む。
- 第10章を読んでP4、M4へ進む。第11章を読んでP5、M5へ進む。
- 第12章を読んでP6、M6へ進む。既習の操作を組み合わせてM7へ進む。

演習全体では次の順序を推奨する。

```text
P0 → P1 → M1 → P2 → M2 → P3 → M3 → P4 → M4
   → P5 → M5 → P6 → M6 → M7（統合課題）
```

Pは問題文だけで試してから解答例を見ることも、解答例を見ながら進めることもできる。M1～M6ではPの手順を見ずに、必要なcommandを自分で選ぶ。M7では、M2、M4、M5で学んだ内容を統合する。
