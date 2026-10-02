from __future__ import annotations

from pathlib import Path
import html
import os
import re
import shutil

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak,
    Preformatted, Image, Table, TableStyle, KeepTogether
)
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parents[1]
TEXTBOOK = ROOT / "docs" / "ja" / "textbook"
HTML_OUT = ROOT / "output" / "html"
PDF_OUT = ROOT / "output" / "pdf"
HTML_OUT.mkdir(parents=True, exist_ok=True)
PDF_OUT.mkdir(parents=True, exist_ok=True)

def resolve_font(env_name: str, candidates: list[Path]) -> Path:
    configured = os.environ.get(env_name)
    search = ([Path(configured)] if configured else []) + candidates
    for path in search:
        if path.is_file():
            return path
    checked = "\n".join(f"- {path}" for path in search)
    raise FileNotFoundError(
        f"Japanese font not found. Set {env_name} to a TrueType font file.\nChecked:\n{checked}"
    )


FONT_REG = resolve_font("JDU_FONT_SANS", [
    Path(r"C:\Windows\Fonts\NotoSansJP-VF.ttf"),
    Path.home() / ".local" / "share" / "fonts" / "NotoSansJP-Regular.ttf",
])
FONT_SERIF = resolve_font("JDU_FONT_SERIF", [
    Path(r"C:\Windows\Fonts\NotoSerifJP-VF.ttf"),
    Path.home() / ".local" / "share" / "fonts" / "NotoSerifJP-Regular.ttf",
])
pdfmetrics.registerFont(TTFont("NotoSansJP", str(FONT_REG)))
pdfmetrics.registerFont(TTFont("NotoSerifJP", str(FONT_SERIF)))

PAGE_W, PAGE_H = A4
MARGIN_X = 18 * mm
MARGIN_TOP = 19 * mm
MARGIN_BOTTOM = 17 * mm

BLUE = colors.HexColor("#245E9A")
INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#526079")
PALE = colors.HexColor("#EEF4FB")
GRID = colors.HexColor("#CBD5E1")


def inline_md(text: str) -> str:
    text = html.escape(text, quote=False)
    code_spans = []
    def preserve_code(match):
        code_spans.append('<font name="NotoSansJP" backColor="#EEF2F7">' + match.group(1) + '</font>')
        return f"\x00CODE{len(code_spans)-1}\x00"
    text = re.sub(r"`([^`]+)`", preserve_code, text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" color="#245E9A">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    for index, span in enumerate(code_spans):
        text = text.replace(f"\x00CODE{index}\x00", span)
    return text


def parse_table(lines: list[str]) -> list[list[str]]:
    rows = []
    for line in lines:
        content = line.strip().strip("|")
        cells, current = [], []
        in_code = False
        escaped = False
        for ch in content:
            if escaped:
                current.append(ch)
                escaped = False
                continue
            if ch == "\\":
                current.append(ch)
                escaped = True
                continue
            if ch == "`":
                in_code = not in_code
                current.append(ch)
                continue
            if ch == "|" and not in_code:
                cells.append("".join(current).strip())
                current = []
            else:
                current.append(ch)
        cells.append("".join(current).strip())
        rows.append(cells)
    if len(rows) >= 2 and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in rows[1]):
        rows.pop(1)
    return rows


def markdown_blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    para: list[str] = []

    def flush_para():
        nonlocal para
        if para:
            yield ("p", " ".join(x.strip() for x in para))
            para = []

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            yield from flush_para()
            lang = line[3:].strip()
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            yield ("code", lang, "\n".join(code))
        elif re.match(r"^#{1,4} ", line):
            yield from flush_para()
            level = len(line) - len(line.lstrip("#"))
            yield ("h", level, line[level + 1:])
        elif re.match(r"^!\[[^]]*\]\([^)]+\)", line):
            yield from flush_para()
            m = re.match(r"^!\[([^]]*)\]\(([^)]+)\)", line)
            yield ("img", m.group(1), m.group(2))
        elif line.startswith("|") and "|" in line[1:]:
            yield from flush_para()
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            i -= 1
            yield ("table", parse_table(table_lines))
        elif re.match(r"^[-*] ", line):
            yield from flush_para()
            items = []
            while i < len(lines) and re.match(r"^[-*] ", lines[i]):
                items.append(lines[i][2:].strip())
                i += 1
            i -= 1
            yield ("ul", items)
        elif re.match(r"^\d+\. ", line):
            yield from flush_para()
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i]).strip())
                i += 1
            i -= 1
            yield ("ol", items)
        elif line.startswith("> "):
            yield from flush_para()
            yield ("quote", line[2:])
        elif not line.strip():
            yield from flush_para()
        else:
            para.append(line)
        i += 1
    yield from flush_para()


def html_inline(text: str) -> str:
    text = html.escape(text)
    code_spans = []
    def preserve_code(match):
        code_spans.append('<code>' + match.group(1) + '</code>')
        return f"\x00CODE{len(code_spans)-1}\x00"
    text = re.sub(r"`([^`]+)`", preserve_code, text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    for index, span in enumerate(code_spans):
        text = text.replace(f"\x00CODE{index}\x00", span)
    return text


CSS = """
@page { size: A4; margin: 18mm; }
body { max-width: 174mm; margin: 0 auto; font-family: 'Noto Sans JP','Yu Gothic',sans-serif; color:#172033; line-height:1.78; font-size:10.5pt; }
h1 { color:#174E84; border-bottom:3px solid #79A9D7; padding-bottom:3mm; page-break-before:always; }
h1:first-of-type { page-break-before:auto; }
h2 { color:#245E9A; margin-top:9mm; border-left:4px solid #4A90C2; padding-left:3mm; }
@media print { h2.chapter-answers { break-before: page; page-break-before: always; } }
h3 { color:#315E79; margin-top:6mm; }
h4 { color:#315E79; margin-top:4mm; margin-bottom:2mm; font-size:10.5pt; }
p { text-align:justify; }
code { font-family: Consolas,'Noto Sans Mono',monospace; background:#EEF2F7; padding:0 1mm; }
pre { background:#172033; color:#F6F8FB; padding:4mm; border-radius:2mm; white-space:pre-wrap; overflow-wrap:anywhere; }
img { display:block; max-width:100%; height:auto; margin:5mm auto 2mm; page-break-inside:avoid; }
table { width:100%; border-collapse:collapse; margin:4mm 0; font-size:9pt; page-break-inside:auto; }
th { background:#245E9A; color:white; }
th,td { border:1px solid #CBD5E1; padding:2mm; vertical-align:top; }
blockquote { background:#EEF4FB; border-left:4px solid #4A90C2; padding:3mm; }
.cover { min-height:230mm; display:flex; flex-direction:column; justify-content:center; text-align:center; page-break-after:always; }
.cover h1 { page-break-before:auto; font-size:26pt; border:0; }
.meta { color:#526079; }
"""


def build_html(title: str, sources: list[Path], output: Path):
    parts = ["<!doctype html><html lang='ja'><head><meta charset='utf-8'>", f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>",
             f"<section class='cover'><h1>{html.escape(title)}</h1><p class='meta'>Ubuntu Server 24.04 LTS / JDU Cyber Security<br>2026-09-25</p></section>"]
    for src in sources:
        for block in markdown_blocks(src):
            kind = block[0]
            if kind == "h":
                answer_class = " class='chapter-answers'" if src.parent == TEXTBOOK and block[1] == 2 and block[2] == "章末解答" else ""
                parts.append(f"<h{block[1]}{answer_class}>{html_inline(block[2])}</h{block[1]}>")
            elif kind == "p": parts.append(f"<p>{html_inline(block[1])}</p>")
            elif kind == "code": parts.append(f"<pre><code>{html.escape(block[2])}</code></pre>")
            elif kind == "img":
                ip = (src.parent / block[2]).resolve()
                rel = Path(os.path.relpath(ip, output.parent)).as_posix()
                parts.append(f"<figure><img src='{rel}' alt='{html.escape(block[1])}'></figure>")
            elif kind == "ul": parts.append("<ul>" + "".join(f"<li>{html_inline(x)}</li>" for x in block[1]) + "</ul>")
            elif kind == "ol": parts.append("<ol>" + "".join(f"<li>{html_inline(x)}</li>" for x in block[1]) + "</ol>")
            elif kind == "quote": parts.append(f"<blockquote>{html_inline(block[1])}</blockquote>")
            elif kind == "table":
                rows = block[1]
                parts.append("<table>")
                for ri,row in enumerate(rows):
                    tag = "th" if ri == 0 else "td"
                    parts.append("<tr>" + "".join(f"<{tag}>{html_inline(c)}</{tag}>" for c in row) + "</tr>")
                parts.append("</table>")
    parts.append("</body></html>")
    output.write_text("\n".join(parts), encoding="utf-8")


styles = getSampleStyleSheet()
BODY = ParagraphStyle("BodyJP", fontName="NotoSerifJP", fontSize=9.3, leading=15.2, textColor=INK, spaceAfter=3.0*mm, splitLongWords=True, wordWrap="CJK")
QUESTION = ParagraphStyle("QuestionJP", parent=BODY, keepWithNext=True)
H1 = ParagraphStyle("H1JP", fontName="NotoSansJP", fontSize=20, leading=28, textColor=BLUE, spaceBefore=3*mm, spaceAfter=6*mm, keepWithNext=True, wordWrap="CJK")
H2 = ParagraphStyle("H2JP", fontName="NotoSansJP", fontSize=14.5, leading=21, textColor=BLUE, spaceBefore=6*mm, spaceAfter=3*mm, keepWithNext=True, wordWrap="CJK", borderColor=colors.HexColor("#7FAAD4"), borderWidth=0, borderPadding=0)
H3 = ParagraphStyle("H3JP", fontName="NotoSansJP", fontSize=11.5, leading=17, textColor=colors.HexColor("#315E79"), spaceBefore=4*mm, spaceAfter=2*mm, keepWithNext=True, wordWrap="CJK")
H4 = ParagraphStyle("H4JP", fontName="NotoSansJP", fontSize=10.5, leading=15, textColor=colors.HexColor("#315E79"), spaceBefore=3*mm, spaceAfter=1.5*mm, keepWithNext=True, wordWrap="CJK")
CAP = ParagraphStyle("CaptionJP", parent=BODY, fontName="NotoSansJP", fontSize=8.3, leading=12.5, textColor=MUTED, alignment=TA_CENTER, spaceBefore=1*mm, spaceAfter=4*mm)
LIST = ParagraphStyle("ListJP", parent=BODY, leftIndent=7*mm, firstLineIndent=-4*mm, bulletIndent=1*mm, spaceAfter=1.5*mm)
CODE = ParagraphStyle("CodeJP", fontName="NotoSansJP", fontSize=7.8, leading=11.2, textColor=INK, splitLongWords=True)
QUOTE = ParagraphStyle("QuoteJP", parent=BODY, leftIndent=6*mm, rightIndent=4*mm, backColor=PALE, borderColor=BLUE, borderWidth=1, borderPadding=7)


class BookDocTemplate(BaseDocTemplate):
    def __init__(self, filename, book_title, **kw):
        self.book_title = book_title
        super().__init__(filename, pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                         topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM, **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
        self.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=self._page))

    def _page(self, canv, doc):
        if doc.page == 1:
            return
        canv.saveState()
        canv.setFont("NotoSansJP", 7.5)
        canv.setFillColor(MUTED)
        canv.drawString(MARGIN_X, PAGE_H - 11*mm, self.book_title)
        canv.drawRightString(PAGE_W - MARGIN_X, 9*mm, str(doc.page))
        canv.setStrokeColor(GRID)
        canv.line(MARGIN_X, PAGE_H - 13*mm, PAGE_W - MARGIN_X, PAGE_H - 13*mm)
        canv.restoreState()


def cover_story(title: str, subtitle: str, meta: str | None = None):
    cover_title = title.replace("オペレーティングシステムとLinuxの基本操作", "オペレーティングシステム<br/>とLinuxの基本操作")
    story = [Spacer(1, 52*mm), Paragraph(cover_title, ParagraphStyle("Cover", fontName="NotoSansJP", fontSize=27, leading=38, alignment=TA_CENTER, textColor=BLUE, wordWrap="CJK"))]
    if subtitle:
        story.extend([Spacer(1, 12*mm), Paragraph(subtitle, ParagraphStyle("Sub", fontName="NotoSansJP", fontSize=13, leading=21, alignment=TA_CENTER, textColor=MUTED, wordWrap="CJK"))])
    if meta is None:
        meta = "Ubuntu Server 24.04 LTS / 公開Lab v1.0.0<br/>JDU Cyber Security / 2026-09-25"
    story.extend([Spacer(1, 60*mm), Paragraph(meta, ParagraphStyle("Meta", fontName="NotoSansJP", fontSize=9.5, leading=15, alignment=TA_CENTER, textColor=MUTED)), PageBreak()])
    return story


def blocks_to_story(src: Path, pagebreak_h1=False):
    story = []
    first_h1 = True
    question_follows = False
    in_answers = False
    for block in markdown_blocks(src):
        kind = block[0]
        if kind == "h":
            level,text = block[1],block[2]
            if level == 1 and pagebreak_h1 and not first_h1:
                story.append(PageBreak())
            if src.parent.name == "textbook" and level == 2 and text in {"章末解答", "Bob yakunidagi javoblar", "Ответы на вопросы главы"}:
                story.append(PageBreak())
                in_answers = True
            if level == 1: first_h1 = False
            story.append(Paragraph(inline_md(text), {1:H1,2:H2,3:H3,4:H4}.get(level,H3)))
            question_follows = not in_answers and level == 3 and bool(re.fullmatch(r"(?:問\d+|Вопрос\s+\d+\.?)", text))
        elif kind == "p":
            sty = CAP if block[1].startswith(("**図", "**写真", "**Рисунок", "**Фото")) or re.match(r"\*\*\d+-\d+-(?:rasm|foto)", block[1]) else QUESTION if question_follows else BODY
            story.append(Paragraph(inline_md(block[1]), sty))
            question_follows = False
        elif kind == "code":
            code = block[2] or " "
            code_flow = Preformatted(code, CODE, maxLineLength=105, splitChars=" /:_-")
            code_box = Table([[code_flow]], colWidths=[170*mm], hAlign="LEFT")
            code_box.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#E9EEF5")),
                ("BOX", (0,0), (-1,-1), 0.6, colors.HexColor("#B8C5D6")),
                ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
                ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ]))
            story.extend([code_box, Spacer(1, 3*mm)])
        elif kind == "img":
            ip = (src.parent / block[2]).resolve()
            max_w,max_h = 170*mm,105*mm
            if ip.suffix.lower() == ".svg":
                if ip.parent.name in {"uz", "ru"}:
                    pdf_raster = ip.with_suffix(".png")
                else:
                    pdf_raster = ROOT / "assets" / "figure-sources-v1.2" / "generated" / f"{ip.stem}-pdf.png"
                if pdf_raster.is_file():
                    with ImageReaderSize(pdf_raster) as (iw,ih):
                        scale=min(max_w/iw,max_h/ih,1)
                        story.append(Image(str(pdf_raster),width=iw*scale,height=ih*scale))
                else:
                    drawing = svg2rlg(str(ip))
                    if drawing is None or not drawing.width or not drawing.height:
                        raise ValueError(f"Could not load SVG figure: {ip}")
                    scale=min(max_w/drawing.width,max_h/drawing.height,1)
                    drawing.scale(scale,scale)
                    drawing.width *= scale
                    drawing.height *= scale
                    drawing.hAlign = "CENTER"
                    story.append(drawing)
            else:
                with ImageReaderSize(ip) as (iw,ih):
                    scale=min(max_w/iw,max_h/ih,1)
                    story.append(Image(str(ip),width=iw*scale,height=ih*scale))
        elif kind in ("ul","ol"):
            for idx,item in enumerate(block[1],1):
                bullet = "•" if kind == "ul" else f"{idx}."
                story.append(Paragraph(f"{bullet} {inline_md(item)}", LIST))
        elif kind == "quote":
            story.append(Paragraph(inline_md(block[1]), QUOTE))
        elif kind == "table":
            rows=block[1]
            ncols=max(len(r) for r in rows)
            pdata=[]
            for ri,row in enumerate(rows):
                row=row+[""]*(ncols-len(row))
                sty=ParagraphStyle(f"T{ri}",fontName="NotoSansJP",fontSize=7.0 if ncols>=4 else 7.8,leading=10.2 if ncols>=4 else 11.2,textColor=colors.white if ri==0 else INK,wordWrap="CJK")
                pdata.append([Paragraph(inline_md(c),sty) for c in row])
            colw=[170*mm/ncols]*ncols
            tbl=Table(pdata,colWidths=colw,repeatRows=1,hAlign="LEFT")
            tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),BLUE),("GRID",(0,0),(-1,-1),0.5,GRID),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F7F9FC")])]))
            story.extend([tbl,Spacer(1,3*mm)])
    return story


class ImageReaderSize:
    def __init__(self,path): self.path=path
    def __enter__(self):
        from PIL import Image as PILImage
        with PILImage.open(self.path) as im:
            self.size=im.size
        return self.size
    def __exit__(self,*args): return False


def build_pdf(title, subtitle, sources, output, chapters=False, meta=None):
    doc=BookDocTemplate(str(output),title,author="JDU Cyber Security",title=title,subject=subtitle)
    story=cover_story(title,subtitle,meta=meta)
    for index,src in enumerate(sources):
        if chapters and index>0: story.append(PageBreak())
        story.extend(blocks_to_story(src,pagebreak_h1=False))
    doc.build(story)


def main():
    chapters=sorted(TEXTBOOK.glob("*.md"))
    sets=[
        ("オペレーティングシステムとLinuxの基本操作","",chapters,"ubuntu_os_textbook_ja"),
        ("Ubuntu・OS基礎 練習課題と解答例","P1～P6 課題と操作手順",[ROOT/"docs/ja/practice.md"],"ubuntu_os_guided_practice_ja"),
        ("Ubuntu・OS基礎 自力課題","M0～M7 Mission Guide",[ROOT/"docs/ja/missions.md"],"ubuntu_os_missions_ja"),
        ("Ubuntu・OS基礎 参照資料","用語集・コマンド早見表",[ROOT/"docs/ja/reference.md"],"ubuntu_os_reference_ja"),
    ]
    for title,subtitle,sources,stem in sets:
        build_html(title,sources,HTML_OUT/f"{stem}.html")
        build_pdf(title,subtitle,sources,PDF_OUT/f"{stem}.pdf",chapters=(stem=="ubuntu_os_textbook_ja"))
        print(f"built {stem}")


if __name__ == "__main__":
    main()
