#!/usr/bin/env python3

import argparse
from pathlib import Path

from core.catalog import MethodCatalog
from core.presets import PresetStore


ROOT = Path(__file__).resolve().parent
METHODS_DIR = ROOT / "methods"
PRESETS_DIR = ROOT / "presets"


def show_banner():
    print()
    print("Mifa")
    print("Modular Build System")
    print("-" * 24)


def list_methods(catalog):
    methods = catalog.discover()

    if not methods:
        print("[i] No methods installed.")
        return

    print(f"{'ID':<20} {'NAME':<30} {'LANGUAGE':<12}")
    print("-" * 64)

    for method in methods:
        print(
            f"{method.get('id', 'unknown'):<20} "
            f"{method.get('name', 'Unnamed'):<30} "
            f"{method.get('language', '-'):<12}"
        )


def show_method(catalog, method_id):
    method = catalog.get(method_id)

    if method is None:
        print(f"[!] Method not found: {method_id}")
        return

    print(f"ID           : {method.get('id', '-')}")
    print(f"Name         : {method.get('name', '-')}")
    print(f"Language     : {method.get('language', '-')}")
    print(f"Architectures: {', '.join(method.get('architectures', []))}")
    print(f"Description  : {method.get('description', '-')}")


def list_presets(store):
    presets = store.discover()

    if not presets:
        print("[i] No presets installed.")
        return

    print(f"{'ID':<20} {'METHOD':<20} {'ARCH':<10} {'BUILD':<10}")
    print("-" * 64)

    for preset in presets:
        print(
            f"{preset.get('id', 'unknown'):<20} "
            f"{preset.get('method', '-'):<20} "
            f"{preset.get('architecture', '-'):<10} "
            f"{preset.get('build_type', '-'):<10}"
        )


def validate_preset(catalog, store, preset_id):
    preset = store.get(preset_id)

    if preset is None:
        print(f"[!] Preset not found: {preset_id}")
        return False

    method_id = preset.get("method")
    method = catalog.get(method_id)

    if method is None:
        print(f"[!] Method referenced by preset does not exist: {method_id}")
        return False

    architecture = preset.get("architecture")
    supported = method.get("architectures", [])

    if architecture not in supported:
        print(
            f"[!] Architecture '{architecture}' is not supported "
            f"by method '{method_id}'"
        )
        return False

    print("[+] Preset validation passed")
    print(f"    Preset       : {preset_id}")
    print(f"    Method       : {method_id}")
    print(f"    Architecture : {architecture}")
    print(f"    Build type   : {preset.get('build_type', '-')}")
    return True


def build_parser():
    parser = argparse.ArgumentParser(
        prog="mifa",
        description="Mifa modular build system"
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "methods",
        help="List installed methods"
    )

    info_parser = subparsers.add_parser(
        "info",
        help="Show information about a method"
    )

    info_parser.add_argument(
        "method",
        help="Method ID"
    )

    subparsers.add_parser(
        "presets",
        help="List installed presets"
    )

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate a preset"
    )

    validate_parser.add_argument(
        "preset",
        help="Preset ID"
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    catalog = MethodCatalog(METHODS_DIR)
    presets = PresetStore(PRESETS_DIR)

    show_banner()

    if args.command == "methods":
        list_methods(catalog)

    elif args.command == "info":
        show_method(catalog, args.method)

    elif args.command == "presets":
        list_presets(presets)

    elif args.command == "validate":
        validate_preset(catalog, presets, args.preset)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
