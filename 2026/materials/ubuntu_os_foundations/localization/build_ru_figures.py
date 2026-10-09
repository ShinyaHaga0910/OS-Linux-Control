"""Generate Russian-labelled SVG and PNG figures using the shared builder."""

from pathlib import Path
import build_uz_figures as diagrams


ROOT = Path(__file__).resolve().parents[1]
diagrams.OUT = ROOT / "assets" / "figures" / "ru"
diagrams.LABELS_PATH = ROOT / "localization" / "figure_labels_ru.tsv"
diagrams.LABEL_COLUMN = "ru"


if __name__ == "__main__":
    diagrams.main()
