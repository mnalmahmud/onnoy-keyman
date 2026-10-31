"""Regression tests for Onnoy's canonical layout and native platform exports."""
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = json.loads((ROOT / "layout/onnoy.json").read_text(encoding="utf-8"))
KEYS = LAYOUT["keys"]
PHYSICAL = "QWERTYUIOP[]ASDFGHJKL;ZXCVBNM1234567890=."


class LayoutTests(unittest.TestCase):
    def test_canonical_layers_and_us_inheritance(self):
        self.assertEqual(LAYOUT["layers"], ["base", "shift", "altgr", "shift_altgr"])
        self.assertEqual(set(KEYS), set(PHYSICAL) - {"="})
        for key, values in KEYS.items():
            with self.subTest(key=key):
                self.assertEqual(len(values), 4)
                self.assertTrue(all(v is None or isinstance(v, str) and len(v) == 1
                                    for v in values))
        self.assertEqual(LAYOUT["passthrough"], {
            "'": ["'", '"', None, None],
            "/": ["্", "?", "/", None],
            ",": [",", "<", "়", None],
        })
        self.assertNotIn("SPACE", KEYS)
        for key in (chr(96), "-", "\\"):
            self.assertNotIn(key, LAYOUT["passthrough"])

    def test_redesigned_assignments(self):
        expected = {
            "Q": ["দ", "ধ", None, None], "W": ["ূ", "ঊ", "ৱ", None],
            "E": ["ে", "এ", None, None], "R": ["র", "ড়", None, None],
            "T": ["ট", "ঠ", "ৎ", None], "Y": ["ী", "ঈ", "য়", None],
            "U": ["ু", "উ", None, None], "I": ["ি", "ই", None, None],
            "O": ["ো", "ও", None, None], "P": ["প", "ফ", None, None],
            "A": ["া", "আ", None, None], "S": ["স", "ষ", None, None],
            "D": ["ড", "ঢ", None, None], "F": ["ত", "থ", None, None],
            "G": ["গ", "ঘ", None, None], "H": ["হ", "ঃ", None, None],
            "J": ["জ", "ঝ", None, None], "K": ["ক", "খ", None, None],
            "L": ["ল", "ঁ", None, None], "Z": ["য", None, None, None],
            "X": ["শ", "ঢ়", None, None], "C": ["চ", "ছ", None, None],
            "V": ["অ", "ৗ", None, None], "B": ["ব", "ভ", None, None],
            "N": ["ন", "ণ", "ঞ", None], "M": ["ম", "ঙ", "ং", "𑷰"],
            "[": ["ৈ", "ঐ", "[", "{"], "]": ["ৌ", "ঔ", "]", "}"],
            ";": ["ৃ", "ঋ", ";", ":"], ".": ["।", ">", ".", None],
            "4": ["৪", "৳", "4", "$"],
        }
        for key, values in expected.items():
            with self.subTest(key=key):
                self.assertEqual(KEYS[key], values)
        self.assertEqual(sum(v == "য়" for vs in KEYS.values() for v in vs), 1)
        self.assertEqual(sum(v == "ঢ়" for vs in KEYS.values() for v in vs), 1)
        for ch in ("ঞ", "ঁ", "ং", "ঙ", "𑷰", "়", "্"):
            self.assertEqual(sum(v == ch for vs in (KEYS | LAYOUT["passthrough"]).values() for v in vs), 1)
        self.assertNotIn("\u200d", json.dumps(LAYOUT, ensure_ascii=False))
        self.assertNotIn("\u200c", json.dumps(LAYOUT, ensure_ascii=False))
        self.assertNotIn("ৰ", json.dumps(LAYOUT, ensure_ascii=False))
        self.assertNotIn("ঽ", json.dumps(LAYOUT, ensure_ascii=False))

    def test_linux_symbols(self):
        xkb = (ROOT / "dist/linux/symbols/onnoy").read_text(encoding="utf-8")
        self.assertIn('include "us(basic)"', xkb)
        self.assertIn('include "level3(ralt_switch)"', xkb)
        for key in ("AE12", "AE11", "BKSL", "TLDE", "SPCE"):
            self.assertNotIn("key <" + key + ">", xkb)
        for regex in (
            r"key <AC10>.*U09C3, U098B, U003B, U003A",
            r"key <AD12>.*U09CC, U0994, U005D, U007D",
            r"key <AB08>.*U002C, U003C, U09BC, VoidSymbol",
            r"key <AB09>.*U0964, U003E, U002E",
            r"key <AC04>.*U09A4, U09A5",
            r"key <AD01>.*U09A6, U09A7",
            r"key <AC03>.*U09A1, U09A2",
            r"key <AD05>.*U099F, U09A0, U09CE",
            r"key <AD06>.*U09C0, U0988, U09DF",
            r"key <AB01>.*U09AF, VoidSymbol",
            r"key <AD04>.*U09B0, U09DC, VoidSymbol",
            r"key <AB02>.*U09B6, U09DD",
            r"key <AC07>.*U099C, U099D, VoidSymbol",
            r"key <AB06>.*U09A8, U09A3, U099E, VoidSymbol",
            r"key <AB07>.*U09AE, U0999, U0982, U11DF0",
            r"key <AC09>.*U09B2, U0981, VoidSymbol",
            r"key <AC11>.*U0027, U0022, VoidSymbol, VoidSymbol",
        ):
            with self.subTest(regex=regex):
                self.assertRegex(xkb, regex)
        for char in ("U09DF", "U09F1", "U09CD"):
            self.assertIn(char, xkb)
        for char in ("U09F0", "U09BD", "U200D", "U200C", "Onnoy.XCompose", "F13"):
            self.assertNotIn(char, xkb)

    def test_windows_klc(self):
        klc = (ROOT / "dist/windows/onnoy.klc").read_text(encoding="utf-8")
        for line in (
            "0D\tOEM_PLUS\t0\t003d 002b -1 -1 -1",
            "27\tOEM_1\t0\t09c3 098b -1 003b 003a",
            "33\tOEM_COMMA\t0\t002c 003c -1 09bc -1",
            "34\tOEM_PERIOD\t0\t0964 003e -1 002e -1",
            "13\tR\t0\t09b0 09dc -1 -1 -1",
            "2D\tX\t0\t09b6 09dd -1 -1 -1",
            "10\tQ\t0\t09a6 09a7 -1 -1 -1",
            "20\tD\t0\t09a1 09a2 -1 -1 -1",
            "14\tT\t0\t099f 09a0 -1 09ce -1",
            "21\tF\t0\t09a4 09a5 -1 -1 -1",
            "15\tY\t0\t09c0 0988 -1 09df -1",
            "2C\tZ\t0\t09af -1 -1 -1 -1",
            "2F\tV\t0\t0985 09d7 -1 -1 -1",
            "30\tB\t0\t09ac 09ad -1 -1 -1",
            "24\tJ\t0\t099c 099d -1 -1 -1",
            "26\tL\t0\t09b2 0981 -1 -1 -1",
            "31\tN\t0\t09a8 09a3 -1 099e -1",
            "32\tM\t0\t09ae 0999 -1 0982 %%",
            "28\tOEM_7\t0\t0027 0022 -1 -1 -1",
            "39\tSPACE\t0\t0020 0020 0020 0020 0020",
            "M\t4\td807 ddf0",
        ):
            with self.subTest(line=line):
                self.assertIn(line, klc)

    def test_macos_inheritance_and_overrides(self):
        root = ET.parse(ROOT / "dist/macos/Onnoy.keylayout").getroot()
        self.assertEqual(root.attrib["maxout"], "1")
        custom = root.find("./keyMapSet[@id='OnnoyMap']")
        inherited = root.find("./keyMapSet[@id='OnnoyUSBase']")
        self.assertEqual(len(custom.findall("keyMap")), 6)
        self.assertEqual(len(inherited.findall("keyMap")), 5)
        def key(layer, code):
            return next(n.attrib for n in layer.findall("key")
                        if n.attrib["code"] == str(code))
        for i in range(6):
            layer = custom.find(f"keyMap[@index='{i}']")
            self.assertEqual(layer.attrib["baseMapSet"], "OnnoyUSBase")
            self.assertEqual(layer.attrib["baseIndex"], str(min(i, 4)))
            self.assertFalse(any(n.attrib["code"] == "24" for n in layer.findall("key")))
        for i, expected in enumerate(("=", "+", "≠", "±")):
            self.assertEqual(key(inherited.find(f"keyMap[@index='{i}']"), 24)["output"], expected)
        self.assertEqual(key(inherited.find("keyMap[@index='4']"), 24)["output"], "=")
        self.assertEqual(key(inherited.find("keyMap[@index='4']"), 15)["output"], "r")
        for i, code, expected in (
            (0, 12, "দ"), (1, 12, "ধ"), (0, 2, "ড"), (1, 2, "ঢ"),
            (0, 41, "ৃ"), (1, 41, "ঋ"), (0, 30, "ৌ"), (1, 30, "ঔ"),
            (2, 43, "়"), (3, 46, "𑷰"), (1, 15, "ড়"), (1, 7, "ঢ়"),
            (0, 6, "য"), (2, 16, "য়"), (0, 9, "অ"), (1, 9, "ৗ"),
            (0, 47, "।"), (1, 47, ">"), (2, 47, "."),
            (0, 44, "্"), (1, 44, "?"), (2, 44, "/"),
            (2, 45, "ঞ"), (2, 46, "ং"), (1, 37, "ঁ"),
        ):
            with self.subTest(index=i, code=code):
                self.assertEqual(key(custom.find(f"keyMap[@index='{i}']"), code)["output"], expected)
        self.assertEqual(key(custom.find("keyMap[@index='1']"), 6)["output"], "")
        self.assertEqual(key(custom.find("keyMap[@index='2']"), 15)["output"], "")
        self.assertEqual(key(custom.find("keyMap[@index='2']"), 39)["output"], "")
        self.assertEqual(key(custom.find("keyMap[@index='3']"), 39)["output"], "")
        self.assertEqual(key(custom.find("keyMap[@index='2']"), 37)["output"], "")
        self.assertEqual(key(custom.find("keyMap[@index='3']"), 43)["output"], "")
        self.assertEqual(key(custom.find("keyMap[@index='2']"), 38)["output"], "")
        self.assertEqual(key(custom.find("keyMap[@index='3']"), 45)["output"], "")
        defined_actions = {a.attrib["id"] for a in root.findall("./actions/action")}
        for node in root.findall(".//keyMap/key"):
            if "action" in node.attrib:
                self.assertIn(node.attrib["action"], defined_actions)


if __name__ == "__main__":
    unittest.main()
