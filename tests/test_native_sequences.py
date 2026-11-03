"""Validate native outputs from the same canonical shortcut table."""
import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

from kalamine.layout import KeyboardLayout, load_layout
from kalamine.utils import Layer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from sequences import altgr_sequences
from apply_native_sequences import apply


class NativeSequences(unittest.TestCase):
    def test_declared_sequences_do_not_displace_kalamine_keys(self):
        layout = KeyboardLayout(load_layout(ROOT / "layout.toml"))
        self.assertEqual(altgr_sequences(ROOT / "layout.toml", layout),
                         {"KeyK": "ক্ষ", "KeyG": "জ্ঞ"})
        self.assertNotIn("ac08", layout.layers[Layer.ALTGR])
        self.assertNotIn("ac05", layout.layers[Layer.ALTGR])

    def test_native_artifacts(self):
        dist = ROOT / "dist"
        if not (dist / "onnoy.klc").exists():
            self.skipTest("Native files not built yet")
        klc = (dist / "onnoy.klc").read_text(encoding="utf-16")
        self.assertIn("K\t6\t0995\t09CD\t09B7", klc)
        self.assertIn("G\t6\t099C\t09CD\t099E", klc)
        self.assertIn("25\tK\t0\t0995\t0996\t-1\t-1\t%%", klc)
        self.assertIn("22\tG\t0\t0997\t0998\t-1\t-1\t%%", klc)
        xml = ET.parse(dist / "onnoy.keylayout")
        keyboard = xml.getroot()
        self.assertEqual(keyboard.attrib["maxout"], "3")
        option = next(m for m in keyboard.iter("keyMap") if m.get("index") == "3")
        outputs = {k.get("code"): k.get("output") for k in option}
        self.assertEqual(outputs["40"], "ক্ষ")
        self.assertEqual(outputs["5"], "জ্ঞ")
        ahk = (dist / "onnoy.ahk").read_text(encoding="utf-8")
        self.assertIn("<^>!SC25::SendInput, {Text}ক্ষ", ahk)
        self.assertIn("<^>!SC22::SendInput, {Text}জ্ঞ", ahk)
        xkb = (dist / "onnoy.xkb_symbols").read_text(encoding="utf-8")
        self.assertIn("{ U0995, U09CD, U09B7 }", xkb)
        self.assertIn("{ U099C, U09CD, U099E }", xkb)


if __name__ == "__main__":
    unittest.main()
