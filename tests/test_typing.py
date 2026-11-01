"""Exact typing sequences; do not normalize away distinct Unicode encodings."""
import unittest
from onnoy.hardware import LAYERS
from onnoy.model import resolve

def emit(*chords):
    mapping=resolve()
    result=[]
    for chord in chords:
        parts=chord.split("+")
        key=parts[-1]
        layer=(("Shift" in parts)*1)+(("AltGr" in parts)*2)
        value=mapping[key][layer]
        if value is not None:
            result.append(value)
    return "".join(result)

class TypingCases(unittest.TestCase):
    def test_bengali_words(self):
        cases={
            ("K","GRAVE","X"):"ক্ষ",
            ("Shift+S","I","K","GRAVE","X","A"):"শিক্ষা",
            ("B","A","AltGr+M","L","A"):"বাংলা",
            ("R","AltGr+J","GRAVE","Z"):"র‍্য",
            ("K","GRAVE","Shift+AltGr+J","X"):"ক্‌ষ",
            ("Shift+4","4","AltGr+PERIOD","5","0"):"৳৪.৫০",
            ("D","AltGr+L"):"ড়",
            ("Shift+D","AltGr+L"):"ঢ়",
        }
        for chords, expected in cases.items():
            with self.subTest(chords=chords):
                self.assertEqual(emit(*chords),expected)
    def test_alias_codepoint_exact(self):
        self.assertEqual(emit("Shift+Z"),chr(0x09DF))
        self.assertEqual(emit("AltGr+Y"),chr(0x09DF))
        self.assertEqual(emit("Shift+AltGr+M"),chr(0x11DF0))
        self.assertEqual(emit("AltGr+J"),chr(0x200D))
        self.assertEqual(emit("Shift+AltGr+J"),chr(0x200C))
    def test_punctuation_and_no_output(self):
        self.assertEqual(emit("SLASH","Shift+SLASH"),"/?")
        self.assertEqual(emit("COMMA","Shift+COMMA"),",<")
        self.assertEqual(emit("GRAVE","AltGr+GRAVE"),"্`")
        self.assertEqual(emit("AltGr+Z"),"")

if __name__=="__main__":unittest.main()
