#!/usr/bin/env python3

import argparse
from pathlib import Path

from core.catalog import MethodCatalog
from core.presets import PresetStore
from core.builds import BuildManager
from core.generator import SourceGenerator
from core.compiler import Compiler


ROOT = Path(__file__).resolve().parent

METHODS_DIR = ROOT / "methods"
PRESETS_DIR = ROOT / "presets"
BUILDS_DIR = ROOT / "builds"


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

    print(
        f"{'ID':<20} "
        f"{'NAME':<30} "
        f"{'LANGUAGE':<12}"
    )
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
    print(
        "Architectures: "
        + ", ".join(
            method.get(
                "architectures",
                []
            )
        )
    )
    print(f"Template     : {method.get('template', '-')}")
    print(f"Source name  : {method.get('source_name', '-')}")
    print(f"Output name  : {method.get('output_name', 'output.exe')}")
    print(f"Description  : {method.get('description', '-')}")


def list_presets(store):
    presets = store.discover()

    if not presets:
        print("[i] No presets installed.")
        return

    print(
        f"{'ID':<20} "
        f"{'METHOD':<20} "
        f"{'ARCH':<10} "
        f"{'BUILD':<10}"
    )
    print("-" * 64)

    for preset in presets:
        print(
            f"{preset.get('id', 'unknown'):<20} "
            f"{preset.get('method', '-'):<20} "
            f"{preset.get('architecture', '-'):<10} "
            f"{preset.get('build_type', '-'):<10}"
        )


def get_validated_method_and_preset(
    catalog,
    store,
    preset_id
):
    preset = store.get(preset_id)

    if preset is None:
        raise ValueError(
            f"Preset not found: {preset_id}"
        )

    method_id = preset.get("method")
    method = catalog.get(method_id)

    if method is None:
        raise ValueError(
            f"Method referenced by preset "
            f"does not exist: {method_id}"
        )

    architecture = preset.get(
        "architecture"
    )

    supported = method.get(
        "architectures",
        []
    )

    if architecture not in supported:
        raise ValueError(
            f"Architecture '{architecture}' "
            f"is not supported by "
            f"method '{method_id}'"
        )

    template = method.get("template")

    if not template:
        raise ValueError(
            f"Method '{method_id}' "
            "does not define a template"
        )

    template_path = (
        Path(method["_path"]) / template
    )

    if not template_path.exists():
        raise FileNotFoundError(
            f"Method template does not exist: "
            f"{template_path}"
        )

    return method, preset


def validate_preset(
    catalog,
    store,
    preset_id
):
    try:
        method, preset = (
            get_validated_method_and_preset(
                catalog,
                store,
                preset_id
            )
        )

    except Exception as exc:
        print(f"[!] {exc}")
        return False

    print("[+] Preset validation passed")
    print(f"    Preset       : {preset_id}")
    print(f"    Method       : {method.get('id')}")
    print(
        f"    Architecture : "
        f"{preset.get('architecture')}"
    )
    print(
        f"    Build type   : "
        f"{preset.get('build_type', '-')}"
    )

    return True


def create_build(
    catalog,
    store,
    manager,
    generator,
    compiler,
    preset_id
):
    try:
        method, preset = (
            get_validated_method_and_preset(
                catalog,
                store,
                preset_id
            )
        )

        print("[+] Configuration validated")

        build_id, build_dir = manager.create(
            method=method,
            preset=preset
        )

        print(
            f"[+] Build workspace created: "
            f"{build_id}"
        )

        source_path = generator.generate(
            method=method,
            preset=preset,
            build_id=build_id,
            build_dir=build_dir
        )

        print(
            f"[+] Source generated: "
            f"{source_path.name}"
        )

        result = compiler.compile(
            method=method,
            preset=preset,
            source_path=source_path,
            build_dir=build_dir
        )

        output_path = result["output"]

        print("[+] Compilation successful")
        print()
        print(f"    Build        : {build_id}")
        print(f"    Method       : {method.get('id')}")
        print(
            f"    Architecture : "
            f"{preset.get('architecture')}"
        )
        print(
            f"    Build type   : "
            f"{preset.get('build_type', '-')}"
        )
        print(
            f"    Compiler     : "
            f"{result['compiler']}"
        )
        print(f"    Source       : {source_path}")
        print(f"    Output       : {output_path}")
        print(f"    Location     : {build_dir}")

    except Exception as exc:
        print(
            f"[!] Build failed: {exc}"
        )


def build_parser():
    parser = argparse.ArgumentParser(
        prog="mifa",
        description="Mifa modular build system"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

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

    build_command = subparsers.add_parser(
        "build",
        help="Generate and compile a new build"
    )

    build_command.add_argument(
        "--preset",
        required=True,
        help="Preset ID"
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    catalog = MethodCatalog(
        METHODS_DIR
    )

    presets = PresetStore(
        PRESETS_DIR
    )

    builds = BuildManager(
        BUILDS_DIR
    )

    generator = SourceGenerator()

    compiler = Compiler()

    show_banner()

    if args.command == "methods":
        list_methods(
            catalog
        )

    elif args.command == "info":
        show_method(
            catalog,
            args.method
        )

    elif args.command == "presets":
        list_presets(
            presets
        )

    elif args.command == "validate":
        validate_preset(
            catalog,
            presets,
            args.preset
        )

    elif args.command == "build":
        create_build(
            catalog,
            presets,
            builds,
            generator,
            compiler,
            args.preset
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
