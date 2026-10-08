# 教員による学生手順の試行

対象は[現行のLab](./lab/README.md)です。教員が学生の手順を別のLearner Labで試すためのガイドです。旧`2026/v1.0.0/`の問題文や構築手順を使いません。練習は[P0～P6](./lab/GUIDED_PRACTICE.md)、自力課題は[M1～M7](./lab/MISSION_GUIDE.md)を参照します。

## 1. 準備

1. テストに使う教員の進捗スタックを[教員用手順](./lab/teacher/README.md)で確認します。本番のスタックや登録キーとは取り違えません。
2. 教員スタックが生成した**そのテスト用の学生セットアップコマンド**を控えます。接続先と登録キーが含まれるため、公開GitHubやスクリーンショットへ載せません。
3. 学生役のLearner Labで`Start Lab`を押し、AWS表示が緑になってからCloudShellを開きます。リージョンを教員の指定に合わせます。

## 2. 学生役として初回セットアップ

[学生用の初回セットアップ手順](./lab/setup/student-registration.ja.md)に従い、教員スタックが生成したコマンドをCloudShellで実行します。公開の`install.sh`を接続先・登録キーなしで実行しても構築前に停止します。テスト用の`@jdu.uz`メールを入力し、`Yes`で確定します。

セットアップと登録の`PASS`を確認します。失敗時は停止箇所を記録し、認証情報が見える画面は共有しません。CloudShellで`jdu-my-progress`を実行し、登録メールとServer ID、進捗ページの言語切替を確認します。

## 3. Ubuntuと課題

CloudShellで`ssh jdu-ubuntu`を実行し、Ubuntu上の`id -un`が`ssm-user`であることを確認します。`/etc/jdu-lab/version`にある`v1.0.0`はLabイメージの内部値で、GitHub Releaseの更新番号とは別です。SSHはSession Manager tunnelを使い、TCP 22のinbound ruleを追加しません。

初回構築直後に`jdu-reset`を実行する必要はありません。Ubuntuで`jdu-check P0`と`jdu-check P1`を実行し、未完了の項目があることを確認します。次に練習P0～P6と自力課題M1～M7を進め、途中と完成後の結果を記録します。P6/M6はUbuntuとCloudShellの両方で確認します。やり直す場合だけ、対象の`jdu-reset`を使います。

## 4. 記録と終了

AWSアカウント、リージョン、スタック状態、初回登録、SSH接続、各P/Mの判定、教員・学生画面との一致を記録します。学生の個人情報、登録キー、秘密鍵、閲覧URLは記録しません。

このガイドは試行項目を示すもので、全項目のAWS実機受入試験が済んだことを意味しません。スタックの削除は試行に含めず、対象と影響を確認して別途判断します。
