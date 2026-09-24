import json
import unittest
from pathlib import Path

from core.catalog import MethodCatalog
from core.presets import PresetStore
from core.workflows import SUPPORT_ENTRIES, alias_map, find_preset


ROOT = Path(__file__).resolve().parents[1]


SUPPORTING = {
    "amsi": {
        "method": "win32-amsi-inspect",
        "role": "inspect",
        "runtime": "native",
    },
    "appcontrol": {
        "method": "win32-appcontrol-inspect",
        "role": "inspect",
        "runtime": "native",
    },
    "trusted": {
        "method": "win32-trusted-hosts",
        "role": "helper",
        "runtime": "native",
    },
    "runner": {
        "method": "win32-runner-helper",
        "role": "helper",
        "runtime": "native",
    },
    "kernel": {
        "method": "kernel-security",
        "role": "inspect",
        "runtime": "kernel",
    },
}


FORBIDDEN_MUTATION_PRIMITIVES = (
    "WriteProcessMemory",
    "VirtualAllocEx",
    "CreateRemoteThread",
    "NtCreateThreadEx",
    "RegSetValue",
    "RegDelete",
    "CreateService",
    "StartService",
    "ControlService",
    "DeleteService",
    "AdjustTokenPrivileges",
    "DeviceIoControl",
    "SetThreadContext",
    "ResumeThread",
    "ShellExecute",
    "WinExec",
)


class Phase4SupportingCapabilityTests(unittest.TestCase):
    def setUp(self):
        self.catalog = MethodCatalog(
            ROOT / "methods"
        )

        self.presets = PresetStore(
            ROOT / "presets"
        )

    def load_method(self, method_id):
        path = (
            ROOT
            / "methods"
            / method_id
            / "method.json"
        )

        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    def test_support_aliases_resolve(self):
        aliases = alias_map()

        for alias, expected in SUPPORTING.items():
            with self.subTest(alias=alias):
                self.assertEqual(
                    aliases.get(alias),
                    expected["method"],
                )

    def test_support_methods_exist(self):
        for alias, expected in SUPPORTING.items():
            with self.subTest(alias=alias):
                self.assertIsNotNone(
                    self.catalog.get(
                        expected["method"]
                    )
                )

    def test_support_metadata(self):
        for alias, expected in SUPPORTING.items():
            with self.subTest(alias=alias):
                method = self.load_method(
                    expected["method"]
                )

                technique = method["technique"]

                self.assertEqual(
                    technique["alias"],
                    alias,
                )

                self.assertEqual(
                    technique["role"],
                    expected["role"],
                )

                self.assertEqual(
                    technique["runtime"],
                    expected["runtime"],
                )

                self.assertFalse(
                    technique["quick"]
                )

    def test_support_x64_x86_presets(self):
        for alias, expected in SUPPORTING.items():
            for architecture in ("x64", "x86"):
                with self.subTest(
                    alias=alias,
                    architecture=architecture,
                ):
                    preset = find_preset(
                        self.presets,
                        expected["method"],
                        architecture,
                    )

                    self.assertIsNotNone(
                        preset
                    )

                    self.assertEqual(
                        preset["method"],
                        expected["method"],
                    )

                    self.assertEqual(
                        preset["architecture"],
                        architecture,
                    )

    def test_support_entries_not_in_quick_entries(self):
        aliases = {
            entry["alias"]
            for entry in SUPPORT_ENTRIES
        }

        self.assertEqual(
            aliases,
            set(SUPPORTING),
        )

    def test_support_templates_do_not_modify_security_state(self):
        for alias, expected in SUPPORTING.items():
            template_dir = (
                ROOT
                / "methods"
                / expected["method"]
                / "templates"
            )

            content = "\n".join(
                path.read_text(
                    encoding="utf-8"
                )
                for path
                in template_dir.rglob("*.tmpl")
            )

            for primitive in FORBIDDEN_MUTATION_PRIMITIVES:
                with self.subTest(
                    alias=alias,
                    primitive=primitive,
                ):
                    self.assertNotIn(
                        primitive,
                        content,
                    )


if __name__ == "__main__":
    unittest.main()
