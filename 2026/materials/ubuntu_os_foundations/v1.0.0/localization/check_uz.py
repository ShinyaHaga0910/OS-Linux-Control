"""Read-only structural checks for translated chapter drafts."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JA = ROOT / "docs" / "ja" / "textbook"
LANG = "uz"
TARGET_ROOT = ROOT / "docs" / LANG
UZ = TARGET_ROOT / "textbook"
FENCE = re.compile(r"^```([^\n]*)\n(.*?)^```", re.MULTILINE | re.DOTALL)
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
URL = re.compile(r"https?://[^)`\s]+")
SECTION = re.compile(r"^## (\d+\.\d+)\b", re.MULTILINE)
LANGUAGE_NAV = re.compile(r"^\[日本語\]\([^)]+\) · \[Русский\]\([^)]+\) · \[O‘zbekcha\]\([^)]+\)$", re.MULTILINE)
TASK_ID = re.compile(r"^## ([PM]\d+)\b", re.MULTILINE)
NUMBERED_ITEM = re.compile(r"^\d+\.\s", re.MULTILINE)


def check_pair(source: Path, target: Path) -> list[str]:
    # GitHub-only language links are navigation, not translated lesson content.
    ja = LANGUAGE_NAV.sub("", source.read_text(encoding="utf-8"))
    uz = LANGUAGE_NAV.sub("", target.read_text(encoding="utf-8"))
    errors = []
    def runnable(text: str) -> list[tuple[str, str]]:
        result = []
        for lang, body in FENCE.findall(text):
            if lang.strip() in {"bash", "sh", "shell", "console"}:
                commands = "\n".join(line for line in body.splitlines() if not line.lstrip().startswith("#"))
                result.append((lang, commands))
        return result
    if runnable(ja) != runnable(uz):
        errors.append("runnable code blocks differ")
    if source.name == "practice.md":
        ja_comments = [[line for line in body.splitlines() if line.lstrip().startswith("#")]
                       for _, body in FENCE.findall(ja)]
        target_comments = [[line for line in body.splitlines() if line.lstrip().startswith("#")]
                           for _, body in FENCE.findall(uz)]
        if [len(block) for block in ja_comments] != [len(block) for block in target_comments]:
            errors.append("command-purpose comments differ")
    if source.name in {"practice.md", "missions.md"}:
        expected = [f"P{i}" for i in range(7)] if source.name == "practice.md" else [f"M{i}" for i in range(1, 8)]
        if TASK_ID.findall(ja) != expected or TASK_ID.findall(uz) != expected:
            errors.append("P/M section IDs differ")
        def numbered_counts(text: str) -> list[int]:
            headings = list(TASK_ID.finditer(text))
            return [len(NUMBERED_ITEM.findall(text[m.end():headings[i + 1].start() if i + 1 < len(headings) else len(text)]))
                    for i, m in enumerate(headings)]
        if numbered_counts(ja) != numbered_counts(uz):
            errors.append("numbered task counts differ")
        if source.name == "practice.md":
            step = re.compile(r"^#### (?:手順|Шаг |\d+-bosqich:)", re.MULTILINE)
            if len(step.findall(ja)) != len(step.findall(uz)):
                errors.append("guided step counts differ")
    if [Path(path).name for path in IMAGE.findall(ja)] != [Path(path).name for path in IMAGE.findall(uz)]:
        errors.append("figure identities differ")
    if URL.findall(ja) != URL.findall(uz):
        errors.append("URLs differ")
    if SECTION.findall(ja) != SECTION.findall(uz):
        errors.append("numbered sections differ")
    if re.search(r"[\u3040-\u30ff\u3400-\u9fff]", uz):
        errors.append("Japanese characters remain")
    if LANG == "uz" and re.search(r"[\u0400-\u04ff]", uz):
        errors.append("Cyrillic characters remain")
    for path in IMAGE.findall(uz):
        if not (target.parent / path).resolve().is_file():
            errors.append(f"missing image: {path}")
    return errors


def main() -> int:
    manifest = json.loads((ROOT / "localization" / "manifest.json").read_text(encoding="utf-8"))
    translation_status = manifest["languages"][LANG]
    if any(translation_status.get(f"{kind}_status") != "synced_to_ja_pending_native_review"
           for kind in ("practice", "missions", "reference", "afterword")):
        print(f"FAIL: {LANG} translation status is not current")
        return 1
    with (ROOT / "localization" / "terminology.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows or any(not row[LANG].strip() for row in rows):
        print(f"FAIL: {LANG} glossary has empty entries")
        return 1
    found = sorted(UZ.glob("[0-9][0-9]-*.md"))
    if not found:
        print(f"FAIL: no {LANG} chapters")
        return 1
    failed = 0
    for target in found:
        source = JA / target.name
        errors = ["missing Japanese source"] if not source.is_file() else check_pair(source, target)
        status = "FAIL" if errors else "PASS"
        print(f"{status}: {target.name}" + (f": {', '.join(errors)}" if errors else ""))
        failed += bool(errors)
    afterword = UZ / "afterword.md"
    if afterword.is_file():
        errors = check_pair(JA / afterword.name, afterword)
        print(f"{'FAIL' if errors else 'PASS'}: {afterword.name}" + (f": {', '.join(errors)}" if errors else ""))
        failed += bool(errors)
    else:
        print(f"FAIL: {LANG} afterword.md is missing")
        failed += 1
    for name in ("practice.md", "missions.md", "reference.md"):
        target = TARGET_ROOT / name
        errors = check_pair(ROOT / "docs" / "ja" / name, target) if target.is_file() else [f"missing {LANG} file"]
        print(f"{'FAIL' if errors else 'PASS'}: {name}" + (f": {', '.join(errors)}" if errors else ""))
        failed += bool(errors)
    figures = sorted((ROOT / "assets" / "figures" / LANG).glob("fig*.svg"))
    if len(figures) != 21:
        print(f"FAIL: expected 21 {LANG} SVG figures, found {len(figures)}")
        failed += 1
    for figure in figures:
        if re.search(r"[\u3040-\u30ff\u3400-\u9fff]", figure.read_text(encoding="utf-8")):
            print(f"FAIL: Japanese text remains in {figure.name}")
            failed += 1
    print(f"Checked {len(found)} {LANG} chapter(s); {failed} failed; translation pending native review.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
