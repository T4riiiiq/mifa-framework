import json
import unittest
from pathlib import Path

from core.catalog import MethodCatalog
from core.presets import PresetStore
from core.workflows import QUICK_ENTRIES, alias_map, find_preset


ROOT = Path(__file__).resolve().parents[1]


FIRST_CLASS = {
    "native": "win32-local-thread",
    "inject": "win32-inject-lab",
    "dll": "win32-dll-injection-lab",
    "reflect": "win32-reflective-map-lab",
    "hollow": "win32-hollow-lab",
    "managed": "win32-managed-lab",
    "jscript": "win32-jscript-lab",
}


TECHNIQUE_METADATA = {
    "native": {
        "role": "technique",
        "runtime": "native",
    },
    "inject": {
        "role": "technique",
        "runtime": "native",
    },
    "dll": {
        "role": "technique",
        "runtime": "native",
    },
    "reflect": {
        "role": "technique",
        "runtime": "native",
    },
    "hollow": {
        "role": "technique",
        "runtime": "native",
    },
    "managed": {
        "role": "technique",
        "runtime": "managed",
    },
    "jscript": {
        "role": "technique",
        "runtime": "script",
    },
}


COMPATIBILITY_METHODS = (
    "win32-inject-lab",
    "win32-dll-injection-lab",
    "win32-reflective-map-lab",
    "win32-hollow-lab",
)


FORBIDDEN_REMOTE_PRIMITIVES = (
    "VirtualAllocEx",
    "WriteProcessMemory",
    "VirtualProtectEx",
    "CreateRemoteThread",
    "NtCreateThreadEx",
    "SetThreadContext",
    "Wow64SetThreadContext",
    "ResumeThread",
)


class Phase4TechniqueTests(unittest.TestCase):
    def setUp(self):
        self.catalog = MethodCatalog(
            ROOT / "methods"
        )

        self.presets = PresetStore(
            ROOT / "presets"
        )

    def load_method_json(self, method_id):
        path = (
            ROOT
            / "methods"
            / method_id
            / "method.json"
        )

        with path.open(
            "r",
            encoding="utf-8",
        ) as handle:
            return json.load(handle)

    def test_first_class_aliases_resolve(self):
        aliases = alias_map()

        for alias, method_id in FIRST_CLASS.items():
            with self.subTest(alias=alias):
                self.assertEqual(
                    aliases.get(alias),
                    method_id,
                )

    def test_first_class_methods_exist(self):
        for alias, method_id in FIRST_CLASS.items():
            with self.subTest(alias=alias):
                self.assertIsNotNone(
                    self.catalog.get(method_id)
                )

    def test_first_class_technique_metadata(self):
        for alias, method_id in FIRST_CLASS.items():
            with self.subTest(alias=alias):
                method = self.load_method_json(
                    method_id
                )

                technique = method.get(
                    "technique"
                )

                self.assertIsInstance(
                    technique,
                    dict,
                )

                self.assertEqual(
                    technique.get("alias"),
                    alias,
                )

                self.assertEqual(
                    technique.get("role"),
                    TECHNIQUE_METADATA[
                        alias
                    ]["role"],
                )

                self.assertEqual(
                    technique.get("runtime"),
                    TECHNIQUE_METADATA[
                        alias
                    ]["runtime"],
                )

                self.assertTrue(
                    technique.get("quick")
                )

    def test_first_class_x64_x86_presets_exist(self):
        for alias, method_id in FIRST_CLASS.items():
            for architecture in (
                "x64",
                "x86",
            ):
                with self.subTest(
                    alias=alias,
                    architecture=architecture,
                ):
                    preset = find_preset(
                        self.presets,
                        method_id,
                        architecture,
                    )

                    self.assertIsNotNone(
                        preset
                    )

                    self.assertEqual(
                        preset.get(
                            "architecture"
                        ),
                        architecture,
                    )

                    self.assertEqual(
                        preset.get("method"),
                        method_id,
                    )

    def test_first_class_quick_entries_are_techniques(self):
        entries = {
            entry["alias"]: entry
            for entry in QUICK_ENTRIES
        }

        for alias in FIRST_CLASS:
            with self.subTest(alias=alias):
                self.assertIn(
                    alias,
                    entries,
                )

                self.assertEqual(
                    entries[alias].get(
                        "category"
                    ),
                    "Techniques",
                )

    def test_compatibility_methods_exclude_remote_execution_primitives(self):
        for method_id in COMPATIBILITY_METHODS:
            method_dir = (
                ROOT
                / "methods"
                / method_id
                / "templates"
            )

            content = "\n".join(
                path.read_text(
                    encoding="utf-8"
                )
                for path in method_dir.rglob(
                    "*.tmpl"
                )
            )

            for primitive in FORBIDDEN_REMOTE_PRIMITIVES:
                with self.subTest(
                    method=method_id,
                    primitive=primitive,
                ):
                    self.assertNotIn(
                        primitive,
                        content,
                    )


if __name__ == "__main__":
    unittest.main()
