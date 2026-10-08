# 教員による学生手順の試行

対象: [Lab v1.0.0](./v1.0.0/README.md)。実際のAWS Academy Learner Labで、学生と同じ手順を確認するためのガイドです。課題の正本は[練習P1～P6](./v1.0.0/GUIDED_PRACTICE.md)と[自力課題M0～M7](./v1.0.0/MISSION_GUIDE.md)です。

## 1. LabとCloudShell

1. Learner Labで`Start Lab`を押し、AWS表示が緑になるまで待ちます。
2. AWS ConsoleでCloudShellを開きます。
3. 教員の進捗サーバーが必要な場合は、先に[教員用手順](./v1.0.0/teacher/README.md)で構築します。

## 2. Ubuntu環境

CloudShellで実行します。

```bash
curl -fsSLO https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/install.sh
bash install.sh --region us-east-1
```

末尾のAWS構成検査がPASSになることを確認します。`LabInstanceProfile`やSession Managerのエラーが出た場合は、Learner Lab側の権限制限を調べます。画面を記録する際は認証情報を除いてください。

## 3. UbuntuへSSH接続

```bash
ssh jdu-ubuntu
```

Ubuntu上で`id -un`が`ssm-user`、`cat /etc/jdu-lab/version`が`v1.0.0`を示すことを確認します。CloudShell専用のSSH鍵とSession Manager tunnelを使うため、Security GroupにTCP 22のinbound ruleを追加しません。

## 4. 初期状態と演習

初回構築直後は`jdu-reset`せずに、Ubuntuで`jdu-check M0`と`jdu-check P1`を実行し、未完了であることを確認します。その後、[練習手順](./v1.0.0/GUIDED_PRACTICE.md)に沿ってP1～P6、[課題文](./v1.0.0/MISSION_GUIDE.md)に沿ってM0～M7を試します。

- P/Mを解く前は0件PASSを意図しています。
- 途中まで解いた状態では、解けた項目のみPASSになることを確認します。
- 完成後は全項目PASSを確認します。
- `jdu-check`を再実行しても結果が安定することを確認します。
- P6/M6はUbuntu側とCloudShell側の両方で`jdu-check`し、Dashboardの両欄を確認します。

やり直しが必要な場合だけ、該当環境で`jdu-reset P1`や`jdu-reset M1`を使います。

## 5. 記録と終了

Region、CloudFormation stack status、AWS構成検査、SSH接続、各P/Mの初期状態・途中・完成後の結果、進捗Dashboardとの一致を記録します。AWS認証情報、session token、秘密鍵、学生の個人情報は保存しません。

終了方法は大学の運用指示に従います。CloudFormation stackの削除試験は、対象を確認して別途行います。
