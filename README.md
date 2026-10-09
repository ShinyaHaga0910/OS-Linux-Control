# OS-Linux-Control — 2026

Japan Digital UniversityのOS・Linux基礎を学ぶ公開教材と実習環境です。2026年度は[Introduction-CyberSecurity](https://github.com/ShinyaHaga0910/Introduction-CyberSecurity)という統合科目の前半で使用し、2027年度以降は独立した科目の教材として使えるように管理します。担当教員の個人GitHubアカウントで管理します。

## 学生向け：2026年度の入口

| 使う場面 | 開く資料 |
| --- | --- |
| 初めて環境を準備する | [初回セットアップ・採点システム登録（日本語・ロシア語・ウズベク語）](./2026/lab/setup/README.md) |
| OS・Linuxの仕組みを学ぶ | [教科書の章別目次・3言語のPDF一覧](./2026/materials/ubuntu_os_foundations/v1.0.0/README.md) |
| 手順を見ながら練習する | [練習P0～P6](./2026/lab/GUIDED_PRACTICE.md) |
| 自分でコマンドを選んで取り組む | [自力課題M1～M7](./2026/lab/MISSION_GUIDE.md) |
| 用語・コマンド・オプションを調べる | [用語集・コマンド早見表](./2026/materials/ubuntu_os_foundations/v1.0.0/docs/ja/reference.md) |
| 接続方法や進捗確認を調べる | [Labの使い方](./2026/lab/README.md) |
| すでにある教員・学生Labを更新する | [既存Labの更新（削除・再構築なし）](./2026/lab/UPDATE_EXISTING.md) |

新しく授業に参加する学生は、上の現行リンクを使ってください。教科書には翻訳初稿がありますが、現在の練習・課題の内容は日本語版が基準です。

## 教員・制作担当者向け

- [進捗サーバーの構築・更新](./2026/lab/teacher/README.md)
- [学生手順の試行](./2026/STUDENT_TRIAL.md)
- [教科書・演習・採点の対応表](./2026/materials/ubuntu_os_foundations/v1.0.0/instructor/coverage.md)
- [教材制作の方針](./COURSE_POLICY.md)・[AI作業の入口](./AGENTS.md)
- [変更・公開の手順](./CONTRIBUTING.md)

## 現行の配置

以下はGitで管理している主要な配置です。`v1.0.0`という名前の場所は2つありますが、役割が異なります。

```text
2026/
├── STUDENT_TRIAL.md                        # 教員が学生の手順を試すガイド
├── lab/                                     # AWS実習Labの編集対象
│   ├── README.md
│   ├── GUIDED_PRACTICE.md                    # 完全手順付き演習P0～P6
│   ├── MISSION_GUIDE.md                      # 自力課題M1～M7
│   ├── install.sh
│   ├── SHA256SUMS
│   ├── setup/                               # 初回登録手順（3言語）
│   ├── cloudformation/                      # 学生用スタック
│   ├── scripts/                             # 学生用の初期化・採点・進捗コマンド
│   ├── teacher/                             # 教員用進捗サーバー
│   └── tests/                               # Labの自動テスト
├── materials/ubuntu_os_foundations/v1.0.0/  # 教科書の公開パスと制作元
│   ├── docs/{ja,uz,ru}/                     # 言語別の章・演習・課題・早見表
│   ├── assets/                               # 図と図の生成元
│   ├── build/                                # PDF・HTMLの生成プログラム
│   ├── localization/                         # 翻訳状態・用語管理
│   ├── output/html/                          # 日本語HTML 4冊
│   └── output/pdf/                           # A4 PDF、各言語4冊
└── v1.0.0/                                  # 旧LabのRaw URLを守る互換コピー。編集しない
```

教材の`materials/.../v1.0.0/`は公開中の教材パスです。`2026/v1.0.0/`は旧Labの互換コピーで、現在の演習・構築手順の入口ではありません。Labの変更は`2026/lab/`で行います。

- [実習Labの説明](./2026/lab/README.md)
- [教科書と制作元の説明](./2026/materials/ubuntu_os_foundations/v1.0.0/README.md)
- [教科書PDF](./2026/materials/ubuntu_os_foundations/v1.0.0/output/pdf/ubuntu_os_textbook_ja.pdf)
- [完全手順付き演習PDF](./2026/materials/ubuntu_os_foundations/v1.0.0/output/pdf/ubuntu_os_guided_practice_ja.pdf)
- [自力課題PDF](./2026/materials/ubuntu_os_foundations/v1.0.0/output/pdf/ubuntu_os_missions_ja.pdf)
- [用語集・コマンド早見表PDF](./2026/materials/ubuntu_os_foundations/v1.0.0/output/pdf/ubuntu_os_reference_ja.pdf)

PDFだけでなく、本文のMarkdown、図の生成元、生成プログラムも同じリポジトリに保存しています。日本語版が現在の内容の正本です。ウズベク語・ロシア語はChatGPTによる翻訳初稿とPDFがあります。旧M0の表記や、日本語の練習問題に後から追加した問題文は、両翻訳版にまだ反映されていません。現在の課題IDは日本語版と現行Labを確認してください。英語版は未作成です。

## 学生の基本手順

1. AWS Academy Learner Labを開始し、CloudShellを開きます。
2. [初回セットアップ手順](./2026/lab/setup/README.md)に従い、教員がGoogle Classroomで配布したコマンドをCloudShellで実行します。
3. `ssh jdu-ubuntu`でUbuntuに接続します。
4. P0～P6で練習し、M1～M7へ取り組みます。

メールの入力忘れや修正は、[学生用手順の「メールだけ再登録する」](./2026/lab/setup/student-registration.ja.md#メールだけ再登録する)を参照してください。初回構築コマンドは再実行しません。

Security Groupのinbound ruleは0件です。SSHのTCP 22をインターネットへ公開しません。秘密鍵はCloudShellから持ち出しません。[教員による学生手順の試行ガイド](./2026/STUDENT_TRIAL.md)もあります。

## 版管理

公開済みの最新リリースは`v1.0.2`です。変更履歴は[CHANGELOG.md](./CHANGELOG.md)とGitHub Releasesで管理します。修正のたびに新しい版番号のディレクトリは作りません。Labの今後の編集対象は`2026/lab/`です。`2026/v1.0.0/`は既存学生のRaw URLを壊さないために残す互換用スナップショットで、編集しません。配布版はGitタグとReleaseで確認してください。既存の教員・学生Labには[削除せずに更新する手順](./2026/lab/UPDATE_EXISTING.md)を使用します。

Gitの過去のコミットと既存の`2026/v1.0.0/`のRaw URLを保持します。既存Labの稼働中設定は自動変更しません。次の学期の新規配布には`2026/lab/`を使用します。

AWS認証情報、パスワード、学生の個人情報は保存しません。AWS Academy Learner Lab実機での全受入試験は未完了です。

## License

ライセンスは未確定です。現時点では、明示的な利用許諾はありません。
