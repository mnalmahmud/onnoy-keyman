"""Regression tests for Onnoy's canonical, four-layer character mapping."""
import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = json.loads((ROOT / "layout/onnoy.json").read_text(encoding="utf-8"))
KEYS = LAYOUT["keys"]
LAYERS = ("base", "shift", "altgr", "shift_altgr")
PHYSICAL = "QWERTYUIOP[]ASDFGHJKL;ZXCVBNM1234567890=."
ALL_KEYS = PHYSICAL + " "


class LayoutTests(unittest.TestCase):
    def test_all_keys_have_four_layers(self):
        self.assertEqual(set(KEYS), set(PHYSICAL) | {"SPACE"})
        for key, values in KEYS.items():
            with self.subTest(key=key):
                self.assertEqual(len(values), 4)
                self.assertTrue(all(value is None or
                                    isinstance(value, str) and 1 <= len(value) <= 4
                                    for value in values))

    def test_passthrough_keys_are_in_canonical_source(self):
        self.assertEqual(LAYOUT["passthrough"], {
            "`": ["`", "~"], "-": ["-", "_"], "\\": ["\\", "|"],
            "'": ["'", '"'], ",": [",", "<"], "/": ["/", "?"],
        })

    def test_known_assignments_and_empty_slots(self):
        expected = {
            "Q": ["ড", "ঢ", None, None],
            "W": ["ট", "ঠ", "ৱ", None],
            "E": ["ে", "এ", None, None],
            "R": ["র", "ৰ", None, None],
            "Y": ["ী", "ঈ", None, None],
            "U": ["ু", "উ", None, None],
            "I": ["ি", "ই", None, None],
            "O": ["ো", "ও", None, None],
            "P": ["প", "ঞ", None, None],
            "F": ["ফ", "্", None, None],
            "L": ["ল", "ং", None, None],
            ";": ["ৌ", "ঔ", ";", ":"],
            "Z": ["য", "ঙ", "\u200d", "\u200c"],
            "X": ["ষ", "়", "𑷰", None],
            "V": ["ভ", "অ", None, None],
            "B": ["ব", "ৗ", None, None],
            "N": ["ন", "ণ", None, None],
            "M": ["ম", "ঁ", None, None],
            "[": ["ৈ", "ঐ", "[", "{"],
            "]": ["ূ", "ঊ", "]", "}"],
            "SPACE": [" ", " ", " ", " "],
            ".": ["।", ">", ".", None],
            "4": ["৪", "৳", "4", "$"],
            "=": ["ৃ", "ঋ", "=", "+"],
        }
        for key, values in expected.items():
            with self.subTest(key=key):
                self.assertEqual(KEYS[key], values)
        empty = [sum(KEYS[key][i] is None for key in PHYSICAL) for i in range(4)]
        self.assertEqual(empty, [0, 0, 21, 35])
        self.assertEqual(sum(empty), 56)

    def test_all_native_outputs_have_scalar_keys(self):
        for key, values in KEYS.items():
            for layer, value in enumerate(values):
                with self.subTest(key=key, layer=layer):
                    self.assertTrue(value is None or len(value) == 1)

    def test_normal_space_and_joiners(self):
        self.assertEqual(KEYS["SPACE"], [" ", " ", " ", " "])
        self.assertEqual(KEYS["Z"][2:], ["\\u200d", "\\u200c"])

    def test_generated_native_layouts_contain_expected_characters(self):
        xkb = (ROOT / "dist/linux/symbols/onnoy").read_text(encoding="utf-8")
        klc = (ROOT / "dist/windows/onnoy.klc").read_text(encoding="utf-8")
        mac = ET.parse(ROOT / "dist/macos/Onnoy.keylayout").getroot()
        self.assertIn("U09CD", xkb)
        self.assertIn("key <AE12>", xkb)
        self.assertIn("U09B0", xkb)
        self.assertIn("U09F0", xkb)
        self.assertIn("U200C", xkb)
        self.assertIn("key <SPCE>", xkb)
        self.assertIn("U200D", xkb)
        self.assertRegex(xkb, r"key <AB01>.*U200D, U200C")
        self.assertRegex(xkb, r"key <SPCE>.*space, space, space, space")
        self.assertIn("39\tSPACE\t0\t0020 0020 0020 0020 0020", klc)
        self.assertIn("2C\tZ\t0\t09af 0999 -1 200d 200c", klc)
        self.assertIn("09cd", klc)
        self.assertIn("X\t3\td807 ddf0", klc)
        self.assertIn("U11DF0", xkb)
        self.assertIn("200d", klc)
        self.assertNotIn("F13", xkb)
        self.assertIn("U200D, U200C", xkb)
        self.assertNotIn("Onnoy.XCompose", xkb)
        self.assertIn("LIGATURE", klc)
        self.assertIn("1A\tOEM_4\t0\t09c8 0990 -1 005b 007b", klc)
        self.assertIn("1B\tOEM_6\t0\t09c2 098a -1 005d 007d", klc)
        self.assertIn("27\tOEM_1\t0\t09cc 0994 -1 003b 003a", klc)
        self.assertIn("18\tO\t0\t09cb 0993 -1 -1 -1", klc)
        self.assertIn("0D\tOEM_PLUS\t0\t09c3 098b -1 003d 002b", klc)
        self.assertIn("13\tR\t0\t09b0 09f0 -1 -1 -1", klc)
        self.assertIn("21\tF\t0\t09ab 09cd -1 -1 -1", klc)
        self.assertIn("2F\tV\t0\t09ad 0985 -1 -1 -1", klc)
        self.assertIn("30\tB\t0\t09ac 09d7 -1 -1 -1", klc)
        self.assertNotIn("G\t3\t099c 09cd 099e", klc)
        self.assertIn("22\tG\t0\t", klc)
        self.assertNotIn(r"\\t", klc)
        self.assertEqual(mac.attrib["maxout"], "1")
        option_map = mac.find(".//keyMap[@index='2']")
        self.assertEqual(next(k.attrib["output"] for k in option_map.findall("key")
                              if k.attrib["code"] == "5"), "")
        self.assertEqual(len(mac.findall(".//keyMap")), 6)
        for index, char in ((2, "\u200d"), (3, "\u200c")):
            layer = mac.find(f".//keyMap[@index='{index}']")
            self.assertEqual(next(k.attrib["output"] for k in layer.findall("key") if k.attrib["code"] == "6"), char)
            self.assertEqual(next(k.attrib["output"] for k in layer.findall("key") if k.attrib["code"] == "49"), " ")
        keymap = mac.find(".//keyMap[@index='0']")
        self.assertIsNotNone(keymap)
        self.assertEqual(next(node.attrib["output"] for node in keymap.findall("key")
                              if node.attrib["code"] == "33"), "ৈ")
        self.assertEqual(next(node.attrib["output"] for node in keymap.findall("key")
                              if node.attrib["code"] == "41"), "ৌ")
        self.assertEqual(next(node.attrib["output"] for node in keymap.findall("key")
                              if node.attrib["code"] == "7"), "ষ")
        self.assertEqual(next(node.attrib["output"] for node in keymap.findall("key")
                              if node.attrib["code"] == "24"), "ৃ")
        self.assertEqual(next(node.attrib["output"] for node in keymap.findall("key")
                              if node.attrib["code"] == "15"), "র")
        shifted_map = mac.find(".//keyMap[@index='1']")
        self.assertEqual(next(node.attrib["output"] for node in shifted_map.findall("key")
                              if node.attrib["code"] == "24"), "ঋ")
        self.assertEqual(next(node.attrib["output"] for node in shifted_map.findall("key")
                              if node.attrib["code"] == "15"), "ৰ")


if __name__ == "__main__":
    unittest.main()
