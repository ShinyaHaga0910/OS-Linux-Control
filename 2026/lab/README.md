# OS-Linux-Control Lab 2026

Status: 次期配布候補。公開済みの最新Releaseはv1.0.1。AWS実機の新パス確認は未実施。

2026年度のAWS Academy Learner Lab用Ubuntu実習環境です。今後の編集対象は`2026/lab/`です。既存学生が使う`2026/v1.0.0/`のRaw URLは互換用スナップショットとして維持します。更新履歴は[CHANGELOG.md](../../CHANGELOG.md)を参照してください。

## 学生の初回構築

操作を順番に確認するには、[初回セットアップ・採点システム登録の手順書（日本語・ロシア語・ウズベク語）](setup/README.md)を開いてください。教員の配布コマンドを実行し、自分専用の進捗ダッシュボードを開くまでを説明しています。

Learner Labを開始し、CloudShellで実行します。

Google Classroomで教員が配布した、このセミスター用の構築コマンドをコピーして実行してください。教員用installerが、実際の進捗送信先と非公開の登録キーを含むコマンドを生成します。公開GitHubには実際のキーを載せません。配布コマンドを公開リポジトリ、公開チャット、スクリーンショットに転載しないでください。送信先・キーを指定せずにinstallerを実行すると、AWSの構築前に停止します。

`install.sh`は、CloudFormationの構築、CloudShell専用SSH鍵、Session Manager tunnel、Ubuntu初期設定、P0～P6とM1～M7の初期化、教員進捗サーバーへの登録を実行します。進捗送信先と登録キーは教員の配布コマンドに含まれ、学生による手入力は不要です。Security Groupのinbound ruleは0件で、TCP 22をインターネットへ公開しません。

初回構築時に、**Google Classroomで使う`@jdu.uz`のメールアドレスを入力**してください。入力は画面に表示されます。空欄や`@jdu.uz`以外のアドレスは受け付けず、表示されたアドレスを確認して`Yes`で確定します。条件を満たせば、そのメールとServer IDを教員の進捗画面で紐づけます。メールの所有者を認証する仕組みではありません。Server IDをClassroomへ手入力して提出する必要はありません。

メールは教員の進捗確認用DynamoDBと自分のCloudShellの非公開ファイルへ保存します。CloudFormation、EC2、公開GitHubにはメールを保存しません。入力・確認中はCloudShellの画面にメールが表示されるため、その画面を撮影・共有しないでください。完了条件はUbuntu初期設定の完了と、教員側に同じEC2・Server IDが登録され、メールが紐づいたことの確認です。通信・登録に失敗した場合は完了と表示しません。

Ubuntuへ接続します。

```bash
ssh jdu-ubuntu
```

### メールだけ再登録する

メールを入れ忘れた、間違えた場合は、**初回構築コマンドを再実行しません**。初回に使ったCloudShellで次を実行します。演習用サーバーと課題の進捗はリセットされません。

```bash
jdu-register --change-email
```

`@jdu.uz`のアドレスを入力し、表示された内容を確認して`Yes`で確定します。`PASS Teacher registration, EC2 identity, and email link confirmed.`が出れば完了です。古い環境でコマンドが使えない場合の更新方法は[メール再登録の学生向け手順](setup/student-registration.ja.md#メールだけ再登録する)を参照してください。登録通信の再確認だけなら`jdu-register`を実行します。教員用スタックを先に更新していないと、新しい登録確認APIは使えません。

## 演習と確認

問題文と手順付き解答を載せた[練習P0～P6](GUIDED_PRACTICE.md)と、[自力課題M1～M7](MISSION_GUIDE.md)があります。旧M0は手順付き練習P0へ移しました。統合課題M7には対応するPを設けていません。

```text
P0 → P1 → M1 → P2 → M2 → P3前半 → 第9章 → P3後半 → M3
   → P4 → M4 → P5 → M5 → P6 → M6 → M7
```

Ubuntu側では、`ssm-user`で実行します。

```bash
jdu-check P1
jdu-check M1
jdu-reset M1   # 最初からやり直すときだけ
```

確認結果は、設定済みの教員進捗サーバーへ自動送信されます。通信を止めてローカル判定だけ行う場合は`--no-submit`を指定します。初回構築直後に学生が`jdu-reset`する必要はありません。P0～P6とM1～M7の初期状態は0件PASSを意図しています。

P6とM6はUbuntuとCloudShellで別々に`jdu-check`を実行します。DashboardはUbuntu側2件、CloudShell側4件を分けて表示し、双方が全件PASSになったときに完了です。

### 既存のUbuntu環境を使い続ける場合

P0への変更とM1所有者判定の削除は、新規構築には自動で入ります。既存環境では、先に教員の進捗サーバーを更新し、その後にUbuntuの配布スクリプト3点を更新します。演習成果物のresetやEC2の再作成は不要です。

教員のCloudShellでは、[教員用の更新手順](teacher/README.md#p0への更新)を実施します。学生のUbuntuでは、`ssm-user`で以下を実行します。

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/scripts/jdu-labcheck -o /tmp/jdu-labcheck-v1.0.0
printf '%s  %s\n' '1b0040fb50b079ae75b16017fab21a002c5b2a9f65d34ca00dfda6079113b8a6' '/tmp/jdu-labcheck-v1.0.0' | sha256sum --check && sudo install -o root -g root -m 0755 /tmp/jdu-labcheck-v1.0.0 /opt/jdu-lab/bin/jdu-labcheck
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/scripts/jdu-fixture -o /tmp/jdu-fixture-v1.0.0
printf '%s  %s\n' 'a8f822c65ac098bb445a0e69c102d23ce01ec68cedb0462493c593ec54dbb651' '/tmp/jdu-fixture-v1.0.0' | sha256sum --check && sudo install -o root -g root -m 0755 /tmp/jdu-fixture-v1.0.0 /opt/jdu-lab/bin/jdu-fixture
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/scripts/jdu-progress -o /tmp/jdu-progress-v1.0.0
printf '%s  %s\n' '6f77a05a934c78ab7c19e447930df7e08a5e1ea85cb2338a030f9c1395f37a2b' '/tmp/jdu-progress-v1.0.0' | sha256sum --check && sudo install -o root -g root -m 0755 /tmp/jdu-progress-v1.0.0 /opt/jdu-lab/bin/jdu-progress
jdu-check list
```

一覧の先頭がP0なら更新済みです。旧コマンド`jdu-check M0`は互換入口としてP0へ切り替えます。P0の新しい記録先は`~/jdu-lab/p0/observation.env`で、P0ディレクトリがまだない場合は旧`m0/observation.env`を読みます。自動で旧ファイルを移動・削除しません。

教員画面ではP0として表示します。新しいP0の結果を優先し、まだP0の提出がない場合は既存M0の結果を表示します。教員側を更新するまではP0の送信が拒否されるため、更新の順序を守ってください。

## 主なファイル

| ファイル | 役割 |
|---|---|
| `install.sh` | CloudShell・CloudFormation・SSH tunnelの初回構築 |
| `cloudformation/lab-environment.json` | 学生用UbuntuのCloudFormation template |
| `scripts/setup-instance.sh` | Ubuntu初期設定と演習の初期化 |
| `scripts/check-aws-environment.sh` | AWS構成のread-only検査 |
| `scripts/jdu-fixture` | Ubuntu側の初期化 |
| `scripts/jdu-labcheck` | Ubuntu側の課題判定 |
| `scripts/jdu-cloudcheck` | CloudShell側P6/M6の判定 |
| `scripts/jdu-progress` | 匿名server IDと結果のHTTPS送信 |
| `scripts/register-student.py` | Classroomメールの入力・紐づけ・教員側への登録確認（CloudShell） |
| `GUIDED_PRACTICE.md` | P0～P6の問題文と手順付き解答 |
| `MISSION_GUIDE.md` | M1～M7の課題文 |
| `tests/run-tests.sh` | ローカル受入試験 |
| `SHA256SUMS` | 配布物のチェックサム |

## 教員用進捗サーバー

学生環境より先に教員のCloudShellで構築します。詳細は[teacher/README.md](teacher/README.md)を参照してください。

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/teacher/install-teacher.sh -o /tmp/jdu-install-teacher.sh
bash /tmp/jdu-install-teacher.sh --region us-east-1
```

教員のCloudShellで`jdu-dashboard`を実行すると、30分有効の閲覧URLが表示されます。端末でリンクをクリックできない場合はURLをコピーしてブラウザで開きます。CloudShellから手元のブラウザを自動起動することはできません。

## 学生が自分の進捗を確認する

学生はCloudShellでも、`ssh jdu-ubuntu`で接続したUbuntu上でも `jdu-my-progress` を実行できます。端末でリンクをクリックできない場合は、表示されたHTTPS URLをコピーしてブラウザで開きます。手元のブラウザは自動起動しません。登録メールとServer ID、自分のP・Mの最新結果だけを表示する読み取り専用ページです。画面上部のボタンで日本語・ウズベク語・ロシア語を切り替えられます。ホスト名とEC2インスタンスIDは表示しません。証明書のインストールや追加のパスワード設定は不要です。URLは最長15分で失効し、期限切れなら同じコマンドで再発行します。URLを共有せず、学校の共有PCでは利用後にページを閉じてください。教員画面のURLは学生へ配布しません。

最新のinstallerで構築した学生CloudShellとUbuntuには、両方にコマンドが自動で入ります。既存環境はサーバーを作り直さず、CloudShellで次のコマンドだけ追加できます（教員側のスタック更新が先です）。

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/scripts/jdu-my-progress -o /tmp/jdu-my-progress
install -D -m 0755 /tmp/jdu-my-progress "$HOME/.local/bin/jdu-my-progress"
jdu-my-progress
```

既存のUbuntuでコマンドが見つからない場合は、`ssh jdu-ubuntu`で接続した**Ubuntu上**で次を一度実行します。登録情報を使ってURLを発行するだけで、課題環境はリセットしません。

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/lab/scripts/install-my-progress-ubuntu.sh -o /tmp/jdu-install-my-progress-ubuntu.sh
bash /tmp/jdu-install-my-progress-ubuntu.sh
jdu-my-progress
```

認証には、その環境にある既存のサーバー登録情報を使用します。Ubuntuでは`ssm-user`が読み取れる`/etc/jdu-lab/progress.env`を使います。メールの入力だけでログインする方式ではありません。学生・教員ともに、練習はP0～P6、課題はM1～M7と表示します。表示と送信コマンドのIDは同じです（例：P1 → `jdu-check P1`）。

旧環境で「no progress endpoint saved」と表示された場合は、教員がこのクラスの実際の送信先URLを確認し、`~/.jdu-student/progress.env` に `JDU_PROGRESS_ENDPOINT=https://…` の1行を追加します。既存のサーバーIDとtokenは変更しません。送信先を別のクラスや古いスタックから転記しないでください。

## 検証範囲と版管理

ローカル自動試験は実施しています。AWS Academy Learner Lab実機での新規構築と全演習の通し受入試験は未完了です。

制作途中の旧版ディレクトリは現行のGitツリーから削除しました。以後の制作途中の変更はこのディレクトリとGitコミット履歴で管理します。旧版の`main`上のURLは使えません。既存のUbuntu環境は自動更新されません。`jdu-my-progress`だけは上記の手順で後から追加できます。その他の環境変更を試す場合は、影響を確認してから再構築してください。

### インスタンスの自動選択

セットアップは、指定リージョンの利用可能なAZと、x86_64対応のTシリーズ・microサイズをAWSへ問い合わせてから構築します。新規構築では数字の世代が新しい種類を優先し、同じ世代では標準型を優先します。T4gなどのArm型は選びません。既存環境への再実行ではインスタンスタイプとAZを維持します。教員が種類を固定する場合は`--instance-type t3.micro`などを指定できます。

この事前確認はAWSの提供範囲の確認です。Academy Labでの起動権限や一時的な容量不足までは保証しません。照会失敗・対応する組み合わせなしの場合は構築前に停止し、失敗したスタックの自動削除は行いません。AWS実機での今回の変更の動作確認は未実施です。
