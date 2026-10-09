# 一次資料と確認記録

初回確認日: 2026-09-18。追加確認日: 第2章 2026-09-21・2026-09-24、第6・8・9・10・11・12章 2026-09-24。本文取得ができた資料と、取得できなかった候補を区別する。

本書は資料の翻訳集ではなく、演習に必要な知識を説明する独自教材である。文章・説明図は独自に作成し、歴史写真は再利用条件を確認して出典を明記する。引用が必要なら出典と引用範囲を明示する。長い転載や公開資料の丸ごとの言い換えはしない。このファイルは確認の記録であり、現行の制作指示はリポジトリ直下の`COURSE_POLICY.md`を参照する。

## 1. 本文を確認した資料

| ID | 資料・URL | 採用する用途 | 注意点 |
| --- | --- | --- | --- |
| H01 | Dennis Ritchie, [The Evolution of the Unix Time-sharing System](https://www.nokia.com/bell-labs/about/dennis-m-ritchie/hist.html) | Unixの成立と、file/process/pipeという教科書の背景 | 当事者による歴史資料。現行Ubuntuの操作資料ではない。誕生1969年と後年の論文公開年を混同しない |
| H02 | kernel.org, [What is Linux?](https://www.kernel.org/linux.html) | Linuxは独自に実装されたUnix系のkernel、distributionとの区別 | Unixのsource codeがそのままLinuxに分岐した図にしない |
| H03 | Apple, [Kernel Architecture Overview](https://developer.apple.com/library/archive/documentation/Darwin/Conceptual/KernelProgramming/Architecture/Architecture.html) | Darwin、Mach、BSD、Apple/NeXTというmacOSの技術的背景 | 旧アーカイブ。現行filesystemやhardwareの説明へ流用しない。kernel内部の技術詳細は本書に不要 |
| H04 | Microsoft, [Windows NT 5.0をWindows 2000へ改称した発表](https://news.microsoft.com/source/1998/10/27/microsoft-renames-windows-nt-5-0-product-line-to-windows-2000-signals-evolution-of-windows-nt-technology-into-mainstream/) | Windows NTの歴史をUnix系とは別の流れで整理するための一次史料 | 1998年の発表。現行Windowsの全構成や最新versionを裏付ける資料としては使わない |
| H05 | Canonical, [About Ubuntu](https://ubuntu.com/about) | Ubuntuというproject/distributionの位置付け | marketing情報をOSの仕組みの説明に代用しない |
| H06 | Wikimedia Commons, [Ken Thompson and Dennis Ritchie--1973.jpg](https://commons.wikimedia.org/wiki/File:Ken_Thompson_and_Dennis_Ritchie--1973.jpg) | 第2章旧版に掲載した人物写真の記録 | 現行本文からは参照しない。旧版の追跡用に保持 |
| H07 | Wikimedia Commons, [DEC PDP-7.jpg](https://commons.wikimedia.org/wiki/File:DEC_PDP-7.jpg) | 初期Unixが開発された機種を示す第2章の写真 | 2018年撮影の保存機。ComputerGeek7066、CC BY-SA 4.0、無加工。Bell Labsで使われた個体とは記さない |
| H08 | Bell Labs史料, [A history of computing at Bell Research Laboratories (1937-1975)](https://archive.computerhistory.org/resources/access/text/2022/08/102804421-05-01-acc.pdf) | 1969年のUnixがPDP-7向けに開発され、後にPDP-11へ移された事実 | 当時の機種を確認するための歴史資料であり、写真の個体特定には用いない |
| S01 | Debian, [Role and Tasks of the Kernel](https://www.debian.org/doc/manuals/debian-handbook/sect.kernel-role-and-tasks.en.html) | hardware抽象化、共通機能、process・memory・file・権限という第1章の説明範囲 | Debianの説明をUbuntuの設定値と混同しない。CPU/memory内部の章へ拡張しない |
| S02 | Linux man-pages, [socket(7)](https://man7.org/linux/man-pages/man7/socket.7.html) | processからkernelの通信機能を利用するsocketの位置付け | API一覧・C言語実装は学生本文の対象外。socketすべてをTCP待受としない |
| S03 | Linux man-pages, [path_resolution(7)](https://man7.org/linux/man-pages/man7/path_resolution.7.html) | path探索、途中のdirectoryの権限 | 内部実装の再現ではなく、fileだけ読取可でも親dirを通れなければ読めない理由に使う |
| S04 | Microsoft Learn, [User mode and kernel mode](https://learn.microsoft.com/en-us/windows-hardware/drivers/gettingstarted/user-mode-and-kernel-mode) | 利用者側とkernel側の分離はLinux固有ではないという補助 | Windows driver開発やCPU保護機構の詳細へ広げない |
| S05 | Canonical, [User management](https://ubuntu.com/server/docs/how-to/security/user-management/) | account、root、sudo、user/group管理の確認 | 最新文書でありLab 24.04と完全一致とは限らない。Lab固有userの権限はLabコードで確認 |
| S06 | Canonical, [Install and manage packages](https://ubuntu.com/server/docs/how-to/software/package-management/) / [Managing your software](https://ubuntu.com/server/docs/tutorial/managing-software/) | APT、`update`・`upgrade`・`install`の違い。2026-09-24に再確認 | `upgrade`前にAPTが示す変更内容を確認する。Ubuntuリリースの更新と区別する |
| S07 | AWS, [Allow and control permissions for SSH connections through Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started-enable-ssh-connections.html) | 演習環境固有の接続方式を確認するための別資料。教科書第12章の一般説明には使用しない | AWSの権限・tunnelとSSHのuser認証は別。通常のprivate IPへの直接接続と同一視しない |
| S08 | GNU Project, [What is a shell?](https://www.gnu.org/software/bash/manual/html_node/What-is-a-shell_003f.html) / [What is Bash?](https://www.gnu.org/software/bash/manual/html_node/What-is-Bash_003f.html) | shellの役割、Bashの位置付け、builtinと外部programの違い | BashをLinux kernel、terminal、GNU tool全体と同一視しない |
| S09 | Microsoft Learn, [Windows commands](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands) | Windowsのcommand shellとPowerShellをUnix shellとは別のcommand環境として整理 | WSLやcross-platform programの存在を理由に、標準command体系が同じと説明しない |
| S10 | Canonical, [OpenSSH server](https://ubuntu.com/server/docs/how-to/security/openssh-server/) | 第6章のSSH公開鍵認証。秘密鍵と公開鍵、`authorized_keys`、認証後の接続 | 鍵認証の成功とファイル操作の許可を同一視しない。LabのSSM経由接続方法は別に扱う |
| S11 | Ubuntu 24.04 man page, [adduser(8)](https://manpages.ubuntu.com/manpages/noble/man8/adduser.8.html) | サービス用アカウント作成時の`nologin`の一般的な設定 | 全サービスアカウントが必ず`nologin`とは書かない |
| S12 | Ubuntu 24.04 man page, [systemd.exec(5)](https://manpages.ubuntu.com/manpages/noble/man5/systemd.exec.5.html) | サービスプロセスを`User=`で指定ユーザーとして実行する説明 | 対話ログインとサービス起動を混同しない |
| S13 | Linux man-pages, [passwd(5)](https://man7.org/linux/man-pages/man5/passwd.5.html)、[credentials(7)](https://man7.org/linux/man-pages/man7/credentials.7.html) | アカウント項目、UID/GID、プロセスの資格情報と権限判定 | 第6章では実効UIDなどの詳細へ進まず、仕組みの位置付けを説明する |
| S14 | GNU Bash Reference Manual, [Special Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html) | 第8章の`$$`による現在のシェルのPIDの表示 | サブシェルでは`$$`が呼び出し元シェルのPIDを表す場合がある。本文は対話シェルでの使用に限定 |
| S15 | Ubuntu 24.04 man page, [systemd.service(5)](https://manpages.ubuntu.com/manpages/noble/man5/systemd.service.5.html) | 第8章のサービス再起動を制御する`Restart=` | シグナル送信後の再起動を全サービス共通の挙動としない |
| S16 | Ubuntu 24.04 man pages, [systemctl(1)](https://manpages.ubuntu.com/manpages/noble/man1/systemctl.1.html)、[systemd.exec(5)](https://manpages.ubuntu.com/manpages/noble/man5/systemd.exec.5.html)、[proc_pid_cwd(5)](https://manpages.ubuntu.com/manpages/noble/man5/proc_pid_cwd.5.html) | 第10章の`cat`、Main PID、作業ディレクトリの説明。2026-09-24確認 | `systemctl cat`はディスク上のファイルを表示し、未再読み込み時にはsystemdが認識する設定と異なる場合がある |
| S17 | Linux man-pages, [connect(2)](https://www.man7.org/linux/man-pages/man2/connect.2.html)、curl [How to use curl](https://curl.se/docs/manpage.html) | 第11章の待受なしの接続拒否と`--max-time`の意味。2026-09-24確認 | タイムアウトを「待受なし」の証拠としない。HTTP応答の成否とTCP待受の有無を分ける |
| S18 | Canonical [OpenSSH server](https://ubuntu.com/server/docs/how-to/security/openssh-server/)、OpenBSD [ssh(1)](https://man.openbsd.org/ssh)、[ssh_config(5)](https://man.openbsd.org/ssh_config)、[scp(1)](https://man.openbsd.org/scp)、GNU [sha256sum(1)](https://man7.org/linux/man-pages/man1/sha256sum.1.html) | 第12章の鍵認証、ホスト認証、SSH別名、遠隔実行、SCP、内容比較。2026-09-24確認 | SSHの認証、ネットワーク到達、接続後のファイル権限を別の条件として説明する。SCPの実装を旧プロトコルに固定しない |

確認済みとは、初回確認日または上記の追加確認日にWeb上の本文・検索結果を取得して用途を評価したことを指す。Ubuntu 24.04の実機で全commandを試験したことを意味しない。

## 2. 取得できなかった候補と次工程

| 候補 | 2026-09-18の結果 | 次回確認時の対応 |
| --- | --- | --- |
| [GNU history](https://www.gnu.org/gnu/gnu-history.html)、[Linux and GNU](https://www.gnu.org/gnu/linux-and-gnu.html) | 取得timeout | GNU userlandとLinux kernelの関係を執筆する際に再取得。失敗時は別の一次資料を探し、確認済み扱いしない |
| [systemd.service v255](https://www.freedesktop.org/software/systemd/man/255/systemd.service.html)、latestのsystemd関連manual | HTTP 403 | Ubuntu 24.04実機の`man systemd.service`、`man systemctl`を優先。必要ならsystemdの該当版公式source中のmanualを参照 |
| [Ubuntu noble systemctl manual](https://manpages.ubuntu.com/manpages/noble/en/man1/systemctl.1.html) | 本文取得不可 | version付き候補としてのみ残す。閲覧・検証済みと書かない |
| [ss(8)掲載ページ](https://man7.org/linux/man-pages/man1/ss.1.html) | 本文取得不可 | 実機の`man ss`でoptionsと欄の意味を確認 |

GNU/Linuxの年表やUbuntuのDebianとの関係について、出典に年号や関係の記載が見つからない場合は追加一次資料を確認する。一般知識から年号を足して「全項目一次情報検証済み」としない。

## 3. 各章で必要な参照確認

| 章 | 優先資料・実機manual | 執筆前に確認すること |
| --- | --- | --- |
| 1 | S01、S04、`man os-release`、`man proc` | OS/kernel/user space、PID 1のLab実値、OS情報とkernel情報の違い |
| 2 | H01～H08、S08、S09 | 継承・影響・独立実装の違い、shellとBashの位置付け、Unix系とWindows NT系の分離、写真の機種と再利用条件 |
| 3 | Canonicalのterminal導入、Bash manual、`help cd` | terminalとshell、builtin、command検索、終了操作 |
| 4 | S03、`man hier`、coreutils manual、nano help | dir階層、symbolic linkの最小説明、保存画面・key表示が実機と一致 |
| 5 | Bash/grep/coreutils manual | pipe、redirect、quote、grepのline番号、末尾N行、出力例 |
| 6 | S05、S10～S13、`man id/getent/su/sudo/usermod/gpasswd` | root・一般・サービス用ユーザーの役割、account/authentication/authorization、primaryとsupplementary、既存sessionと所属更新 |
| 7 | `man chmod/chown/umask/path_resolution` | file/dirのrwx、setgidとumask、親dir、今回の通常permissionモデルの範囲 |
| 8 | S14、S15、`man ps/kill/proc`、Bash `help kill` | signal、PID指定、サービスのRestart設定、`/proc/PID`と現在のシェルPID |
| 9 | S06、`man apt/dpkg-query` | 導入前後、version、packageにより自動起動があり得ること |
| 10 | S16、Ubuntu 24.04のsystemd manual、Lab unit | User、WorkingDirectory、ExecStart、active/enabled、MainPID、`/proc/PID/cwd` |
| 11 | S02、S17、`man ss/curl/journalctl`、Lab web program | TCP待受、IPのscope、HTTP statusとcurl終了status、journalの出所 |
| 12 | S18、`man ssh/ssh_config/scp` | ホスト鍵とユーザー鍵、SSH別名と通信経路、遠隔コマンドの引用、SCP方向、内容と属性の違い |
| 巻末まとめ | 1～12章の資料 | 新しい仕組みやM7の解法順序を追加せず、既習機能と後続単元の関係だけを記す |

この表は制作時の必須確認先であり、各manualを今回すべて確認したという記録ではない。

## 4. 図の出典と正確さ

- 自作図は「本教材作成」とし、裏付けにした一次資料を図の近くか章末へ示す。公式図の転載と誤解させない。
- Unix系図では「source・技術の継承」と「設計上の影響」を異なる矢印・凡例で表す。WindowsをUnixの子として描かない。
- OS層図は概念図と明示する。GUIを使うために必ずCLIを通る構造にしない。
- service/socket図では、systemdがserviceを管理し、service processがsocket利用を要求し、kernelが通信機能を提供する主体を分ける。
- 図の必要性は説明上の役割で判定する。公式に都合のよい一枚図がないことを理由に、図を省いたり無関係な図を代用したりしない。

## 2026-10-02 コマンドの読み方と検索・末尾表示

- GNU Grep公式マニュアル：https://www.gnu.org/software/grep/manual/grep.html 。g/re/p（global / regular expression / print）の由来を公式検索結果で確認。
- GNU Findutils公式マニュアル：https://www.gnu.org/software/findutils/manual/html_mono/find.html 。検索開始位置・式の構造を公式検索結果で確認。詳細指定はローカルGNU find --helpと、使った検索の動作で確認。
- GNU Coreutilsのid/tail説明：https://www.gnu.org/software/coreutils/manual/html_node/id-invocation.html 、 https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html 。ページ取得はタイムアウトのため、今回のオプション説明はローカルGNU id --help、tail --helpで確認。Ubuntu実機での今回の教材操作は未検証。
- cd/pwdはBash help、grepの指定はgrep --helpでも照合。英語欄は学習用の意味対応とし、未確認の歴史的略語由来を断定しない。
