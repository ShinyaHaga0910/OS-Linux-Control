# 教員用進捗サーバー

学生の課題提出を受け取り、教員用の一覧と学生本人用の進捗ページを提供します。学生の演習用EC2とは別のCloudFormationスタックで管理します。

作成するものはAPI GatewayのHTTPS窓口、Lambda関数1つ、DynamoDBテーブル1つです。学生・教員の進捗ページは、どちらもこのLambdaが生成します。

使用する最新版は、このリポジトリの`main`にある`2026/v1.0.0/teacher/install-teacher.sh`です。既定のスタック名`jdu-linux-progress-2026-v140`の末尾は既存環境の名前であり、現在のスクリプトの版番号ではありません。同じ名前のスタックへ最新版を適用します。

検証範囲と更新順序の詳細は[登録処理の検証記録](registration-validation.md)を参照してください。

## 教員のCloudShellで構築する

教員のAWS Academy Learner Labを開始し、CloudShellで実行します。

```bash
curl -fsSL   https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/v1.0.0/teacher/install-teacher.sh   -o /tmp/jdu-install-teacher.sh
bash /tmp/jdu-install-teacher.sh --region us-east-1
```

Academy Labで許可されたリージョンを指定してください。Lambdaの実行ロールが`LabRole`以外の場合は、`--role-name ROLE_NAME`を追加します。

構築が成功すると、実際の送信先URLと登録キーを含む学生用セットアップコマンドが表示されます。そのコマンドをGoogle Classroomで履修者へ配布します。学生はコピーして実行するだけで、送信先や登録キーを個別に入力する必要はありません。教員の管理キーは学生用コマンドに含まれません。

## セミスターごとの登録キー

登録キーは、初回にランダム生成されます。教員のCloudShellの`~/.jdu-teacher/registration.key`へ権限`0600`で保存し、通常の更新では同じキーを再利用します。AWS側には新規登録を確認するためのハッシュ値を保存します。以前公開された旧キーは、識別用ハッシュで検出して自動的に交換します。

セミスター開始時に登録キーを交換する場合だけ、同じスタックに対して次を実行します。

```bash
bash /tmp/jdu-install-teacher.sh --region us-east-1 --rotate-registration-key
```

更新後の学生用コマンドは`~/.jdu-teacher/student-setup-command.txt`にも保存されます。このファイルや登録キー入りのコマンド、ログ、スクリーンショットを公開GitHubへ載せず、履修者向けのGoogle Classroomで配布してください。

登録キーを交換しても、管理キー、既存の学生登録、DynamoDBの提出記録、学生サーバーの認証トークンは維持されます。登録済みの学生は引き続き提出・閲覧できます。旧登録キーによる新規登録だけが拒否されます。

更新に失敗した場合は、元のキーと再試行用の非公開キーを保持します。登録キーを持つ人は新規登録できるため、配布先は履修者に限定します。登録キーはメールアドレスの本人確認を行うものではありません。

## 教員が進捗を確認する

教員のCloudShellで実行します。

```bash
jdu-dashboard
```

`~/.jdu-teacher/admin.key`の管理キーで認証し、30分間有効な閲覧URLを表示します。そのURLをブラウザで開いてください。管理キー自体はURLに含めません。学生用の登録キーでは、教員ページを開けません。

教員ページには全学生の登録メールと進捗が表示されます。閲覧URLは有効期限内ならそのURLを持つ人が利用できるため、学生へ配布しないでください。

学生・教員の両ページは、`P0 → P1 → M1 → P2 → M2 → … → P6 → M6 → M7`の順に表示します。表示名と提出コマンドのIDは同じです。未提出は「—」、途中は黄色、全項目完了は緑色です。表示するのは最新の提出結果で、過去の最高点ではありません。

P6とM6はUbuntu側2項目とCloudShell側4項目の内訳を表示します。両側の合計6項目が完了すると、その課題を完了として表示します。

## 学生が自分の進捗を確認する

学生のCloudShellで実行します。

```bash
jdu-my-progress
```

学生サーバーの非公開認証トークンで`POST /student/session`へ認証し、最長15分有効な閲覧URLを発行します。学生はそのURLをブラウザで開きます。

アクセス先は教員側の`GET /student/progress`です。学生自身のEC2へアクセスするのではなく、教員側に保存した提出結果から、その学生のサーバーに紐づく記録だけを表示します。メールアドレスや他の学生の記録は表示しません。

AWS管理のHTTPS証明書を使用するため、学生PCへ証明書をインストールする必要はありません。認証済みの閲覧URLを開く際に、追加のAWSログインも不要です。URLが失効したら、CloudShellで`jdu-my-progress`を再実行します。

学生用の閲覧URLでは、教員ページの閲覧、課題の提出、メール変更、教員用URLの発行はできません。学生用と教員用の閲覧権限は別々に管理します。学生サーバーの恒久的な認証トークンは閲覧URLに含めません。共有PCでは閲覧後にページを閉じ、URLを他人へ共有しないでください。

ページにはキャッシュを保存しない設定と参照元を送らない設定を付け、外部の画像・スクリプトを読み込みません。アプリケーションは毎回有効期限を確認し、期限切れの記録はDynamoDBのTTL機能で後から削除されます。

## 学生の構築時に選ぶインスタンス

学生のセットアップは`--instance-type auto`が既定です。指定リージョンで利用可能なAZと、x86_64対応のTシリーズ・microサイズを調べます。数字の世代が新しい種類を優先し、同じ世代では標準型を優先します。例えばT3とT3aではT3を先に選び、その種類を利用できるAZを選びます。これは世代による選択であり、価格や性能の順位ではありません。

T4gなどのArm型は選びません。種類を固定する場合は`--instance-type t3.micro`などを指定できます。その場合も、CPUの対応とAZでの提供状況を確認します。既存環境を通常更新する場合は、インスタンスタイプとサブネットの配置を維持します。

この確認はAWSの提供状況を調べるもので、起動時の空き容量やAcademy Labの起動権限を保証するものではありません。問い合わせの失敗や候補がない場合は、構築を停止します。

初回構築に失敗して学生スタックが`ROLLBACK_COMPLETE`になった場合は、その失敗した学生スタックだけを削除し、削除完了後に現在の学生用コマンドを再実行します。同じ登録情報を再利用するため、学生の`~/.jdu-student`は残してください。教員スタックやAcademyの基盤スタックは削除しません。セットアップスクリプトは失敗したスタックを自動削除しません。

## 登録メールと提出データ

DynamoDBには、ランダムなServer ID、学生が入力したGoogle Classroom用メールアドレス、EC2の識別情報、P0～P6・M1～M7の最新提出結果、日時を保存します。学生氏名は保存しません。学生はUbuntu上の`jdu-progress id`で自分のServer IDを確認できます。

メールは初回セットアップ時に一度入力します。サーバー登録とEC2の識別情報を確認した後、認証トークン付きのHTTPS通信で`/link-email`へ送信します。学生のCloudShellの`~/.jdu-student/student-email.txt`へ権限`0600`で保存し、教員側のDynamoDBにも保存します。CloudFormationやEC2へメールを渡さず、構築出力にも表示しません。

メールの表示は認証済みの教員ページに限定します。学生向けの登録確認では、メールが紐づいているかどうかだけを返します。保存データとローカルのメール記録は、大学の保管方針に従って不要になった時点で削除します。

メールは学生の自己申告であり、Google認証やメールの所有者確認は行っていません。Google Classroomの履修者一覧と照合してください。再構築により同じメールに複数のサーバーが紐づいた場合は、EC2のインスタンスIDと最終提出日時で現在の環境を確認します。Classroomへの成績の自動返却は行いません。学生がServer IDをClassroomへ手入力して提出する必要はありません。

メールを修正する場合は、学生が同じCloudShellで`jdu-register --change-email`を実行します。登録通信だけを再確認する場合は`jdu-register`を実行します。課題のresetや点数の変更は行いません。初回の登録に失敗している場合は、先にセットアップと登録のログを確認してください。

`progress.env`、認証トークン、SSH秘密鍵、進捗ページの閲覧URLを学生の提出物として集めないでください。

課題の判定は学生のUbuntu上で`jdu-check P0`などを実行して行い、その結果を教員側へ送信します。P6とM6はCloudShell側の判定も必要です。教員側は送信結果を保存・表示し、学生のEC2へログインして再採点する処理は行いません。学生が演習サーバーの管理権限を持つため、この進捗表示だけでは試験の不正防止を保証できません。

## P0への更新

既存環境へP0の提出対応とP表記の進捗ページを適用するには、教員のCloudShellで最新版を取得し、同じアカウント・リージョン・スタック名で実行します。既定の構成では次を使います。

```bash
curl -fsSL https://raw.githubusercontent.com/ShinyaHaga0910/OS-Linux-Control/main/2026/v1.0.0/teacher/install-teacher.sh -o /tmp/jdu-install-teacher.sh
bash /tmp/jdu-install-teacher.sh --region us-east-1 --stack-name jdu-linux-progress-2026-v140
jdu-dashboard
```

通常の更新では保存済みのキーを再利用します。今回の更新で`--rotate-registration-key`を付ける必要はありません。学生の登録や既存提出を削除する必要もありません。

教員スタックを更新すると、学生・教員の両ページにP表記が反映されます。既存のM0の提出はP0欄で参照でき、新しいP0の提出があればその結果を優先します。

構築済みの学生EC2で`jdu-check P0`を使うには、教員スタックを先に更新した後、学生EC2の判定・初期化・送信スクリプトを更新します。これから最新版で新規構築する学生環境には、P0対応が自動で入ります。GitHub上のファイル更新だけでは、稼働中のAWS環境は更新されません。

## 参考資料

確認日：2026-09-29。

- [API GatewayのHTTP API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop.html)
- [クライアント証明書を使う相互TLS認証](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-mutual-tls.html)
