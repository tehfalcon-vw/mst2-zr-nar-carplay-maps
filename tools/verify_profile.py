#!/usr/bin/env python3
"""Verify an extracted unit filesystem against the locked P0367T profile."""

import argparse
import hashlib
import json
from pathlib import Path
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path, help="root of an extracted unit filesystem")
    parser.add_argument(
        "--profile",
        type=Path,
        default=Path(__file__).parents[1] / "profiles" / "MST2_US_VW_ZR_P0367T.json",
    )
    args = parser.parse_args()
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    failed = False
    for unit_path, expected in profile["files"].items():
        path = args.root / unit_path.lstrip("/")
        if not path.is_file():
            print(f"MISSING  {unit_path}")
            failed = True
            continue
        data = path.read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        good = len(data) == expected["size"] and actual == expected["sha256"]
        print(f"{'OK' if good else 'MISMATCH':8} {unit_path}")
        failed |= not good
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
