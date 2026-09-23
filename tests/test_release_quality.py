import json
import unittest
from pathlib import Path


ROOT = Path(
    __file__
).resolve().parents[1]


class ReleaseQualityTests(
    unittest.TestCase
):
    def test_version_is_1_2_0(
        self
    ):
        version = (
            ROOT
            / "VERSION"
        ).read_text(
            encoding="utf-8"
        ).strip()

        self.assertEqual(
            version,
            "1.2.0"
        )

    def test_expected_catalog_counts(
        self
    ):
        method_count = len([
            path
            for path in (
                ROOT / "methods"
            ).iterdir()
            if (
                path.is_dir()
                and (
                    path
                    / "method.json"
                ).is_file()
            )
        ])

        preset_count = len(
            list(
                (
                    ROOT
                    / "presets"
                ).glob(
                    "*.json"
                )
            )
        )

        self.assertEqual(
            method_count,
            34
        )

        self.assertEqual(
            preset_count,
            60
        )

    def test_all_presets_reference_existing_methods(
        self
    ):
        methods = {
            path.parent.name
            for path in (
                ROOT
                / "methods"
            ).glob(
                "*/method.json"
            )
        }

        for path in (
            ROOT
            / "presets"
        ).glob(
            "*.json"
        ):
            data = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

            with self.subTest(
                preset=path.name
            ):
                self.assertIn(
                    data.get(
                        "method"
                    ),
                    methods
                )

    def test_generated_directories_ignored(
        self
    ):
        text = (
            ROOT
            / ".gitignore"
        ).read_text(
            encoding="utf-8"
        )

        required = [
            "builds/*",
            "payloads/*",
            "dist/*",
        ]

        for pattern in required:
            with self.subTest(
                pattern=pattern
            ):
                self.assertIn(
                    pattern,
                    text
                )

    def test_release_tools_exist(
        self
    ):
        for relative in [
            "tools/verify.py",
            "tools/release_validate.py",
            "tools/prepare_smoke.py",
        ]:
            with self.subTest(
                path=relative
            ):
                self.assertTrue(
                    (
                        ROOT
                        / relative
                    ).is_file()
                )

    def test_phase3_release_docs_exist(
        self
    ):
        for relative in [
            "docs/PHASE3_BATCH3_INTEGRATION_VALIDATION.md",
            "docs/V1_2_VALIDATION.md",
            "docs/RELEASE_NOTES_v1.2.md",
        ]:
            with self.subTest(
                path=relative
            ):
                self.assertTrue(
                    (
                        ROOT
                        / relative
                    ).is_file()
                )

    def test_smoke_tool_covers_phase3_methods(
        self
    ):
        text = (
            ROOT
            / "tools"
            / "prepare_smoke.py"
        ).read_text(
            encoding="utf-8"
        )

        required = [
            "win32-payload-inspect",
            "win32-file-buffer",
            "win32-base64-buffer",
            "win32-hex-buffer",
            "win32-pe-runtime-info",
            "win32-pe-section-characteristics",
        ]

        for method_id in required:
            with self.subTest(
                method=method_id
            ):
                self.assertIn(
                    f'"{method_id}"',
                    text
                )


if __name__ == "__main__":
    unittest.main()
