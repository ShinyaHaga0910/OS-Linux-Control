# 2026年度教材の制作方針

この文書は、教科書・練習課題・自力課題・Labの関係を維持するための現行方針である。制作時だけ使ったAIへの引継ぎ記録や旧スライド案より、こちらを優先する。

## 1. 学習の目的と対象

Linux未経験の大学生が、操作の手順だけでなく、コンピューター・OS・Linuxの機能と理由を説明できるようにする。ファイル、ユーザー、権限、プロセス、パッケージ、サービス、ソケット、ログ、SSHを、自分の操作と観測結果に結び付ける。後続のNetwork、Nginx、BIND 9、PostgreSQLへ進むための土台とする。

教科書は「一回の授業の説明原稿」ではない。授業回や20～30分という長さに合わせて説明を削らない。章は知識のまとまりであり、学生は進度に合わせて読む・練習する・戻る。初回授業で全体像とLab参加を扱うが、全員に同じ時点で同じ章の完了を要求しない。

## 2. 教材の形と説明の深さ

- A4縦の教科書を、章別Markdown、説明図、HTML、PDFで管理する。PPTXやスライドを正本にしない。
- 本文は初学者が教員の口頭補足なしでも筋道を追える文章にする。用語の列挙や図のラベルだけで説明を済ませない。
- 機能ごとに「必要な理由 → 用語 → 処理する主体 → 具体例 → 操作または観測 → 誤解しやすい点」を自然につなぐ。未説明の用語やコマンドを突然使わない。
- 図は文章を補う情報を持たせる。対象に応じて、関係図、階層図、比較図、処理の流れ、端末出力の注釈図を選ぶ。線や色の意味、役割の違いを技術的に確認する。本文で使う図には図番号、簡潔なキャプション、代替テキストを付ける。
- CPU・メモリ・保存領域は役割とOSとの関係まで説明する。CPU命令、キャッシュ、ページ置換、ディスク内部、カーネルのコード解析は扱わない。Ubuntuは授業で使うLinuxディストリビューションの一例として説明する。
- 教科書の章末問題には解答を次ページから載せる。理解確認は学習用であり、Labの新しい必須採点項目にしない。

## 3. 演習との接続

教科書は12章と章番号のない巻末まとめで構成する。第1～3章でコンピューター、OS、Unix/Linuxの位置付け、GUI・CLI・シェルを導入する。第4～12章でファイル、入出力、ユーザー・グループ、権限、プロセス、APT、systemd、通信・ログ、SSHを説明する。詳細な[章と演習の対応](./2026/materials/ubuntu_os_foundations/v1.0.0/instructor/coverage.md)を保つ。

練習P0～P6は、まず課題文を示し、その後に初心者向けの完全な操作例を載せる。`cd`、編集、保存、実行場所、ユーザー切替、`exit`などを省かない。自力課題M1～M7は要件を示し、コマンドを学生が選ぶ。PとMは別の対象を使い、Pを終えてもMが自動でPASSにならない。旧M0は手順付き練習P0に変更する。統合課題M7に対応するPは作らない。M7の完成手順を教科書に掲載しない。

採点スクリプトは到達状態を確認するもので、理解や操作経路を全面的に証明するものではない。教材の編集だけを理由に課題条件やLabの初期状態を変えない。課題条件を変更する依頼がある場合は、問題文・fixture・checker・教員Dashboard・テストを一組として扱う。

## 4. 正本と配布コピー

| 内容 | 編集する正本 | 関連する配布物・確認先 |
| --- | --- | --- |
| 教科書本文 | [`docs/ja/textbook/`](./2026/materials/ubuntu_os_foundations/v1.0.0/docs/ja/textbook/) | `output/html/`と`output/pdf/`を再生成 |
| 練習P0～P6 | [`docs/ja/practice.md`](./2026/materials/ubuntu_os_foundations/v1.0.0/docs/ja/practice.md) | [`LabのGUIDED_PRACTICE.md`](./2026/lab/GUIDED_PRACTICE.md)と`docs/ja/GUIDED_PRACTICE.md`を同内容に保つ |
| 自力課題M1～M7 | [`docs/ja/missions.md`](./2026/materials/ubuntu_os_foundations/v1.0.0/docs/ja/missions.md) | [`LabのMISSION_GUIDE.md`](./2026/lab/MISSION_GUIDE.md)を同内容に保つ |
| 用語・コマンド早見表 | [`docs/ja/reference.md`](./2026/materials/ubuntu_os_foundations/v1.0.0/docs/ja/reference.md) | 用語の技術的意味を本文と一致させる |
| 図 | [`assets/figure-sources-v1.2/`](./2026/materials/ubuntu_os_foundations/v1.0.0/assets/figure-sources-v1.2/) | [`figure-register.md`](./2026/materials/ubuntu_os_foundations/v1.0.0/instructor/figure-register.md)と本文・PDFを確認 |
| Lab実装 | [`2026/lab/`](./2026/lab/) | CloudFormation、初期設定、採点、教員進捗、テストの整合を確認 |

`output/`のPDF・HTMLは学生が入手できるようGitに含める。ただし修正元はMarkdownと図の生成元である。公開済みのRaw URLを壊さないことを優先し、リリースごとに新しい`v1.x`フォルダを増やさない。Labの今後の変更は`2026/lab/`で行い、Gitコミット・タグ・GitHub Releasesと[CHANGELOG.md](./CHANGELOG.md)で管理する。`2026/v1.0.0/`は既存URLのために残す互換用スナップショットであり、編集しない。

## 5. 多言語化

現在の翻訳元は日本語版である。英語版は将来の構想であり、現時点では存在しない。ウズベク語版とロシア語版のMarkdownとPDFは現行日本語版に内容を同期したChatGPT翻訳初稿である。母語話者による校閲と学生試読が済むまでは承認版と表示しない。

章ID・図ID・設問と解答の対応を言語間で維持する。コマンド、オプション、パス、URL、ユーザー名、サービス名、ポート、チェックIDは翻訳しない。用語は[`terminology.csv`](./2026/materials/ubuntu_os_foundations/v1.0.0/localization/terminology.csv)と各言語のスタイルガイドで管理する。ウズベク語では指定したIT用語を英語のまま用い、ロシア語では定着した専門用語を採用する。翻訳の状態と更新順は[`localization/README.md`](./2026/materials/ubuntu_os_foundations/v1.0.0/localization/README.md)を参照する。

## 6. 根拠・品質・変更手順

技術や歴史の説明には、Ubuntu公式文書、man pages、GNU、Linux kernel、Bell Labsなどの一次資料を優先する。確認日と用途を[資料台帳](./2026/materials/ubuntu_os_foundations/v1.0.0/instructor/source-register.md)に残す。写真・転載物は権利と出典を[画像記録](./2026/materials/ubuntu_os_foundations/v1.0.0/assets/historical/README.md)で確認する。未確認は未確認と書く。

変更の順序は、(1) ユーザーが求めた範囲と現行の正本を確認、(2) 対応する本文・図・問題・Labの関係を確認、(3) 正本を編集、(4) 必要な配布コピーと生成物を更新、(5) 相対リンク・同内容コピー・該当テスト・PDF表示を確認、(6) 実機試験と静的検査を区別して報告、である。原稿の再生成手順は[BUILD.md](./2026/materials/ubuntu_os_foundations/v1.0.0/BUILD.md)、検証の現状は[validation.md](./2026/materials/ubuntu_os_foundations/v1.0.0/instructor/validation.md)を参照する。

完成判断では、説明が初学者に通じること、技術的に正確なこと、演習へ接続すること、図が理解を助けること、MarkdownがPDFへ欠落なく反映されること、A4で読めることを分けて確認する。ファイル数・ページ数・自動テストのPASSだけで教育上の完成を宣言しない。
