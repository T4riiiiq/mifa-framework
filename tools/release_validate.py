#!/usr/bin/env python3

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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

FORBIDDEN_TRACKED_SUFFIXES = {
    ".exe",
    ".dll",
    ".bin",
    ".o",
    ".obj",
}

FORBIDDEN_TRACKED_PREFIXES = {
    "builds/",
    "dist/",
    "payloads/",
}

ALLOWED_TRACKED_GENERATED = {
    "builds/.gitkeep",
    "dist/.gitkeep",
    "payloads/.gitkeep",
}

FIXTURE_DATA = {
    "text": b"Mifa release validation fixture\n",
    "json": b'{"mifa":"release-validation"}\n',
    "raw": b"Mifa release validation fixture\x00",
    "pe": b"MZ" + (b"\x00" * 62),
}

FIXTURE_SUFFIX = {
    "text": ".txt",
    "json": ".json",
    "raw": ".bin",
    "pe": ".exe",
}

PAYLOAD_TYPE_PRIORITY = (
    "text",
    "json",
    "raw",
    "pe",
)


def sha256_file(path):
    digest = hashlib.sha256()

    with Path(path).open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def git_output(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return None

    return result.stdout


def check_tracked_artifacts():
    output = git_output("ls-files")

    if output is None:
        return [
            "Unable to inspect tracked files with git ls-files"
        ]

    errors = []

    for line in output.splitlines():
        path = line.strip()

        if not path:
            continue

        if path in ALLOWED_TRACKED_GENERATED:
            continue

        suffix = Path(path).suffix.lower()

        if suffix in FORBIDDEN_TRACKED_SUFFIXES:
            errors.append(
                f"Tracked binary/object artifact: {path}"
            )

        for prefix in FORBIDDEN_TRACKED_PREFIXES:
            if path.startswith(prefix):
                errors.append(
                    f"Tracked generated artifact: {path}"
                )
                break

    return errors


def check_git_clean():
    output = git_output(
        "status",
        "--porcelain",
    )

    if output is None:
        return [
            "Unable to inspect git status"
        ]

    if output.strip():
        return [
            "Working tree is not clean"
        ]

    return []


def run_unit_tests():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    return {
        "passed": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def payload_contract(method):
    contract = method.get("payload_contract")

    if isinstance(contract, dict):
        return contract

    return {
        "required": method.get(
            "requires_payload",
            False,
        ),
        "types": list(
            method.get(
                "payload_types",
                [],
            )
        ),
        "transforms": [
            "copy"
        ],
        "default_transform": "copy",
    }


def select_payload_fixture(method):
    contract = payload_contract(method)

    accepted_types = contract.get(
        "types",
        method.get(
            "payload_types",
            [],
        ),
    )

    payload_type = None

    for candidate in PAYLOAD_TYPE_PRIORITY:
        if candidate in accepted_types:
            payload_type = candidate
            break

    if payload_type is None:
        raise ValueError(
            "Payload-required method has no supported "
            "release-validation fixture type"
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
        raise ValueError(
            "Payload contract default transform is not "
            "listed in accepted transforms"
        )

    return (
        payload_type,
        transform,
    )


def create_payload_fixture(
    method,
    fixture_dir,
):
    payload_type, transform = (
        select_payload_fixture(
            method
        )
    )

    fixture_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    suffix = FIXTURE_SUFFIX[
        payload_type
    ]

    fixture_path = (
        fixture_dir
        / (
            method.get(
                "id",
                "payload",
            )
            + suffix
        )
    )

    fixture_path.write_bytes(
        FIXTURE_DATA[
            payload_type
        ]
    )

    return {
        "path": fixture_path,
        "type": payload_type,
        "transform": transform,
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Run Mifa release validation across "
            "methods and presets."
        )
    )

    parser.add_argument(
        "--compile",
        action="store_true",
        help=(
            "Compile every valid preset in a "
            "temporary workspace. Payload-required "
            "methods receive deterministic harmless "
            "build fixtures."
        ),
    )

    parser.add_argument(
        "--strict-git",
        action="store_true",
        help=(
            "Require a clean git working tree."
        ),
    )

    parser.add_argument(
        "--json",
        dest="json_path",
        help=(
            "Write a machine-readable validation "
            "summary to this path."
        ),
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

    methods = catalog.discover()
    presets = store.discover()

    failures = []
    warnings = []
    method_map = {}
    preset_ids = set()

    summary = {
        "version": (
            ROOT / "VERSION"
        ).read_text(
            encoding="utf-8"
        ).strip(),
        "method_count": len(methods),
        "preset_count": len(presets),
        "methods_valid": 0,
        "presets_valid": 0,
        "compiled": 0,
        "payload_fixture_compiled": 0,
        "compile_skipped_payload": 0,
        "unit_tests_passed": False,
        "failures": [],
        "warnings": [],
        "compile_results": [],
    }

    print(
        "Mifa Release Validation"
    )
    print(
        "=" * 48
    )

    for method in methods:
        method_id = method.get(
            "id"
        )

        if method_id in method_map:
            failures.append(
                f"Duplicate method ID: {method_id}"
            )
            continue

        method_map[
            method_id
        ] = method

        errors = schema.validate(
            method
        )

        if errors:
            for error in errors:
                failures.append(
                    f"{method_id}: {error}"
                )
        else:
            summary[
                "methods_valid"
            ] += 1

    print(
        f"Methods : "
        f"{summary['methods_valid']}"
        f"/{len(methods)} valid"
    )

    valid_presets = []

    for preset in presets:
        preset_id = preset.get(
            "id"
        )

        if (
            not isinstance(
                preset_id,
                str,
            )
            or not preset_id.strip()
        ):
            failures.append(
                "Preset with missing/invalid ID"
            )
            continue

        if preset_id in preset_ids:
            failures.append(
                f"Duplicate preset ID: {preset_id}"
            )
            continue

        preset_ids.add(
            preset_id
        )

        method_id = preset.get(
            "method"
        )

        method = method_map.get(
            method_id
        )

        if method is None:
            failures.append(
                f"{preset_id}: references missing "
                f"method '{method_id}'"
            )
            continue

        architecture = preset.get(
            "architecture"
        )

        build_type = preset.get(
            "build_type"
        )

        if architecture is None:
            failures.append(
                f"{preset_id}: missing architecture"
            )
            continue

        if build_type is None:
            failures.append(
                f"{preset_id}: missing build_type"
            )
            continue

        parameters, parameter_errors = (
            resolver.resolve(
                method=method,
                preset=preset,
                cli_items=[],
            )
        )

        errors = compatibility.validate_preset(
            method=method,
            preset=preset,
            parameter_errors=parameter_errors,
        )

        if errors:
            for error in errors:
                failures.append(
                    f"{preset_id}: {error}"
                )

            continue

        valid_presets.append(
            (
                preset,
                method,
                parameters,
            )
        )

        summary[
            "presets_valid"
        ] += 1

    print(
        f"Presets : "
        f"{summary['presets_valid']}"
        f"/{len(presets)} valid"
    )

    artifact_errors = (
        check_tracked_artifacts()
    )

    failures.extend(
        artifact_errors
    )

    if not artifact_errors:
        print(
            "Tracked artifacts : clean"
        )

    unit = run_unit_tests()

    summary[
        "unit_tests_passed"
    ] = unit[
        "passed"
    ]

    if unit[
        "passed"
    ]:
        print(
            "Unit tests        : PASS"
        )
    else:
        failures.append(
            "Unit tests failed"
        )

        print(
            "Unit tests        : FAIL"
        )

        if unit[
            "stdout"
        ]:
            print(
                unit[
                    "stdout"
                ]
            )

        if unit[
            "stderr"
        ]:
            print(
                unit[
                    "stderr"
                ]
            )

    if args.compile:
        print()
        print(
            "Compile matrix"
        )
        print(
            "-" * 48
        )

        with tempfile.TemporaryDirectory(
            prefix="mifa-release-"
        ) as temporary:
            temporary_root = Path(
                temporary
            )

            fixture_dir = (
                temporary_root
                / "_fixtures"
            )

            for (
                preset,
                method,
                parameters,
            ) in valid_presets:
                preset_id = preset[
                    "id"
                ]

                build_dir = (
                    temporary_root
                    / preset_id
                )

                payload_info = None
                payload_type = None
                payload_transform = None
                used_fixture = False

                try:
                    if method.get(
                        "requires_payload",
                        False,
                    ):
                        fixture = (
                            create_payload_fixture(
                                method=method,
                                fixture_dir=fixture_dir,
                            )
                        )

                        payload_type = fixture[
                            "type"
                        ]

                        payload_transform = fixture[
                            "transform"
                        ]

                        payload_info = (
                            payload_manager.prepare(
                                payload_path=fixture[
                                    "path"
                                ],
                                build_dir=build_dir,
                                method=method,
                                payload_type=payload_type,
                                transform=payload_transform,
                            )
                        )

                        used_fixture = True

                    generated = (
                        generator.generate(
                            method=method,
                            preset=preset,
                            build_id="RELEASE-CHECK",
                            build_dir=build_dir,
                            payload_info=payload_info,
                            payload_type=payload_type,
                            parameters=parameters,
                        )
                    )

                    result = (
                        compiler.compile(
                            method=method,
                            preset=preset,
                            generated_files=generated,
                            build_dir=build_dir,
                        )
                    )

                    output = Path(
                        result[
                            "output"
                        ]
                    )

                    summary[
                        "compiled"
                    ] += 1

                    if used_fixture:
                        summary[
                            "payload_fixture_compiled"
                        ] += 1

                    summary[
                        "compile_results"
                    ].append({
                        "preset": preset_id,
                        "architecture": preset.get(
                            "architecture"
                        ),
                        "output_name": output.name,
                        "size_bytes": output.stat().st_size,
                        "sha256": sha256_file(
                            output
                        ),
                        "payload_fixture": (
                            {
                                "type": payload_type,
                                "transform": payload_transform,
                            }
                            if used_fixture
                            else None
                        ),
                    })

                    fixture_note = (
                        " [fixture:"
                        + str(
                            payload_type
                        )
                        + "/"
                        + str(
                            payload_transform
                        )
                        + "]"
                        if used_fixture
                        else ""
                    )

                    print(
                        f"[PASS] {preset_id}"
                        f"{fixture_note}"
                    )

                except Exception as exc:
                    failures.append(
                        f"{preset_id}: compile failed: "
                        f"{exc}"
                    )

                    print(
                        f"[FAIL] {preset_id}: "
                        f"{exc}"
                    )

    if args.strict_git:
        git_errors = (
            check_git_clean()
        )

        failures.extend(
            git_errors
        )

        if not git_errors:
            print(
                "Git working tree : clean"
            )

    summary[
        "failures"
    ] = failures

    summary[
        "warnings"
    ] = warnings

    if args.json_path:
        json_path = Path(
            args.json_path
        )

        if not json_path.is_absolute():
            json_path = (
                ROOT / json_path
            )

        json_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        json_path.write_text(
            json.dumps(
                summary,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        print(
            f"JSON summary      : "
            f"{json_path}"
        )

    print()
    print(
        "=" * 48
    )

    print(
        f"Compiled          : "
        f"{summary['compiled']}"
    )

    print(
        f"Payload fixtures  : "
        f"{summary['payload_fixture_compiled']}"
    )

    print(
        f"Skipped payload   : "
        f"{summary['compile_skipped_payload']}"
    )

    print(
        f"Warnings          : "
        f"{len(warnings)}"
    )

    print(
        f"Failures          : "
        f"{len(failures)}"
    )

    if failures:
        print()

        for failure in failures:
            print(
                f"[!] {failure}"
            )

        return 1

    print(
        "[+] Release validation passed"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
