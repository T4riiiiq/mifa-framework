#!/usr/bin/env python3

import argparse
from pathlib import Path

from core.catalog import MethodCatalog
from core.presets import PresetStore
from core.builds import BuildManager
from core.generator import SourceGenerator
from core.compiler import Compiler
from core.payloads import PayloadManager
from core.compatibility import CompatibilityChecker
from core.schema import MethodSchemaValidator
from core.parameters import ParameterResolver


ROOT = Path(__file__).resolve().parent

METHODS_DIR = (
    ROOT / "methods"
)

PRESETS_DIR = (
    ROOT / "presets"
)

BUILDS_DIR = (
    ROOT / "builds"
)


def show_banner():
    print()
    print("Mifa")
    print("Modular Build System")
    print("-" * 24)


def list_methods(
    catalog
):
    methods = catalog.discover()

    if not methods:
        print(
            "[i] No methods installed."
        )
        return

    print(
        f"{'ID':<28} "
        f"{'NAME':<34} "
        f"{'LANGUAGE':<12}"
    )

    print("-" * 78)

    for method in methods:
        print(
            f"{method.get('id', 'unknown'):<28} "
            f"{method.get('name', 'Unnamed'):<34} "
            f"{method.get('language', '-'):<12}"
        )


def show_method(
    catalog,
    method_id
):
    method = catalog.get(
        method_id
    )

    if method is None:
        print(
            f"[!] Method not found: "
            f"{method_id}"
        )
        return

    print(
        f"ID              : "
        f"{method.get('id', '-')}"
    )

    print(
        f"Name            : "
        f"{method.get('name', '-')}"
    )

    print(
        f"Language        : "
        f"{method.get('language', '-')}"
    )

    print(
        "Architectures   : "
        + ", ".join(
            method.get(
                "architectures",
                []
            )
        )
    )

    print(
        f"Requires payload: "
        f"{method.get('requires_payload', False)}"
    )

    payload_types = method.get(
        "payload_types",
        []
    )

    print(
        "Payload types   : "
        + (
            ", ".join(
                payload_types
            )
            if payload_types
            else "-"
        )
    )

    payload_contract = method.get(
        "payload_contract"
    )

    if payload_contract is not None:
        transforms = payload_contract.get(
            "transforms",
            [
                "copy"
            ]
        )

        print(
            "Payload xforms : "
            + ", ".join(
                transforms
            )
        )

        print(
            f"Payload default: "
            f"{payload_contract.get('default_transform', 'copy')}"
        )

        print(
            f"Payload limits : "
            f"{payload_contract.get('min_size_bytes', 1)}"
            f".."
            f"{payload_contract.get('max_size_bytes', '-')}"
            f" bytes"
        )

    build_types = method.get(
        "build_types",
        [
            "release",
            "debug"
        ]
    )

    print(
        "Build types     : "
        + ", ".join(
            build_types
        )
    )

    sources = method.get(
        "sources",
        []
    )

    print(
        f"Source files    : "
        f"{len(sources)}"
    )

    for source in sources:
        marker = (
            "compile"
            if source.get(
                "compile"
            )
            else "asset"
        )

        print(
            f"                  "
            f"{source.get('output', '-')} "
            f"({marker})"
        )

    parameters = method.get(
        "parameters",
        {}
    )

    print(
        f"Parameters      : "
        f"{len(parameters)}"
    )

    for name, spec in parameters.items():
        required = (
            "required"
            if spec.get(
                "required",
                False
            )
            else "optional"
        )

        parameter_type = spec.get(
            "type",
            "str"
        )

        default = (
            spec.get(
                "default",
                "<none>"
            )
        )

        print(
            f"                  "
            f"{name} "
            f"({parameter_type}, "
            f"{required}, "
            f"default={default})"
        )

    runtime_arguments = method.get(
        "runtime_arguments",
        []
    )

    print(
        f"Runtime args    : "
        f"{len(runtime_arguments)}"
    )

    for argument in runtime_arguments:
        required = (
            "required"
            if argument.get(
                "required",
                True
            )
            else "optional"
        )

        print(
            f"                  "
            f"{argument.get('name', '-')} "
            f"({argument.get('type', 'str')}, "
            f"{required})"
        )

    print(
        f"Output name     : "
        f"{method.get('output_name', 'output.exe')}"
    )

    print(
        f"Description     : "
        f"{method.get('description', '-')}"
    )


def list_presets(
    store
):
    presets = store.discover()

    if not presets:
        print(
            "[i] No presets installed."
        )
        return

    print(
        f"{'ID':<32} "
        f"{'METHOD':<28} "
        f"{'ARCH':<10} "
        f"{'BUILD':<10}"
    )

    print("-" * 84)

    for preset in presets:
        print(
            f"{preset.get('id', 'unknown'):<32} "
            f"{preset.get('method', '-'):<28} "
            f"{preset.get('architecture', '-'):<10} "
            f"{preset.get('build_type', '-'):<10}"
        )


def check_methods(
    catalog,
    schema
):
    methods = catalog.discover()

    if not methods:
        print(
            "[i] No methods installed."
        )
        return False

    valid = 0
    invalid = 0

    for method in methods:
        method_id = method.get(
            "id",
            "unknown"
        )

        errors = schema.validate(
            method
        )

        print()

        if errors:
            invalid += 1

            print(
                f"[!] {method_id}"
            )

            for error in errors:
                print(
                    f"    - {error}"
                )

        else:
            valid += 1

            print(
                f"[+] {method_id}"
            )

            print(
                "    Contract valid"
            )

    print()
    print("-" * 24)

    total = (
        valid + invalid
    )

    print(
        f"{total} methods checked"
    )

    print(
        f"{valid} valid"
    )

    print(
        f"{invalid} invalid"
    )

    return (
        invalid == 0
    )


def get_method_and_preset(
    catalog,
    store,
    schema,
    preset_id
):
    preset = store.get(
        preset_id
    )

    if preset is None:
        raise ValueError(
            f"Preset not found: "
            f"{preset_id}"
        )

    method_id = preset.get(
        "method"
    )

    method = catalog.get(
        method_id
    )

    if method is None:
        raise ValueError(
            f"Method referenced by preset "
            f"does not exist: "
            f"{method_id}"
        )

    schema_errors = (
        schema.validate(
            method
        )
    )

    if schema_errors:
        message = "; ".join(
            schema_errors
        )

        raise ValueError(
            f"Invalid method contract "
            f"'{method_id}': "
            f"{message}"
        )

    method_path = Path(
        method["_path"]
    )

    for source in method.get(
        "sources",
        []
    ):
        template_path = (
            method_path
            / source["template"]
        )

        if not template_path.exists():
            raise FileNotFoundError(
                f"Method template does "
                f"not exist: "
                f"{template_path}"
            )

    return (
        method,
        preset
    )


def run_compatibility_check(
    checker,
    method,
    preset,
    payload_path=None,
    payload_type=None,
    payload_transform=None,
    parameter_errors=None
):
    errors = checker.validate(
        method=method,
        preset=preset,
        payload_path=payload_path,
        payload_type=payload_type,
        payload_transform=payload_transform,
        parameter_errors=parameter_errors
    )

    if errors:
        print(
            "[!] Compatibility validation failed"
        )

        for error in errors:
            print(
                f"    - {error}"
            )

        return False

    return True


def validate_preset(
    catalog,
    store,
    schema,
    compatibility,
    parameter_resolver,
    preset_id
):
    try:
        method, preset = (
            get_method_and_preset(
                catalog,
                store,
                schema,
                preset_id
            )
        )

    except Exception as exc:
        print(
            f"[!] {exc}"
        )
        return False

    resolved_parameters, parameter_errors = (
        parameter_resolver.resolve(
            method=method,
            preset=preset,
            cli_items=[]
        )
    )

    errors = compatibility.validate_preset(
        method=method,
        preset=preset,
        parameter_errors=parameter_errors
    )

    if errors:
        print(
            "[!] Preset validation failed"
        )

        for error in errors:
            print(
                f"    - {error}"
            )

        return False

    print(
        "[+] Preset validation passed"
    )

    print(
        f"    Preset       : "
        f"{preset_id}"
    )

    print(
        f"    Method       : "
        f"{method.get('id')}"
    )

    print(
        f"    Architecture : "
        f"{preset.get('architecture')}"
    )

    print(
        f"    Build type   : "
        f"{preset.get('build_type', '-')}"
    )

    print(
        f"    Payload req. : "
        f"{method.get('requires_payload', False)}"
    )

    print(
        f"    Parameters   : "
        f"{len(resolved_parameters)}"
    )

    print(
        f"    Sources      : "
        f"{len(method.get('sources', []))}"
    )

    return True


def create_build(
    catalog,
    store,
    schema,
    manager,
    generator,
    compiler,
    payload_manager,
    compatibility,
    parameter_resolver,
    preset_id,
    payload_path=None,
    payload_type=None,
    payload_transform=None,
    parameter_items=None
):
    build_dir = None

    try:
        method, preset = (
            get_method_and_preset(
                catalog,
                store,
                schema,
                preset_id
            )
        )

        (
            resolved_parameters,
            parameter_errors
        ) = parameter_resolver.resolve(
            method=method,
            preset=preset,
            cli_items=parameter_items
        )

        compatible = (
            run_compatibility_check(
                checker=compatibility,
                method=method,
                preset=preset,
                payload_path=payload_path,
                payload_type=payload_type,
                payload_transform=payload_transform,
                parameter_errors=parameter_errors
            )
        )

        if not compatible:
            return

        print(
            "[+] Method contract valid"
        )

        print(
            "[+] Compatibility validation passed"
        )

        if resolved_parameters:
            print(
                f"[+] Parameters resolved: "
                f"{len(resolved_parameters)}"
            )

            for name, value in (
                resolved_parameters.items()
            ):
                print(
                    f"    - {name}={value}"
                )

        build_id, build_dir = (
            manager.create(
                method=method,
                preset=preset,
                parameters=resolved_parameters
            )
        )

        print(
            f"[+] Build workspace created: "
            f"{build_id}"
        )

        payload_info = None

        if payload_path is not None:
            payload_info = (
                payload_manager.prepare(
                    payload_path=Path(
                        payload_path
                    ),
                    build_dir=build_dir,
                    method=method,
                    payload_type=payload_type,
                    transform=payload_transform
                )
            )

            manager.attach_payload(
                build_dir=build_dir,
                payload_info=payload_info,
                payload_type=payload_type
            )

            print(
                f"[+] Payload staged: "
                f"{payload_info['name']}"
            )

            print(
                f"[+] Payload type: "
                f"{payload_type}"
            )

            print(
                f"[+] Payload transform: "
                f"{payload_info['transform']}"
            )

            print(
                f"[+] Source SHA256: "
                f"{payload_info['source']['sha256']}"
            )

            print(
                f"[+] Staged SHA256: "
                f"{payload_info['staged']['sha256']}"
            )

        generated_files = (
            generator.generate(
                method=method,
                preset=preset,
                build_id=build_id,
                build_dir=build_dir,
                payload_info=payload_info,
                payload_type=payload_type,
                parameters=resolved_parameters
            )
        )

        print(
            f"[+] Sources generated: "
            f"{len(generated_files)}"
        )

        for item in generated_files:
            print(
                f"    - "
                f"{item['path'].name} "
                f"("
                f"{'compile' if item['compile'] else 'asset'}"
                f")"
            )

        result = compiler.compile(
            method=method,
            preset=preset,
            generated_files=generated_files,
            build_dir=build_dir
        )

        manifest = (
            manager.mark_success(
                build_dir=build_dir,
                generated_files=generated_files,
                compile_result=result
            )
        )

        output_path = (
            result["output"]
        )

        print(
            "[+] Compilation successful"
        )

        print(
            "[+] Build manifest finalized"
        )

        print()

        print(
            f"    Build        : "
            f"{build_id}"
        )

        print(
            f"    Status       : "
            f"{manifest['status']}"
        )

        print(
            f"    Method       : "
            f"{method.get('id')}"
        )

        print(
            f"    Architecture : "
            f"{preset.get('architecture')}"
        )

        print(
            f"    Build type   : "
            f"{preset.get('build_type', '-')}"
        )

        if resolved_parameters:
            print(
                f"    Parameters   : "
                f"{len(resolved_parameters)}"
            )

        if payload_info is not None:
            print(
                f"    Payload      : "
                f"{payload_info['name']}"
            )

            print(
                f"    Payload type : "
                f"{payload_type}"
            )

            print(
                f"    Transform    : "
                f"{payload_info['transform']}"
            )

            print(
                f"    Source size  : "
                f"{payload_info['source']['size_bytes']} bytes"
            )

            print(
                f"    Staged size  : "
                f"{payload_info['staged']['size_bytes']} bytes"
            )

        print(
            f"    Compiler     : "
            f"{result['compiler']}"
        )

        print(
            f"    Sources      : "
            f"{len(generated_files)}"
        )

        print(
            f"    Output       : "
            f"{output_path}"
        )

        print(
            f"    SHA256       : "
            f"{manifest['output']['sha256']}"
        )

        print(
            f"    Size         : "
            f"{manifest['output']['size_bytes']} bytes"
        )

        print(
            f"    Location     : "
            f"{build_dir}"
        )

    except Exception as exc:
        if build_dir is not None:
            try:
                manager.mark_failed(
                    build_dir,
                    exc
                )

            except Exception:
                pass

        print(
            f"[!] Build failed: "
            f"{exc}"
        )


def build_parser():
    parser = argparse.ArgumentParser(
        prog="mifa",
        description=(
            "Mifa modular build system"
        )
    )

    subparsers = (
        parser.add_subparsers(
            dest="command"
        )
    )

    subparsers.add_parser(
        "methods",
        help="List installed methods"
    )

    subparsers.add_parser(
        "check",
        help="Validate all method contracts"
    )

    info_parser = (
        subparsers.add_parser(
            "info",
            help=(
                "Show information "
                "about a method"
            )
        )
    )

    info_parser.add_argument(
        "method",
        help="Method ID"
    )

    subparsers.add_parser(
        "presets",
        help="List installed presets"
    )

    validate_parser = (
        subparsers.add_parser(
            "validate",
            help="Validate a preset"
        )
    )

    validate_parser.add_argument(
        "preset",
        help="Preset ID"
    )

    build_command = (
        subparsers.add_parser(
            "build",
            help=(
                "Generate and compile "
                "a new build"
            )
        )
    )

    build_command.add_argument(
        "--preset",
        required=True,
        help="Preset ID"
    )

    build_command.add_argument(
        "--payload",
        required=False,
        help="Path to payload/input file"
    )

    build_command.add_argument(
        "--payload-type",
        required=False,
        help="Payload type"
    )

    build_command.add_argument(
        "--payload-transform",
        required=False,
        choices=[
            "copy",
            "base64",
            "hex"
        ],
        help=(
            "Payload staging transform. "
            "Method contract controls which "
            "transforms are accepted."
        )
    )

    build_command.add_argument(
        "--set",
        dest="parameters",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help=(
            "Override a declared method "
            "parameter. May be repeated."
        )
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

    generator = (
        SourceGenerator()
    )

    compiler = Compiler()

    payload_manager = (
        PayloadManager()
    )

    compatibility = (
        CompatibilityChecker()
    )

    schema = (
        MethodSchemaValidator()
    )

    parameter_resolver = (
        ParameterResolver()
    )

    show_banner()

    if args.command == "methods":
        list_methods(
            catalog
        )

    elif args.command == "check":
        check_methods(
            catalog,
            schema
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
            schema,
            compatibility,
            parameter_resolver,
            args.preset
        )

    elif args.command == "build":
        create_build(
            catalog=catalog,
            store=presets,
            schema=schema,
            manager=builds,
            generator=generator,
            compiler=compiler,
            payload_manager=payload_manager,
            compatibility=compatibility,
            parameter_resolver=parameter_resolver,
            preset_id=args.preset,
            payload_path=args.payload,
            payload_type=args.payload_type,
            payload_transform=args.payload_transform,
            parameter_items=args.parameters
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
