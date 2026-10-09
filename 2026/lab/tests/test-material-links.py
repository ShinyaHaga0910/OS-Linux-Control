"""Audit current material links and generated legacy copies."""

from pathlib import Path
import importlib.util
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = Path(sys.argv[1]).resolve()
MATERIALS = ROOT / "2026/materials/ubuntu_os_foundations"
LEGACY = MATERIALS / "v1.0.0"
REPOSITORY = "ShinyaHaga0910/OS-Linux-Control"


def destination(source: Path, url: str) -> Path | None:
    parsed = urlparse(url)
    if parsed.scheme:
        for host, prefix in (
            ("github.com", f"/{REPOSITORY}/blob/main/"),
            ("github.com", f"/{REPOSITORY}/tree/main/"),
            ("raw.githubusercontent.com", f"/{REPOSITORY}/main/"),
        ):
            if parsed.netloc == host and parsed.path.startswith(prefix):
                return (ROOT / unquote(parsed.path[len(prefix):])).resolve()
        return None
    return (source.parent / unquote(parsed.path)).resolve() if parsed.path else source


sources = [*ROOT.glob("*.md"), *MATERIALS.rglob("*.md"), *(ROOT / "2026/lab").rglob("*.md")]
count = 0
for source in sources:
    text = re.sub(r"(?ms)^```.*?^```\s*$", "", source.read_text(encoding="utf-8"))
    for url in re.findall(r"!?\[[^]]*\]\(([^)]+)\)", text):
        target = destination(source, url)
        if target is None:
            continue
        assert target.is_relative_to(ROOT), (source, url, target)
        assert target.exists(), (source, url, target)
        if not source.is_relative_to(LEGACY):
            assert not target.is_relative_to(LEGACY), (source, "current link points to compatibility copy", url)
        count += 1

spec = importlib.util.spec_from_file_location("sync_legacy", MATERIALS / "build/sync_legacy_paths.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert module.sync(check=True) > 0
print(f"PASS {count} local/current material links and generated compatibility URLs")
