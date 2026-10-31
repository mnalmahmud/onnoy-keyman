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
        self.assertEqual(set(KEYS), set(PHYSICAL))
        for key, values in KEYS.items():
            with self.subTest(key=key):
                self.assertEqual(len(values), 4)
                self.assertTrue(all(value is None or
                                    isinstance(value, str) and 1 <= len(value) <= 4
                                    for value in values))

    def test_passthrough_keys_are_in_canonical_source(self):
        self.assertEqual(LAYOUT["passthrough"], {
            "'": ["'", '"', "\u200d", "\u200c"], "/": ["্", "?", "/", None],
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
            "A": ["া", "আ", None, None],
            "H": ["হ", "ঃ", "ঽ", None],
            "F": ["ফ", None, None, None],
            "L": ["ল", "ং", None, None],
            ";": ["ৌ", "ঔ", ";", ":"],
            "Z": ["য", "ঙ", None, None],
            "S": ["স", "ষ", None, None],
            "X": ["শ", "়", "𑷰", None],
            "V": ["ভ", "অ", None, None],
            "B": ["ব", "ৗ", None, None],
            "N": ["ন", "ণ", None, None],
            "M": ["ম", "ঁ", None, None],
            "[": ["ৈ", "ঐ", "[", "{"],
            "]": ["ূ", "ঊ", "]", "}"],
            ".": ["।", ">", ".", None],
            "4": ["৪", "৳", "4", "$"],
            "=": ["ৃ", "ঋ", "=", "+"],
        }
        for key, values in expected.items():
            with self.subTest(key=key):
                self.assertEqual(KEYS[key], values)
        empty = [sum(KEYS[key][i] is None for key in PHYSICAL) for i in range(4)]
        self.assertEqual(empty, [0, 1, 22, 36])
        self.assertEqual(sum(empty), 59)

    def test_all_native_outputs_have_scalar_keys(self):
        for key, values in KEYS.items():
            for layer, value in enumerate(values):
                with self.subTest(key=key, layer=layer):
                    self.assertTrue(value is None or len(value) == 1)

    def test_normal_space_and_joiners(self):
        self.assertNotIn("SPACE", KEYS)
        for key in ("`", "-", "\\", ","):
            self.assertNotIn(key, LAYOUT["passthrough"])
        self.assertEqual(KEYS["Z"][2:], [None, None])
        self.assertNotIn("`", LAYOUT["passthrough"])
        self.assertEqual(LAYOUT["passthrough"]["\'"][2:], ["\u200d", "\u200c"])
        self.assertEqual(LAYOUT["passthrough"]["/"], ["্", "?", "/", None])
        self.assertIsNone(KEYS["F"][1])

    def test_generated_native_layouts_contain_expected_characters(self):
        xkb = (ROOT / "dist/linux/symbols/onnoy").read_text(encoding="utf-8")
        klc = (ROOT / "dist/windows/onnoy.klc").read_text(encoding="utf-8")
        mac = ET.parse(ROOT / "dist/macos/Onnoy.keylayout").getroot()
        self.assertIn("U09CD", xkb)
        self.assertIn("key <AE12>", xkb)
        self.assertIn("U09B0", xkb)
        self.assertRegex(xkb, r"key <AC01>.*U09BE, U0986, VoidSymbol")
        self.assertRegex(xkb, r"key <AC06>.*U09B9, U0983, U09BD")
        self.assertRegex(xkb, r"key <AC02>.*U09B8, U09B7")
        self.assertRegex(xkb, r"key <AB02>.*U09B6, U09BC")
        self.assertIn("U09F0", xkb)
        self.assertIn("U200C", xkb)
        self.assertNotIn("key <SPCE>", xkb)
        self.assertNotIn("key <AE11>", xkb)
        self.assertNotIn("key <BKSL>", xkb)
        self.assertNotIn("key <AB08>", xkb)
        self.assertIn("U200D", xkb)
        self.assertRegex(xkb, r"key <AC11>.*U200D, U200C")
        self.assertNotIn("key <TLDE>", xkb)
        self.assertRegex(xkb, r"key <AB10>.*U09CD, U003F, U002F, VoidSymbol")
        self.assertRegex(xkb, r"key <AB01>.*VoidSymbol, VoidSymbol")
        self.assertIn('include "us(basic)"', xkb)
        self.assertIn("39\tSPACE\t0\t0020 0020 0020 0020 0020", klc)
        self.assertIn("2C\tZ\t0\t09af 0999 -1 -1 -1", klc)
        self.assertIn("1E\tA\t0\t09be 0986 -1 -1 -1", klc)
        self.assertIn("23\tH\t0\t09b9 0983 -1 09bd -1", klc)
        self.assertIn("1F\tS\t0\t09b8 09b7 -1 -1 -1", klc)
        self.assertIn("2D\tX\t0\t09b6 09bc -1 %% -1", klc)
        self.assertIn("35\tOEM_2\t0\t09cd 003f -1 002f -1", klc)
        self.assertIn("29\tOEM_3\t0\t0060 007e -1 -1 -1", klc)
        self.assertIn("28\tOEM_7\t0\t0027 0022 -1 200d 200c", klc)
        self.assertIn("09cd", klc)
        self.assertIn("X\t3\td807 ddf0", klc)
        self.assertIn("U11DF0", xkb)
        self.assertIn("200d", klc)
        self.assertNotIn("F13", xkb)
        self.assertIn("U200D, U200C", xkb)
        self.assertNotIn("Onnoy.XCompose", xkb)
        self.assertIn("LIGATURE", klc)
        self.assertIn("1A\tOEM_4\t0\t09c8 0990 001b 005b 007b", klc)
        self.assertIn("1B\tOEM_6\t0\t09c2 098a 001d 005d 007d", klc)
        self.assertIn("27\tOEM_1\t0\t09cc 0994 -1 003b 003a", klc)
        self.assertIn("18\tO\t0\t09cb 0993 -1 -1 -1", klc)
        self.assertIn("0D\tOEM_PLUS\t0\t09c3 098b -1 003d 002b", klc)
        self.assertIn("13\tR\t0\t09b0 09f0 -1 -1 -1", klc)
        self.assertIn("21\tF\t0\t09ab -1 -1 -1 -1", klc)
        self.assertIn("2F\tV\t0\t09ad 0985 -1 -1 -1", klc)
        self.assertIn("30\tB\t0\t09ac 09d7 -1 -1 -1", klc)
        self.assertNotIn("G\t3\t099c 09cd 099e", klc)
        self.assertIn("22\tG\t0\t", klc)
        self.assertNotIn(r"\\t", klc)
        self.assertEqual(mac.attrib["maxout"], "1")
        option_map = mac.find(".//keyMap[@index='2']")
        self.assertEqual(next(k.attrib["output"] for k in option_map.findall("key")
                              if k.attrib["code"] == "5"), "")
        self.assertEqual(len(mac.findall(".//keyMap")), 11)
        self.assertEqual(len(mac.findall("./keyMapSet[@id=\'OnnoyMap\']/keyMap")), 6)
        self.assertEqual(len(mac.findall("./keyMapSet[@id=\'OnnoyUSBase\']/keyMap")), 5)
        for index, char in ((2, "\u200d"), (3, "\u200c")):
            layer = mac.find(f".//keyMap[@index='{index}']")
            self.assertEqual(next(k.attrib["output"] for k in layer.findall("key") if k.attrib["code"] == "39"), char)
            self.assertFalse(any(k.attrib["code"] == "50" for k in layer.findall("key")))
            self.assertFalse(any(k.attrib["code"] == "49" for k in layer.findall("key")))
            self.assertEqual(next(k.attrib["output"] for k in layer.findall("key") if k.attrib["code"] == "6"), "")
        # Every sparse Onnoy map inherits the corresponding native reference.
        custom = mac.find("./keyMapSet[@id='OnnoyMap']")
        inherited = mac.find("./keyMapSet[@id='OnnoyUSBase']")
        for i in range(6):
            override = custom.find(f"keyMap[@index='{i}']")
            self.assertEqual(override.attrib["baseMapSet"], "OnnoyUSBase")
            self.assertEqual(override.attrib["baseIndex"], str(min(i, 4)))
        # Command and Control share the same native ASCII shortcut map.
        self.assertIsNone(inherited.find("keyMap[@index='5']"))
        cmd = inherited.find("keyMap[@index='4']")
        self.assertEqual(next(k.attrib["output"] for k in cmd.findall("key") if k.attrib["code"] == "15"), "r")
        self.assertEqual(next(k.attrib["output"] for k in cmd.findall("key") if k.attrib["code"] == "0"), "a")
        self.assertEqual(next(k.attrib["output"] for k in cmd.findall("key") if k.attrib["code"] == "14"), "e")
        self.assertEqual(next(k.attrib["output"] for k in cmd.findall("key") if k.attrib["code"] == "34"), "i")
        defined_actions = {k.attrib["id"] for k in mac.findall("./actions/action")}
        for key in mac.findall(".//keyMap/key"):
            if "action" in key.attrib:
                self.assertIn(key.attrib["action"], defined_actions)
        self.assertEqual(next(k.attrib["output"] for k in cmd.findall("key") if k.attrib["code"] == "50"), "`")
        ordinary = inherited.find("keyMap[@index='0']")
        shifted = inherited.find("keyMap[@index='1']")
        option_base = inherited.find("keyMap[@index='2']")
        get = lambda layer, code: next(k.attrib for k in layer.findall("key") if k.attrib["code"] == str(code))
        self.assertEqual(get(ordinary, 27)["output"], "-")
        self.assertEqual(get(shifted, 27)["output"], "_")
        self.assertEqual(get(ordinary, 43)["output"], ",")
        self.assertEqual(get(shifted, 43)["output"], "<")
        self.assertEqual(get(ordinary, 50)["output"], "`")
        self.assertEqual(get(shifted, 50)["output"], "~")
        self.assertEqual(get(option_base, 50)["action"], "1")
        self.assertEqual(get(option_base, 49)["output"], " ")
        self.assertTrue(any(k.attrib["code"] == "39" for k in custom.find("keyMap[@index='2']").findall("key")))
        self.assertFalse(any(k.attrib["code"] == "39" for k in custom.find("keyMap[@index='4']").findall("key")))
        self.assertIn("53\tDECIMAL", klc)
        self.assertIn("56\tOEM_102", klc)
        self.assertIn("2B\tOEM_5\t0\t005c 007c 001c -1 -1", klc)
        self.assertIn("33\tOEM_COMMA\t0\t002c 003c -1 -1 -1", klc)
        base = mac.find(".//keyMap[@index='0']")
        shift = mac.find(".//keyMap[@index='1']")
        option = mac.find(".//keyMap[@index='2']")
        self.assertEqual(next(k.attrib["output"] for k in base.findall("key") if k.attrib["code"] == "44"), "্")
        self.assertEqual(next(k.attrib["output"] for k in shift.findall("key") if k.attrib["code"] == "44"), "?")
        self.assertEqual(next(k.attrib["output"] for k in option.findall("key") if k.attrib["code"] == "44"), "/")
        self.assertEqual(next(k.attrib["output"] for k in shift.findall("key") if k.attrib["code"] == "3"), "")
        keymap = mac.find(".//keyMap[@index='0']")
        self.assertIsNotNone(keymap)
        self.assertEqual(next(node.attrib["output"] for node in keymap.findall("key")
                              if node.attrib["code"] == "33"), "ৈ")
        self.assertEqual(next(node.attrib["output"] for node in keymap.findall("key")
                              if node.attrib["code"] == "41"), "ৌ")
        self.assertEqual(next(node.attrib["output"] for node in keymap.findall("key")
                              if node.attrib["code"] == "7"), "শ")
        self.assertEqual(next(node.attrib["output"] for node in keymap.findall("key")
                              if node.attrib["code"] == "24"), "ৃ")
        self.assertEqual(next(node.attrib["output"] for node in keymap.findall("key")
                              if node.attrib["code"] == "15"), "র")
        shifted_map = mac.find(".//keyMap[@index='1']")
        self.assertEqual(next(node.attrib["output"] for node in shifted_map.findall("key")
                              if node.attrib["code"] == "1"), "ষ")
        altgr_map = mac.find("./keyMapSet[@id='OnnoyMap']/keyMap[@index='2']")
        self.assertEqual(next(node.attrib["output"] for node in altgr_map.findall("key")
                              if node.attrib["code"] == "4"), "ঽ")
        self.assertEqual(next(node.attrib["output"] for node in altgr_map.findall("key")
                              if node.attrib["code"] == "0"), "")
        self.assertEqual(next(node.attrib["output"] for node in shifted_map.findall("key")
                              if node.attrib["code"] == "24"), "ঋ")
        self.assertEqual(next(node.attrib["output"] for node in shifted_map.findall("key")
                              if node.attrib["code"] == "15"), "ৰ")


if __name__ == "__main__":
    unittest.main()
