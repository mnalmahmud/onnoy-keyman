"""Validate generated sources rather than requiring imported platform-base templates."""
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]

class BuildTests(unittest.TestCase):
    def test_source_files_exist(self):
        for rel in ("dist/linux/symbols/onnoy","dist/macos/Onnoy.keylayout",
                    "dist/windows/onnoy.klc","dist/keyman/onnoy.kmn",
                    "dist/web/layout.json"):
            with self.subTest(rel=rel):
                f=ROOT/rel
                self.assertTrue(f.is_file())
                self.assertGreater(f.stat().st_size,100)

    def test_generated_macos_xml(self):
        root=ET.parse(ROOT/"dist/macos/Onnoy.keylayout").getroot()
        self.assertEqual(root.tag,"keyboard")
        self.assertEqual(len(root.findall("./keyMapSet[@id='OnnoyMap']/keyMap")),6)

    def test_no_template_copies_used_by_generator(self):
        from onnoy.backends import linux,windows,macos
        import inspect
        for backend in (linux,windows,macos):
            code=inspect.getsource(backend)
            self.assertNotIn("platform-bases/",code)
            self.assertNotIn('MAC_BASE',code)
            self.assertNotIn('WIN_BASE',code)
