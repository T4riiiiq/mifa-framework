#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "mifa"
TARGET_DIR = Path.home() / ".local" / "bin"
TARGET = TARGET_DIR / "mifa"


def main():
    parser = argparse.ArgumentParser(
        description="Install the Mifa command into ~/.local/bin using a symbolic link."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing ~/.local/bin/mifa entry.",
    )
    args = parser.parse_args()

    if not SOURCE.is_file():
        print(f"[!] Mifa launcher not found: {SOURCE}")
        return 1

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    if TARGET.exists() or TARGET.is_symlink():
        if not args.force:
            print(f"[!] Target already exists: {TARGET}")
            print("    Re-run with --force to replace it.")
            return 1
        TARGET.unlink()

    TARGET.symlink_to(SOURCE)
    print(f"[+] Installed: {TARGET}")

    path_entries = os.environ.get("PATH", "").split(os.pathsep)
    if str(TARGET_DIR) not in path_entries:
        print("[i] ~/.local/bin is not currently in PATH.")
        print("[i] Add this to your shell profile:")
        print('    export PATH="$HOME/.local/bin:$PATH"')
    else:
        print("[+] Run Mifa with: mifa")

    return 0


if __name__ == "__main__":
    sys.exit(main())
