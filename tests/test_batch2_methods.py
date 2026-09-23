import json
import unittest
from pathlib import Path

from core.schema import MethodSchemaValidator


ROOT = Path(
    __file__
).resolve().parents[1]

METHOD_IDS = [
    "win32-api-resolve",
    "win32-local-buffer",
    "win32-local-thread",
    "win32-dll-load-info",
    "win32-file-map",
    "win32-runtime-helper",
]

DISALLOWED_REMOTE_EXECUTION_TOKENS = [
    "VirtualAllocEx",
    "WriteProcessMemory",
    "CreateRemoteThread",
    "NtCreateThreadEx",
    "PAGE_EXECUTE",
]


class Batch2MethodTests(
    unittest.TestCase
):
    def test_method_contracts(
        self
    ):
        schema = (
            MethodSchemaValidator()
        )

        for method_id in METHOD_IDS:
            with self.subTest(
                method=method_id
            ):
                path = (
                    ROOT
                    / "methods"
                    / method_id
                    / "method.json"
                )

                data = json.loads(
                    path.read_text(
                        encoding="utf-8"
                    )
                )

                self.assertEqual(
                    schema.validate(
                        data
                    ),
                    []
                )

    def test_templates_exist(
        self
    ):
        for method_id in METHOD_IDS:
            path = (
                ROOT
                / "methods"
                / method_id
                / "method.json"
            )

            data = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

            for source in data[
                "sources"
            ]:
                with self.subTest(
                    method=method_id,
                    source=source[
                        "template"
                    ]
                ):
                    template = (
                        path.parent
                        / source[
                            "template"
                        ]
                    )

                    self.assertTrue(
                        template.is_file()
                    )

    def test_x64_x86_presets_exist(
        self
    ):
        for method_id in METHOD_IDS:
            for arch in (
                "x64",
                "x86"
            ):
                with self.subTest(
                    method=method_id,
                    arch=arch
                ):
                    path = (
                        ROOT
                        / "presets"
                        / (
                            f"{method_id}-"
                            f"{arch}.json"
                        )
                    )

                    data = json.loads(
                        path.read_text(
                            encoding="utf-8"
                        )
                    )

                    self.assertEqual(
                        data["method"],
                        method_id
                    )

                    self.assertEqual(
                        data["architecture"],
                        arch
                    )

    def test_no_remote_execution_primitives(
        self
    ):
        for method_id in METHOD_IDS:
            template_dir = (
                ROOT
                / "methods"
                / method_id
                / "templates"
            )

            combined = "\n".join(
                path.read_text(
                    encoding="utf-8"
                )
                for path in template_dir.glob(
                    "*.tmpl"
                )
            )

            for token in (
                DISALLOWED_REMOTE_EXECUTION_TOKENS
            ):
                with self.subTest(
                    method=method_id,
                    token=token
                ):
                    self.assertNotIn(
                        token,
                        combined
                    )


if __name__ == "__main__":
    unittest.main()
