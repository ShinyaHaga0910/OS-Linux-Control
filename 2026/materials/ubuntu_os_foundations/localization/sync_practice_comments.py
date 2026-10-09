"""Synchronize translated command-purpose comments with the Japanese practice source.

The command lines are never translated or edited. Unknown Japanese comments fail
closed so a source revision cannot silently drop teaching explanations.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"^```(bash|sh|shell|console)\n(.*?)^```", re.MULTILINE | re.DOTALL)
SOURCE = ROOT / "docs" / "ja" / "practice.md"
MAP = ROOT / "localization" / "practice_comments.tsv"


def executable(body: str) -> list[str]:
    return [line for line in body.splitlines() if not line.lstrip().startswith("#")]


def main() -> None:
    with MAP.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    translations = {row["ja"]: row for row in rows}
    assert len(translations) == len(rows), "duplicate comment key"
    ja_blocks = list(FENCE.finditer(SOURCE.read_text(encoding="utf-8")))
    for lang in ("ru", "uz"):
        target = ROOT / "docs" / lang / "practice.md"
        current = target.read_text(encoding="utf-8")
        blocks = list(FENCE.finditer(current))
        assert len(ja_blocks) == len(blocks), f"{lang}: different code block count"
        replacements: list[tuple[int, int, str]] = []
        for ja, translated in zip(ja_blocks, blocks, strict=True):
            assert ja.group(1) == translated.group(1), f"{lang}: code language differs"
            assert executable(ja.group(2)) == executable(translated.group(2)), (
                f"{lang}: executable commands differ"
            )
            lines = []
            for line in ja.group(2).splitlines():
                if line.lstrip().startswith("#"):
                    key = line.lstrip()[1:].strip()
                    assert key in translations, f"untranslated Japanese comment: {key}"
                    lines.append(f"# {translations[key][lang]}")
                else:
                    lines.append(line)
            body = "\n".join(lines) + ("\n" if ja.group(2).endswith("\n") else "")
            replacements.append((translated.start(2), translated.end(2), body))
        for start, end, body in reversed(replacements):
            current = current[:start] + body + current[end:]
        current = re.sub(r"(?m)^### (Шаг |\d+-bosqich:)", r"#### \1", current)
        target.write_text(current, encoding="utf-8")
        print(f"{lang}: synchronized {len(blocks)} command blocks")


if __name__ == "__main__":
    main()
