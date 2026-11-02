"""Kalamine's native mapping must agree with the Keyman source."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "dist/onnoy.json"
KEYMAN = ROOT / "keyman/onnoy.kmn"
EXTRAS = {
    "Backquote": "K_BKQUOTE", "Minus": "K_HYPHEN", "Equal": "K_EQUAL",
    "BracketLeft": "K_LBRKT", "BracketRight": "K_RBRKT",
    "Backslash": "K_BKSLASH", "Semicolon": "K_COLON",
    "Quote": "K_QUOTE", "Comma": "K_COMMA", "Period": "K_PERIOD",
    "Slash": "K_SLASH", "IntlBackslash": "K_oE2", "Space": "K_SPACE",
}

def keyman_id(code):
    if code.startswith("Key"):
        return "K_" + code[3:]
    if code.startswith("Digit"):
        return "K_" + code[5:]
    return EXTRAS[code]

def keyman_rules():
    rules = {}
    for line in KEYMAN.read_text(encoding="utf-8-sig").splitlines():
        if not line.startswith("+ ["):
            continue
        match = re.fullmatch(r"\+ \[([^]]+)\] > (nul|U\+[0-9A-Fa-f]{4,6})", line)
        if not match:
            raise AssertionError(f"Invalid Keyman rule: {line}")
        chord, output = match.groups()
        fields = chord.split()
        layer = int("SHIFT" in fields) + 2 * int("RALT" in fields)
        position = (fields[-1], layer)
        if position in rules:
            raise AssertionError(f"Duplicate Keyman rule: {position}")
        rules[position] = None if output == "nul" else chr(int(output[2:], 16))
    return rules

class KeyboardContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = json.loads(NATIVE.read_text(encoding="utf-8"))["keymap"]
        cls.keyman = keyman_rules()

    def test_all_layers_match(self):
        expected = {}
        for code, values in self.native.items():
            for layer in range(4):
                expected[(keyman_id(code), layer)] = values[layer] if layer < len(values) else None
        # Kalamine versions may omit the spacebar from the web descriptor.
        if ("K_SPACE", 0) not in expected:
            for layer in range(4):
                expected[("K_SPACE", layer)] = " "
        self.assertEqual(expected, self.keyman)

    def test_core_outputs(self):
        required = {
            ("K_K", 0): "ক", ("K_K", 1): "খ",
            ("K_BKQUOTE", 0): "্", ("K_BKQUOTE", 1): "়",
            ("K_J", 2): "\u200d", ("K_D", 2): "\u200c",
            ("K_W", 2): "ৱ", ("K_4", 1): "৳",
            ("K_4", 2): "4", ("K_4", 3): "$",
            ("K_S", 2): "ষ",
        }
        for chord, output in required.items():
            with self.subTest(chord=chord):
                self.assertEqual(self.keyman[chord], output)

    def test_mobile_coverage(self):
        touch = json.loads((ROOT / "keyman/onnoy.keyman-touch-layout").read_text(encoding="utf-8"))
        keys = [key for layer in touch["phone"]["layer"]
                for row in layer["row"] for key in row["key"]]
        ids = {value["id"] for key in keys
               for value in [key, *key.get("sk", [])]}
        for output in "়্ৱঁংৎষঢ়\u200d\u200c":
            self.assertIn("U_" + f"{ord(output):04X}", ids)
        self.assertEqual({layer["id"] for layer in touch["phone"]["layer"]},
                         {"default", "shift", "numeric"})

if __name__ == "__main__":
    unittest.main()
