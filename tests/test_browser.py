"""Chromium smoke test for Keyman typing and the restored four-layer UI."""
import os
import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.environ.get("RUN_BROWSER_TESTS") == "1", "Browser test is opt-in")
class BrowserSmoke(unittest.TestCase):
    def test_typing_and_four_layers(self):
        from playwright.sync_api import sync_playwright
        server = ThreadingHTTPServer(
            ("127.0.0.1", 0),
            partial(SimpleHTTPRequestHandler, directory=str(ROOT / "site")))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                page = browser.new_page()
                page.goto(f"http://127.0.0.1:{server.server_port}/", wait_until="load")
                page.wait_for_function("document.querySelector('#status').classList.contains('ready')", timeout=30000)
                self.assertEqual(page.locator("[data-layer]").count(), 4)
                self.assertGreater(page.locator("#keyboard .keyboard-key").count(), 45)
                page.locator("[data-layer='2']").click()
                self.assertEqual(page.locator("[data-layer='2']").get_attribute("aria-pressed"), "true")
                self.assertEqual(page.locator("#keyboard .keyboard-key[data-code='KeyJ'] .key-output").inner_text(), "ZWJ")
                page.locator("[data-layer='3']").click()
                self.assertEqual(page.locator("[data-layer='3']").get_attribute("aria-pressed"), "true")
                page.locator("[data-layer='0']").click()
                page.locator("#editor").focus()
                page.keyboard.press("k")
                self.assertEqual(page.locator("#editor").input_value(), "ক")
                page.keyboard.press("Backquote")
                page.keyboard.press("x")
                self.assertEqual(page.locator("#editor").input_value(), "ক্ষ")
                page.locator("#inspect").click()
                self.assertFalse(page.locator("#unicode-panel").is_hidden())
                self.assertIn("U+0995", page.locator("#codepoints").inner_text())
                page.locator("#geometry").select_option("iso")
                self.assertGreater(page.locator("#keyboard .keyboard-key").count(), 45)
                browser.close()
        finally:
            server.shutdown()
            server.server_close()
