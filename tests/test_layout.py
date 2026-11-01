"""Generator regressions: all targets read the same authoritative Unicode source."""
import unittest
from xml.etree import ElementTree as ET
from onnoy.model import load, resolve
from onnoy.backends import linux,windows,macos,keyman,web
import json

class NativeLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map=resolve(load(), "iso")

    def test_xkb_iso_grave_and_layers(self):
        symbols=linux.render(self.map)
        self.assertIn('include "us(basic)"',symbols)
        self.assertIn('key <LSGT> { type[Group1]="FOUR_LEVEL", symbols[Group1]=[ U005C, U007C',symbols)
        self.assertIn('key <TLDE> { type[Group1]="FOUR_LEVEL", symbols[Group1]=[ U09CD, U007E, U0060',symbols)
        self.assertIn('key <AC07> { type[Group1]="FOUR_LEVEL", symbols[Group1]=[ U099C, U099D, U200D, U200C',symbols)
        self.assertIn('key <AC09> { type[Group1]="FOUR_LEVEL", symbols[Group1]=[ U09B2, U0981, U09BC',symbols)

    def test_windows_unicode_and_utf16_surrogates(self):
        text=windows.render(self.map)
        self.assertIn("29\tOEM_3\t0\t09cd\t007e\t-1\t0060",text)
        self.assertIn("56\tOEM_102\t0\t005c\t007c",text)
        self.assertIn("LIGATURE",text)
        self.assertIn("d807\tdfF0".lower().replace("\t",""),text.lower().replace("\t","").replace(" ","")) if False else None
        # U+11DF0 is the surrogate pair D807 DDF0.
        self.assertIn("d807 ddf0",text.lower())

    def test_macos_self_contained(self):
        source=macos.render(self.map)
        root=ET.fromstring(source.split("\n",2)[2])
        self.assertIsNone(root.find("./keyMapSet[@id='OnnoyUSBase']"))
        keys=root.findall("./keyMapSet[@id='OnnoyMap']/keyMap")
        self.assertEqual(len(keys),6)
        def output(layer,code):
            return keys[layer].find(f"./key[@code='{code}']").get("output")
        self.assertEqual(output(0,50),"্")
        self.assertEqual(output(2,50),"`")
        self.assertEqual(output(0,10),"\\")
        self.assertEqual(output(1,10),"|")
        self.assertEqual(output(2,38),"‍")
        self.assertEqual(output(3,38),"‌")
        self.assertEqual(output(4,38),"j")

    def test_keyman_physical_rules(self):
        source=keyman.render(self.map)
        self.assertIn("+ [RALT K_J] > U+200D",source)
        self.assertIn("+ [SHIFT RALT K_J] > U+200C",source)
        self.assertIn("+ [RALT K_COLON] > U+003B",source)
        self.assertIn("+ [K_oE2] > U+005C",source)
        self.assertIn("+ [RALT K_Z] > nul",source)

    def test_browser_visualizer_data(self):
        ref=json.loads(web.render(self.map))
        self.assertEqual(ref["keys"]["KeyJ"][2],"‍")
        self.assertEqual(ref["keys"]["KeyZ"][1],"য়")
        self.assertEqual(ref["keys"]["IntlBackslash"][0],"\\")

if __name__=="__main__":unittest.main()
