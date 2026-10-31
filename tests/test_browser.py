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
        self.assertEqual(self.page.locator(".keyboard-key").count(), 46)
        self.assertEqual(self.page.locator(".keyboard-row").count(), 5)
        self.page.locator('button[data-layer="2"]').click()
        self.assertIn("ZWJ", self.page.locator(".keyboard-row").nth(2).inner_text())
        self.assertNotIn("ZWJ", self.page.locator(".keyboard-row").nth(0).inner_text())
        self.assertNotIn("ZWJ", self.page.locator(".keyboard-row").nth(4).inner_text())
        self.page.locator('button[data-layer="3"]').click()
        self.assertIn("ZWNJ", self.page.locator(".keyboard-row").nth(2).inner_text())
        self.assertNotIn("ZWNJ", self.page.locator(".keyboard-row").nth(0).inner_text())
        self.assertNotIn("ZWNJ", self.page.locator(".keyboard-row").nth(4).inner_text())
        self.page.locator(".keyboard-row").nth(1).locator("button").nth(1).click()
        self.assertIn("AltGr + Shift: —", self.page.locator("#key-details").inner_text())
        # The renderer must display the complete approved sequences.
        self.page.locator('button[data-layer="1"]').click()
        self.assertIn("ঈ", self.page.locator(".keyboard-row").nth(1).inner_text())
        self.assertIn("ৰ", self.page.locator(".keyboard-row").nth(1).inner_text())
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(
            self.page.locator(".keyboard-row").nth(2).locator("button").nth(4)
                     .locator(".key-symbol").inner_text(), "—"
        )

    def test_assamese_wa_on_altgr_w(self):
        w = lambda: self.page.locator(".keyboard-row").nth(1).locator("button").nth(1).locator(".key-symbol").inner_text()
        v = lambda: self.page.locator(".keyboard-row").nth(3).locator("button").nth(3).locator(".key-symbol").inner_text()
        self.page.locator('button[data-layer="1"]').click()
        self.assertEqual(v(), "অ")
        b = self.page.locator(".keyboard-row").nth(3).locator("button").nth(4).locator(".key-symbol").inner_text()
        self.assertEqual(b, "ৗ")
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(w(), "ৱ")
        self.assertEqual(v(), "—")

    def test_altgr_x_combining_anusvara_above(self):
        self.page.locator('button[data-layer="2"]').click()
        x = self.page.locator(".keyboard-row").nth(3).locator("button").nth(1)
        self.assertIn("𑷰", x.get_attribute("aria-label") or "")

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
        bracket = lambda key: self.page.locator('.keyboard-key[data-key="' + key + '"] .key-symbol').inner_text()
        self.assertEqual(bracket("["), "ৈ")
        self.assertEqual(bracket("]"), "ূ")
        self.page.locator('button[data-layer="1"]').click()
        self.assertEqual(bracket("["), "ঐ")
        self.assertEqual(bracket("]"), "ঊ")
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(bracket("["), "[")
        self.assertEqual(bracket("]"), "]")
        self.page.locator('button[data-layer="3"]').click()
        self.assertEqual(bracket("["), "{")
        self.assertEqual(bracket("]"), "}")

    def test_ra_ri_virama_nukta_and_ascii_equals(self):
        key = lambda k: self.page.locator('.keyboard-key[data-key="' + k + '"] .key-symbol').inner_text()
        self.assertEqual(key("R"), "র")
        self.assertEqual(key("="), "ৃ")
        self.assertEqual(key("F"), "ফ")
        self.assertEqual(key("X"), "ষ")
        self.assertEqual(key("-"), "-")
        self.assertEqual(key("/"), "্")
        self.assertEqual(key("`"), "`")
        self.page.locator('button[data-layer="1"]').click()
        self.assertEqual(key("R"), "ৰ")
        self.assertEqual(key("="), "ঋ")
        self.assertEqual(key("F"), "—")
        self.assertEqual(key("X"), "়")
        self.assertEqual(key("-"), "_")
        self.assertEqual(key("/"), "?")
        self.assertEqual(key("`"), "~")
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(key("="), "=")
        self.assertEqual(key("/"), "/")
        self.assertEqual(key("`"), "—")
        self.assertEqual(key("\'"), "ZWJ")
        self.page.locator('button[data-layer="3"]').click()
        self.assertEqual(key("="), "+")
        self.assertEqual(key("`"), "—")
        self.assertEqual(key("\'"), "ZWNJ")

    def test_direct_nfc_o_and_au_signs(self):
        key = lambda k: self.page.locator('.keyboard-key[data-key="' + k + '"] .key-symbol').inner_text()
        self.assertEqual(key("O"), "ো")
        self.assertEqual(key(";"), "ৌ")
        self.page.locator('button[data-layer="1"]').click()
        self.assertEqual(key("O"), "ও")
        self.assertEqual(key(";"), "ঔ")
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
        self.page.keyboard.press("Shift+v")
        self.assertEqual(editor.input_value(), "অ")


if __name__ == "__main__":
    unittest.main()
