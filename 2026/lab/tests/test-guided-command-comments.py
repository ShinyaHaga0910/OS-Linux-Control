#!/usr/bin/env python3
"""Require a purpose comment before every command in the guided solutions."""

from pathlib import Path
import re
import sys


practice = Path(sys.argv[1]).read_text(encoding="utf-8")
sections = re.findall(r"^## (P[0-6])\b(.*?)(?=^## |\Z)", practice, re.M | re.S)
assert len(sections) == 7, "expected P0-P6"

for mission, section in sections:
    assert "### 解答例（操作手順）" in section, mission
    solution = section.split("### 解答例（操作手順）", 1)[1]
    blocks = re.findall(r"^```bash\n(.*?)^```", solution, re.M | re.S)
    assert blocks, f"{mission}: no shell commands"
    commands = 0
    for block in blocks:
        previous = ""
        for line in block.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                previous = stripped
                continue
            assert previous.startswith("# "), f"{mission}: missing comment before {stripped}"
            commands += 1
            previous = ""
    assert commands > 0, mission
    print(f"PASS {mission}: {commands} commands have purpose comments")

assert "P3手順5～6" not in practice, "stale P3 step reference"
