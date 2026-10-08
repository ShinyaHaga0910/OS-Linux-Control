# オペレーティングシステムとLinuxの基本操作

公開パス: **v1.0.0**。このディレクトリは更新のたびに増やさず、原稿と配布物を同じ場所で管理します。日本語版の原稿、図、PDFは静的に検証しています。個別の更新履歴は[検証記録](./instructor/validation.md)を参照してください。AWS Academy Learner Lab実機での全演習通し試験と学生試読は未実施です。

Linux未経験の学生が、コンピューター、OS、Linuxの機能を理由と仕組みから学ぶA4縦の教科書です。章別Markdownを本文の正本とし、説明図20点と歴史写真1点を組み込みました。PPTXは作成していません。現行の演習・課題と実行環境は[Labの案内](../../../lab/README.md)を参照してください。`2026/v1.0.0/`の旧Labとは区別します。

## 学生向けの教材

GitHubで読む場合は、下の章別目次と[練習P0～P6](../../../lab/GUIDED_PRACTICE.md)、[自力課題M1～M7](../../../lab/MISSION_GUIDE.md)、[用語集・コマンド早見表](./docs/ja/reference.md)を開いてください。環境がまだない場合は、[初回セットアップ](../../../lab/setup/README.md)から始めます。

PDFは次の一覧から開けます。

| 言語 | 教科書 | 練習 | 自力課題 | 用語・コマンド早見表 |
| --- | --- | --- | --- | --- |
| 日本語（現行） | [PDF](./output/pdf/ubuntu_os_textbook_ja.pdf) | [P0～P6 PDF](./output/pdf/ubuntu_os_guided_practice_ja.pdf) | [M1～M7 PDF](./output/pdf/ubuntu_os_missions_ja.pdf) | [PDF](./output/pdf/ubuntu_os_reference_ja.pdf) |
| ロシア語（翻訳初稿） | [PDF](./output/pdf/ubuntu_os_textbook_ru.pdf) | [PDF](./output/pdf/ubuntu_os_guided_practice_ru.pdf) | [PDF](./output/pdf/ubuntu_os_missions_ru.pdf) | [PDF](./output/pdf/ubuntu_os_reference_ru.pdf) |
| ウズベク語（翻訳初稿） | [PDF](./output/pdf/ubuntu_os_textbook_uz.pdf) | [PDF](./output/pdf/ubuntu_os_guided_practice_uz.pdf) | [PDF](./output/pdf/ubuntu_os_missions_uz.pdf) | [PDF](./output/pdf/ubuntu_os_reference_uz.pdf) |

ロシア語・ウズベク語の練習・課題には旧M0の表記と、日本語版に後から追加した問題文の未反映があります。現在のP0～P6・M1～M7の要件は、上の日本語版を使ってください。[翻訳の管理](./localization/README.md)で更新状況を確認できます。

## 教材と制作元

- 教科書正本: [`docs/ja/textbook/`](./docs/ja/textbook/)
- 練習課題と解答例P0～P6: [`docs/ja/practice.md`](./docs/ja/practice.md)
- 自力課題M1～M7: [`docs/ja/missions.md`](./docs/ja/missions.md)
- 用語集・コマンド早見表: [`docs/ja/reference.md`](./docs/ja/reference.md)
- 説明図と歴史写真: [`assets/`](./assets/)
- 図の生成元: [`assets/figure-sources-v1.2/`](./assets/figure-sources-v1.2/)
- HTML: [`output/html/`](./output/html/)（日本語4冊）
- A4 PDF: [`output/pdf/`](./output/pdf/)（各言語4冊）
- PDFと図の生成プログラム: [`build/`](./build/)
- 再生成手順: [`BUILD.md`](./BUILD.md)
- 多言語化の管理: [`localization/`](./localization/)

教科書は12章と巻末まとめで構成します。章末問題の解答は次ページから掲載します。練習と課題は学生の進度に応じて使用し、章番号を授業回と1対1で対応させません。

## 章構成

1. [コンピューターとオペレーティングシステム](./docs/ja/textbook/01-os-and-system.md)
2. [Unixから現在のOSへ](./docs/ja/textbook/02-unix-linux-os-history.md)
3. [GUI・CLI・ターミナル・シェル](./docs/ja/textbook/03-interfaces-and-shell.md)
4. [ファイル、ディレクトリ、パス、編集](./docs/ja/textbook/04-files-paths-editor.md)
5. [テキストと入出力](./docs/ja/textbook/05-text-and-streams.md)
6. [ユーザー、グループ、ログイン](./docs/ja/textbook/06-users-groups-sessions.md)
7. [アクセス権と共有ディレクトリ](./docs/ja/textbook/07-permissions-and-sharing.md)
8. [プログラムとプロセス](./docs/ja/textbook/08-processes-and-signals.md)
9. [パッケージと導入](./docs/ja/textbook/09-packages-and-apt.md)
10. [systemdとサービス](./docs/ja/textbook/10-services-and-systemd.md)
11. [ソケット、HTTP、ログ](./docs/ja/textbook/11-sockets-http-and-logs.md)
12. [SSHによる遠隔操作とファイル転送](./docs/ja/textbook/12-ssh-and-file-transfer.md)

[巻末まとめ](./docs/ja/textbook/afterword.md)・[練習と課題の対応表](./instructor/coverage.md)も参照できます。

CPU・メモリ・保存領域の役割とOSがそれらを管理する理由は説明します。CPUやディスク内部の詳細は対象外です。

## 言語構成

将来は英語版を翻訳原本にする予定ですが、英語版はまだありません。現時点の翻訳元は日本語版です。[ウズベク語版](./docs/uz/README.md)はChatGPTで教科書12章・巻末・練習・課題・参照資料と図21点の初稿を作成し、A4 PDF 4冊を生成しました。母語話者による校閲と学生試読は未実施のため、承認版ではありません。同じ章ID・図IDを各言語で維持します。コマンド、パス、ユーザー名、グループ名、ユニット名、チェックIDは全言語で共通とし、訳語は[`localization/terminology.csv`](./localization/terminology.csv)で管理します。

[ロシア語版](./docs/ru/README.md)もChatGPTで教科書12章・巻末・練習・課題・参照資料、図21点、A4 PDF 4冊の初稿を作成しました。ロシア語で定着したIT用語を用い、コマンド等のリテラル値は保持しています。ロシア語話者の校閲と学生試読は未実施です。

日本語の練習P0～P6には、2026年9月に各Pの問題文を追加しました。ウズベク語版とロシア語版の練習原稿・PDFは、現時点ではこの追加前の内容です。翻訳が終わるまでは日本語版を参照してください。

## 設計と検証

- [教材全体の制作方針](../../../../COURSE_POLICY.md)
- [演習対応表](./instructor/coverage.md)
- [図台帳](./instructor/figure-register.md)
- [一次資料・確認記録](./instructor/source-register.md)
- [制作・検証記録](./instructor/validation.md)

MarkdownからHTML・PDFへの変換、A4寸法、文字抽出、フォント埋め込み、章末解答の改ページ、P/M本文と公開Labの一致を静的に確認します。実機での新規構築・全演習通し実行・学生試読は別の受入作業です。

制作途中の旧版ディレクトリは現行のGitツリーから削除しました。今後の制作途中の変更は、このディレクトリとGitのコミット履歴で管理します。
