"""Cross-platform source-contract tests independent from generated native files."""
import unittest
from onnoy.hardware import STANDARD, ISO_EXTRA, LAYERS, XKB, WINDOWS, MAC, KEYMAN, BROWSER
from onnoy.model import load, resolve, validate

class MappingContractTests(unittest.TestCase):
    def test_sparse_schema(self):
        data = load()
        self.assertNotIn("passthrough", data)
        self.assertEqual(set(data), {"name","keys"})
        for fields in data["keys"].values():
            self.assertTrue(set(fields) <= set(LAYERS))
            self.assertNotIn(None, fields.values())

    def test_approved_sequences(self):
        a = resolve(geometry="ansi")
        cases = {
            ("GRAVE","base"):"্", ("GRAVE","shift"):"~",
            ("GRAVE","altgr"):"`", ("SLASH","base"):"/",
            ("SLASH","shift"):"?", ("COMMA","base"):",",
            ("COMMA","shift"):"<", ("S","shift"):"শ",
            ("X","base"):"ষ", ("X","shift"):"ঢ়",
            ("Z","shift"):"য়", ("Y","altgr"):"য়",
            ("J","altgr"):"‍", ("J","shift_altgr"):"‌",
            ("L","altgr"):"়", ("B","altgr"):"ৰ",
            ("M","shift_altgr"):"𑷰", ("W","altgr"):"ৱ",
            ("N","altgr"):"ঞ", ("4","shift"):"৳",
            ("4","shift_altgr"):"$"
        }
        for (key,layer), output in cases.items():
            with self.subTest(key=key,layer=layer):
                self.assertEqual(a[key][LAYERS.index(layer)],output)

    def test_symbol_and_alpha_omissions(self):
        a=resolve()
        self.assertEqual(a["Q"][2:], (None,None))
        self.assertEqual(a["COMMA"], (",","<",None,None))
        self.assertEqual(a["SLASH"], ("/","?",None,None))
        self.assertEqual(a["MINUS"], ("-","_",None,None))
        self.assertEqual(a["SPACE"], (" "," "," "," "))
        self.assertNotIn(ISO_EXTRA,a)

    def test_iso(self):
        a=resolve(geometry="ansi")
        iso=resolve(geometry="iso")
        self.assertEqual(iso[ISO_EXTRA], ("\\","|",None,None))
        for key in STANDARD:
            self.assertEqual(a[key],iso[key])

    def test_reject_bad_scalars(self):
        import copy
        d=load()
        for bad in (None,"", "abc", "\ud800"):
            clone=copy.deepcopy(d)
            clone["keys"]["J"]["base"]=bad
            with self.assertRaises(ValueError):
                validate(clone)

    def test_physical_tables_cover_all_positions(self):
        for target in (XKB,WINDOWS,MAC,KEYMAN,BROWSER):
            self.assertEqual(set(target), set(STANDARD)|{ISO_EXTRA})

if __name__=="__main__":
    unittest.main()
