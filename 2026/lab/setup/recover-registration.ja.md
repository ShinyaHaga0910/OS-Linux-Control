# 既存EC2の採点システム連携を復旧する

対象は、Ubuntuで課題を実施できるが、登録情報の欠落・不一致で教員の進捗システムと連携できない学生です。**初回構築に使ったCloudShell**で実行します。UbuntuへSSH接続した後ではありません。

EC2、CloudFormation、演習ファイルは変更しません。Server IDや学生固有トークンを新しく生成せず、既存Ubuntuに残っている情報を使います。教員側の点数を削除・初期化しません。今回はモック試験を実施しており、学生AWSでの復旧通し試験は未実施です。

## 1. 登録情報を復旧する

以下の`https://TEACHER_API_ENDPOINT`を、Google Classroomで教員が案内する**採点システムの送信先**に置き換えます。`/dashboard?session=...`が付く閲覧URLではありません。

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/scripts/recover-existing-registration.py -o /tmp/jdu-recover-registration.py &&
printf '%s  %s\n' '37a8541613fadcaa07da6336130c90eea3e9f38600b5c040081432e36a13f513' '/tmp/jdu-recover-registration.py' | sha256sum --check &&
python3 /tmp/jdu-recover-registration.py --region us-east-1 --progress-endpoint https://TEACHER_API_ENDPOINT
```

既存スタック名やSSH接続名を変更した学生は、教員確認のうえで`--stack-name 名前`、`--ssh-host 名前`を追加します。既定値は`jdu-intro-cybersecurity-2026`と`jdu-ubuntu`です。

必要な場合だけ、次の入力欄が表示されます。

```text
Semester registration key (hidden):
```

教員からGoogle Classroomで受け取った今セミスターの登録キーを貼り付け、Enterを押します。入力した文字は画面に表示されません。管理キーやメールのパスワードではありません。キーをコマンド引数や提出物に記載する必要はありません。

成功すると次が表示されます。

```text
PASS Teacher registration and existing EC2 identity confirmed.
```

復旧処理は次の順に確認します。

1. 既存CloudFormationスタックの状態とEC2のIDを読み取り、SSH接続先・ユーザーと照合する。
2. 既存UbuntuのServer ID・トークン・送信先を読み取り、指定した教員送信先と照合する。内容は画面に表示しない。
3. CloudShellが別のServer ID・教員送信先に紐づいている場合は停止する。
4. Ubuntuの認証情報で教員の登録を確認する。401で拒否された場合だけ、非表示で入力した初回登録キーを使い、同じServer ID・トークンで登録を試す。
5. 教員側の登録と実EC2の一致が確認できた後に限り、CloudShellの情報を復旧する。変更前のローカル設定は同じ非公開フォルダにバックアップする。

登録情報とバックアップはCloudShellの`~/.jdu-student/`に保存します。フォルダは`0700`、ファイルは`0600`です。認証情報を含むため、フォルダの内容を提出・共有しないでください。正常な設定のまま繰り返しても新しいServer IDは作りません。

## 2. ツールを更新し、メールを紐づける

手順1が成功した後、同じCloudShellで実行します。

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/scripts/update-existing-cloudshell.sh -o /tmp/jdu-update-existing-cloudshell.sh &&
printf '%s  %s\n' '890a92f55ce9183fb10eee8c76ba2c32a03d283edb8deac626fec0f3b96b9087' '/tmp/jdu-update-existing-cloudshell.sh' | sha256sum --check &&
bash /tmp/jdu-update-existing-cloudshell.sh --region us-east-1 --change-email
```

大学メールを入力して`Yes`で確定します。`PASS Teacher registration, EC2 identity, and email link confirmed.`が表示されることを確認します。カスタムのスタック・SSH名を使う場合は手順1と同じ指定を追加します。

## 3. 完了済み課題の結果を再送する

```bash
ssh jdu-ubuntu
jdu-check P0
jdu-my-progress
```

ほかの完了済み課題も`jdu-check 課題ID`で再採点・再送します。P6・M6はUbuntu側とCloudShell側の両方で確認します。結果は現在の演習状態から判定するため、過去に合格した時点の点数を自動復元する処理ではありません。

## 停止した場合

| 表示・状態 | 対応 |
| --- | --- |
| HTTP 401 | 入力した登録キー、送信先、教員側の設定を確認する。キーを交換せず教員へ相談する |
| HTTP 403／404 | APIの送信先・ルート・権限などを教員が確認する。登録キーの再入力だけで直るとは限らない |
| `Server ID already has another token` | 教員側に別のトークンが登録されている。自動で上書きしない。本人・実EC2・保持する課題記録を教員が照合する |
| SSH接続先・スタック・Server IDの不一致 | 別のLabや別サーバーで操作していないか確認する。初回installerは再実行しない |
| Ubuntu側にも設定がない・読めない | 自動復旧の対象外。CloudShellや過去の設定を教員が確認する。新しいIDを作って解決したことにしない |
| タイムアウト・通信エラー | Labの起動状態と接続先を確認する。EC2やスタックを削除しない |

エラー文は教員に見せて構いませんが、キー、トークン、`progress.env`、ダッシュボードの閲覧URLは共有しないでください。
