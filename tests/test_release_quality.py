import ast
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseQualityTests(unittest.TestCase):
    def test_version_is_2_0_0(self):
        version = (
            ROOT / "VERSION"
        ).read_text(
            encoding="utf-8"
        ).strip()

        self.assertEqual(
            version,
            "2.0.0",
        )

    def test_expected_v2_catalog_counts(self):
        method_count = len([
            path
            for path in (
                ROOT / "methods"
            ).iterdir()
            if (
                path.is_dir()
                and (
                    path / "method.json"
                ).is_file()
            )
        ])

        preset_count = len(
            list(
                (
                    ROOT / "presets"
                ).glob("*.json")
            )
        )

        self.assertEqual(
            method_count,
            45,
        )

        self.assertEqual(
            preset_count,
            82,
        )

    def test_all_presets_reference_existing_methods(self):
        methods = {
            path.parent.name
            for path in (
                ROOT / "methods"
            ).glob("*/method.json")
        }

        for path in (
            ROOT / "presets"
        ).glob("*.json"):
            data = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

            with self.subTest(
                preset=path.name
            ):
                self.assertIn(
                    data.get("method"),
                    methods,
                )

    def test_generated_directories_ignored(self):
        text = (
            ROOT / ".gitignore"
        ).read_text(
            encoding="utf-8"
        )

        for pattern in [
            "builds/*",
            "payloads/*",
            "dist/*",
        ]:
            with self.subTest(
                pattern=pattern
            ):
                self.assertIn(
                    pattern,
                    text,
                )

    def test_release_tools_exist(self):
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
                        ROOT / relative
                    ).is_file()
                )

    def test_v2_release_docs_exist(self):
        for relative in [
            "docs/TECHNIQUE_COVERAGE_MATRIX.md",
            "docs/PHASE4_BATCH3_RELEASE.md",
            "docs/V2_VALIDATION.md",
            "docs/RELEASE_NOTES_v2.0.md",
        ]:
            with self.subTest(
                path=relative
            ):
                self.assertTrue(
                    (
                        ROOT / relative
                    ).is_file()
                )

    def test_v2_smoke_catalog(self):
        path = (
            ROOT
            / "tools"
            / "prepare_smoke.py"
        )

        tree = ast.parse(
            path.read_text(
                encoding="utf-8"
            )
        )

        smoke_methods = None

        for node in tree.body:
            if not isinstance(
                node,
                ast.Assign,
            ):
                continue

            for target in node.targets:
                if (
                    isinstance(target, ast.Name)
                    and target.id == "SMOKE_METHODS"
                ):
                    smoke_methods = ast.literal_eval(
                        node.value
                    )

        self.assertIsNotNone(
            smoke_methods
        )

        self.assertEqual(
            len(smoke_methods),
            21,
        )

        required = {
            "win32-local-thread",
            "win32-payload-inspect",
            "win32-pe-runtime-info",
            "win32-reflective-map-lab",
            "win32-managed-lab",
            "win32-jscript-lab",
            "win32-amsi-inspect",
            "win32-appcontrol-inspect",
            "win32-trusted-hosts",
            "win32-runner-helper",
            "kernel-security",
        }

        self.assertTrue(
            required.issubset(
                set(smoke_methods)
            )
        )

    def test_readme_identifies_v2(self):
        text = (
            ROOT / "README.md"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "**Current version:** `2.0.0`",
            text,
        )

        self.assertIn(
            "45 valid method contracts",
            text,
        )

        self.assertIn(
            "82 x64/x86 presets",
            text,
        )


if __name__ == "__main__":
    unittest.main()
