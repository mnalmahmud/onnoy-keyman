"""Verify exact Unicode sequences and the actual website examples."""
import html
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from benchmark import onnoy, variant, measure, ASCII, xkb

class Samples(HTMLParser):
    def __init__(self):
        super().__init__()
        self.samples = []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "button" and "data-sample" in data:
            self.samples.append((html.unescape(data["data-sample"]), data["data-sequence"]))

def emit(sequence):
    mapping = onnoy()
    output = ""
    for chord in sequence.split():
        pieces = chord.split("+")
        layer = int("Shift" in pieces[:-1]) + 2 * int("AltGr" in pieces[:-1])
        output += mapping[pieces[-1]][layer]
    return output

class TypingTests(unittest.TestCase):
    def test_words(self):
        samples = {
            "Shift+S": "ষ", "X": "শ", "K I": "কি",
            "K O": "কো", "K ]": "কৌ",
            "K / Shift+S": "ক্ষ",
            "Shift+R": "ড়", "Shift+X": "ঢ়", "AltGr+Y": "য়",
            "D AltGr+,": "ড়", "Shift+D AltGr+,": "ঢ়",
            "B A Shift+L L A": "বাংলা",
            "X I K / Shift+S A": "শিক্ষা",
            "Shift+4 4 AltGr+. 5 0": "৳৪.৫০",
            "Q": "দ", "Shift+Q": "ধ",
            "D": "ড", "Shift+D": "ঢ",
            "Shift+T": "ঠ", "AltGr+T": "ৎ",
            "Shift+F": "থ", "Shift+P": "ফ",
            "Shift+V": "ৗ", "Shift+B": "ভ",
            "Shift+M": "ঙ", "AltGr+M": "ঞ", "AltGr+L": "ঁ",
            "AltGr+,": "়", "Shift+AltGr+,": "𑷰",
            "=": "=", "Shift+=": "+",
            "AltGr+J": "\u200d", "AltGr+N": "\u200c",
            "/": "্", "Shift+/": "?", "AltGr+/": "/",
            "AltGr+SPACE": " ", "Shift+AltGr+SPACE": " "
        }
        for keys, expected in samples.items():
            with self.subTest(keys=keys):
                self.assertEqual(unicodedata.normalize("NFD", emit(keys)),
                                 unicodedata.normalize("NFD", expected))

    def test_web_examples(self):
        parser = Samples()
        parser.feed((ROOT / "web/index.html").read_text(encoding="utf-8"))
        self.assertEqual(len(parser.samples), 4)
        for expected, sequence in parser.samples:
            self.assertEqual(unicodedata.normalize("NFD", emit(sequence)),
                             unicodedata.normalize("NFD", expected))
    def test_variants_not_default(self):
        mapping = onnoy()
        self.assertEqual(mapping["F"][:2], ["ত", "থ"])
        self.assertEqual(mapping["Q"][:2], ["দ", "ধ"])
        self.assertEqual(mapping["D"][:2], ["ড", "ঢ"])
        self.assertEqual(mapping["R"], ["র", "ড়", None, None])
        self.assertEqual(sum(v == "ঢ়" for vals in mapping.values() for v in vals), 1)
        self.assertEqual(mapping["Y"], ["ী", "ঈ", "য়", None])
        self.assertEqual(mapping["Z"], ["য", None, None, None])
        self.assertEqual(sum(v == "য়" for vs in mapping.values() for v in vs), 1)
        self.assertEqual(mapping[","][2:], ["়", "𑷰"])
        self.assertEqual(mapping["="][:2], ["=", "+"])
        self.assertEqual(mapping["H"][2], None)
        self.assertEqual(mapping["/"], ["্", "?", "/", None])
        self.assertEqual(mapping[chr(96)][2:], [None, None])
        self.assertEqual(mapping["'"][2:], [None, None])
        self.assertEqual(mapping["J"], ["জ", "ঝ", "\u200d", None])
        self.assertEqual(mapping["N"], ["ন", "ণ", "\u200c", None])
        self.assertEqual(mapping["M"], ["ম", "ঙ", "ঞ", None])
        self.assertEqual(mapping["L"], ["ল", "ং", "ঁ", None])
        for ch in ("\u200d", "\u200c", "ঞ", "ঁ"):
            self.assertEqual(sum(v == ch for vs in mapping.values() for v in vs), 1)
        self.assertEqual(mapping["X"], ["শ", "ঢ়", None, None])
        self.assertEqual(variant(mapping, "shift-f")["F"][1], "্")
        self.assertEqual(variant(mapping, "altgr-f")["F"][2], "্")

    def test_reference_parser_and_ascii(self):
        self.assertEqual(ASCII["space"], " ")
        self.assertEqual(ASCII["quotedbl"], '"')
        reference = 'xkb_symbols "ben-kagapa" {\n key <AC08> { [ U0995, U0996 ] };\n};'
        self.assertEqual(xkb(reference, "ben-kagapa")["K"][:2], ["ক", "খ"])

    def test_uncovered_codepoints_not_silently_dropped(self):
        self.assertEqual(measure("ক্", onnoy())["unavailable_codepoints"], 0)
        self.assertGreater(measure("𐀀", onnoy())["unavailable_codepoints"], 0)

if __name__ == "__main__":
    unittest.main()
