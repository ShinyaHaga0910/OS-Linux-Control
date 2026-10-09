"""Build localized figures from reviewed Japanese diagrams and label map."""

from __future__ import annotations

import csv
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "figures"
D2 = ROOT / "assets" / "figure-sources-v1.2" / "d2"
TYPST = ROOT / "assets" / "figure-sources-v1.2" / "typst"
OUT = SOURCE / "uz"
LABELS_PATH = ROOT / "localization" / "figure_labels_uz.tsv"
LABEL_COLUMN = "uz"
JAPANESE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
TYPST_NAMES = {"fig06-path-tree", "fig07-nano-workflow", "fig16-ss-output-anatomy"}


def load_labels() -> dict[str, str]:
    with LABELS_PATH.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    labels = {row["ja"]: row[LABEL_COLUMN] for row in rows}
    if len(labels) != len(rows) or not all(labels.values()):
        raise ValueError("Figure label map contains duplicate or empty entries")
    return labels


def localize_d2(path: Path, labels: dict[str, str], d2: str, font: Path, temp: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for japanese, uzbek in sorted(labels.items(), key=lambda pair: len(pair[0]), reverse=True):
        text = text.replace(japanese, uzbek)
    if JAPANESE.search(text):
        raise ValueError(f"Japanese labels remain in {path.name}")
    source = temp / path.name
    source.write_text(text, encoding="utf-8")
    flags = ["--layout", "elk", "--pad", "36", "--font-regular", str(font), "--font-bold", str(font), "--font-semibold", str(font)]
    for fmt in ("svg", "png"):
        output = OUT / f"{path.stem}.{fmt}"
        command = [d2, *flags]
        if fmt == "png":
            command += ["--scale", "2"]
        command += [str(source), str(output)]
        subprocess.run(command, check=True, cwd=temp)
        if fmt == "svg":
            svg = output.read_text(encoding="utf-8")
            svg = re.sub(r"@font-face\s*\{.*?\}", "", svg, flags=re.DOTALL)
            svg = re.sub(r"d2-\d+-font-(regular|bold|semibold|italic)", "NotoSansJP", svg)
            output.write_text(svg, encoding="utf-8")


def localize_typst(path: Path, labels: dict[str, str], typst: str, temp: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for japanese, uzbek in sorted(labels.items(), key=lambda pair: len(pair[0]), reverse=True):
        text = text.replace(japanese, uzbek)
    if JAPANESE.search(text):
        raise ValueError(f"Japanese labels remain in {path.name}")
    source = temp / path.name
    source.write_text(text, encoding="utf-8")
    # fig16 imports the unchanged terminal screenshot from its relative source directory.
    if path.stem == "fig16-ss-output-anatomy":
        text = text.replace('"../generated/fig16-terminal.svg"', '"../assets/figure-sources-v1.2/generated/fig16-terminal.svg"')
        source.write_text(text, encoding="utf-8")
    for fmt in ("svg", "png"):
        output = OUT / f"{path.stem}.{fmt}"
        command = [typst, "compile", "--root", str(ROOT), "--format", fmt]
        if fmt == "png":
            command += ["--ppi", "220"]
        command += [str(source), str(output)]
        subprocess.run(command, check=True)


def main() -> None:
    labels = load_labels()
    OUT.mkdir(parents=True, exist_ok=True)
    d2 = shutil.which("d2") or str(Path("C:/Program Files/D2/d2.exe"))
    if not Path(d2).is_file():
        raise FileNotFoundError("D2 is required to redraw localized diagrams")
    font = Path("C:/Windows/Fonts/NotoSansJP-VF.ttf")
    if not font.is_file():
        raise FileNotFoundError("Noto Sans JP font is required to redraw localized diagrams")
    with tempfile.TemporaryDirectory(prefix="jdu-uz-d2-", dir=ROOT) as scratch:
        temp = Path(scratch)
        shutil.copy2(D2 / "theme.d2", temp / "theme.d2")
        for figure in sorted(D2.glob("fig*.d2")):
            localize_d2(figure, labels, d2, font, temp)
    typst = shutil.which("typst")
    if not typst:
        candidates = list(Path.home().glob("AppData/Local/Microsoft/WinGet/Packages/Typst.Typst_*/typst-*/typst.exe"))
        typst = str(candidates[0]) if candidates else None
    if not typst:
        raise FileNotFoundError("Typst is required to localize figures 06, 07, and 16")
    with tempfile.TemporaryDirectory(prefix="jdu-uz-figures-", dir=ROOT) as scratch:
        for stem in sorted(TYPST_NAMES):
            localize_typst(TYPST / f"{stem}.typ", labels, typst, Path(scratch))
    if len(list(OUT.glob("fig*.svg"))) != 21:
        raise ValueError("Expected 21 localized SVG figures")
    print(f"Generated 21 localized SVG figures in {OUT}")


if __name__ == "__main__":
    main()
