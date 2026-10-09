# 図の生成元 v1.2

本文使用図20点と、旧第13章から外したfig19を、再生成可能な技術図として管理する。旧版PNGは`assets/figures/*.png`に保持し、新版は同じbasenameのSVGとして追加する。

## 共通仕様

- 本文用フォント: Noto Sans JP
- コマンド用フォント: Consolas
- OS・システム: 青
- アプリケーション・サービス: 緑
- ハードウェア: オレンジ
- ユーザー・認証: 紫
- エラー・拒否: 赤
- 背景: 白
- 枠線: 濃紺
- 最終出力: SVG

## 分類

| 図 | 図の種類 | 生成ソフトウェア |
| --- | --- | --- |
| fig01 | PCとサーバーの比較図 | D2 |
| fig02 | OSの入れ子型レイヤー図 | D2 |
| fig02b | 起動ワークフロー図 | D2 |
| fig02c | ホスト比較・接続図 | D2 |
| fig03 | Unix系とWindows NT系を分離し、Ubuntu・Debian・Fedoraを示す歴史・関係図 | D2 |
| fig04 | Linuxディストリビューションのレイヤー図 | D2 |
| fig05 | GUIとCLIの操作経路図 | D2 |
| fig06 | `tree`表示型のディレクトリ階層図 | Typst |
| fig07 | nanoの操作ワークフロー図 | Typst |
| fig08 | 標準入出力のデータフロー図 | D2 |
| fig09 | ユーザーとグループの関係図 | D2 |
| fig10 | permission classの判断フロー図 | D2 |
| fig11 | setgid設定前後の比較図 | D2 |
| fig12 | package・program・process・serviceの関係図 | D2 |
| fig13 | APTの処理フロー図 | D2 |
| fig14 | systemdの管理関係・状態図 | D2 |
| fig15 | service・process・socketのコンポーネント図 | D2 |
| fig16 | `ss`出力の注釈付きターミナル図 | Freeze + Typst |
| fig17 | SSHの接続元・接続先と鍵の関係図 | D2 |
| fig18 | SCPの送受信方向図 | D2 |
| fig19 | 旧第13章の統合サービス関係図（本文からは参照しない） | D2 |

## 再生成

Windows PowerShellで教材ディレクトリから実行する。

```powershell
powershell -ExecutionPolicy Bypass -File build/build_diagrams.ps1
```

必要なソフトウェアはD2、Typst、Freezeである。生成スクリプトは、21点がそろわない場合に失敗する。
