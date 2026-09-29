# 環境登録機能の検証記録

2026-09-29：ローカル自動試験は合格。AWSへの教員スタック更新と学生Learner Lab実機確認は未実施。

## 実装した変更

- 教員installerが実際のBaseUrlと登録キーを渡す学生コマンドを生成する。
- 学生installerがcloud-init完了・初期設定成功を待ち、認証済みAPIでServer IDとEC2の一致を確認する。
- Classroomのメールを初回一度入力し、教員のDynamoDBへ紐づける。再利用・誤入力修正に対応する。
- 教員Dashboardにメール・Server ID・instance IDを表示する。入力メールの本人認証は行わない。

## 自動確認

`bash 2026/v1.0.0/tests/run-tests.sh` が全件合格。既存のP/M判定、CloudFormation構造、SHA256、SSM接続・HTTPS進捗送信のmock試験に加えて以下を確認した。

- 実際の教員コマンドから新endpoint・登録キーを取得でき、admin keyを含まない。
- 初期設定失敗時はメール登録処理へ進まず、登録失敗時も構築完了を表示しない。
- 登録状況・メール更新APIはserver tokenを要求し、未認証・誤tokenを拒否する。
- 不正メール形式を拒否し、既存の匿名登録が入力メールを消さない。
- 状況APIはメール本文・tokenを返さず、認証済み教員Dashboardにメールを表示する。
- メールを初回入力、次回再利用、修正できる。入力メールを標準出力へ表示しない。
- 別instance ID、不成立の登録確認を完了扱いにしない。

## AWSで有効にする順序

1. 教員が同じアカウント・リージョン・既存スタック名で最新install-teacher.shを実行する。既存データを維持するため、スタックの削除・作り直しはしない。
2. teacher/README.mdにある方法で `jdu-dashboard` を開く。
3. 教員installerが表示した新しい学生用コマンドを、テスト用学生Learner Labで実行する。
4. 初期設定完了→メール入力→登録確認成功→Dashboardにメールと同じinstance IDが表示されることを確認する。
5. `jdu-check` の結果が更新され、メール修正が反映されることを確認してから学生へ配布する。

既存の学生環境に入力コマンドを追加する場合、教員APIを更新してから新installerを実行する。installerは以前からP6/M6のCloudShell側を初期化するため、既に課題を進めた環境へ無断で再実行しない。再試行・メール修正だけならCloudShellの `jdu-register` を使い、課題をresetしない。
