"""Real Chromium smoke tests for the GitHub Pages build.

These intentionally block the remote Keyman script: the key reference and
ordinary editor controls must work even when the network is unavailable.
The Keyman compiler itself is checked separately by the build workflow.
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
        self.page.route("https://s.keyman.com/**", lambda route: route.abort())
        self.page.goto(f"http://127.0.0.1:{self.server.server_port}/", wait_until="domcontentloaded")
        self.page.locator(".keyboard-key").first.wait_for()

    def tearDown(self):
        self.page.close()

    def test_reference_and_four_layers(self):
        self.assertEqual(self.page.locator(".keyboard-key").count(), 37)
        self.assertEqual(self.page.locator(".keyboard-row").count(), 4)
        self.page.locator('button[data-layer="2"]').click()
        self.assertIn("ZWJ", self.page.locator(".keyboard-row").nth(3).inner_text())
        self.page.locator('button[data-layer="3"]').click()
        self.assertIn("ZWNJ", self.page.locator(".keyboard-row").nth(3).inner_text())
        self.page.locator(".keyboard-row").nth(1).locator("button").nth(1).click()
        self.assertIn("AltGr + Shift: —", self.page.locator("#key-details").inner_text())
        # The renderer must display the complete approved sequences.
        self.page.locator('button[data-layer="1"]').click()
        self.assertIn("ক্ষ", self.page.locator(".keyboard-row").nth(3).inner_text())
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(
            self.page.locator(".keyboard-row").nth(2).locator("button").nth(4)
                     .locator(".key-symbol").inner_text(), "—"
        )
        self.assertIn("্য", self.page.locator(".keyboard-row").nth(1).inner_text())

    def test_design_d_y_layers(self):
        y = lambda: self.page.locator(".keyboard-row").nth(1).locator("button").nth(5).locator(".key-symbol").inner_text()
        self.assertEqual(y(), "য়")
        self.page.locator('button[data-layer="1"]').click()
        self.assertEqual(y(), "য")
        self.page.locator('button[data-layer="2"]').click()
        self.assertEqual(y(), "্য")
        self.page.locator('button[data-layer="3"]').click()
        self.assertEqual(y(), "—")

    def test_editor_inspector_copy_and_failure_fallback(self):
        self.page.locator("#status-label").get_by_text("Keyboard unavailable").wait_for()
        editor = self.page.locator("#editor")
        editor.fill("বাংলা")
        self.assertEqual(self.page.locator("#count").inner_text(), "5")
        self.assertTrue(self.page.locator("#copy").is_enabled())
        self.page.locator("#inspect").click()
        self.assertFalse(self.page.locator("#unicode-panel").is_hidden())
        self.assertIn("U+09AC", self.page.locator("#codepoints").inner_text())
        self.page.locator("#clear").click()
        self.assertEqual(editor.input_value(), "")
        self.assertFalse(self.page.locator("#copy").is_enabled())


if __name__ == "__main__":
    unittest.main()
