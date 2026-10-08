# OS-Linux-Control — 2026

Japan Digital UniversityのOS・Linux基礎を学ぶ公開教材と実習環境です。2026年度は[Introduction-CyberSecurity](https://github.com/ShinyaHaga0910/Introduction-CyberSecurity)という統合科目の前半で使用し、2027年度以降は独立した科目の教材として使えるように管理します。担当教員の個人GitHubアカウントで管理します。

## 2026年度の入口

- [学生向け：Labの構築と課題](./2026/v1.0.0/README.md)
- [学生向け：日本語の教科書とPDF](./2026/materials/ubuntu_os_foundations/v1.0.0/README.md)
- [教員向け：進捗サーバー](./2026/v1.0.0/teacher/README.md)
- [教員向け：学生手順の試行](./2026/STUDENT_TRIAL.md)
- [教材制作の方針](./COURSE_POLICY.md)・[AI作業の入口](./AGENTS.md)

## 現行の配置

```text
2026/
├── v1.0.0/                                  # AWS実習Lab。配布URLを固定
│   ├── README.md
│   ├── GUIDED_PRACTICE.md                    # 完全手順付き演習P0～P6
│   ├── MISSION_GUIDE.md                      # 自力課題M1～M7
│   ├── install.sh
│   ├── cloudformation/
│   ├── scripts/
│   ├── teacher/                             # 教員用進捗サーバー
│   └── tests/
└── materials/ubuntu_os_foundations/v1.0.0/  # 教科書と制作元
    ├── docs/{ja,uz,ru}/                     # 言語別の章・演習・課題・早見表
    ├── assets/                               # 図と図の生成元
    ├── build/                                # PDF・HTMLの生成プログラム
    ├── localization/                         # 翻訳状態・用語管理
    ├── output/html/
    └── output/pdf/                           # A4 PDF 4冊
```

- [実習Labの説明](./2026/v1.0.0/README.md)
- [教科書と制作元の説明](./2026/materials/ubuntu_os_foundations/v1.0.0/README.md)
- [教科書PDF](./2026/materials/ubuntu_os_foundations/v1.0.0/output/pdf/ubuntu_os_textbook_ja.pdf)
- [完全手順付き演習PDF](./2026/materials/ubuntu_os_foundations/v1.0.0/output/pdf/ubuntu_os_guided_practice_ja.pdf)
- [自力課題PDF](./2026/materials/ubuntu_os_foundations/v1.0.0/output/pdf/ubuntu_os_missions_ja.pdf)
- [用語集・コマンド早見表PDF](./2026/materials/ubuntu_os_foundations/v1.0.0/output/pdf/ubuntu_os_reference_ja.pdf)

PDFだけでなく、本文のMarkdown、図の生成元、生成プログラムも同じリポジトリに保存しています。日本語版が現在の内容の正本です。ウズベク語・ロシア語は初稿とPDFがありますが、母語話者の校閲前です。日本語の練習問題に後から追加した問題文は、両翻訳版にまだ反映されていません。英語版は未作成です。

## 学生の基本手順

1. AWS Academy Learner Labを開始し、CloudShellを開きます。
2. [Labの初回構築手順](./2026/v1.0.0/README.md)に従います。
3. `ssh jdu-ubuntu`でUbuntuに接続します。
4. P0～P6で練習し、M1～M7へ取り組みます。

メールの入力忘れや修正は、[同じLab手順ページの「メールだけ再登録する」](./2026/v1.0.0/README.md#メールだけ再登録する)を参照してください。初回構築コマンドは再実行しません。

Security Groupのinbound ruleは0件です。SSHのTCP 22をインターネットへ公開しません。秘密鍵はCloudShellから持ち出しません。[教員による学生手順の試行ガイド](./2026/STUDENT_TRIAL.md)もあります。

## 版管理

現行リリースは`v1.0.1`です。変更履歴は[CHANGELOG.md](./CHANGELOG.md)とGitHub Releasesで管理します。修正のたびに新しい版番号のディレクトリは作りません。制作途中の変更は同じファイルに反映し、Gitのコミット履歴で管理します。`2026/v1.0.0/`は最初の配布時に定めた学生向けURLを維持するための固定パスであり、現行リリース番号を表しません。Labの`install.sh`とCloudFormationの公開パス、PDFの公開パスは維持します。

Gitの過去のコミットは保持します。旧版の`main`上のURLは使えません。以前のURLを使っている手順書や既存Labは、新しいURLへ更新してください。

AWS認証情報、パスワード、学生の個人情報は保存しません。AWS Academy Learner Lab実機での全受入試験は未完了です。

## License

ライセンスは公開前に確定します。現時点では、明示的な利用許諾はありません。
