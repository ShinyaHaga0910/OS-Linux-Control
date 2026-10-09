"""Build four A4 Uzbek PDFs without modifying the Japanese outputs."""

from pathlib import Path
import build_materials as materials


ROOT = Path(__file__).resolve().parents[1]
UZ = ROOT / "docs" / "uz"
materials.TEXTBOOK = UZ / "textbook"
OUTPUT = ROOT / "output" / "pdf"
META = "Ubuntu Server 24.04 LTS<br/>JDU Cyber Security / 2026 / ChatGPT tarjima qoralamasi"


def main() -> None:
    sets = [
        ("Operatsion tizim va Linux asosiy amallari", "", sorted(materials.TEXTBOOK.glob("*.md")), "ubuntu_os_textbook_uz", True),
        ("Ubuntu va OS asoslari: to‘liq mashqlar", "P0–P6: topshiriqlar va qadamma-qadam yechim", [UZ / "practice.md"], "ubuntu_os_guided_practice_uz", False),
        ("Ubuntu va OS asoslari: mustaqil topshiriqlar", "M1–M7 Mission Guide", [UZ / "missions.md"], "ubuntu_os_missions_uz", False),
        ("Ubuntu va OS asoslari: ma’lumotnoma", "Atamalar va commandlar jadvali", [UZ / "reference.md"], "ubuntu_os_reference_uz", False),
    ]
    for title, subtitle, sources, stem, chapters in sets:
        if not all(source.is_file() for source in sources):
            raise FileNotFoundError(f"Missing source for {stem}")
        output = OUTPUT / f"{stem}.pdf"
        materials.build_pdf(title, subtitle, sources, output, chapters=chapters, meta=META)
        print(f"built {output.name}")


if __name__ == "__main__":
    main()
