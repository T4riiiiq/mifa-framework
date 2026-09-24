import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

METHODS = [
    "win32-payload-inspect",
    "win32-file-buffer",
    "win32-base64-buffer",
    "win32-hex-buffer",
    "win32-pe-runtime-info",
    "win32-pe-section-characteristics",
]

FORBIDDEN = [
    "VirtualAllocEx",
    "WriteProcessMemory",
    "CreateRemoteThread",
    "NtCreateThreadEx",
    "QueueUserAPC",
    "PAGE_EXECUTE",
    "WinExec",
    "ShellExecute",
]


class Phase3Batch2MethodTests(unittest.TestCase):
    def test_method_files_and_templates_exist(self):
        for method_id in METHODS:
            method_path = ROOT / "methods" / method_id / "method.json"
            with self.subTest(method=method_id):
                self.assertTrue(method_path.is_file())
                data = json.loads(method_path.read_text(encoding="utf-8"))
                self.assertEqual(data["id"], method_id)
                self.assertEqual(set(data["architectures"]), {"x64", "x86"})
                for source in data["sources"]:
                    self.assertTrue((method_path.parent / source["template"]).is_file())

    def test_x64_x86_presets_exist(self):
        for method_id in METHODS:
            for arch in ("x64", "x86"):
                path = ROOT / "presets" / f"{method_id}-{arch}.json"
                with self.subTest(method=method_id, arch=arch):
                    self.assertTrue(path.is_file())
                    data = json.loads(path.read_text(encoding="utf-8"))
                    self.assertEqual(data["method"], method_id)
                    self.assertEqual(data["architecture"], arch)

    def test_payload_inspector_uses_contract_v2(self):
        data = json.loads(
            (ROOT / "methods" / "win32-payload-inspect" / "method.json").read_text(encoding="utf-8")
        )
        self.assertTrue(data["requires_payload"])
        self.assertEqual(set(data["payload_types"]), {"raw", "text", "json", "pe"})
        contract = data["payload_contract"]
        self.assertEqual(set(contract["transforms"]), {"copy", "base64", "hex"})
        self.assertEqual(contract["default_transform"], "copy")

    def test_decoders_are_local_inspection_only(self):
        for method_id in ("win32-base64-buffer", "win32-hex-buffer"):
            text = (ROOT / "methods" / method_id / "templates" / "main.c.tmpl").read_text(encoding="utf-8")
            with self.subTest(method=method_id):
                self.assertIn("Execution     : no", text)
                for primitive in FORBIDDEN:
                    self.assertNotIn(primitive, text)

    def test_all_new_templates_exclude_remote_execution_primitives(self):
        for method_id in METHODS:
            method_dir = ROOT / "methods" / method_id
            for path in method_dir.glob("templates/*"):
                text = path.read_text(encoding="utf-8")
                with self.subTest(method=method_id, template=path.name):
                    for primitive in FORBIDDEN:
                        self.assertNotIn(primitive, text)

    def test_expected_catalog_growth(self):
        methods = [
            p for p in (ROOT / "methods").iterdir()
            if p.is_dir() and (p / "method.json").is_file()
        ]
        presets = list((ROOT / "presets").glob("*.json"))
        self.assertGreaterEqual(len(methods), 34)
        self.assertGreaterEqual(len(presets), 60)


if __name__ == "__main__":
    unittest.main()
