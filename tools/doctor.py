#!/usr/bin/env python3

import argparse
import json
import shutil
import sys
from pathlib import Path


ROOT = Path(
    __file__
).resolve().parents[1]

REQUIRED_DIRECTORIES = [
    "core",
    "methods",
    "presets",
    "tests",
    "builds",
    "payloads",
    "dist",
    "docs",
]

COMPILERS = [
    "x86_64-w64-mingw32-gcc",
    "x86_64-w64-mingw32-g++",
    "i686-w64-mingw32-gcc",
    "i686-w64-mingw32-g++",
]


def count_json_files(
    directory
):
    return len(
        list(
            directory.glob(
                "*.json"
            )
        )
    )


def parse_json_tree(
    directory
):
    errors = []
    count = 0

    for path in sorted(
        directory.rglob(
            "*.json"
        )
    ):
        count += 1

        try:
            json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

        except Exception as exc:
            errors.append(
                f"{path.relative_to(ROOT)}: "
                f"{exc}"
            )

    return (
        count,
        errors
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Check the local Mifa development "
            "and build environment."
        )
    )

    parser.add_argument(
        "--require-compilers",
        action="store_true",
        help=(
            "Exit non-zero if any configured "
            "MinGW-w64 compiler is missing."
        )
    )

    args = parser.parse_args()

    failures = []

    print(
        "Mifa Doctor"
    )
    print(
        "-" * 40
    )

    version_path = (
        ROOT / "VERSION"
    )

    if version_path.is_file():
        version = (
            version_path
            .read_text(
                encoding="utf-8"
            )
            .strip()
        )

        print(
            f"[+] Version       : "
            f"{version}"
        )

    else:
        failures.append(
            "VERSION file is missing"
        )

        print(
            "[!] Version       : missing"
        )

    for name in REQUIRED_DIRECTORIES:
        path = (
            ROOT / name
        )

        if path.is_dir():
            print(
                f"[+] Directory     : "
                f"{name}/"
            )

        else:
            failures.append(
                f"Required directory missing: "
                f"{name}/"
            )

            print(
                f"[!] Directory     : "
                f"{name}/ missing"
            )

    method_dirs = [
        path
        for path in (
            ROOT / "methods"
        ).iterdir()
        if (
            path.is_dir()
            and (
                path / "method.json"
            ).is_file()
        )
    ]

    preset_count = count_json_files(
        ROOT / "presets"
    )

    print(
        f"[+] Methods       : "
        f"{len(method_dirs)}"
    )

    print(
        f"[+] Presets       : "
        f"{preset_count}"
    )

    json_count, json_errors = (
        parse_json_tree(
            ROOT / "methods"
        )
    )

    preset_json_count, preset_errors = (
        parse_json_tree(
            ROOT / "presets"
        )
    )

    if not json_errors:
        print(
            f"[+] Method JSON   : "
            f"{json_count} parsed"
        )

    else:
        failures.extend(
            json_errors
        )

    if not preset_errors:
        print(
            f"[+] Preset JSON   : "
            f"{preset_json_count} parsed"
        )

    else:
        failures.extend(
            preset_errors
        )

    missing_compilers = []

    for compiler in COMPILERS:
        resolved = shutil.which(
            compiler
        )

        if resolved:
            print(
                f"[+] Compiler      : "
                f"{compiler}"
            )

        else:
            missing_compilers.append(
                compiler
            )

            print(
                f"[-] Compiler      : "
                f"{compiler} missing"
            )

    if (
        args.require_compilers
        and missing_compilers
    ):
        failures.append(
            "Missing compiler(s): "
            + ", ".join(
                missing_compilers
            )
        )

    print(
        "-" * 40
    )

    if failures:
        print(
            f"[!] Doctor found "
            f"{len(failures)} issue(s)"
        )

        for failure in failures:
            print(
                f"    - {failure}"
            )

        return 1

    print(
        "[+] Environment looks ready"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
