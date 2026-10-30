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
            "Z": ["য", "ঙ", None, None],
            "X": ["ষ", "়", "𑷰", None],
            "V": ["ভ", "ৗ", None, None],
            "B": ["ব", "অ", None, None],
            "N": ["ন", "ণ", None, None],
            "M": ["ম", "ঁ", None, None],
            "[": ["ৈ", "ঐ", "[", "{"],
            "]": ["ূ", "ঊ", "]", "}"],
            "SPACE": [" ", " ", "\u200d", "\u200c"],
            ".": ["।", ">", ".", None],
            "4": ["৪", "৳", "4", "$"],
            "=": ["ৃ", "ঋ", "=", "+"],
        }
        for key, values in expected.items():
            with self.subTest(key=key):
                self.assertEqual(KEYS[key], values)
        empty = [sum(KEYS[key][i] is None for key in PHYSICAL) for i in range(4)]
        self.assertEqual(empty, [0, 0, 22, 36])
        self.assertEqual(sum(empty), 58)

    def test_touch_layout_generated_from_source(self):
        import subprocess
        subprocess.run(["python3", "scripts/generate.py", "--check"], cwd=ROOT, check=True)
        touch = json.loads((ROOT / "source/onnoy.keyman-touch-layout").read_text(encoding="utf-8"))
        layers = {layer["id"]: layer for layer in touch["phone"]["layer"]}
        self.assertEqual(set(layers), {"default", "shift", "altgr", "shift_altgr", "numeric"})
        for name, index in (("default", 0), ("shift", 1), ("altgr", 2), ("shift_altgr", 3)):
            rows = layers[name]["row"]
            for keys, row in zip(("QWERTYUIOP[]", "ASDFGHJKL;", "ZXCVBNM"), rows):
                for key, node in zip(keys, row["key"]):
                    expected = KEYS[key][index]
                    if expected is None:
                        self.assertEqual(node["sp"], 9)
                    else:
                        self.assertEqual(node["id"], ("U_" if len(expected) == 1 else "T_SEQ_") + "_".join("%04X" % ord(c) for c in expected))

    def test_touch_ri_pair_accessible_without_equals_key(self):
        touch = json.loads((ROOT / "source/onnoy.keyman-touch-layout").read_text(encoding="utf-8"))
        layer = next(layer for layer in touch["phone"]["layer"] if layer["id"] == "default")
        key_r = layer["row"][0]["key"][3]
        subkeys = {subkey["id"] for subkey in key_r["sk"]}
        self.assertTrue({"U_09C3", "U_098B", "U_09F0"} <= subkeys)

    def test_all_keyman_rules_match_json(self):
        source = (ROOT / "source/onnoy.kmn").read_text(encoding="utf-8")
        regex = re.compile(r"^\+ \[(?:(SHIFT) )?(?:(RALT) )?K_([A-Z0-9]+)\] > (nul|U\+[0-9A-F]{4,6}(?: U\+[0-9A-F]{4,6})*)$", re.M)
        found = {}
        for shift, alt, key, output in regex.findall(source):
            index = int(bool(shift)) + int(bool(alt)) * 2
            self.assertNotIn((key, index), found)
            found[(key, index)] = output
        self.assertEqual(len(found), 168)
        for key in list(PHYSICAL) + ["SPACE"]:
            for index in range(4):
                output = KEYS[key][index]
                expected = "nul" if output is None else " ".join("U+%04X" % ord(c) for c in output)
                with self.subTest(key=key, layer=LAYERS[index]):
                    self.assertEqual(found[({".": "PERIOD", "[": "LBRKT", "]": "RBRKT", ";": "COLON", "=": "EQUAL"}.get(key, key), index)], expected)

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
        self.assertIn("39\tSPACE\t0\t0020 0020 0020 200d 200c", klc)
        self.assertIn("09cd", klc)
        self.assertIn("X\t3\td807 ddf0", klc)
        self.assertIn("U11DF0", xkb)
        self.assertIn("200d", klc)
        compose = (ROOT / "dist/linux/Onnoy.XCompose").read_text(encoding="utf-8")
        self.assertNotIn("<F13>", compose)
        self.assertNotIn("F13", xkb)
        self.assertIn("LIGATURE", klc)
        self.assertIn("1A\tOEM_4\t0\t09c8 0990 -1 005b 007b", klc)
        self.assertIn("1B\tOEM_6\t0\t09c2 098a -1 005d 007d", klc)
        self.assertIn("27\tOEM_1\t0\t09cc 0994 -1 003b 003a", klc)
        self.assertIn("18\tO\t0\t09cb 0993 -1 -1 -1", klc)
        self.assertIn("0D\tOEM_PLUS\t0\t09c3 098b -1 003d 002b", klc)
        self.assertIn("13\tR\t0\t09b0 09f0 -1 -1 -1", klc)
        self.assertIn("21\tF\t0\t09ab 09cd -1 -1 -1", klc)
        self.assertNotIn("G\t3\t099c 09cd 099e", klc)
        self.assertIn("22\tG\t0\t", klc)
        self.assertNotIn(r"\\t", klc)
        self.assertEqual(mac.attrib["maxout"], "1")
        option_map = mac.find(".//keyMap[@index='2']")
        self.assertEqual(next(k.attrib["output"] for k in option_map.findall("key")
                              if k.attrib["code"] == "5"), "")
        self.assertEqual(len(mac.findall(".//keyMap")), 6)
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
