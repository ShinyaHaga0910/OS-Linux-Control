"""Generate compatibility entry pages and copies for previously published URLs."""

from pathlib import Path
import argparse
import json
import os
import shutil

ROOT = Path(__file__).resolve().parents[1]


def entry_text(relative: str, source: Path, target: Path) -> str:
    link = Path(os.path.relpath(source, target.parent)).as_posix()
    if relative.startswith("docs/ru/"):
        return f"# Материал перенесён\n\nЭтот адрес сохранён для совместимости.\n\n[Открыть текущий материал]({link})\n\nВерсия публикации определяется по GitHub Releases, а не по имени этой папки.\n"
    if relative.startswith("docs/uz/"):
        return f"# Material ko‘chirildi\n\nBu manzil eski linklar uchun saqlangan.\n\n[Joriy materialni ochish]({link})\n\nNashr versiyasi bu katalog nomi bilan emas, GitHub Releases orqali belgilanadi.\n"
    return f"# 教材の移行先\n\nこの場所は、配布済みリンクを維持するための互換用入口です。\n\n[現行の資料を開く]({link})\n\n現行教材の正本は版番号を含まない場所にあります。配布版はGitHub Releasesで確認してください。\n"


def sync(check: bool = False) -> int:
    manifest = json.loads((ROOT / "compatibility-manifest.json").read_text(encoding="utf-8"))
    legacy = ROOT / manifest["legacy_directory"]
    assert legacy.resolve().parent == ROOT.resolve()
    failures = []
    for relative in manifest["files"]:
        source, target = ROOT / relative, legacy / relative
        assert source.resolve().is_relative_to(ROOT.resolve())
        assert not source.resolve().is_relative_to(legacy.resolve())
        assert target.resolve().is_relative_to(legacy.resolve())
        if not source.is_file():
            failures.append(f"missing current file: {relative}")
            continue
        expected = entry_text(relative, source, target).encode("utf-8") if source.suffix == ".md" else source.read_bytes()
        if check:
            if not target.is_file() or target.read_bytes() != expected:
                failures.append(f"stale compatibility file: {relative}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.suffix == ".md":
                target.write_bytes(expected)
            else:
                shutil.copyfile(source, target)
    if failures:
        raise RuntimeError("\n".join(failures))
    return len(manifest["files"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    options = parser.parse_args()
    count = sync(options.check)
    print(f"PASS {count} legacy material URLs" if options.check else f"Synced {count} legacy material URLs")
