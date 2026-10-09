# 教材の再生成

このディレクトリのMarkdownと生成プログラムから、図、HTML、A4 PDFを再生成できる。

## 必要環境

- Python 3.11以降
- `requirements.txt`に記載したPython package
- D2 0.9以降
- Typst 0.15以降
- Freeze 0.2以降
- Noto Sans JPとNoto Serif JPのTrueType font

Windowsの標準配置では、次のfontを使用する。

```text
C:\Windows\Fonts\NotoSansJP-VF.ttf
C:\Windows\Fonts\NotoSerifJP-VF.ttf
```

別の場所へ導入した場合は、環境変数でTrueType font fileを指定する。

```powershell
$env:JDU_FONT_SANS='C:\path\to\NotoSansJP-Regular.ttf'
$env:JDU_FONT_SERIF='C:\path\to\NotoSerifJP-Regular.ttf'
```

Linuxでは同じ名前の環境変数をexportする。

## 生成順序

repositoryの教材version directoryで実行する。

```bash
python -m pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File build/build_diagrams.ps1
python build/build_materials.py
```

図の生成先は`assets/figures/`である。HTMLとPDFの生成先は`output/html/`、`output/pdf/`である。出力file名には`_ja`、`_uz`、`_ru`などのlanguage codeを付ける。将来の英語版も同じ規則を使用する。

ウズベク語版は次の順で確認・再生成する。翻訳そのものは自動翻訳プログラムではなく、`docs/uz/`のMarkdownで管理する。

```bash
python localization/check_uz.py
python localization/build_uz_figures.py
python build/build_uz_pdf.py
```

`localization/figure_labels_uz.tsv`が図中ラベルの訳語正本である。21点のウズベク語図は`assets/figures/uz/`に、4冊のA4 PDFは`output/pdf/*_uz.pdf`に生成する。原稿の言語別配置は`docs/ja/`、`docs/uz/`、`docs/ru/`を使用する。

ロシア語版は、図中ラベルの訳語を`localization/figure_labels_ru.tsv`で管理する。訳したMarkdownを`docs/ru/`に置き、次の順で検証・再生成する。

```bash
python localization/check_ru.py
python localization/build_ru_figures.py
python build/build_ru_pdf.py
```

全言語のPDF・HTMLを更新した後、配布済みURLの互換コピーを同期する。

```bash
python build/sync_legacy_paths.py
```

`compatibility-manifest.json`は移行前に公開していたMarkdown・PDF・HTML・画像の一覧である。`v1.0.0/`のMarkdownは現行ファイルへの案内、その他は生成コピーになる。手動では編集しない。`python build/sync_legacy_paths.py --check`で案内とコピーの一致を確認できる。

ロシア語図21点は`assets/figures/ru/`に、A4 PDF 4冊は`output/pdf/*_ru.pdf`に生成する。`docs/en/`は将来作成する。

現行図はSVGである。PDF生成時には、同じ生成元から作る高解像度PNGを使用し、日本語の字体と配置を固定する。旧版のPNG 21点は比較と復元のために同じ`assets/figures/`へ保持するが、現行本文からは参照しない。

## 正本と生成物

- 内容の正本: `docs/<language-code>/`
- 現行図の生成元: `assets/figure-sources-v1.2/`
- 現行図の一括生成: `build/build_diagrams.ps1`
- 旧版PNGの生成元: `build/generate_figures.py`
- HTML/PDF生成元: `build/build_materials.py`
- 旧教材URLの互換層: `build/sync_legacy_paths.py`と`compatibility-manifest.json`
- 訳語管理: `localization/terminology.csv`
- 制作状態: `localization/manifest.json`
- `output/`は配布用生成物であり、本文修正は`docs/`へ行う。

## 検証

生成後はPDFを画像化し、文字切れ、図の分断、矢印と文字の重なり、コード欠落、表の重なり、空白ページを確認する。章末解答が章末問題の次ページから始まることも確認する。SVGが21点あることを確認する。日本語のP/M本文は現行の`2026/lab/`にある配布コピーとの一致も確認する。
