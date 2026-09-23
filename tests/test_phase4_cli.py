import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from core.catalog import MethodCatalog
from core.presets import PresetStore
from core.ui import TerminalUI
from core.workflows import alias_map, find_preset, resolve_target


ROOT = Path(__file__).resolve().parents[1]


class Phase4CliTests(unittest.TestCase):
    def setUp(self):
        self.catalog = MethodCatalog(ROOT / "methods")
        self.presets = PresetStore(ROOT / "presets")

    def test_quick_aliases_resolve(self):
        aliases = alias_map()
        self.assertEqual(aliases["peinfo"], "win32-pe-runtime-info")
        self.assertEqual(aliases["filebuf"], "win32-file-buffer")

    def test_direct_method_id_resolves(self):
        self.assertEqual(
            resolve_target("win32-pe-runtime-info", self.catalog),
            "win32-pe-runtime-info",
        )

    def test_unknown_target_rejected(self):
        self.assertIsNone(resolve_target("not-a-real-method", self.catalog))

    def test_find_x64_quick_preset(self):
        preset = find_preset(self.presets, "win32-file-buffer", "x64")
        self.assertIsNotNone(preset)
        self.assertEqual(preset.get("architecture"), "x64")

    def test_ui_can_disable_ansi(self):
        ui = TerminalUI(enabled=False)
        self.assertEqual(ui.success("[+]"), "[+]")
        self.assertNotIn("\033[", ui.accent("Mifa"))

    def test_banner_renders_without_ansi(self):
        ui = TerminalUI(enabled=False)
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            ui.banner("1.2.0")
        output = buffer.getvalue()
        self.assertIn("M I F A", output)
        self.assertIn("Windows Research Framework", output)
        self.assertNotIn("\033[", output)


if __name__ == "__main__":
    unittest.main()
