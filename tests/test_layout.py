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

    def test_known_assignments_and_empty_slots(self):
        expected = {
            "E": ["ে", "এ", "ৈ", "ঐ"],
            "I": ["ি", "ই", "ী", "ঈ"],
            "U": ["ু", "উ", "ূ", "ঊ"],
            "O": ["ো", "ও", "ৌ", "ঔ"],
            "F": ["্", "়", None, None],
            "Q": ["ড", "ঢ", "ড়", "ঢ়"],
            "W": ["ট", "ঠ", "ৱ", None],
            "V": ["অ", None, "ৗ", None],
            "G": ["গ", "ঘ", None, None],
            "Y": ["য়", "য", "্য", None],
            "X": ["ষ", "ক্ষ", None, None],
            "Z": ["ং", "ঙ", None, None],
            "SPACE": [" ", " ", "\u200d", "\u200c"],
            "M": ["ম", "ঁ", None, None],
            "N": ["ন", "ণ", "ঞ", None],
            ".": ["।", ">", ".", None],
            "4": ["৪", "৳", "4", "$"],
        }
        for key, values in expected.items():
            with self.subTest(key=key):
                self.assertEqual(KEYS[key], values)
        empty = [sum(KEYS[key][i] is None for key in PHYSICAL) for i in range(4)]
        self.assertEqual(empty, [0, 2, 14, 30])
        self.assertEqual(sum(empty), 46)

    def test_touch_layout_generated_from_source(self):
        import subprocess
        subprocess.run(["python3", "scripts/generate.py", "--check"], cwd=ROOT, check=True)
        touch = json.loads((ROOT / "source/onnoy.keyman-touch-layout").read_text(encoding="utf-8"))
        layers = {layer["id"]: layer for layer in touch["phone"]["layer"]}
        self.assertEqual(set(layers), {"default", "shift", "altgr", "shift_altgr", "numeric"})
        for name, index in (("default", 0), ("shift", 1), ("altgr", 2), ("shift_altgr", 3)):
            rows = layers[name]["row"]
            for keys, row in zip(("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"), rows):
                for key, node in zip(keys, row["key"]):
                    expected = KEYS[key][index]
                    if expected is None:
                        self.assertEqual(node["sp"], 9)
                    else:
                        self.assertEqual(node["id"], ("U_" if len(expected) == 1 else "T_SEQ_") + "_".join("%04X" % ord(c) for c in expected))

    def test_all_keyman_rules_match_json(self):
        source = (ROOT / "source/onnoy.kmn").read_text(encoding="utf-8")
        regex = re.compile(r"^\+ \[(?:(SHIFT) )?(?:(RALT) )?K_([A-Z0-9]+)\] > (nul|U\+[0-9A-F]{4,6}(?: U\+[0-9A-F]{4,6})*)$", re.M)
        found = {}
        for shift, alt, key, output in regex.findall(source):
            index = int(bool(shift)) + int(bool(alt)) * 2
            self.assertNotIn((key, index), found)
            found[(key, index)] = output
        self.assertEqual(len(found), 152)
        for key in list(PHYSICAL) + ["SPACE"]:
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
        self.assertIn("key <SPCE>", xkb)
        self.assertIn("U200D", xkb)
        self.assertIn("39\tSPACE\t0\t0020 0020 0020 200d 200c", klc)
        self.assertIn("09cd", klc)
        self.assertIn("200d", klc)
        compose = (ROOT / "dist/linux/Onnoy.XCompose").read_text(encoding="utf-8")
        self.assertIn('<F13> : "্য"', compose)
        self.assertIn('<F14> : "ক্ষ"', compose)
        self.assertNotIn("জ্ঞ", compose)
        self.assertNotIn("<F15>", compose)
        self.assertIn("F13", xkb)
        self.assertIn("F14", xkb)
        self.assertNotIn("F15", xkb)
        self.assertIn("LIGATURE", klc)
        self.assertIn("X\t1\t0995 09cd 09b7", klc)
        self.assertNotIn("G\t3\t099c 09cd 099e", klc)
        self.assertIn("22\tG\t0\t", klc)
        self.assertIn("Y\t3\t09cd 09af", klc)
        self.assertNotIn(r"\\t", klc)
        self.assertEqual(mac.attrib["maxout"], "3")
        option_map = mac.find(".//keyMap[@index='2']")
        self.assertEqual(next(k.attrib["output"] for k in option_map.findall("key")
                              if k.attrib["code"] == "5"), "")
        self.assertEqual(len(mac.findall(".//keyMap")), 6)
        keymap = mac.find(".//keyMap[@index='0']")
        self.assertIsNotNone(keymap)
        self.assertEqual(next(node.attrib["output"] for node in keymap.findall("key")
                              if node.attrib["code"] == "3"), "্")


if __name__ == "__main__":
    unittest.main()
