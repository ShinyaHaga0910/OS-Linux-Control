from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
def resolve_font() -> Path:
    configured = os.environ.get("JDU_FONT_SANS")
    candidates = ([Path(configured)] if configured else []) + [
        Path(r"C:\Windows\Fonts\NotoSansJP-VF.ttf"),
        Path.home() / ".local" / "share" / "fonts" / "NotoSansJP-Regular.ttf",
    ]
    for path in candidates:
        if path.is_file():
            return path
    checked = "\n".join(f"- {path}" for path in candidates)
    raise FileNotFoundError(
        "Japanese font not found. Set JDU_FONT_SANS to a TrueType font file.\n"
        f"Checked:\n{checked}"
    )


FONT = resolve_font()

W, H = 1800, 1050
BG = "#F7F9FC"
INK = "#172033"
MUTED = "#526079"
BLUE = "#DCEBFF"
BLUE_STROKE = "#2563A6"
GREEN = "#DCF5E5"
GREEN_STROKE = "#23834D"
ORANGE = "#FFF0D6"
ORANGE_STROKE = "#B66516"
PURPLE = "#EEE4FF"
PURPLE_STROKE = "#6941A5"
RED = "#FFE1E1"
RED_STROKE = "#B33A3A"
GRAY = "#E9EDF3"
GRAY_STROKE = "#657187"


def font(size=42, bold=False):
    return ImageFont.truetype(str(FONT), size=size, layout_engine=ImageFont.Layout.BASIC)


def canvas(title, subtitle=""):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((35, 30, W - 35, H - 30), radius=28, fill="white", outline="#D6DEEA", width=3)
    d.text((85, 65), title, font=font(54, True), fill=INK)
    return im, d


def wrap(text, chars):
    lines = []
    for part in text.split("\n"):
        lines.extend(textwrap.wrap(part, width=chars, break_long_words=True, replace_whitespace=False) or [""])
    return "\n".join(lines)


def box(d, xy, title, body="", fill=BLUE, stroke=BLUE_STROKE, title_size=37, body_size=28, radius=22):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=stroke, width=4)
    d.text((x1 + 28, y1 + 23), title, font=font(title_size, True), fill=INK)
    if body:
        chars = max(8, int((x2 - x1 - 56) / (body_size * 0.78)))
        d.multiline_text((x1 + 28, y1 + 82), wrap(body, chars), font=font(body_size), fill=INK, spacing=10)


def arrow(d, start, end, label="", color="#314B6E", dashed=False, width=6):
    x1, y1 = start
    x2, y2 = end
    if dashed:
        steps = 20
        for i in range(0, steps, 2):
            a = i / steps
            b = min(1, (i + 1) / steps)
            d.line((x1 + (x2-x1)*a, y1 + (y2-y1)*a, x1 + (x2-x1)*b, y1 + (y2-y1)*b), fill=color, width=width)
    else:
        d.line((x1, y1, x2, y2), fill=color, width=width)
    import math
    angle = math.atan2(y2-y1, x2-x1)
    length = 22
    for delta in (2.55, -2.55):
        d.line((x2, y2, x2 + length*math.cos(angle+delta), y2 + length*math.sin(angle+delta)), fill=color, width=width)
    if label:
        mx, my = (x1+x2)//2, (y1+y2)//2
        bb = d.textbbox((0,0), label, font=font(25, True))
        tw, th = bb[2]-bb[0], bb[3]-bb[1]
        d.rounded_rectangle((mx-tw/2-10, my-th/2-7, mx+tw/2+10, my+th/2+7), radius=8, fill="white")
        d.text((mx-tw/2, my-th/2-3), label, font=font(25, True), fill=color)


def note(d, xy, text, color=MUTED, size=26):
    d.multiline_text(xy, wrap(text, 70), font=font(size), fill=color, spacing=8)


def save(im, name):
    im.save(OUT / name, "PNG", optimize=True)


def fig01():
    im,d=canvas("パソコンとサーバーに共通する構成")
    d.rounded_rectangle((75,180,845,925),radius=28,outline=BLUE_STROKE,width=5)
    d.text((110,195),"パソコン",font=font(42,True),fill=BLUE_STROKE)
    box(d,(130,285,790,405),"利用者と入出力","キーボード / マウス / ディスプレイ",PURPLE,PURPLE_STROKE,title_size=31,body_size=24)
    box(d,(130,455,790,575),"アプリケーション","ブラウザ / 文書作成 / 学習用ツール",GREEN,GREEN_STROKE,title_size=31,body_size=24)
    box(d,(130,625,790,745),"OS","入力・実行・保存・表示を管理",BLUE,BLUE_STROKE,title_size=31,body_size=24)
    box(d,(130,775,790,910),"ハードウェア","CPU / メモリ / ストレージ / ネットワーク",ORANGE,ORANGE_STROKE,title_size=29,body_size=20)
    arrow(d,(460,405),(460,455)); arrow(d,(460,575),(460,625)); arrow(d,(460,745),(460,775))

    d.rounded_rectangle((955,180,1725,925),radius=28,outline=GREEN_STROKE,width=5)
    d.text((990,195),"サーバー",font=font(42,True),fill=GREEN_STROKE)
    box(d,(1010,285,1670,405),"ネットワーク上の利用者","別のコンピューターから要求",PURPLE,PURPLE_STROKE,title_size=31,body_size=24)
    box(d,(1010,455,1670,575),"サーバーアプリケーション","Web / データベース / DNS",GREEN,GREEN_STROKE,title_size=31,body_size=24)
    box(d,(1010,625,1670,745),"OS","実行・保存・保護・通信を管理",BLUE,BLUE_STROKE,title_size=31,body_size=24)
    box(d,(1010,775,1670,910),"ハードウェアまたは仮想マシン","CPU / メモリ / ストレージ / ネットワーク",ORANGE,ORANGE_STROKE,title_size=27,body_size=20)
    arrow(d,(1340,405),(1340,455)); arrow(d,(1340,575),(1340,625)); arrow(d,(1340,745),(1340,775))
    save(im,"fig01-os-resource-map.png")


def fig02():
    im,d=canvas("ユーザー空間とカーネル空間")
    d.rounded_rectangle((95,170,1705,840),radius=30,outline="#7A4EAB",width=7)
    d.text((125,185),"広い意味でのOS環境",font=font(38,True),fill="#6B2FA0")
    d.rounded_rectangle((140,260,1660,575),radius=24,fill="#F5F0FF",outline=PURPLE_STROKE,width=4)
    d.text((180,280),"ユーザー空間",font=font(38,True),fill=PURPLE_STROKE)
    box(d,(190,365,610,525),"GUI関連プログラム","ウィンドウ / ボタン",PURPLE,PURPLE_STROKE,title_size=30,body_size=24)
    box(d,(690,365,1110,525),"CLI関連プログラム","ターミナル / シェル / コマンド",BLUE,BLUE_STROKE,title_size=30,body_size=23)
    box(d,(1190,365,1610,525),"アプリケーションとサービス","Web / DB / SSH",GREEN,GREEN_STROKE,title_size=28,body_size=24)
    d.rounded_rectangle((140,625,1660,820),radius=24,fill=ORANGE,outline=ORANGE_STROKE,width=4)
    d.text((180,647),"カーネル空間",font=font(38,True),fill=ORANGE_STROKE)
    d.text((490,650),"CPU / メモリ / プロセス / ファイル / アクセス権 / ネットワーク",font=font(28),fill=INK)
    for x in (400,900,1400): arrow(d,(x,575),(x,625),width=4)
    d.text((750,585),"システムコール",font=font(23,True),fill="#314B6E")
    box(d,(430,875,1370,1015),"ハードウェア","CPU / メモリ / ストレージ / 入出力装置 / ネットワーク",GRAY,GRAY_STROKE,title_size=28,body_size=20)
    arrow(d,(900,820),(900,875),width=4)
    save(im,"fig02-user-kernel-boundary.png")


def fig02b():
    im,d=canvas("電源投入からサービスが動くまで")
    stages=[
        ((75,300,335,500),"1. ファームウェア","ハードウェアを初期化",GRAY,GRAY_STROKE),
        ((410,300,670,500),"2. ブートローダー","カーネルを読み込む",PURPLE,PURPLE_STROKE),
        ((745,300,1005,500),"3. Linuxカーネル","メモリ・デバイス・\nファイルを準備",ORANGE,ORANGE_STROKE),
        ((1080,300,1340,500),"4. systemd","最初の管理プロセス\nPID 1",BLUE,BLUE_STROKE),
        ((1415,300,1725,500),"5. サービス","SSH・Web・DB\nログ管理",GREEN,GREEN_STROKE),
    ]
    for xy,t,b,f,s in stages: box(d,xy,t,b,f,s,title_size=29,body_size=23)
    for x1,x2 in ((335,410),(670,745),(1005,1080),(1340,1415)): arrow(d,(x1,400),(x2,400),width=5)
    box(d,(1120,680,1660,850),"サービスの実体","一つ以上のプロセスが動く\n例: データベースプロセス",GREEN,GREEN_STROKE,title_size=31,body_size=26)
    arrow(d,(1570,500),(1570,680),"起動・監視",width=5)
    save(im,"fig02b-linux-boot-sequence.png")


def fig02c():
    im,d=canvas("ホストとユーザーを区別する")
    hosts=[
        ((80,250,520,800),"学生PC","hostname: student-pc","手元の利用者\nブラウザ\nローカルファイル",PURPLE,PURPLE_STROKE),
        ((680,250,1120,800),"CloudShell","hostname: cloud-host","Linuxユーザー\nプロセス\nホームディレクトリ",BLUE,BLUE_STROKE),
        ((1280,250,1720,800),"Ubuntuサーバー","hostname: ip-...","ssm-user\nサービスプロセス\nサーバーファイル",GREEN,GREEN_STROKE),
    ]
    for xy,title,host,body,fill,stroke in hosts:
        x1,y1,x2,y2=xy
        d.rounded_rectangle(xy,radius=24,fill=fill,outline=stroke,width=5)
        d.text((x1+28,y1+25),title,font=font(35,True),fill=INK)
        d.text((x1+28,y1+92),host,font=font(25,True),fill=stroke)
        d.multiline_text((x1+28,y1+180),body,font=font(27),fill=INK,spacing=20)
        d.text((x1+28,y2-90),"独立したOS環境",font=font(27,True),fill=stroke)
    arrow(d,(520,525),(680,525),"ブラウザ",width=5)
    arrow(d,(1120,525),(1280,525),"SSH",width=5)
    note(d,(250,900),"ホスト名はコンピューターを識別し、ユーザー名・UID・GIDはそのホスト上の操作主体を識別する。",size=27)
    save(im,"fig02c-host-user-identity.png")


def fig03():
    im,d=canvas("Unixから現在のOSへの関係", "実線=ソース・技術の継承 / 破線=設計上の影響・互換性の目標 / 太枠=現在のシステム")
    box(d,(90,250,360,390),"Unix","1969 Bell Labs",ORANGE,ORANGE_STROKE)
    box(d,(470,190,740,330),"BSD","Unix系の発展",GREEN,GREEN_STROKE)
    box(d,(470,430,740,570),"GNU","Unix互換ツール",GREEN,GREEN_STROKE)
    box(d,(850,430,1120,570),"Linuxカーネル","独立実装",BLUE,BLUE_STROKE)
    box(d,(1240,350,1700,620),"Ubuntu","Linuxカーネル + ツール群\n+ パッケージ管理 + 設定",PURPLE,PURPLE_STROKE)
    box(d,(850,160,1120,300),"Darwin","Mach + BSD等",BLUE,BLUE_STROKE)
    box(d,(1240,120,1700,280),"macOS","Darwin + Apple層",PURPLE,PURPLE_STROKE)
    box(d,(850,720,1120,860),"Windows NT","別系統",GRAY,GRAY_STROKE)
    box(d,(1240,700,1700,880),"現在のWindows","NT系列",PURPLE,PURPLE_STROKE)
    arrow(d,(360,290),(470,250),"継承"); arrow(d,(740,250),(850,230),"技術")
    arrow(d,(1120,230),(1240,200),"基盤"); arrow(d,(740,500),(850,500),"ツール群")
    arrow(d,(1120,500),(1240,470),"カーネル")
    arrow(d,(360,340),(850,470),"影響",dashed=True)
    arrow(d,(1120,790),(1240,790),"製品系列")
    note(d,(100,900),"Linuxは歴史上のUnixソースコードから直接分岐したものではない。macOSはLinuxディストリビューションではない。WindowsはUnixの子として描かない。",size=25)
    save(im,"fig03-os-history-map.png")


def fig04():
    im,d=canvas("UbuntuはLinuxカーネルだけではない", "ディストリビューションは複数のソフトウェアと更新方針を統合する")
    layers=[((300,760,1500,900),"ハードウェア","CPU / メモリ / ディスク / ネットワーク",ORANGE,ORANGE_STROKE),((300,610,1500,740),"Linuxカーネル","プロセス・メモリ・ファイルシステム・デバイス・ネットワーク",BLUE,BLUE_STROKE),((300,455,1500,585),"ライブラリ・基本コマンド・シェル","GNUツール群等を含むユーザー空間",GREEN,GREEN_STROKE),((300,300,1500,430),"システム管理・パッケージ管理","systemd / APT / 設定",PURPLE,PURPLE_STROKE),((300,145,1500,275),"アプリケーション・サービス","SSH / Web / 学生のコマンド",GRAY,GRAY_STROKE)]
    for xy,t,b,f,s in layers: box(d,xy,t,b,f,s,title_size=34,body_size=27)
    d.rounded_rectangle((230,105,1570,945),radius=34,outline="#7A4EAB",width=8)
    d.text((1270,105),"Ubuntu",font=font(40,True),fill="#6B2FA0")
    save(im,"fig04-linux-distribution-stack.png")


def fig05():
    im,d=canvas("CLIを構成するもの", "ターミナルは画面、シェルは解釈、コマンドは処理を行う")
    box(d,(80,240,360,390),"人","文字を入力",PURPLE,PURPLE_STROKE)
    box(d,(470,240,780,390),"ターミナル","入力と表示の場",GRAY,GRAY_STROKE)
    box(d,(890,240,1200,390),"Bashシェル","文字列を解釈",BLUE,BLUE_STROKE)
    box(d,(1310,240,1690,390),"コマンドプロセス","ls / grep / curl",GREEN,GREEN_STROKE)
    for a,b,l in [((360,315),(470,315),"キー"),((780,315),(890,315),"文字列"),((1200,315),(1310,315),"起動")]: arrow(d,a,b,l)
    box(d,(890,620,1200,790),"シェル組み込み","cd / type / help",ORANGE,ORANGE_STROKE)
    box(d,(1310,620,1690,790),"外部実行ファイル","/usr/bin/grep 等",ORANGE,ORANGE_STROKE)
    arrow(d,(1050,390),(1050,620),"シェル内部"); arrow(d,(1120,390),(1480,620),"PATHで探索")
    note(d,(100,880),"SSH後もターミナル画面は同じに見えるが、文字列を解釈するシェルのホストはUbuntuへ変わる。")
    save(im,"fig05-gui-cli-shell.png")


def fig06():
    im,d=canvas("パスはディレクトリの名前を順にたどる", "絶対パスは / から、相対パスは現在位置から")
    box(d,(100,210,300,330),"/","ルート (root)",ORANGE,ORANGE_STROKE)
    box(d,(430,210,680,330),"srv","ディレクトリ",BLUE,BLUE_STROKE)
    box(d,(810,210,1160,330),"jdu-share","ディレクトリ",BLUE,BLUE_STROKE)
    box(d,(1300,210,1690,330),"README.txt","ファイル",GREEN,GREEN_STROKE)
    arrow(d,(300,270),(430,270),"srv"); arrow(d,(680,270),(810,270),"jdu-share"); arrow(d,(1160,270),(1300,270),"README.txt")
    d.text((210,440),"絶対パス: /srv/jdu-share/README.txt",font=font(38,True),fill=INK)
    box(d,(430,610,810,770),"現在位置","/srv/jdu-share",PURPLE,PURPLE_STROKE)
    box(d,(1160,610,1550,770),"対象","README.txt",GREEN,GREEN_STROKE)
    arrow(d,(810,690),(1160,690),"相対パス")
    note(d,(430,845),"pwdで基準点を確認する。~ は現在ユーザーのホームディレクトリへ展開される。")
    save(im,"fig06-path-tree.png")


def fig07():
    im,d=canvas("nano: 開く → 編集 → 保存 → 終了", "画面下の ^ は Ctrlキー を表す")
    d.rounded_rectangle((110,205,1690,790),radius=20,fill="#172033",outline="#4A5A73",width=4)
    d.rectangle((110,205,1690,270),fill="#1F5E8C")
    d.text((150,217),"GNU nano     observation.env",font=font(32,True),fill="white")
    sample="OS_ID=ubuntu\nOS_VERSION_ID=24.04\nKERNEL_RELEASE=（実機で確認）\nPID1_COMM=systemd\nUSER_NAME=ssm-user\nHOST_NAME=（実機で確認）"
    d.multiline_text((165,320),sample,font=font(31),fill="#F4F7FB",spacing=17)
    d.rectangle((110,695,1690,790),fill="#263A52")
    d.text((150,715),"^O Write Out     ^X Exit     ^W Where Is",font=font(31,True),fill="white")
    steps=[("1","nano FILE","開く"),("2","文字入力","編集"),("3","Ctrl+O → Enter","保存"),("4","Ctrl+X","終了"),("5","cat FILE","再読")]
    x=115
    for num,key,label in steps:
        box(d,(x,840,x+300,990),f"{num}. {label}",key,BLUE,BLUE_STROKE,title_size=30,body_size=25)
        x+=335
    save(im,"fig07-nano-workflow.png")


def fig08():
    im,d=canvas("プロセスの三つの標準ストリーム", "> はstdoutをファイルへ、| は次のプロセスへ接続する")
    box(d,(650,330,1150,700),"コマンドプロセス","stdin  0\nstdout 1\nstderr 2",BLUE,BLUE_STROKE,title_size=40,body_size=34)
    box(d,(90,390,450,550),"入力元","キーボード / ファイル\n前のコマンド",GREEN,GREEN_STROKE)
    box(d,(1350,220,1710,380),"通常結果","ターミナル / ファイル\n次のコマンド",PURPLE,PURPLE_STROKE)
    box(d,(1350,650,1710,810),"エラー・警告","通常はターミナル\n2>で別接続",RED,RED_STROKE)
    arrow(d,(450,470),(650,470),"stdin")
    arrow(d,(1150,430),(1350,300),"stdout")
    arrow(d,(1150,600),(1350,730),"stderr")
    note(d,(100,890),"入力ファイルと出力ファイルを同じ名前にすると、> が先に内容を空にする危険がある。")
    save(im,"fig08-standard-streams.png")


def fig09():
    im,d=canvas("主グループと補助グループ", "共有用途は追加グループで管理できる")
    box(d,(100,260,480,470),"jduops","主グループ: jduops\n補助グループ: ops",BLUE,BLUE_STROKE)
    box(d,(100,610,480,820),"jduviewer","主グループ: jduviewer\n補助グループ: なし",GRAY,GRAY_STROKE)
    box(d,(750,330,1120,520),"グループ ops","共有作業者",GREEN,GREEN_STROKE)
    box(d,(1330,330,1700,520),"/srv/jdu-share","グループ: ops\nmode: 2775",PURPLE,PURPLE_STROKE)
    arrow(d,(480,370),(750,410),"所属"); arrow(d,(1120,425),(1330,425),"グループアクセス")
    arrow(d,(480,710),(750,500),"非所属",color=RED_STROKE,dashed=True)
    note(d,(700,700),"グループ登録を変えても、既存シェルの所属グループ一覧は更新されない場合がある。新しいセッションで確認する。")
    save(im,"fig09-user-group-membership.png")


def fig10():
    im,d=canvas("アクセス権クラスの選択", "所有者 → グループ → その他 のどの一欄を使うか判断する")
    box(d,(80,300,430,500),"操作プロセス","UID: jduviewer\nGroups: jduviewer",BLUE,BLUE_STROKE)
    box(d,(610,180,960,350),"所有者一致?","ファイル所有者 = root",ORANGE,ORANGE_STROKE)
    box(d,(610,440,960,610),"グループ一致?","ファイルグループ = ops",ORANGE,ORANGE_STROKE)
    box(d,(610,700,960,870),"その他 (others)","どちらも不一致",ORANGE,ORANGE_STROKE)
    box(d,(1190,180,1690,350),"所有者欄を使う","rw-",GREEN,GREEN_STROKE)
    box(d,(1190,440,1690,610),"グループ欄を使う","rw-",GREEN,GREEN_STROKE)
    box(d,(1190,700,1690,870),"その他欄を使う","r--",GREEN,GREEN_STROKE)
    arrow(d,(430,400),(610,265),"照合"); arrow(d,(430,400),(610,525),"照合"); arrow(d,(430,400),(610,785),"不一致時")
    arrow(d,(960,265),(1190,265),"yes"); arrow(d,(960,525),(1190,525),"yes"); arrow(d,(960,785),(1190,785),"適用")
    save(im,"fig10-permission-decision.png")


def fig11():
    im,d=canvas("ディレクトリのsetgid効果", "新規ファイルのグループを親ディレクトリへそろえる")
    box(d,(100,250,700,450),"setgidなし","親グループ: ops\n作成ユーザー主グループ: jduops",GRAY,GRAY_STROKE)
    box(d,(100,620,700,820),"setgidあり (2775)","親グループ: ops\n作成ユーザー主グループ: jduops",BLUE,BLUE_STROKE)
    box(d,(1100,250,1700,450),"新規ファイル","グループ: jduops になり得る",RED,RED_STROKE)
    box(d,(1100,620,1700,820),"新規ファイル","グループ: ops を継承",GREEN,GREEN_STROKE)
    arrow(d,(700,350),(1100,350),"作成")
    arrow(d,(700,720),(1100,720),"作成")
    note(d,(520,900),"setgidは所有者や内容を複製せず、mode全体も固定しない。新規modeにはumaskも影響する。",size=25)
    save(im,"fig11-setgid-inheritance.png")


def fig12():
    im,d=canvas("保存されたものと実行中のものを区別する", "パッケージ・プログラム・プロセス・サービスは同義ではない")
    box(d,(80,280,420,480),"パッケージ","ファイル群とバージョン\n依存・導入情報",ORANGE,ORANGE_STROKE)
    box(d,(540,280,880,480),"プログラムファイル","保存領域にある\n命令",GREEN,GREEN_STROKE)
    box(d,(1000,280,1340,480),"プロセス","実行中\nPIDを持つ",BLUE,BLUE_STROKE)
    box(d,(1460,280,1720,480),"サービス","継続機能\n管理単位",PURPLE,PURPLE_STROKE)
    arrow(d,(420,380),(540,380),"インストール"); arrow(d,(880,380),(1000,380),"実行"); arrow(d,(1460,380),(1340,380),"管理")
    box(d,(540,650,1340,830),"同じプログラムから複数プロセス","PID 2401 / PID 2455 / PID 2510",GRAY,GRAY_STROKE)
    arrow(d,(1170,480),(950,650),"複数起動")
    note(d,(150,900),"プロセスを終了してもプログラムファイルは残る。パッケージをインストールしただけで常にプロセスが動くとは限らない。")
    save(im,"fig12-program-process-service.png")


def fig13():
    im,d=canvas("APTでパッケージを導入する流れ", "インデックス更新とパッケージ本体の導入を分ける")
    box(d,(80,270,430,470),"リポジトリ","パッケージ本体\nメタデータ",PURPLE,PURPLE_STROKE)
    box(d,(610,270,980,470),"ローカルインデックス","利用可能バージョン\n依存情報",BLUE,BLUE_STROKE)
    box(d,(1160,270,1510,470),"導入済みパッケージ","ファイル・バージョン\nローカルデータベース",GREEN,GREEN_STROKE)
    box(d,(1160,650,1510,820),"コマンド","/usr/bin/cmatrix",ORANGE,ORANGE_STROKE)
    arrow(d,(430,370),(610,370),"apt update")
    arrow(d,(980,370),(1160,370),"apt install")
    arrow(d,(1335,470),(1335,650),"提供")
    note(d,(160,705),"apt updateだけではコマンドは増えない。\n導入済みと実行中も別の状態。",size=30)
    save(im,"fig13-apt-flow.png")


def fig14():
    im,d=canvas("systemdサービスの設定と実行", "ユニットを読み、実プロセスと対応させる")
    box(d,(80,300,430,550),"ユニットファイル","User=\nWorkingDirectory=\nExecStart=",GRAY,GRAY_STROKE)
    box(d,(610,300,960,550),"systemd (PID 1)","start / stop\nenable / state",BLUE,BLUE_STROKE)
    box(d,(1140,300,1490,550),"サービスプロセス","Main PID\n実行ユーザー / cwd",GREEN,GREEN_STROKE)
    box(d,(1140,700,1490,870),"カーネル","CPU・ファイル・ソケット",ORANGE,ORANGE_STROKE)
    arrow(d,(430,425),(610,425),"読む"); arrow(d,(960,425),(1140,425),"起動・監視"); arrow(d,(1315,550),(1315,700),"利用")
    note(d,(120,740),"active = 現在動作中\nenabled = 起動時の自動起動有効",size=31)
    save(im,"fig14-systemd-service-lifecycle.png")


def fig15():
    im,d=canvas("サービスからHTTP応答まで", "管理・実行・通信・リクエストを別の役割として見る")
    box(d,(80,250,380,430),"systemd","プロセスを管理",BLUE,BLUE_STROKE)
    box(d,(520,250,850,430),"サービスプロセス","HTTP処理を実行",GREEN,GREEN_STROKE)
    box(d,(990,250,1320,430),"カーネルソケット","127.0.0.1:8081\nLISTEN",ORANGE,ORANGE_STROKE)
    box(d,(1460,250,1710,430),"curl","クライアント",PURPLE,PURPLE_STROKE)
    arrow(d,(380,340),(520,340),"起動"); arrow(d,(850,340),(990,340),"作成を依頼"); arrow(d,(1460,340),(1320,340),"リクエスト")
    box(d,(520,650,850,830),"コンテンツファイル","サービスユーザーが読む",GRAY,GRAY_STROKE)
    box(d,(990,650,1320,830),"ジャーナル","REQUESTを記録",GRAY,GRAY_STROKE)
    arrow(d,(680,430),(680,650),"読み取り"); arrow(d,(760,430),(1100,650),"ログ出力")
    note(d,(1350,680),"サービスactive\n≠ HTTP正常",size=34)
    save(im,"fig15-service-process-socket.png")


def fig16():
    im,d=canvas("ss -lntp の一行を読む", "State → Local Address:Port → Process PID の順に照合する")
    d.rounded_rectangle((90,230,1710,530),radius=18,fill="#172033")
    headers="State   Recv-Q Send-Q Local Address:Port  Peer Address:Port  Process"
    row='LISTEN  0      5      127.0.0.1:8081     0.0.0.0:*        users:(("python3",pid=2451,fd=3))'
    d.text((135,275),headers,font=font(28,True),fill="#A7C7E7")
    d.text((135,365),row,font=font(25),fill="white")
    boxes=[((90,690,390,850),"LISTEN","接続待ち",GREEN,GREEN_STROKE),((520,690,960,850),"127.0.0.1:8081","アドレス : ポート",ORANGE,ORANGE_STROKE),((1100,690,1710,850),"pid=2451","サービスのMain PIDと比較",BLUE,BLUE_STROKE)]
    for xy,t,b,f,s in boxes: box(d,xy,t,b,f,s,title_size=32,body_size=26)
    arrow(d,(240,690),(240,510),""); arrow(d,(740,690),(740,510),""); arrow(d,(1400,690),(1400,510),"")
    note(d,(100,930),"2451は表示例。実機のPIDを読む。-pのprocess欄は権限不足で見えない場合がある。",size=25)
    save(im,"fig16-ss-output-anatomy.png")


def fig17():
    im,d=canvas("CloudShellからプライベートなUbuntuへ接続する", "AWSのトンネルとSSHユーザー認証は別の層")
    box(d,(70,300,360,500),"学生PC","ブラウザ",PURPLE,PURPLE_STROKE)
    box(d,(500,300,800,500),"CloudShell","SSHクライアント\n秘密鍵",BLUE,BLUE_STROKE)
    box(d,(940,300,1280,500),"Session Manager","AWS認証・トンネル",ORANGE,ORANGE_STROKE)
    box(d,(1420,300,1730,500),"Ubuntu EC2","ssm-user\nSSHサーバー",GREEN,GREEN_STROKE)
    arrow(d,(360,400),(500,400),"Console"); arrow(d,(800,400),(940,400),"開始"); arrow(d,(1280,400),(1420,400),"SSH通信")
    box(d,(500,700,800,850),"ホストエイリアス","jdu-ubuntu",GRAY,GRAY_STROKE)
    arrow(d,(650,700),(650,500),"設定")
    note(d,(950,700),"インターネットへTCP 22を公開する構成ではない。\nエイリアスはDNS名とは限らない。",size=29)
    save(im,"fig17-ssh-ssm-path.png")


def fig18():
    im,d=canvas("SCPのアップロードとダウンロード", "コマンドを実行するCloudShellをローカルとして方向を読む")
    box(d,(120,300,650,650),"CloudShell (ローカル)","local-source.txt\ndownloaded-result.txt",BLUE,BLUE_STROKE)
    box(d,(1150,300,1680,650),"Ubuntu (リモート)","upload.txt\nremote-result.txt",GREEN,GREEN_STROKE)
    arrow(d,(650,390),(1150,390),"アップロード: local → remote",color=BLUE_STROKE)
    arrow(d,(1150,560),(650,560),"ダウンロード: remote → local",color=GREEN_STROKE)
    note(d,(330,790),"scp SOURCE DESTINATION\nリモートパスは host:path の形。転送元と転送先を逆にしない。",size=32)
    save(im,"fig18-scp-directions.png")


def fig19():
    im,d=canvas("M7: OS機能を一つのシステムとして結ぶ", "設定 → 保存状態 → 実行状態 → 通信 → 観測")
    items=[((90,220,410,390),"ユーザー / グループ","誰のプロセスか",BLUE,BLUE_STROKE),((530,220,850,390),"アクセス権","何を読めるか",GREEN,GREEN_STROKE),((970,220,1290,390),"コンテンツファイル","何を返すか",GRAY,GRAY_STROKE),((1410,220,1710,390),"ユニットファイル","どう起動するか",PURPLE,PURPLE_STROKE),((1410,570,1710,740),"サービスプロセス","Main PID",BLUE,BLUE_STROKE),((970,570,1290,740),"ソケット","アドレス : ポート",ORANGE,ORANGE_STROKE),((530,570,850,740),"HTTP","ステータス / 本文",GREEN,GREEN_STROKE),((90,570,410,740),"ジャーナル","リクエストログ",GRAY,GRAY_STROKE)]
    for xy,t,b,f,s in items: box(d,xy,t,b,f,s,title_size=31,body_size=25)
    arrow(d,(410,305),(530,305),"資格"); arrow(d,(850,305),(970,305),"保護"); arrow(d,(1290,305),(1410,305),"パス")
    arrow(d,(1560,390),(1560,570),"systemd起動"); arrow(d,(1410,655),(1290,655),"待受 (listen)"); arrow(d,(970,655),(850,655),"応答"); arrow(d,(530,655),(410,655),"記録")
    note(d,(290,875),"一つのPASSだけで全体を推測しない。各層を対応するコマンドで観測する。",size=29)
    save(im,"fig19-integrated-service-system.png")


for fn in [fig01,fig02,fig02b,fig02c,fig03,fig04,fig05,fig06,fig07,fig08,fig09,fig10,fig11,fig12,fig13,fig14,fig15,fig16,fig17,fig18,fig19]:
    fn()

print(f"generated {len(list(OUT.glob('fig*.png')))} figures in {OUT}")
