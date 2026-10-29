"""Regression tests for Onnoy's canonical, four-layer character mapping."""
import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEYS = json.loads((ROOT / "layout/onnoy.json").read_text(encoding="utf-8"))["keys"]
LAYERS = ("base", "shift", "altgr", "shift_altgr")
PHYSICAL = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890."


class LayoutTests(unittest.TestCase):
    def test_all_keys_have_four_layers(self):
        self.assertEqual(set(KEYS), set(PHYSICAL))
        for key, values in KEYS.items():
            with self.subTest(key=key):
                self.assertEqual(len(values), 4)
                self.assertTrue(all(value is None or
                                    isinstance(value, str) and 1 <= len(value) <= 4
                                    for value in values))

    def test_known_assignments_and_empty_slots(self):
        expected = {
            "E": ["ে", "এ", "ৈ", "ঐ"],
            "I": ["ি", "ই", "ী", "ঈ"],
            "U": ["ু", "উ", "ূ", "ঊ"],
            "O": ["ো", "ও", "ৌ", "ঔ"],
            "F": ["্", "়", None, None],
            "Q": ["ড", "ঢ", "ড়", "ঢ়"],
            "W": ["ট", "ঠ", None, None],
            "G": ["গ", "ঘ", "জ্ঞ", None],
            "Y": ["য", "য়", "্য", None],
            "X": ["ষ", "ক্ষ", None, None],
            "Z": ["ঞ", "ঙ", "\u200c", "\u200d"],
            ".": ["।", ">", ".", None],
            "4": ["৪", "৳", "4", "$"],
        }
        for key, values in expected.items():
            with self.subTest(key=key):
                self.assertEqual(KEYS[key], values)
        empty = [sum(KEYS[key][i] is None for key in PHYSICAL) for i in range(4)]
        self.assertEqual(empty, [0, 1, 13, 29])
        self.assertEqual(sum(empty), 43)

    def test_all_keyman_rules_match_json(self):
        source = (ROOT / "source/onnoy.kmn").read_text(encoding="utf-8")
        regex = re.compile(r"^\+ \[(?:(SHIFT) )?(?:(RALT) )?K_([A-Z0-9]+)\] > (nul|U\+[0-9A-F]{4,6}(?: U\+[0-9A-F]{4,6})*)$", re.M)
        found = {}
        for shift, alt, key, output in regex.findall(source):
            index = int(bool(shift)) + int(bool(alt)) * 2
            self.assertNotIn((key, index), found)
            found[(key, index)] = output
        self.assertEqual(len(found), 148)
        for key in PHYSICAL:
            for index in range(4):
                output = KEYS[key][index]
                expected = "nul" if output is None else " ".join("U+%04X" % ord(c) for c in output)
                with self.subTest(key=key, layer=LAYERS[index]):
                    self.assertEqual(found[("PERIOD" if key == "." else key, index)], expected)

    def test_generated_native_layouts_contain_expected_characters(self):
        xkb = (ROOT / "dist/linux/symbols/onnoy").read_text(encoding="utf-8")
        klc = (ROOT / "dist/windows/onnoy.klc").read_text(encoding="utf-8")
        mac = ET.parse(ROOT / "dist/macos/Onnoy.keylayout").getroot()
        self.assertIn("U09CD", xkb)
        self.assertIn("U200C", xkb)
        self.assertIn("09cd", klc)
        self.assertIn("200d", klc)
        compose = (ROOT / "dist/linux/Onnoy.XCompose").read_text(encoding="utf-8")
        self.assertIn('<F13> : "জ্ঞ"', compose)
        self.assertIn('<F14> : "্য"', compose)
        self.assertIn('<F15> : "ক্ষ"', compose)
        self.assertIn("F13", xkb)
        self.assertIn("F14", xkb)
        self.assertIn("F15", xkb)
        self.assertIn("LIGATURE", klc)
        self.assertIn("X\\t1\\t0995 09cd 09b7", klc)
        self.assertIn("G\\t3\\t099c 09cd 099e", klc)
        self.assertIn("Y\\t3\\t09cd 09af", klc)
        self.assertEqual(mac.attrib["maxout"], "3")
        self.assertEqual(len(mac.findall(".//keyMap")), 6)
        keymap = mac.find(".//keyMap[@index='0']")
        self.assertIsNotNone(keymap)
        self.assertEqual(next(node.attrib["output"] for node in keymap.findall("key")
                              if node.attrib["code"] == "3"), "্")


if __name__ == "__main__":
    unittest.main()
