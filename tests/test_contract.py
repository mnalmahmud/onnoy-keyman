"""Regression tests for the generated Keyman keyboard and mobile layout."""
import json
import re
import sys
import unittest
from pathlib import Path

from kalamine.layout import KeyboardLayout, load_layout
from kalamine.utils import Layer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from toml_to_kmn import generate, render  # noqa: E402


def keyman_rules(source):
    rules = {}
    for line in source.splitlines():
        if not line.startswith("+ ["):
            continue
        match = re.fullmatch(r"\+ \[([^]]+)\] > (nul|U\+[0-9A-Fa-f]{4,6})", line)
        if not match:
            raise AssertionError(f"Invalid generated Keyman rule: {line}")
        chord, value = match.groups()
        if chord in rules:
            raise AssertionError(f"Duplicate Keyman rule: {chord}")
        rules[chord] = None if value == "nul" else chr(int(value[2:], 16))
    return rules


class KeymanGeneration(unittest.TestCase):
    def test_build_regenerates_source(self):
        compiled = (ROOT / "keyman/onnoy.kmn").read_text(encoding="utf-8")
        self.assertEqual(compiled, generate(ROOT / "layout.toml"))

    def test_core_outputs_and_unmapped_chords(self):
        rules = keyman_rules(generate(ROOT / "layout.toml"))
        expected = {
            "K_K": "ক", "SHIFT K_K": "খ",
            "K_BKQUOTE": "্", "SHIFT K_BKQUOTE": "়",
            "RALT K_J": "\u200d", "SHIFT RALT K_J": "\u200c",
            "K_D": "ড", "SHIFT K_D": "ঢ",
            "RALT K_D": "দ", "SHIFT RALT K_D": "ধ",
            "K_T": "ট", "SHIFT K_T": "ঠ",
            "RALT K_T": "ত", "SHIFT RALT K_T": "থ",
            "K_Q": "দ", "SHIFT K_Q": "ধ",
            "K_F": "ত", "SHIFT K_F": "থ",
            "RALT K_W": "ৱ", "SHIFT K_4": "৳",
            "RALT K_4": "4", "SHIFT RALT K_4": "$",
            "RALT K_S": "ষ",
            "RALT K_Q": None,
        }
        for chord, value in expected.items():
            with self.subTest(chord=chord):
                self.assertEqual(rules[chord], value)
        self.assertEqual(len(rules) % 4, 0)

    def test_editing_toml_changes_keyman_output(self):
        layout = KeyboardLayout(load_layout(ROOT / "layout.toml"))
        before = keyman_rules(render(layout))
        layout.layers[Layer.BASE]["ac08"] = "ঙ"
        after = keyman_rules(render(layout))
        self.assertEqual(before["K_K"], "ক")
        self.assertEqual(after["K_K"], "ঙ")
        self.assertEqual(after["SHIFT K_K"], before["SHIFT K_K"])

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
