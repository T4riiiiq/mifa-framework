import base64
import binascii
import json
import tempfile
import unittest
from pathlib import Path

from core.compatibility import CompatibilityChecker
from core.payloads import PayloadManager
from core.schema import MethodSchemaValidator


class PayloadV2Tests(
    unittest.TestCase
):
    def setUp(self):
        self.manager = (
            PayloadManager()
        )

        self.method = {
            "id": "payload-test",
            "name": "Payload Test",
            "language": "c",
            "architectures": [
                "x64"
            ],
            "requires_payload": True,
            "payload_types": [
                "raw",
                "text",
                "json",
                "pe"
            ],
            "payload_contract": {
                "required": True,
                "types": [
                    "raw",
                    "text",
                    "json",
                    "pe"
                ],
                "transforms": [
                    "copy",
                    "base64",
                    "hex"
                ],
                "default_transform":
                    "copy",
                "min_size_bytes":
                    1,
                "max_size_bytes":
                    1024
            },
            "sources": [
                {
                    "template":
                        "templates/main.c.tmpl",
                    "output":
                        "main.c",
                    "compile":
                        True
                }
            ],
            "output_name":
                "payload-test.exe"
        }

        self.preset = {
            "id":
                "payload-test-x64",
            "method":
                "payload-test",
            "architecture":
                "x64",
            "build_type":
                "release"
        }

    def _prepare(
        self,
        data,
        payload_type="raw",
        transform=None,
        name="input.bin"
    ):
        temporary = (
            tempfile.TemporaryDirectory()
        )

        self.addCleanup(
            temporary.cleanup
        )

        root = Path(
            temporary.name
        )

        source = (
            root / name
        )

        source.write_bytes(
            data
        )

        build_dir = (
            root / "build"
        )

        info = self.manager.prepare(
            payload_path=source,
            build_dir=build_dir,
            method=self.method,
            payload_type=payload_type,
            transform=transform
        )

        return (
            root,
            source,
            build_dir,
            info
        )

    def test_copy_preserves_bytes_and_provenance(
        self
    ):
        data = b"Mifa payload v2"

        _, _, build_dir, info = (
            self._prepare(
                data
            )
        )

        staged = (
            build_dir
            / info[
                "staged"
            ][
                "file"
            ]
        )

        self.assertEqual(
            staged.read_bytes(),
            data
        )

        self.assertEqual(
            info[
                "source"
            ][
                "size_bytes"
            ],
            len(
                data
            )
        )

        self.assertEqual(
            info[
                "source"
            ][
                "sha256"
            ],
            info[
                "staged"
            ][
                "sha256"
            ]
        )

    def test_base64_transform(
        self
    ):
        data = b"abc123"

        _, _, build_dir, info = (
            self._prepare(
                data,
                transform="base64"
            )
        )

        staged = (
            build_dir
            / info[
                "staged"
            ][
                "file"
            ]
        )

        self.assertEqual(
            staged.read_bytes(),
            base64.b64encode(
                data
            )
        )

        self.assertEqual(
            info[
                "transform"
            ],
            "base64"
        )

    def test_hex_transform(
        self
    ):
        data = b"\x00\x10\xff"

        _, _, build_dir, info = (
            self._prepare(
                data,
                transform="hex"
            )
        )

        staged = (
            build_dir
            / info[
                "staged"
            ][
                "file"
            ]
        )

        self.assertEqual(
            staged.read_bytes(),
            binascii.hexlify(
                data
            )
        )

    def test_text_adapter_rejects_invalid_utf8(
        self
    ):
        with self.assertRaises(
            ValueError
        ):
            self._prepare(
                b"\xff\xfe",
                payload_type="text",
                name="input.txt"
            )

    def test_json_adapter_accepts_valid_json(
        self
    ):
        data = json.dumps(
            {
                "mifa":
                    3
            }
        ).encode(
            "utf-8"
        )

        _, _, _, info = (
            self._prepare(
                data,
                payload_type="json",
                name="input.json"
            )
        )

        self.assertEqual(
            info[
                "type"
            ],
            "json"
        )

    def test_pe_adapter_requires_mz(
        self
    ):
        with self.assertRaises(
            ValueError
        ):
            self._prepare(
                b"not-a-pe",
                payload_type="pe",
                name="input.exe"
            )

    def test_schema_accepts_payload_contract_v2(
        self
    ):
        errors = (
            MethodSchemaValidator()
            .validate(
                self.method
            )
        )

        self.assertEqual(
            errors,
            []
        )

    def test_compatibility_rejects_unsupported_transform(
        self
    ):
        errors = (
            CompatibilityChecker()
            .validate(
                method=self.method,
                preset=self.preset,
                payload_path="input.bin",
                payload_type="raw",
                payload_transform="gzip"
            )
        )

        self.assertTrue(
            any(
                "transform"
                in error.lower()
                for error in errors
            )
        )


if __name__ == "__main__":
    unittest.main()


class PayloadManifestTests(
    unittest.TestCase
):
    def test_build_manifest_records_contract_and_provenance(
        self
    ):
        from core.builds import BuildManager

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            builds_dir = root / "builds"

            method = {
                "id": "payload-test",
                "name": "Payload Test",
                "language": "c",
                "runtime_arguments": [],
                "payload_contract": {
                    "required": True,
                    "types": ["raw"],
                    "transforms": ["copy", "base64"],
                    "default_transform": "copy"
                }
            }

            preset = {
                "id": "payload-test-x64",
                "architecture": "x64",
                "build_type": "release"
            }

            manager = BuildManager(
                builds_dir
            )

            _, build_dir = manager.create(
                method=method,
                preset=preset
            )

            payload_info = {
                "transform": "base64",
                "source": {
                    "name": "input.bin",
                    "suffix": ".bin",
                    "mime_type": None,
                    "size_bytes": 3,
                    "sha256": "sourcehash"
                },
                "staged": {
                    "file": "input/input.bin.b64",
                    "name": "input.bin.b64",
                    "size_bytes": 4,
                    "sha256": "stagedhash"
                },
                "file": "input/input.bin.b64",
                "name": "input.bin.b64",
                "size_bytes": 4,
                "sha256": "stagedhash"
            }

            manager.attach_payload(
                build_dir=build_dir,
                payload_info=payload_info,
                payload_type="raw"
            )

            manifest = json.loads(
                (
                    build_dir
                    / "build.json"
                ).read_text(
                    encoding="utf-8"
                )
            )

            self.assertEqual(
                manifest[
                    "payload_contract"
                ][
                    "default_transform"
                ],
                "copy"
            )

            self.assertEqual(
                manifest[
                    "payload"
                ][
                    "transform"
                ],
                "base64"
            )

            self.assertEqual(
                manifest[
                    "payload"
                ][
                    "source"
                ][
                    "sha256"
                ],
                "sourcehash"
            )

            self.assertEqual(
                manifest[
                    "payload"
                ][
                    "staged"
                ][
                    "sha256"
                ],
                "stagedhash"
            )


class PayloadGeneratorTests(
    unittest.TestCase
):
    def test_generator_renders_payload_v2_tokens(
        self
    ):
        from core.generator import SourceGenerator

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            method_dir = root / "method"
            templates = method_dir / "templates"
            templates.mkdir(parents=True)

            (
                templates
                / "main.c.tmpl"
            ).write_text(
                "type={{PAYLOAD_TYPE}}\n"
                "transform={{PAYLOAD_TRANSFORM}}\n"
                "source={{PAYLOAD_SOURCE_NAME}}\n"
                "staged={{PAYLOAD_STAGED_NAME}}\n"
                "source_sha={{PAYLOAD_SOURCE_SHA256}}\n"
                "staged_sha={{PAYLOAD_STAGED_SHA256}}\n",
                encoding="utf-8"
            )

            method = {
                "_path": str(method_dir),
                "parameters": {},
                "sources": [
                    {
                        "template": "templates/main.c.tmpl",
                        "output": "main.c",
                        "compile": True
                    }
                ]
            }

            preset = {
                "architecture": "x64",
                "build_type": "release"
            }

            payload_info = {
                "transform": "hex",
                "source": {
                    "name": "input.bin",
                    "size_bytes": 3,
                    "sha256": "sourcehash"
                },
                "staged": {
                    "name": "input.bin.hex",
                    "size_bytes": 6,
                    "sha256": "stagedhash"
                },
                "name": "input.bin.hex",
                "size_bytes": 6,
                "sha256": "stagedhash"
            }

            generated = SourceGenerator().generate(
                method=method,
                preset=preset,
                build_id="TEST",
                build_dir=root / "build",
                payload_info=payload_info,
                payload_type="raw",
                parameters={}
            )

            rendered = (
                generated[0]["path"]
                .read_text(
                    encoding="utf-8"
                )
            )

            self.assertIn(
                "transform=hex",
                rendered
            )

            self.assertIn(
                "source=input.bin",
                rendered
            )

            self.assertIn(
                "staged=input.bin.hex",
                rendered
            )

            self.assertIn(
                "source_sha=sourcehash",
                rendered
            )

            self.assertIn(
                "staged_sha=stagedhash",
                rendered
            )
