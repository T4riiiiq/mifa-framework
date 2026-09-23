import json
import unittest
from pathlib import Path


ROOT = Path(
    __file__
).resolve().parents[1]


class ReleaseQualityTests(
    unittest.TestCase
):
    def test_version_is_1_1_0(
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
            "1.1.0"
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
            "tools/doctor.py",
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


if __name__ == "__main__":
    unittest.main()
