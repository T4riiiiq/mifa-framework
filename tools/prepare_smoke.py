#!/usr/bin/env python3

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(
    __file__
).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT)
    )

from core.catalog import MethodCatalog
from core.compatibility import CompatibilityChecker
from core.compiler import Compiler
from core.generator import SourceGenerator
from core.parameters import ParameterResolver
from core.presets import PresetStore
from core.schema import MethodSchemaValidator


METHODS_DIR = (
    ROOT / "methods"
)

PRESETS_DIR = (
    ROOT / "presets"
)

SMOKE_METHODS = [
    "parameter-test",
    "win32-api-resolve",
    "win32-local-buffer",
    "win32-local-thread",
    "win32-dll-load-info",
    "win32-file-map",
    "win32-runtime-helper",
]


def sha256_file(
    path
):
    digest = hashlib.sha256()

    with Path(
        path
    ).open(
        "rb"
    ) as handle:
        while True:
            chunk = handle.read(
                1024 * 1024
            )

            if not chunk:
                break

            digest.update(
                chunk
            )

    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Build the curated Mifa v1.1 "
            "Windows smoke-test bundle."
        )
    )

    parser.add_argument(
        "--arch",
        choices=[
            "x64",
            "x86"
        ],
        default="x86"
    )

    args = parser.parse_args()

    catalog = MethodCatalog(
        METHODS_DIR
    )

    store = PresetStore(
        PRESETS_DIR
    )

    schema = (
        MethodSchemaValidator()
    )

    compatibility = (
        CompatibilityChecker()
    )

    resolver = (
        ParameterResolver()
    )

    generator = (
        SourceGenerator()
    )

    compiler = (
        Compiler()
    )

    output_dir = (
        ROOT
        / "dist"
        / (
            "v1.1-smoke-"
            + args.arch
        )
    )

    if output_dir.exists():
        shutil.rmtree(
            output_dir
        )

    output_dir.mkdir(
        parents=True
    )

    manifest = {
        "version":
            (
                ROOT / "VERSION"
            ).read_text(
                encoding="utf-8"
            ).strip(),

        "architecture":
            args.arch,

        "binaries":
            []
    }

    with tempfile.TemporaryDirectory(
        prefix="mifa-smoke-"
    ) as temporary:
        temporary_root = Path(
            temporary
        )

        for method_id in SMOKE_METHODS:
            preset_id = (
                f"{method_id}-"
                f"{args.arch}"
            )

            preset = store.get(
                preset_id
            )

            if preset is None:
                raise RuntimeError(
                    f"Preset not found: "
                    f"{preset_id}"
                )

            method = catalog.get(
                method_id
            )

            if method is None:
                raise RuntimeError(
                    f"Method not found: "
                    f"{method_id}"
                )

            schema_errors = schema.validate(
                method
            )

            if schema_errors:
                raise RuntimeError(
                    f"{method_id}: "
                    + "; ".join(
                        schema_errors
                    )
                )

            parameters, parameter_errors = (
                resolver.resolve(
                    method=method,
                    preset=preset,
                    cli_items=[]
                )
            )

            compatibility_errors = (
                compatibility.validate_preset(
                    method=method,
                    preset=preset,
                    parameter_errors=parameter_errors
                )
            )

            if compatibility_errors:
                raise RuntimeError(
                    f"{preset_id}: "
                    + "; ".join(
                        compatibility_errors
                    )
                )

            build_dir = (
                temporary_root
                / preset_id
            )

            generated = (
                generator.generate(
                    method=method,
                    preset=preset,
                    build_id=(
                        "SMOKE-"
                        + args.arch.upper()
                    ),
                    build_dir=build_dir,
                    parameters=parameters
                )
            )

            result = compiler.compile(
                method=method,
                preset=preset,
                generated_files=generated,
                build_dir=build_dir
            )

            source_output = Path(
                result[
                    "output"
                ]
            )

            destination = (
                output_dir
                / source_output.name
            )

            shutil.copy2(
                source_output,
                destination
            )

            manifest[
                "binaries"
            ].append({
                "method":
                    method_id,

                "preset":
                    preset_id,

                "file":
                    destination.name,

                "size_bytes":
                    destination.stat().st_size,

                "sha256":
                    sha256_file(
                        destination
                    )
            })

            print(
                f"[+] {preset_id} -> "
                f"{destination.name}"
            )

    manifest_path = (
        output_dir
        / "smoke_manifest.json"
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2
        )
        + "\n",
        encoding="utf-8"
    )

    print()
    print(
        f"[+] Smoke bundle ready: "
        f"{output_dir}"
    )

    print(
        f"[+] Binaries: "
        f"{len(manifest['binaries'])}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
