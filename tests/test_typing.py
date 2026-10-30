"""Verify exact Unicode sequences and the actual website examples."""
import html
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from benchmark import onnoy, variant, measure

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
        samples = {"K I": "কি", "K O": "কো", "K ;": "কৌ",
                   "K Shift+F X": "ক্ষ", "Q Shift+X": "ড়",
                   "B A Shift+L L A": "বাংলা",
                   "Shift+S I K Shift+F X A": "শিক্ষা",
                   "Shift+4 4 AltGr+. 5 0": "৳৪.৫০"}
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
        self.assertEqual(mapping["F"][:2], ["ফ", "্"])
        self.assertEqual(mapping["/"][0], "/")
        self.assertEqual(variant(mapping, "slash")["/"][0], "্")
        self.assertEqual(variant(mapping, "altgr-f")["F"][2], "্")
    def test_uncovered_codepoints_not_silently_dropped(self):
        self.assertEqual(measure("ক্", onnoy())["unavailable_codepoints"], 0)
        self.assertGreater(measure("𐀀", onnoy())["unavailable_codepoints"], 0)

if __name__ == "__main__":
    unittest.main()
