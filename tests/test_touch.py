"""Mobile touch contract: all explicit Unicode scalars must remain reachable."""
import json
import unittest

from onnoy.model import load, resolve
from onnoy.hardware import ALPHABET
from onnoy.backends import touch, keyman

class MobileTouchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping = resolve(load(), "iso")
        cls.layout = touch.render_data(cls.mapping)
        cls.layers = {
            layer["id"]: layer for layer in cls.layout["phone"]["layer"]
        }

    @staticmethod
    def flattened(layer):
        return [key for row in layer["row"] for key in row["key"]]

    @staticmethod
    def outputs(layer):
        return {
            key["id"] for key in MobileTouchTests.flattened(layer)
        } | {
            popup["id"]
            for key in MobileTouchTests.flattened(layer)
            for popup in key.get("sk", [])
        }

    def test_standard_three_phone_layers(self):
        self.assertEqual(set(self.layers), {"default", "shift", "numeric"})
        for layer in self.layers.values():
            self.assertEqual(len(layer["row"]), 4)
        self.assertEqual(
            [len(row["key"]) for row in self.layers["default"]["row"]],
            [10,9,9,7])
        self.assertEqual(
            [len(row["key"]) for row in self.layers["numeric"]["row"]],
            [10,10,10,7])

    def test_alphabet_keys_resolve_canonical_outputs(self):
        for layer_name, idx in (("default",0), ("shift",1)):
            for key in self.flattened(self.layers[layer_name]):
                if key["id"] not in {f"K_{letter}" for letter in ALPHABET}:
                    continue
                physical = key["id"].removeprefix("K_")
                output = self.mapping[physical][idx]
                self.assertEqual(key["text"],touch.caption(output))
                if idx:
                    self.assertEqual(key.get("layer"),"shift")

    def test_explicit_source_characters_are_all_reachable(self):
        # Primary virtual keys carry canonical Base/Shift outputs via KMN.
        # Direct U_xxxx keys include long-press alternatives and symbols.
        all_keys = set()
        for layer in self.layers.values():
            all_keys |= self.outputs(layer)
        reachable = {
            self.mapping[key][layer]
            for layer, _ in ((0,"base"),(1,"shift"))
            for key in ALPHABET
            if self.mapping[key][layer] is not None
        }
        reachable |= {
            chr(int(code[2:],16))
            for code in all_keys if code.startswith("U_")
        }
        expected = {
            value for mapping in load()["keys"].values()
            for value in mapping.values()
        }
        self.assertFalse(expected - reachable, f"Missing touch characters: {expected-reachable!r}")

    def test_critical_onscreen_keys(self):
        base=self.flattened(self.layers["default"])
        self.assertIn("U_09CD",{key["id"] for key in base})
        self.assertIn("K_SPACE",{key["id"] for key in base})
        self.assertIn("K_BKSP",{key["id"] for key in base})
        self.assertIn("K_ENTER",{key["id"] for key in base})
        for layer in self.layers.values():
            self.assertIn("K_LOPT",{key["id"] for key in self.flattened(layer)})
        self.assertTrue(any(k.get("nextlayer")=="numeric" for k in base))
        self.assertTrue(any(k.get("nextlayer")=="default" for k in self.flattened(self.layers["numeric"])))
        self.assertTrue(any(k.get("nextlayer")=="shift" for k in base))

    def test_joiners_nukta_assamese_and_supplementary(self):
        keys=set()
        for layer in self.layers.values():
            keys |= self.outputs(layer)
        for value in ("\u200D","\u200C","়","ৰ","ৱ","𑷰"):
            self.assertIn(touch.unicode_key(value),keys)

    def test_digits_and_ascii_fallbacks(self):
        numeric = self.layers["numeric"]
        all_keys=self.outputs(numeric)
        for ascii_digit in "0123456789":
            self.assertIn(touch.unicode_key(ascii_digit), all_keys)
        for bengali_digit in "০১২৩৪৫৬৭৮৯":
            self.assertIn(touch.unicode_key(bengali_digit), all_keys)

    def test_unicode_popups_not_alternative_character_source(self):
        rendered=json.loads(touch.render(self.mapping))
        self.assertEqual(rendered,self.layout)
        self.assertIn("store(&layoutfile) 'onnoy.keyman-touch-layout'",keyman.render(self.mapping))
        for layer in self.layers.values():
            for key in self.flattened(layer):
                self.assertTrue(key["id"].startswith(("K_","U_")))
                for popup in key.get("sk",[]):
                    self.assertTrue(popup["id"].startswith(("K_","U_")))

if __name__=="__main__":
    unittest.main()
