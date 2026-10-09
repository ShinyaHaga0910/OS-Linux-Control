# 図台帳

すべて本教材用の自作図。現行版は再生成可能なSVGである。確認日: 2026-09-24。本文で使用する図は20点で、旧第13章のfig19は再利用に備えて保持するが本文からは参照しない。

- D2: 構造図、比較図、関係図、処理フロー図の19点
- Typst: 操作ワークフロー図の1点
- Freeze + Typst: 注釈付きターミナル図の1点
- 生成元: `assets/figure-sources-v1.2/`
- 旧版: `assets/figures/`内の同名PNG 21点を保持。現行本文からは参照しない。

| 図 | 参照章 | 図の形式 | 生成 | 解消する疑問 | 正確さの注意 |
| --- | --- | --- | --- | --- | --- |
| fig01 | 1 | 比較図 | D2 | パソコンとサーバーは何を共有するか | 用途の違いを機械原理の違いとして描かない |
| fig02 | 1 | 入れ子型レイヤー図 | D2 | ユーザー空間とカーネル空間の関係 | GUI/CLIを空間そのものとせず、ユーザー空間の関連プログラムとして描く |
| fig02b | 1 | 起動ワークフロー図 | D2 | 電源投入後にサービスが動くまでの順序 | systemd自身をWebやDBの処理主体として描かない |
| fig02c | 1 | ホスト比較・接続図 | D2 | ホスト名とユーザー識別の違い | 学生PC、CloudShell、Ubuntuを独立したOS環境として描く |
| fig03 | 2 | 系統分離付き歴史・関係図 | D2 | Unix系・Unix互換系とWindows NT系の関係 | 継承と影響を線種で分け、Windowsを独立した枠へ置く。Ubuntu、Debian、FedoraをLinuxディストリビューションの例として並列表示し、BashをOSとして描かない |
| fig04 | 2 | ディストリビューションのレイヤー図 | D2 | Linux kernelとUbuntuの違い | Ubuntuはkernelだけではない |
| fig05 | 3 | 操作経路図 | D2 | terminal、shell、commandの役割 | SSH時は解釈hostが変わる |
| fig06 | 4 | `tree`表示型の階層図 | Typst | `/`から各ファイルまでの階層関係 | `/home/ssm-user`は`/`とは別の位置であることが分かるようにする |
| fig07 | 4 | nano操作ワークフロー図 | Typst | nanoの保存操作 | 実画面に近いキー表示、保存後の再読を含む |
| fig08 | 5 | データフロー図 | D2 | stdin/stdout/stderrとredirect | `>`はstdout、stderrは別 |
| fig09 | 6 | ユーザー・グループ関係図 | D2 | primary/supplementary group | 登録と既存sessionの資格を分ける |
| fig10 | 7 | permission判断フロー図 | D2 | u/g/oのどの欄を使うか | 権限を単純加算しない。ACLは範囲外 |
| fig11 | 7 | setgid設定前後の比較図 | D2 | setgidが何を継承するか | groupのみ。modeはumask等も影響 |
| fig12 | 8 | 概念関係図 | D2 | package/program/process/serviceの違い | 終了と削除を混同しない |
| fig13 | 9 | APT処理フロー図 | D2 | apt update/installの違い | indexとpackage本体を分ける |
| fig14 | 10 | 管理関係・状態図 | D2 | unit/systemd/process/kernel | 設定とlive状態を分ける |
| fig15 | 11 | コンポーネント図 | D2 | service/process/socket/client | serviceとsocketを常に一対一にしない |
| fig16 | 11 | 注釈付きターミナル図 | Freeze + Typst | ss出力のどこを読むか | PIDは例、権限不足でprocess欄が見えない場合あり |
| fig17 | 12 | 接続元・接続先の関係図 | D2 | ユーザー鍵とホスト鍵をどちらで保持・確認するか | 鍵の二つの目的と通信経路を混同しない |
| fig18 | 12 | 送受信方向図 | D2 | SCPのアップロード・ダウンロード方向 | コマンドを実行する側を接続元とする |
| fig19 | 参照なし | 旧第13章の統合サービス関係図 | D2 | 旧版の復元・比較用に保持 | 現行教科書には含めない |

## 目視確認

生成元21点をcontact sheetで確認済み。本文参照の20点は説明対象と一致し、A4 PDF内の実寸でも再確認済みである。fig19のみ本文では使用しない。

第2章には、20点の本文使用図とは別に歴史写真1点を掲載する。画像の出典、作者、ライセンス、確認日は`assets/historical/README.md`で管理する。
