"""Check Russian drafts against the current Japanese source."""

import check_uz as checker


checker.LANG = "ru"
checker.TARGET_ROOT = checker.ROOT / "docs" / "ru"
checker.UZ = checker.TARGET_ROOT / "textbook"


if __name__ == "__main__":
    raise SystemExit(checker.main())
