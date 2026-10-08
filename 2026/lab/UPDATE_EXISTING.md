# 既存Labの更新（スタックを削除しない）

この手順は、すでに教員用・学生用の環境を構築したクラス向けです。CloudFormationスタックを削除せず、学生のEC2も作り直しません。新しいスタックでの初期構築は、新規学生の受入試験や次年度の授業向けです。

スタックを削除すると、教員側の進捗記録や学生側の演習成果・接続情報を失う可能性があります。今回の更新にその操作は不要です。教員スタックを先に更新し、学生は後から自分のCloudShellで更新します。作業前に、対象のAWSアカウントとリージョンを確認してください。本番への適用は教員が別途決定します。

## 1. 教員：同じスタックと鍵で更新

以前の教員用CloudShellで実行します。`~/.jdu-teacher/progress.env`、`admin.key`、`registration.key`が保存されている必要があります。鍵の内容を表示・共有しないでください。

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/teacher/update-existing-teacher.sh -o /tmp/jdu-update-existing-teacher.sh
printf '%s  %s\n' 'cc6cf61fbb2db3457fd70ce60e8c80733be566e7fc72ec91d827faea3611af3a' '/tmp/jdu-update-existing-teacher.sh' | sha256sum --check
bash /tmp/jdu-update-existing-teacher.sh --region us-east-1
```

このスクリプトは、保存済みのスタックがなければ停止します。鍵を再生成・交換せず、同じCloudFormationスタックを更新します。成功後、`jdu-dashboard`で新しい閲覧URLを発行して表示を確認します。表示されるURLは共有しないでください。

```bash
jdu-dashboard
```

## 2. 学生：CloudShellと既存Ubuntuを更新

教員の更新完了後、学生は**初回構築に使ったCloudShell**で実行します。`ssh jdu-ubuntu`でUbuntuへ入った後ではありません。

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/scripts/update-existing-cloudshell.sh -o /tmp/jdu-update-existing-cloudshell.sh
printf '%s  %s\n' '890a92f55ce9183fb10eee8c76ba2c32a03d283edb8deac626fec0f3b96b9087' '/tmp/jdu-update-existing-cloudshell.sh' | sha256sum --check
bash /tmp/jdu-update-existing-cloudshell.sh --region us-east-1
```

このスクリプトは、既存の学生スタック・SSH接続先・CloudShellとUbuntuの登録先が一致することを先に確認します。その後、配布ファイルのSHA-256を確認し、CloudShellの補助コマンドとUbuntuの採点コマンドを更新します。学生用CloudFormationは再実行せず、演習ファイル・Server ID・トークン・SSH鍵・進捗送信先をリセットしません。

メールが未登録の場合は、`@jdu.uz`のアドレスを入力し、表示された内容を確認して`Yes`で確定します。すでに登録済みならメールを保持します。訂正したい学生だけ、更新後にCloudShellで次を実行します。

```bash
jdu-register --change-email
```

更新後はUbuntuに接続し、必要な課題だけを再判定します。`jdu-check`は結果を教員側へ自動送信します。`jdu-my-progress`は自分用の閲覧URLを1行表示します。URLを他人へ送らないでください。

```bash
ssh jdu-ubuntu
command -v jdu-my-progress
jdu-check P0
jdu-my-progress
```

P3・M3について`REVIEW`と表示された場合は、更新スクリプトが古い停止状態を安全に判別できなかったことを示します。完了済みの演習は勝手にリセットしません。未完了の課題だけ、Ubuntu上で`jdu-reset P3`または`jdu-reset M3`を実行してください。

## 対象外の操作

- 教員用・学生用の既存CloudFormationスタックを削除すること。
- 学生に初回の`install.sh`を再実行させること。
- 教員の登録鍵を通常更新で交換すること。
- 学生全員へメールの再入力を強制すること。入力漏れ・誤登録だけを訂正します。

初回構築に失敗して`ROLLBACK_COMPLETE`となった、使い始める前のスタックだけは別の復旧手順が必要です。稼働中のクラスの更新と混同しないでください。
