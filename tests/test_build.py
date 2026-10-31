"""Native artifact checks; run after generating platform sources."""
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class BuildTests(unittest.TestCase):
    def test_native_sources_present(self):
        for file in ("dist/linux/symbols/onnoy", "dist/macos/Onnoy.keylayout", "dist/windows/onnoy.klc"):
            with self.subTest(file=file):
                target = ROOT / file
                self.assertTrue(target.exists())
                self.assertGreater(target.stat().st_size, 200)

    def test_macos_native_layout_is_valid_xml(self):
        root = ET.parse(ROOT / "dist/macos/Onnoy.keylayout").getroot()
        self.assertEqual(root.tag, "keyboard")
        self.assertEqual(len(root.findall("./keyMapSet[@id=\'OnnoyMap\']/keyMap")), 6)
        self.assertEqual(len(root.findall("./keyMapSet[@id=\'OnnoyUSBase\']/keyMap")), 5)

    def test_no_app_runtime_in_native_layouts(self):
        for file in ("dist/linux/symbols/onnoy", "dist/windows/onnoy.klc", "dist/macos/Onnoy.keylayout"):
            content = (ROOT / file).read_text(encoding="utf-8")
            self.assertNotIn("keyman", content.lower())

if __name__ == "__main__":
    unittest.main()
