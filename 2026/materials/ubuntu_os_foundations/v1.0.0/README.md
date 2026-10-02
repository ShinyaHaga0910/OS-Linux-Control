# オペレーティングシステムとLinuxの基本操作

版: **v1.0.0**。更新: 2026-09-25。日本語版の原稿、図、PDFを静的に検証済みです。AWS Academy Learner Lab実機での全演習通し試験と学生試読は未実施です。

Linux未経験の学生が、コンピューター、OS、Linuxの機能を理由と仕組みから学ぶA4縦の教科書です。章別Markdownを本文の正本とし、説明図20点と歴史写真1点を組み込みました。PPTXは作成していません。対応する[公開Lab v1.0.0](../../../v1.0.0/README.md)の学生向け演習・課題文と整合します。

## 教材と制作元

- 教科書正本: [`docs/ja/textbook/`](./docs/ja/textbook/)
- 練習課題と解答例P0～P6: [`docs/ja/practice.md`](./docs/ja/practice.md)
- 自力課題M1～M7: [`docs/ja/missions.md`](./docs/ja/missions.md)
- 用語集・コマンド早見表: [`docs/ja/reference.md`](./docs/ja/reference.md)
- 説明図と歴史写真: [`assets/`](./assets/)
- 図の生成元: [`assets/figure-sources-v1.2/`](./assets/figure-sources-v1.2/)
- HTML 4冊: [`output/html/`](./output/html/)
- A4 PDF 4冊: [`output/pdf/`](./output/pdf/)
- PDFと図の生成プログラム: [`build/`](./build/)
- 再生成手順: [`BUILD.md`](./BUILD.md)
- 多言語化の管理: [`localization/`](./localization/)

教科書は12章と巻末まとめで構成します。章末問題の解答は次ページから掲載します。練習と課題は学生の進度に応じて使用し、章番号を授業回と1対1で対応させません。

## 章構成

1. コンピューターとオペレーティングシステム
2. Unixから現在のOSへ
3. GUI・CLI・ターミナル・シェル
4. ファイル、ディレクトリ、パス、編集
5. テキストと入出力
6. ユーザー、グループ、ログイン
7. アクセス権と共有ディレクトリ
8. プログラムとプロセス
9. パッケージと導入
10. systemdとサービス
11. ソケット、HTTP、ログ
12. SSHによる遠隔操作とファイル転送

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
