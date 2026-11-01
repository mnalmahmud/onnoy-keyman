"""Source-level web regression checks; browser integration requires compiled KeymanWeb."""
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
class BrowserIntegrationSourceTests(unittest.TestCase):
    def test_uses_keymanweb_instead_of_second_translator(self):
        script=(ROOT/"web/app.js").read_text(encoding="utf-8")
        html=(ROOT/"web/index.html").read_text(encoding="utf-8")
        self.assertIn("engine.addKeyboards",script)
        self.assertIn("engine.setActiveKeyboard",script)
        self.assertIn("layout.keys",script)
        self.assertNotIn("function translateKey(",script)
        self.assertIn("keymanweb.js",html)
