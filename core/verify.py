import json
import shutil
from pathlib import Path

from core.ui import TerminalUI


REQUIRED_DIRECTORIES = [
    "core", "methods", "presets", "tests",
    "builds", "payloads", "dist", "docs",
]

COMPILERS = [
    "x86_64-w64-mingw32-gcc",
    "x86_64-w64-mingw32-g++",
    "i686-w64-mingw32-gcc",
    "i686-w64-mingw32-g++",
]


def _parse_json_tree(root, directory):
    errors = []
    count = 0
    for path in sorted(directory.rglob("*.json")):
        count += 1
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
    return count, errors


def run_verification(root, strict=False, ui=None):
    root = Path(root).resolve()
    ui = ui if ui is not None else TerminalUI()
    failures = []

    print(ui.heading("Verify"))
    ui.rule(48)

    version_path = root / "VERSION"
    if version_path.is_file():
        version = version_path.read_text(encoding="utf-8").strip()
        print(ui.success("[+]") + f" Version       : {version}")
    else:
        failures.append("VERSION file is missing")
        print(ui.error("[!]") + " Version       : missing")

    for name in REQUIRED_DIRECTORIES:
        path = root / name
        if path.is_dir():
            print(ui.success("[+]") + f" Directory     : {name}/")
        else:
            failures.append(f"Required directory missing: {name}/")
            print(ui.error("[!]") + f" Directory     : {name}/ missing")

    methods_dir = root / "methods"
    presets_dir = root / "presets"
    method_dirs = [
        path for path in methods_dir.iterdir()
        if path.is_dir() and (path / "method.json").is_file()
    ]
    preset_count = len(list(presets_dir.glob("*.json")))

    print(ui.success("[+]") + f" Methods       : {len(method_dirs)}")
    print(ui.success("[+]") + f" Presets       : {preset_count}")

    method_json_count, method_errors = _parse_json_tree(root, methods_dir)
    preset_json_count, preset_errors = _parse_json_tree(root, presets_dir)

    if method_errors:
        failures.extend(method_errors)
    else:
        print(ui.success("[+]") + f" Method JSON   : {method_json_count} parsed")

    if preset_errors:
        failures.extend(preset_errors)
    else:
        print(ui.success("[+]") + f" Preset JSON   : {preset_json_count} parsed")

    missing_compilers = []
    for compiler in COMPILERS:
        if shutil.which(compiler):
            print(ui.success("[+]") + f" Compiler      : {compiler}")
        else:
            missing_compilers.append(compiler)
            print(ui.warning("[-]") + f" Compiler      : {compiler} missing")

    if strict and missing_compilers:
        failures.append("Missing compiler(s): " + ", ".join(missing_compilers))

    ui.rule(48)

    if failures:
        print(ui.error(f"[!] Verify found {len(failures)} issue(s)"))
        for failure in failures:
            print("    - " + failure)
        return 1

    print(ui.success("[+] Environment looks ready"))
    return 0
