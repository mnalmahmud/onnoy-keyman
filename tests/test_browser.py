"""Real Chromium smoke tests for the GitHub Pages build.

The website uses a tiny client-side preview and needs no third-party
keyboard runtime. The tests run with all external networks unavailable.
"""
import functools
import http.server
import threading
import unittest
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

SITE = Path(__file__).resolve().parents[1] / "site"


@unittest.skipUnless(sync_playwright, "Install playwright to run browser smoke tests")
class BrowserSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SITE.is_dir():
            raise RuntimeError("Stage site/ before running browser smoke tests")
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE))
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def setUp(self):
        self.page = self.browser.new_page()
        self.page.route("https://**/*", lambda route: route.abort())
        self.page.goto(f"http://127.0.0.1:{self.server.server_port}/", wait_until="domcontentloaded")
        self.page.locator(".keyboard-key").first.wait_for()

    def tearDown(self):
        self.page.close()

    def test_reference_and_four_layers(self):
        self.assertEqual(self.page.locator(".keyboard-key").count(), 47)
        self.assertEqual(self.page.locator(".keyboard-row").count(), 5)
        key = lambda k: self.page.locator('.keyboard-key[data-key="' + k + '"] .key-symbol').inner_text()
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(key("'"), "ZWJ")
        self.assertEqual(key(","), "়")
        self.page.locator('button[data-layer="3"]').click()
        self.assertEqual(key("'"), "ZWNJ")
        self.assertEqual(key(","), "𑷰")
        self.assertEqual(key("W"), "—")
        self.page.locator('button[data-layer="1"]').click()
        self.assertEqual(key("Y"), "ঈ")
        self.assertEqual(key("R"), "ড়")
        self.assertEqual(key("Z"), "য়")

    def test_assamese_wa_on_altgr_w(self):
        key = lambda k: self.page.locator('.keyboard-key[data-key="' + k + '"] .key-symbol').inner_text()
        self.assertEqual(key("V"), "অ")
        self.assertEqual(key("B"), "ব")
        self.page.locator('button[data-layer="1"]').click()
        self.assertEqual(key("V"), "ৗ")
        self.assertEqual(key("B"), "ভ")
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(key("W"), "ৱ")
        self.assertEqual(key("V"), "—")

    def test_combining_marks_on_comma(self):
        key = lambda k: self.page.locator('.keyboard-key[data-key="' + k + '"] .key-symbol').inner_text()
        self.assertEqual(key(","), ",")
        self.page.locator('button[data-layer="1"]').click()
        self.assertEqual(key(","), "<")
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(key(","), "়")
        self.assertEqual(key("X"), "—")
        self.page.locator('button[data-layer="3"]').click()
        self.assertEqual(key(","), "𑷰")

    def test_design_d_y_layers(self):
        y = lambda: self.page.locator(".keyboard-row").nth(1).locator("button").nth(5).locator(".key-symbol").inner_text()
        self.assertEqual(y(), "ী")
        self.page.locator('button[data-layer="1"]').click()
        self.assertEqual(y(), "ঈ")
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(y(), "—")
        self.page.locator('button[data-layer="3"]').click()
        self.assertEqual(y(), "—")

    def test_bracket_vowels_and_original_brace_shortcuts(self):
        key = lambda k: self.page.locator('.keyboard-key[data-key="' + k + '"] .key-symbol').inner_text()
        self.assertEqual(key("["), "ৈ")
        self.assertEqual(key("]"), "ৌ")
        self.page.locator('button[data-layer="1"]').click()
        self.assertEqual(key("["), "ঐ")
        self.assertEqual(key("]"), "ঔ")
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(key("["), "[")
        self.assertEqual(key("]"), "]")
        self.page.locator('button[data-layer="3"]').click()
        self.assertEqual(key("["), "{")
        self.assertEqual(key("]"), "}")

    def test_ra_ri_virama_nukta_and_ascii_equals(self):
        key = lambda k: self.page.locator('.keyboard-key[data-key="' + k + '"] .key-symbol').inner_text()
        self.assertEqual(key("R"), "র")
        self.assertEqual(key(";"), "ৃ")
        self.assertEqual(key("="), "=")
        self.assertEqual(key("F"), "ত")
        self.assertEqual(key("T"), "ট")
        self.assertEqual(key("X"), "শ")
        self.assertEqual(key("V"), "অ")
        self.assertEqual(key("/"), "্")
        self.page.locator('button[data-layer="1"]').click()
        self.assertEqual(key("R"), "ড়")
        self.assertEqual(key(";"), "ঋ")
        self.assertEqual(key("="), "+")
        self.assertEqual(key("F"), "থ")
        self.assertEqual(key("T"), "ঠ")
        self.assertEqual(key("P"), "ফ")
        self.assertEqual(key("Z"), "য়")
        self.assertEqual(key("X"), "—")
        self.assertEqual(key("S"), "ষ")
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(key("R"), "ঢ়")
        self.assertEqual(key("T"), "ৎ")
        self.assertEqual(key("N"), "ঞ")
        self.assertEqual(key("M"), "ঁ")
        self.assertEqual(key(","), "়")
        self.assertEqual(key("/"), "/")
        self.assertEqual(key("'"), "ZWJ")
        self.assertEqual(key("H"), "—")
        self.page.locator('button[data-layer="3"]').click()
        self.assertEqual(key(","), "𑷰")
        self.assertEqual(key("'"), "ZWNJ")

    def test_direct_nfc_o_and_au_signs(self):
        key = lambda k: self.page.locator('.keyboard-key[data-key="' + k + '"] .key-symbol').inner_text()
        self.assertEqual(key("O"), "ো")
        self.assertEqual(key("]"), "ৌ")
        self.assertEqual(key(";"), "ৃ")
        self.page.locator('button[data-layer="1"]').click()
        self.assertEqual(key("O"), "ও")
        self.assertEqual(key("]"), "ঔ")
        self.assertEqual(key(";"), "ঋ")
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(key(";"), ";")
        self.page.locator('button[data-layer="3"]').click()
        self.assertEqual(key(";"), ":")

    def test_redesigned_sections_examples_and_search(self):
        self.assertTrue(self.page.locator("#studio").count() == 1)
        self.assertTrue(self.page.locator("#install").count() == 1)
        self.assertEqual(self.page.locator(".install-card").count(), 3)
        self.page.locator('[data-sample="বাংলা"]').click()
        self.assertEqual(self.page.locator("#editor").input_value(), "বাংলা")
        self.page.locator("#key-search").fill("11df0")
        self.assertIn("matching keys", self.page.locator("#search-feedback").inner_text())
        self.assertEqual(self.page.locator(".keyboard-key.search-match").count(), 1)
        self.page.locator("#key-search").fill("ZZNOTFOUND")
        self.assertEqual(self.page.locator(".keyboard-key.search-match").count(), 0)
        self.page.locator("#key-search").fill("")
        self.assertEqual(self.page.locator(".keyboard-key.search-dim").count(), 0)

    def test_editor_inspector_copy_and_native_preview(self):
        self.page.locator("#status-label").get_by_text("Preview ready").wait_for()
        editor = self.page.locator("#editor")
        editor.fill("বাংলা")
        self.assertEqual(self.page.locator("#count").inner_text(), "5 code points · 2 graphemes")
        self.assertTrue(self.page.locator("#copy").is_enabled())
        self.page.locator("#inspect").click()
        self.assertFalse(self.page.locator("#unicode-panel").is_hidden())
        self.assertIn("U+09AC", self.page.locator("#codepoints").inner_text())
        self.page.locator("#clear").click()
        self.assertEqual(editor.input_value(), "")
        self.assertFalse(self.page.locator("#copy").is_enabled())

    def test_browser_preview_typing_and_shortcuts(self):
        editor = self.page.locator("#editor")
        editor.focus()
        self.page.keyboard.press("k")
        self.page.keyboard.press("i")
        self.assertEqual(editor.input_value(), "কি")
        self.page.keyboard.press("ControlOrMeta+A")
        self.assertEqual(editor.input_value(), "কি")
        self.page.keyboard.press("Backspace")
        self.assertEqual(editor.input_value(), "")
        self.page.keyboard.press("v")
        self.assertEqual(editor.input_value(), "অ")
        self.page.keyboard.press("Shift+v")
        self.assertEqual(editor.input_value(), "অৗ")


if __name__ == "__main__":
    unittest.main()
