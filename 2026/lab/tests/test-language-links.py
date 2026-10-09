#!/usr/bin/env python3
"""Check language navigation and current translation-status notices."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse


ROOT = Path(sys.argv[1]).resolve()
LAB = ROOT / "2026/lab"
DOCS = ROOT / "2026/materials/ubuntu_os_foundations/docs"
LABELS = ("日本語", "Русский", "O‘zbekcha")
LANGS = ("ja", "ru", "uz")
LINK = re.compile(r"\[(日本語|Русский|O‘zbekcha)\]\(([^)]+)\)")
GITHUB_PREFIX = "/ShinyaHaga0910/OS-Linux-Control/blob/main/"


def resolve_link(source: Path, destination: str) -> Path:
    parsed = urlparse(destination)
    if parsed.scheme:
        assert parsed.scheme == "https" and parsed.netloc == "github.com", destination
        assert parsed.path.startswith(GITHUB_PREFIX), destination
        return (ROOT / unquote(parsed.path[len(GITHUB_PREFIX) :])).resolve()
    assert not parsed.netloc, destination
    return (source.parent / unquote(parsed.path)).resolve()


def check_navigation(source: Path, targets: dict[str, Path]) -> None:
    assert source.is_file(), source
    top = "\n".join(source.read_text(encoding="utf-8").splitlines()[:7])
    links = LINK.findall(top)
    assert [label for label, _ in links] == list(LABELS), (source, links)
    for label, destination in links:
        actual = resolve_link(source, destination)
        expected = targets[label].resolve()
        assert actual == expected and actual.is_file(), (source, label, actual, expected)


def check_local_links(source: Path) -> None:
    text = source.read_text(encoding="utf-8")
    for destination in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        if urlparse(destination).scheme:
            continue
        path = unquote(destination.split("#", 1)[0])
        target = (source.parent / path).resolve() if path else source
        assert target.exists(), (source, destination, target)


def trio(*paths: Path) -> None:
    targets = dict(zip(LABELS, paths, strict=True))
    for path in paths:
        check_navigation(path, targets)


trio(LAB / "UPDATE_EXISTING.md", LAB / "UPDATE_EXISTING.ru.md", LAB / "UPDATE_EXISTING.uz.md")
trio(*(LAB / "setup" / f"student-registration.{lang}.md" for lang in LANGS))
trio(*(DOCS / lang / "README.md" for lang in LANGS))
for name in ("practice.md", "missions.md", "reference.md"):
    trio(*(DOCS / lang / name for lang in LANGS))
for name in sorted((DOCS / "ja/textbook").glob("*.md")):
    trio(*(DOCS / lang / "textbook" / name.name for lang in LANGS))

for source, name in (
    (LAB / "GUIDED_PRACTICE.md", "practice.md"),
    (DOCS / "ja/GUIDED_PRACTICE.md", "practice.md"),
    (LAB / "MISSION_GUIDE.md", "missions.md"),
):
    check_navigation(source, dict(zip(LABELS, (DOCS / lang / name for lang in LANGS), strict=True)))

for source, targets in (
    (ROOT / "README.md", tuple(DOCS / lang / "README.md" for lang in LANGS)),
    (LAB / "README.md", tuple(LAB / "setup" / f"student-registration.{lang}.md" for lang in LANGS)),
    (LAB / "setup/README.md", tuple(LAB / "setup" / f"student-registration.{lang}.md" for lang in LANGS)),
    (DOCS.parent / "README.md", tuple(DOCS / lang / "README.md" for lang in LANGS)),
):
    check_navigation(source, dict(zip(LABELS, targets, strict=True)))

for source in (
    ROOT / "README.md",
    LAB / "README.md",
    LAB / "setup/README.md",
    DOCS.parent / "README.md",
    *(DOCS / lang / "README.md" for lang in LANGS),
    *(LAB / "setup" / f"student-registration.{lang}.md" for lang in LANGS),
    LAB / "UPDATE_EXISTING.md",
    LAB / "UPDATE_EXISTING.ru.md",
    LAB / "UPDATE_EXISTING.uz.md",
):
    check_local_links(source)


def bash_blocks(path: Path) -> list[str]:
    return re.findall(r"(?ms)^```bash\n(.*?)^```", path.read_text(encoding="utf-8"))


guide_blocks = bash_blocks(LAB / "UPDATE_EXISTING.md")
assert len(guide_blocks) == 5, len(guide_blocks)
for lang in ("ru", "uz"):
    assert bash_blocks(LAB / f"UPDATE_EXISTING.{lang}.md") == guide_blocks, lang
    for name in ("practice.md", "missions.md"):
        text = (DOCS / lang / name).read_text(encoding="utf-8")
        assert text.splitlines()[4].startswith("> "), (lang, name)

practice = (DOCS / "ja/practice.md").read_bytes()
assert practice == (DOCS / "ja/GUIDED_PRACTICE.md").read_bytes()
assert practice == (LAB / "GUIDED_PRACTICE.md").read_bytes()
assert (DOCS / "ja/missions.md").read_bytes() == (LAB / "MISSION_GUIDE.md").read_bytes()
print("PASS current student Markdown language navigation, counterpart links, translation status, and update-guide commands")
