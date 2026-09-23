#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.ui import TerminalUI
from core.verify import run_verification


def main():
    parser = argparse.ArgumentParser(
        description="Verify the local Mifa development and build environment."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any configured MinGW-w64 compiler is missing.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colors.",
    )
    args = parser.parse_args()

    return run_verification(
        root=ROOT,
        strict=args.strict,
        ui=TerminalUI(enabled=False if args.no_color else None),
    )


if __name__ == "__main__":
    sys.exit(main())
