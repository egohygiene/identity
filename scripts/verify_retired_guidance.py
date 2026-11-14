#!/usr/bin/env python3
"""Keep completed one-time guidance writers out of the active workflow set."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

RETIRED = {"refine-guidance-docs", "refine-guidance-docs-v2"}
HISTORICAL_BRANCH = "feat/13-brand-guidance-v1"


def verify(root: Path) -> list[str]:
    errors = []
    for path in sorted((root / ".github/workflows").glob("*")):
        if path.suffix not in {".yml", ".yaml"} or not path.is_file():
            continue
        if path.stem in RETIRED or HISTORICAL_BRANCH in path.read_text(encoding="utf-8"):
            errors.append(f"Retired guidance automation is active: {path.name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    args = parser.parse_args()
    errors = verify(args.repository_root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Retired guidance workflows remain inactive")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
