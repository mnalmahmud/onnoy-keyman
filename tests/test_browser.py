"""Optional Chromium smoke test of compiled web typing and diagram."""
import os
import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

@unittest.skipUnless(os.environ.get("RUN_BROWSER_TESTS") == "1", "Browser test is opt-in")
class BrowserSmoke(unittest.TestCase):
    def test_typing(self):
        from playwright.sync_api import sync_playwright
        server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT / "site")))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                page = browser.new_page()
                page.goto(f"http://127.0.0.1:{server.server_port}/", wait_until="load")
                page.wait_for_function("document.querySelector('#status').textContent.includes('Ready — Onnoy')")
                page.locator("#editor").focus()
                page.keyboard.press("k")
                self.assertEqual(page.locator("#editor").input_value(), "ক")
                page.keyboard.press("Backquote")
                page.keyboard.press("x")
                self.assertEqual(page.locator("#editor").input_value(), "ক্ষ")
                page.wait_for_function("document.querySelector('x-keyboard').layout.keyMap.KeyK?.[0] === 'ক'")
                browser.close()
        finally:
            server.shutdown()
            server.server_close()
