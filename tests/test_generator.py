import tempfile
import unittest
from pathlib import Path

from core.generator import SourceGenerator


class GeneratorTests(
    unittest.TestCase
):
    def test_parameter_rendering(
        self
    ):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(
                temp
            )

            method_dir = (
                root / "method"
            )

            template_dir = (
                method_dir / "templates"
            )

            template_dir.mkdir(
                parents=True
            )

            (
                template_dir
                / "main.cpp.tmpl"
            ).write_text(
                'const char* x = "{{PARAM_MESSAGE}}";\n'
                'int n = {{PARAM_COUNT}};\n'
                'bool enabled = {{PARAM_ENABLED}};\n',
                encoding="utf-8"
            )

            method = {
                "_path": str(
                    method_dir
                ),
                "parameters": {
                    "message": {
                        "type": "str",
                        "render": "c_string"
                    },
                    "count": {
                        "type": "int"
                    },
                    "enabled": {
                        "type": "bool"
                    }
                },
                "sources": [
                    {
                        "template":
                            "templates/main.cpp.tmpl",
                        "output":
                            "main.cpp",
                        "compile":
                            True
                    }
                ]
            }

            preset = {
                "architecture": "x64",
                "build_type": "release"
            }

            build_dir = (
                root / "build"
            )

            generated = (
                SourceGenerator().generate(
                    method=method,
                    preset=preset,
                    build_id="K-TEST",
                    build_dir=build_dir,
                    parameters={
                        "message":
                            'A "quoted" value',
                        "count":
                            3,
                        "enabled":
                            True
                    }
                )
            )

            text = (
                generated[0]["path"]
                .read_text(
                    encoding="utf-8"
                )
            )

            self.assertIn(
                'A \\"quoted\\" value',
                text
            )

            self.assertIn(
                "int n = 3;",
                text
            )

            self.assertIn(
                "bool enabled = true;",
                text
            )


if __name__ == "__main__":
    unittest.main()
