# 初回セットアップと採点システムへの登録

[言語を選ぶ](README.md) · [Русский](student-registration.ru.md) · [O‘zbekcha](student-registration.uz.md)

**教員のコマンドを実行し、自分専用の進捗ダッシュボードを開ければ完了です。** この手順では、演習用サーバーを作り、Google Classroomで使うメールアドレスとサーバーを教員の採点・進捗システムで紐づけます。P0の演習はこの後に行います。

初めてセットアップする学生向けです。すでに演習を進めている場合は、構築コマンドを再実行せず、下の「困ったとき」を確認してください。

## 1. Learner Labを開始する

まだAWS Academyに登録していない場合は、先に[AWS Academyの登録・ログイン手順書](https://github.com/ShinyaHaga0910/Introduction-CyberSecurity/blob/main/orientation/aws-academy/README.md)を進めます。

教員が指定したLearner Labを開き、`Start Lab`を押します。AWSの表示が緑になってから`AWS`を開き、AWSコンソールへ移動してください。

## 2. CloudShellを開く

AWSコンソールのリージョンを教員が指定したものに合わせ、CloudShellを開きます。入力できる状態になるまで待ちます。

以下の操作はすべて**CloudShell**で行います。Ubuntuサーバーへログインする操作は、この手順にはありません。

## 3. 教員が配布したコマンドを実行する

Google Classroomで、**今セミスター用のセットアップコマンド**を開きます。コマンド全体をコピーし、CloudShellに貼り付けてEnterを押してください。

教員の採点システムの送信先と初回登録キーは、このコマンドに含まれます。自分で書き換える必要はありません。実際のコマンドはGoogle Classroomから取得してください。

処理は、演習用サーバーの作成、Ubuntuの初期設定、教員のシステムへの登録を順番に行います。完了するまで待ち、同じコマンドを並行して実行しないでください。

## 4. 自分のメールアドレスを入力する

途中で次の入力欄が表示されます。

```text
Classroom email (visible):
```

**Google Classroomで使用する自分の`@jdu.uz`メールアドレス**を入力してEnterを押します。入力した文字は画面に表示されます。空欄や`@jdu.uz`以外では先へ進みません。画面に表示されたアドレスを確認し、正しければ`Yes`と入力してEnterを押します。間違っていればEnterだけを押して入力し直します。パスワードは入力しません。アドレスが見える画面を撮影・共有しないでください。

このメールアドレスを、教員があなたのサーバーと課題の進捗を確認するときに使います。Server IDをGoogle Classroomへ別途提出する必要はありません。メールアドレスの所有者を認証する操作ではないため、入力間違いがないよう確認してください。

## 5. セットアップの成功を確認する

次の2つの表示を確認します。

```text
PASS Teacher registration, EC2 identity, and email link confirmed.
PASS The AWS lab environment is ready.
```

最初はサーバーの登録とメールの紐づけ、次は演習環境の準備完了を表します。エラーが出た場合や、この表示が揃わない場合は、まだ完了していません。

## 6. 自分専用のダッシュボードを開く

CloudShellで実行できます。また、`ssh jdu-ubuntu`でUbuntuに接続した後も、Ubuntu上で同じコマンドを実行できます。新しく構築したUbuntuには自動で入っています。

```bash
jdu-my-progress
```

表示されたリンクをクリックしてください。クリックできない場合は、表示されたHTTPSのURLをコピーしてブラウザで開きます。CloudShellやSSH先のUbuntuから、手元のブラウザを自動起動することはできません。これが**自分専用の進捗ダッシュボード**です。教員側のシステムが提供するページで、自分の結果だけが表示されます。自分でダッシュボード用サーバーを作る必要はありません。

P0～P6、M1～M7の進捗を確認できます。最初は未提出のため、結果が空欄や「—」でも正常です。見出しには登録メールアドレスとServer IDを表示します。画面上部のボタンで日本語・ウズベク語・ロシア語を切り替えられます。ホスト名とEC2インスタンスIDは表示しません。

URLの有効期限は15分です。期限切れの場合は、CloudShellまたはUbuntuで`jdu-my-progress`をもう一度実行して新しいURLを開きます。学生PCへの証明書のインストールは不要です。

すでに構築したUbuntuで`jdu-my-progress: command not found`と表示された場合だけ、**UbuntuへSSH接続した後**に次を一度実行してください。演習の進捗はリセットされません。

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/v1.0.0/scripts/install-my-progress-ubuntu.sh -o /tmp/jdu-install-my-progress-ubuntu.sh
bash /tmp/jdu-install-my-progress-ubuntu.sh
jdu-my-progress
```

表示されたURLはブラウザで開きます。URLや認証情報を他の人へ送らないでください。Ubuntu上の登録情報が読めないというエラーが出た場合は、`ssm-user`で接続しているか確認し、解決しなければ教員へ連絡してください。

## 完了確認

- セットアップ成功の2つの`PASS`が表示された。
- 自分専用の進捗ダッシュボードを開けた。

両方を確認したら初回登録は完了です。次の授業・演習では[P0の手順](../GUIDED_PRACTICE.md#p0-environment-and-os)へ進みます。この登録だけでP0が合格になるわけではありません。

## 困ったとき

| 状況 | CloudShellで行うこと |
| --- | --- |
| メールを入れ忘れた、または間違えた | `jdu-register --change-email`を初回に使ったCloudShellで実行する |
| 登録状態をもう一度確認したい | `jdu-register`を実行する |
| ダッシュボードのURLが期限切れ | `jdu-my-progress`を実行する |
| セットアップや登録に失敗した | 止まった手順とエラーを教員に伝える。自己判断でスタックを削除しない |

配布コマンドの登録キー、秘密鍵、認証トークン、ダッシュボードの専用URLは公開・共有しないでください。共有PCでは確認後にダッシュボードを閉じてください。

### メールだけ再登録する

初回の構築コマンドは再実行しません。**初回に使ったCloudShell**で次を実行し、メールだけを入力し直します。演習用サーバーや課題は作り直しません。

```bash
jdu-register --change-email
```

`@jdu.uz`のメールを入力して`Yes`で確定します。`PASS Teacher registration, EC2 identity, and email link confirmed.`が表示されれば完了です。登録情報が見つからない場合は、別のCloudShellで操作していないか確認し、教員へ連絡してください。

古い環境で`jdu-register: command not found`または`--change-email`が使えない場合だけ、同じCloudShellで次を実行します。取得した本体のSHA-256を確認してから更新し、メール入力へ進みます。照合に失敗した場合は更新しません。

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/v1.0.0/scripts/register-student.py -o /tmp/jdu-register-new && \
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/v1.0.0/SHA256SUMS -o /tmp/jdu-register-checksums && \
awk '$2 == "scripts/register-student.py" {print $1 "  /tmp/jdu-register-new"}' /tmp/jdu-register-checksums | sha256sum --check --status && \
install -D -m 0755 /tmp/jdu-register-new "$HOME/.local/bin/jdu-register" && \
"$HOME/.local/bin/jdu-register" --change-email
```

## 教員の事前準備

学生へ配布する前に、[教員用手順](../teacher/README.md)に従って採点・進捗サーバーを準備・更新し、生成された今セミスター用のコマンドをGoogle Classroomで配布します。登録後は教員の`jdu-dashboard`でメールアドレスとServer IDの紐づけを確認できます。
