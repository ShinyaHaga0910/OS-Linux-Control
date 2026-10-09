"""Build four A4 Russian PDFs without changing Japanese or Uzbek outputs."""

from pathlib import Path
import build_materials as materials


ROOT = Path(__file__).resolve().parents[1]
RU = ROOT / "docs" / "ru"
materials.TEXTBOOK = RU / "textbook"
OUTPUT = ROOT / "output" / "pdf"
META = "Ubuntu Server 24.04 LTS<br/>JDU Cyber Security / 2026 / черновой перевод ChatGPT"


def main() -> None:
    sets = [
        ("Операционная система и основные команды Linux", "", sorted(materials.TEXTBOOK.glob("*.md")), "ubuntu_os_textbook_ru", True),
        ("Основы Ubuntu и ОС: пошаговые упражнения", "P0–P6: задания и решения", [RU / "practice.md"], "ubuntu_os_guided_practice_ru", False),
        ("Основы Ubuntu и ОС: самостоятельные задания", "M1–M7", [RU / "missions.md"], "ubuntu_os_missions_ru", False),
        ("Основы Ubuntu и ОС: справочник", "Термины и команды", [RU / "reference.md"], "ubuntu_os_reference_ru", False),
    ]
    for title, subtitle, sources, stem, chapters in sets:
        if not all(source.is_file() for source in sources):
            raise FileNotFoundError(f"Missing source for {stem}")
        output = OUTPUT / f"{stem}.pdf"
        materials.build_pdf(title, subtitle, sources, output, chapters=chapters, meta=META)
        print(f"built {output.name}")


if __name__ == "__main__":
    main()
