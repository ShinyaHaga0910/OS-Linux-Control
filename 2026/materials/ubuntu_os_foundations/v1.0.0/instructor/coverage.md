# 教科書・演習・採点対応表

基準: [現行のLab](../../../../lab/README.md)。旧`2026/v1.0.0/`は互換コピーであり、この対応表の基準ではない。P1の所有者判定は、完成対象のファイルがそろうまでPASSしない。

| 対象 | 本文章 | 練習課題と解答例 | 自力課題 | 採点数 | 教材で説明する判定根拠 |
| --- | --- | --- | --- | ---: | --- |
| P0 | 1、3、4 | practice P0 | なし | 6 | OS ID/version、kernel、PID1、user、hostを別の観測元から取得 |
| 1 | 4、5 | P1 | M1 | P6 / M6 | path、directory、copy、削除、grep、tail、redirect（P1の所有者条件は維持、M1は所有者を採点しない） |
| 2 | 6、7 | P2 | M2 | P6 / M6 | group登録、2775、664、setgid、writer作成、viewer read/write |
| 3 | 8、9 | P3 | M3 | P2 / M2 | Main PID照合とservice停止、指定packageの導入・実行可能な実体file・version |
| 4 | 10 | P4 | M4 | P2 / M2 | 変更されていないunitのactiveとenabled |
| 5 | 6、7、10、11 | P5 | M5 | P4 / M4 | loopback socketとPID、HTTP/permission、current log、closed port |
| 6 Ubuntu | 5、12 | P6 | M6 | P2 / M2 | upload内容・owner・644、remote値 |
| 6 CloudShell | 5、12 | P6 | M6 | P4 / M4 | local source、upload hash、remote値、download hash |
| 7 | 6、7、10、11 | なし | M7 | 6 | file、writer/viewer、service、socket、HTTP、journal |

合計: P0～P6は32判定、M1～M7は31判定。M6はUbuntu 2件とCloudShell 4件を分ける。

## 理解を自動採点で代替しない項目

- OSとkernel、distributionの区別。
- Unix、Linux、macOS、Windowsの歴史的位置付け。
- GUI/CLI、terminal/shellの区別。
- なぜそのpermission classが選ばれるか。
- installed、running、active、enabled、listening、HTTP成功の区別。
- local/remote、Host alias/DNS、AWS認証/SSH認証の区別。

これらは章末問いと授業中の説明で確認する。新しい必須提出物やchecker条件にはしない。

## checkerで確認できることの限界

- 最終状態は確認できるが、学生が指定の学習経路で操作したことまでは証明しない。
- checker自身のHTTP requestもlogを作る。
- permission probeはcheckerが別userで実行するため、学生自身の失敗体験の証明ではない。
- M6は実行環境ごとにcheckerが異なる。Dashboardの二欄を合算して完了とする。
- P1～P6も学生側のcheckerが最終状態を判定し、教員のDashboardへ結果を送る。教員サーバーによる独立した再採点ではない。P6はUbuntu側2件とCloudShell側4件の両方で完了を判定する。
