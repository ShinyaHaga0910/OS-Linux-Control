# Scripts

このdirectoryには、CloudFormationとUbuntu EC2で使用する公開scriptを格納します。

- `setup-instance.sh`: EC2 UserDataから実行する。
- `check-aws-environment.sh`: CloudShellからAWS構成をread-onlyで確認する。
- `jdu-fixture`: Ubuntu内の練習課題P0～P6と自力課題M1～M7をresetする。
- `jdu-labcheck`: Ubuntu内でP0～P6とM1～M7の状態を確認する。
- `jdu-cloudcheck`: CloudShell側のP6またはM6成果物4件を確認し、結果を自動送信する。
- `jdu-my-progress`: CloudShellの登録情報を使用して、自分専用の読み取り用URLを発行する（最長15分）。
- `jdu-worker`: M3のprocess観察用program。
- `jdu-http-service`: M4、M5、M7のservice、socket、HTTP、journal観察用program。
- `jdu-prepare-student-home`: Session Managerが作成した`ssm-user`の課題directoryを初期化する。

教師専用の採点条件、秘密情報、学生情報は格納しません。
