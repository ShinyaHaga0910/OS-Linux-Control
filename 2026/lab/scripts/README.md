# 学生用スクリプト

このディレクトリには、CloudShellとUbuntu EC2で使用する公開スクリプトを置きます。現行の編集対象は`2026/lab/scripts/`です。旧`2026/v1.0.0/scripts/`は互換コピーのため編集しません。

- `setup-instance.sh`: EC2 UserDataから実行する。
- `check-aws-environment.sh`: CloudShellからAWS構成をread-onlyで確認する。
- `jdu-fixture`: Ubuntu内の練習課題P0～P6と自力課題M1～M7をresetする。
- `jdu-labcheck`: Ubuntu内でP0～P6とM1～M7の状態を確認する。
- `jdu-cloudcheck`: CloudShell側のP6またはM6成果物4件を確認し、結果を自動送信する。
- `jdu-cloud-reset`: CloudShell側のP6またはM6の練習・課題ファイルを初期化する。
- `jdu-progress`: Ubuntuから教員側へ登録・判定結果を送信する。
- `jdu-my-progress`: CloudShellまたはUbuntuの保存済み接続先を使い、自分専用の閲覧URLを発行する（最長15分）。表示言語は教員側のページで切り替える。
- `install-my-progress-ubuntu.sh`: 既存Ubuntu環境へ`jdu-my-progress`を追加する。
- `register-student.py`: CloudShellに`jdu-register`として設置する。初回メール登録と`--change-email`による修正を担当する。
- `jdu-worker`: プロセス観察用プログラム。
- `jdu-http-service`: サービス、ソケット、HTTP、ログの観察用プログラム。
- `jdu-prepare-student-home`: `ssm-user`の演習用ホームディレクトリを準備する。

教師専用の採点条件、秘密情報、学生情報は格納しません。
