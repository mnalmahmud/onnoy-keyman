"""Chromium smoke tests for typing and the four-layer keyboard interface."""
import os
import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.environ.get("RUN_BROWSER_TESTS") == "1", "Browser test is opt-in")
class BrowserSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0),
            partial(SimpleHTTPRequestHandler, directory=str(ROOT / "site")),
        )
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}/"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def test_typing_and_four_layers(self):
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                page = browser.new_page()
                page.goto(self.url, wait_until="load")
                page.wait_for_function(
                    "document.querySelector('#status').classList.contains('ready')",
                    timeout=30000,
                )
                self.assertEqual(page.locator("[data-layer]").count(), 4)
                self.assertGreater(page.locator("#keyboard .keyboard-key").count(), 45)
                page.locator("[data-layer='2']").click()
                self.assertEqual(
                    page.locator("[data-layer='2']").get_attribute("aria-pressed"), "true"
                )
                page.locator("#keyboard .keyboard-key[data-code='KeyK']").click()
                self.assertEqual(page.locator("#key-details .inspector-output").count(), 4)
                self.assertIn("ক", page.locator("#key-details").inner_text())
                self.assertIn("খ", page.locator("#key-details").inner_text())
                self.assertEqual(
                    page.locator("#keyboard .keyboard-key[data-code='KeyJ'] .key-output").inner_text(),
                    "ZWJ",
                )
                page.locator("[data-layer='3']").click()
                self.assertEqual(
                    page.locator("[data-layer='3']").get_attribute("aria-pressed"), "true"
                )
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
                page.set_viewport_size({"width": 390, "height": 844})
                self.assertTrue(page.locator(".keyboard-scroll-hint").is_visible())
            finally:
                browser.close()

    def test_keyboard_reference_failure_keeps_typing_available(self):
        """A missing visualizer must not disable Keyman input."""
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                page = browser.new_page()
                page.route(
                    "**/layout.json",
                    lambda route: route.fulfill(
                        status=404, content_type="application/json", body="{}"
                    ),
                )
                page.goto(self.url, wait_until="load")
                page.wait_for_function(
                    "document.querySelector('#status-label').textContent.includes('Typing ready')",
                    timeout=30000,
                )
                self.assertIn(
                    "Reference unavailable", page.locator("#status-label").inner_text()
                )
                self.assertFalse(page.locator("#error-help").is_hidden())
                page.locator("#editor").focus()
                page.keyboard.press("k")
                self.assertEqual(page.locator("#editor").input_value(), "ক")
            finally:
                browser.close()
