#!/usr/bin/env python3

import argparse
import base64
import binascii
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT),
    )

from core.catalog import MethodCatalog
from core.compatibility import CompatibilityChecker
from core.compiler import Compiler
from core.generator import SourceGenerator
from core.parameters import ParameterResolver
from core.payloads import PayloadManager
from core.presets import PresetStore
from core.schema import MethodSchemaValidator


METHODS_DIR = ROOT / "methods"
PRESETS_DIR = ROOT / "presets"

SMOKE_METHODS = [
    "parameter-test",
    "win32-api-resolve",
    "win32-local-buffer",
    "win32-local-thread",
    "win32-dll-load-info",
    "win32-file-map",
    "win32-runtime-helper",
    "win32-payload-inspect",
    "win32-file-buffer",
    "win32-base64-buffer",
    "win32-hex-buffer",
    "win32-pe-runtime-info",
    "win32-pe-section-characteristics",
    "win32-reflective-map-lab",
    "win32-managed-lab",
    "win32-jscript-lab",
    "win32-amsi-inspect",
    "win32-appcontrol-inspect",
    "win32-trusted-hosts",
    "win32-runner-helper",
    "kernel-security",
]


SMOKE_PAYLOAD = (
    b"Mifa v2.0 smoke payload fixture\n"
)

RUNTIME_TEXT = (
    b"Mifa v2.0 runtime smoke test"
)


def sha256_file(path):
    digest = hashlib.sha256()

    with Path(path).open(
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


def version_series():
    version = (
        ROOT / "VERSION"
    ).read_text(
        encoding="utf-8"
    ).strip()

    parts = version.split(".")

    if len(parts) >= 2:
        return (
            parts[0]
            + "."
            + parts[1]
        )

    return version


def build_payload_fixture(
    method,
    build_dir,
    fixture_path,
    payload_manager,
):
    contract = method.get(
        "payload_contract",
        {},
    )

    accepted_types = contract.get(
        "types",
        method.get(
            "payload_types",
            [],
        ),
    )

    if "text" not in accepted_types:
        raise RuntimeError(
            f"{method.get('id')}: curated smoke "
            "fixture requires text payload support"
        )

    transforms = contract.get(
        "transforms",
        ["copy"],
    )

    transform = contract.get(
        "default_transform",
        "copy",
    )

    if transform not in transforms:
        raise RuntimeError(
            f"{method.get('id')}: invalid default "
            "payload transform"
        )

    return payload_manager.prepare(
        payload_path=fixture_path,
        build_dir=build_dir,
        method=method,
        payload_type="text",
        transform=transform,
    )


def write_runtime_assets(
    output_dir,
):
    text_path = (
        output_dir
        / "smoke-test.txt"
    )

    b64_path = (
        output_dir
        / "smoke-test.b64"
    )

    hex_path = (
        output_dir
        / "smoke-test.hex"
    )

    js_path = (
        output_dir
        / "smoke-test.js"
    )

    text_path.write_bytes(
        RUNTIME_TEXT
    )

    b64_path.write_bytes(
        base64.b64encode(
            RUNTIME_TEXT
        )
    )

    hex_path.write_bytes(
        binascii.hexlify(
            RUNTIME_TEXT
        )
    )

    js_path.write_text(
        'var mifaSmoke = "v2";\n',
        encoding="utf-8",
    )

    return [
        text_path,
        b64_path,
        hex_path,
        js_path,
    ]


def powershell_runner():
    return r'''$ErrorActionPreference = "Continue"

$log = Join-Path $PSScriptRoot "runtime-results.txt"
Remove-Item $log -ErrorAction SilentlyContinue

Set-Location $PSScriptRoot

$tests = @(
    @{
        Name = "parameter-test"
        Command = { .\\parameter-test.exe smoke-test }
    },
    @{
        Name = "win32-api-resolve"
        Command = { .\\win32-api-resolve.exe kernel32.dll GetCurrentProcessId }
    },
    @{
        Name = "win32-local-buffer"
        Command = { .\\win32-local-buffer.exe }
    },
    @{
        Name = "win32-local-thread"
        Command = { .\\win32-local-thread.exe }
    },
    @{
        Name = "win32-dll-load-info"
        Command = { .\\win32-dll-load-info.exe C:\\Windows\\System32\\version.dll }
    },
    @{
        Name = "win32-file-map"
        Command = { .\\win32-file-map.exe C:\\Windows\\System32\\notepad.exe }
    },
    @{
        Name = "win32-runtime-helper"
        Command = { .\\win32-runtime-helper.exe smoke-test }
    },
    @{
        Name = "win32-payload-inspect"
        Command = { .\\win32-payload-inspect.exe }
    },
    @{
        Name = "win32-file-buffer"
        Command = { .\\win32-file-buffer.exe .\\smoke-test.txt }
    },
    @{
        Name = "win32-base64-buffer"
        Command = { .\\win32-base64-buffer.exe .\\smoke-test.b64 }
    },
    @{
        Name = "win32-hex-buffer"
        Command = { .\\win32-hex-buffer.exe .\\smoke-test.hex }
    },
    @{
        Name = "win32-pe-runtime-info"
        Command = { .\\win32-pe-runtime-info.exe C:\\Windows\\System32\\notepad.exe }
    },
    @{
        Name = "win32-pe-section-characteristics"
        Command = { .\\win32-pe-section-characteristics.exe C:\\Windows\\System32\\notepad.exe }
    },
    @{
        Name = "win32-reflective-map-lab"
        Command = { .\\win32-reflective-map-lab.exe C:\\Windows\\System32\\notepad.exe }
    },
    @{
        Name = "win32-managed-lab"
        Command = { .\\win32-managed-lab.exe C:\\Windows\\System32\\notepad.exe }
    },
    @{
        Name = "win32-jscript-lab"
        Command = { .\\win32-jscript-lab.exe .\\smoke-test.js }
    },
    @{
        Name = "win32-amsi-inspect"
        Command = { .\\win32-amsi-inspect.exe }
    },
    @{
        Name = "win32-appcontrol-inspect"
        Command = { .\\win32-appcontrol-inspect.exe }
    },
    @{
        Name = "win32-trusted-hosts"
        Command = { .\\win32-trusted-hosts.exe }
    },
    @{
        Name = "win32-runner-helper"
        Command = { .\\win32-runner-helper.exe .\\smoke-test.txt }
    },
    @{
        Name = "kernel-security"
        Command = { .\\kernel-security.exe }
    }
)

$failures = 0
$index = 1

foreach ($test in $tests) {
    $header = "===== TEST $index : $($test.Name) ====="
    $header | Tee-Object -FilePath $log -Append

    $output = & $test.Command 2>&1
    $code = $LASTEXITCODE

    $output | Tee-Object -FilePath $log -Append
    "ExitCode: $code`n" | Tee-Object -FilePath $log -Append

    if ($code -ne 0) {
        $failures++
    }

    $index++
}

"===== SUMMARY =====" | Tee-Object -FilePath $log -Append
"Tests: $($tests.Count)" | Tee-Object -FilePath $log -Append
"Failures: $failures" | Tee-Object -FilePath $log -Append

if ($failures -ne 0) {
    exit 1
}

exit 0
'''


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Build the curated Mifa v2.0 "
            "Windows smoke-test bundle."
        )
    )

    parser.add_argument(
        "--arch",
        choices=[
            "x64",
            "x86",
        ],
        default="x86",
    )

    args = parser.parse_args()

    catalog = MethodCatalog(
        METHODS_DIR
    )

    store = PresetStore(
        PRESETS_DIR
    )

    schema = MethodSchemaValidator()
    compatibility = CompatibilityChecker()
    resolver = ParameterResolver()
    generator = SourceGenerator()
    compiler = Compiler()
    payload_manager = PayloadManager()

    series = version_series()

    output_dir = (
        ROOT
        / "dist"
        / (
            "v"
            + series
            + "-smoke-"
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

    runtime_assets = (
        write_runtime_assets(
            output_dir
        )
    )

    runner_path = (
        output_dir
        / "run_smoke.ps1"
    )

    runner_path.write_text(
        powershell_runner(),
        encoding="utf-8",
    )

    manifest = {
        "version": (
            ROOT / "VERSION"
        ).read_text(
            encoding="utf-8"
        ).strip(),
        "architecture": args.arch,
        "method_count": len(
            SMOKE_METHODS
        ),
        "binaries": [],
        "runtime_assets": [
            {
                "file": path.name,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(
                    path
                ),
            }
            for path in runtime_assets
        ],
        "runner": {
            "file": runner_path.name,
            "sha256": sha256_file(
                runner_path
            ),
        },
    }

    with tempfile.TemporaryDirectory(
        prefix="mifa-smoke-"
    ) as temporary:
        temporary_root = Path(
            temporary
        )

        fixture_path = (
            temporary_root
            / "smoke-payload.txt"
        )

        fixture_path.write_bytes(
            SMOKE_PAYLOAD
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
                    cli_items=[],
                )
            )

            compatibility_errors = (
                compatibility.validate_preset(
                    method=method,
                    preset=preset,
                    parameter_errors=parameter_errors,
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

            payload_info = None
            payload_type = None

            if method.get(
                "requires_payload",
                False,
            ):
                payload_info = (
                    build_payload_fixture(
                        method=method,
                        build_dir=build_dir,
                        fixture_path=fixture_path,
                        payload_manager=payload_manager,
                    )
                )

                payload_type = "text"

            generated = (
                generator.generate(
                    method=method,
                    preset=preset,
                    build_id=(
                        "SMOKE-"
                        + args.arch.upper()
                    ),
                    build_dir=build_dir,
                    payload_info=payload_info,
                    payload_type=payload_type,
                    parameters=parameters,
                )
            )

            result = compiler.compile(
                method=method,
                preset=preset,
                generated_files=generated,
                build_dir=build_dir,
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
                destination,
            )

            binary_entry = {
                "method": method_id,
                "preset": preset_id,
                "file": destination.name,
                "size_bytes": destination.stat().st_size,
                "sha256": sha256_file(
                    destination
                ),
            }

            if payload_info is not None:
                binary_entry[
                    "payload_fixture"
                ] = {
                    "type": payload_type,
                    "transform": payload_info.get(
                        "transform"
                    ),
                    "source_sha256": payload_info.get(
                        "source",
                        {},
                    ).get(
                        "sha256"
                    ),
                    "staged_sha256": payload_info.get(
                        "staged",
                        {},
                    ).get(
                        "sha256"
                    ),
                }

            manifest[
                "binaries"
            ].append(
                binary_entry
            )

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
            indent=2,
        )
        + "\n",
        encoding="utf-8",
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

    print(
        f"[+] Runtime assets: "
        f"{len(runtime_assets)}"
    )

    print(
        f"[+] Runner: "
        f"{runner_path.name}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
