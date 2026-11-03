"""Chromium smoke tests for typing and the four-layer keyboard interface."""
import json
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
                page.wait_for_function("document.querySelector('#status').classList.contains('ready')", timeout=30000)
                self.assertEqual(page.locator("[data-layer]").count(), 4)
                self.assertGreater(page.locator("#keyboard .keyboard-key").count(), 45)
                page.locator("[data-layer='2']").click()
                self.assertEqual(page.locator("[data-layer='2']").get_attribute("aria-pressed"), "true")
                page.locator("#keyboard .keyboard-key[data-code='KeyK']").click()
                self.assertEqual(page.locator("#key-details .inspector-output").count(), 4)
                self.assertIn("ক", page.locator("#key-details").inner_text())
                self.assertIn("খ", page.locator("#key-details").inner_text())
                self.assertEqual(page.locator("#keyboard .keyboard-key[data-code='KeyJ'] .key-output").inner_text(), "ZWJ")
                self.assertEqual(page.locator("#keyboard .keyboard-key[data-code='KeyK'] .key-output").inner_text(), "ক্ষ")
                self.assertEqual(page.locator("#keyboard .keyboard-key[data-code='KeyG'] .key-output").inner_text(), "জ্ঞ")
                self.assertEqual(page.locator("#keyboard .keyboard-key[data-code='KeyY'] .key-output").inner_text(), "ঈ")
                self.assertEqual(page.locator("#keyboard .keyboard-key[data-code='KeyH'] .key-output").inner_text(), "◌্")
                self.assertEqual(page.locator("#keyboard .keyboard-key[data-code='KeyD'] .key-output").inner_text(), "দ")
                self.assertEqual(page.locator("#keyboard .keyboard-key[data-code='KeyT'] .key-output").inner_text(), "—")
                page.locator("[data-layer='3']").click()
                self.assertEqual(page.locator("[data-layer='3']").get_attribute("aria-pressed"), "true")
                self.assertEqual(page.locator("#keyboard .keyboard-key[data-code='KeyD'] .key-output").inner_text(), "ধ")
                self.assertEqual(page.locator("#keyboard .keyboard-key[data-code='KeyT'] .key-output").inner_text(), "—")
                self.assertEqual(page.locator("#keyboard .keyboard-key[data-code='KeyJ'] .key-output").inner_text(), "ZWNJ")
                page.locator("[data-layer='0']").click()
                page.locator("#editor").focus()
                page.keyboard.press("k")
                self.assertEqual(page.locator("#editor").input_value(), "ক")
                page.keyboard.press("Backquote")
                page.keyboard.press("x")
                self.assertEqual(page.locator("#editor").input_value(), "ক্ষ")
                self.assertEqual(
                    page.locator("#keystroke-log kbd").all_inner_texts(),
                    ["k", "`", "x"],
                )
                page.keyboard.press("Shift+k")
                self.assertEqual(page.locator("#keystroke-log kbd").last.inner_text(), "K")
                # AltGr+A (and AltGr+Q) have no mapping and do not modify text.
                page.evaluate("""() => {
                    const editor = document.querySelector('#editor');
                    for (const code of ['KeyA', 'KeyQ']) {
                        for (const shift of [false, true]) {
                            editor.dispatchEvent(new KeyboardEvent('keydown', {
                                bubbles: true, key: code === 'KeyA' ? 'a' : 'q',
                                code, altKey: true, ctrlKey: true,
                                shiftKey: shift
                            }));
                        }
                    }
                }""")
                self.assertEqual(page.locator("#keystroke-log kbd").last.inner_text(), "K")
                self.assertEqual(page.locator("#keystroke-log kbd").count(), 4)
                # Emulate browsers that express AltGr through Ctrl+Alt.
                page.evaluate("""() => {
                    const editor = document.querySelector('#editor');
                    for (const [key, code, shift] of [['w', 'KeyW', false], ['D', 'KeyD', true]]) {
                        editor.dispatchEvent(new KeyboardEvent('keydown', {
                            bubbles: true, key, code,
                            altKey: true, ctrlKey: true, shiftKey: shift
                        }));
                    }
                }""")
                # Synthetic keydowns do not insert text: a synchronized
                # panel must never invent keystrokes for those events.
                self.assertEqual(
                    page.locator("#keystroke-log kbd").all_inner_texts(),
                    ["k", "`", "x", "K"],
                )
                # Synthetic modifier events above do not insert text.
                # Test Backspace against real text and real key tokens.
                page.locator("#clear").click()
                page.locator("#editor").fill("")
                page.locator("#editor").focus()
                page.keyboard.press("k")
                page.keyboard.press("Shift+k")
                self.assertEqual(page.locator("#keystroke-log kbd").all_inner_texts(), ["k", "K"])
                page.keyboard.press("Backspace")
                self.assertEqual(page.locator("#keystroke-log kbd").all_inner_texts(), ["k"])
                self.assertNotIn("⌫", page.locator("#keystroke-log").inner_text())
                page.keyboard.press("Backspace")
                page.keyboard.press("Backspace")
                self.assertEqual(page.locator("#keystroke-log kbd").count(), 0)
                self.assertTrue(page.locator("#keystroke-placeholder").is_visible())
                self.assertTrue(page.locator("#clear-keystrokes").is_disabled())
                page.keyboard.press("k")
                self.assertEqual(page.locator("#keystroke-log kbd").all_inner_texts(), ["k"])
                page.locator("#clear-keystrokes").click()
                self.assertEqual(page.locator("#keystroke-log kbd").all_inner_texts(), ["k"])
                page.locator("#clear").click()
                self.assertEqual(page.locator("#keystroke-log kbd").count(), 0)
                self.assertTrue(page.locator("#keystroke-placeholder").is_visible())
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
                page.route("**/layout.json", lambda route: route.fulfill(
                    status=404, content_type="application/json", body="{}"))
                page.goto(self.url, wait_until="load")
                page.wait_for_function(
                    "document.querySelector('#status-label').textContent.includes('Typing ready')",
                    timeout=30000)
                self.assertIn("Reference unavailable", page.locator("#status-label").inner_text())
                self.assertFalse(page.locator("#error-help").is_hidden())
                page.locator("#editor").focus()
                page.keyboard.press("k")
                self.assertEqual(page.locator("#editor").input_value(), "ক")
                # Without the keymap, display the actual Unicode character,
                # never an invented physical keystroke.
                self.assertEqual(page.locator("#keystroke-log kbd").all_inner_texts(), ["ক"])
                self.assertIn("Unmapped character", page.locator("#keystroke-log kbd").first.get_attribute("aria-label"))
            finally:
                browser.close()

    def test_keystroke_history_checks_all_four_layers(self):
        """Only actual editor output creates tokens; every layer is supported."""
        from playwright.sync_api import sync_playwright

        layout = json.loads((ROOT / "site/layout.json").read_text(encoding="utf-8"))
        for code, layer in [
            ("KeyQ", 0), ("KeyS", 1), ("KeyA", 2), ("KeyW", 3)
        ]:
            layout["keys"][code][layer] = None

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                page = browser.new_page()
                page.route("**/layout.json", lambda route: route.fulfill(
                    status=200, content_type="application/json",
                    body=json.dumps(layout, ensure_ascii=False)
                ))
                page.goto(self.url, wait_until="load")
                page.wait_for_function(
                    "document.querySelector('#status').classList.contains('ready')",
                    timeout=30000,
                )
                # A keydown without a text mutation isn't a typed character.
                page.evaluate("""() => {
                    const editor = document.getElementById('editor');
                    editor.focus();
                    const send = (code, shift = false, altgr = false) =>
                        editor.dispatchEvent(new KeyboardEvent('keydown', {
                            bubbles: true, code, key: code.slice(3).toLowerCase(),
                            shiftKey: shift, ctrlKey: altgr, altKey: altgr
                        }));
                    send('KeyQ');
                    send('KeyS', true);
                    send('KeyA', false, true);
                    send('KeyW', true, true);
                    send('KeyK');
                }""")
                self.assertEqual(page.locator("#keystroke-log kbd").count(), 0)

                # Each assigned layer is recognized when its output actually
                # appears in the editor.
                page.evaluate("""() => {
                    const editor = document.getElementById('editor');
                    const insert = (code, text, shift = false, altgr = false) => {
                        editor.dispatchEvent(new KeyboardEvent('keydown', {
                            bubbles: true, code, key: code.slice(3).toLowerCase(),
                            shiftKey: shift, ctrlKey: altgr, altKey: altgr
                        }));
                        editor.value += text;
                        editor.dispatchEvent(new InputEvent('input', {
                            bubbles: true, inputType: 'insertText', data: text
                        }));
                    };
                    insert('KeyK', 'ক');
                    insert('KeyQ', 'ধ', true);
                    insert('KeyW', 'ৱ', false, true);
                    insert('KeyD', 'ধ', true, true);
                }""")
                self.assertEqual(
                    page.locator("#keystroke-log kbd").all_inner_texts(),
                    ["k", "Q", "⇮w", "⇮D"],
                )
                self.assertEqual(page.locator("#editor").input_value(), "কধৱধ")
            finally:
                browser.close()

    def test_replacing_or_editing_text_resets_keystroke_history(self):
        """The panel must not retain keys from text replaced with Ctrl+A."""
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
                page.locator("#editor").focus()
                page.keyboard.press("k")
                page.keyboard.press("Shift+k")
                self.assertEqual(page.locator("#editor").input_value(), "কখ")
                self.assertEqual(page.locator("#keystroke-log kbd").all_inner_texts(), ["k", "K"])

                # Ctrl+A is a selection, not a new keystroke. Replacing the
                # selected text should discard the previously recorded keys.
                page.keyboard.press("Control+a")
                page.keyboard.press("q")
                self.assertEqual(page.locator("#editor").input_value(), "দ")
                self.assertEqual(page.locator("#keystroke-log kbd").all_inner_texts(), ["q"])

                # Backspace at the start deletes nothing; history stays put.
                page.keyboard.press("Home")
                page.keyboard.press("Backspace")
                self.assertEqual(page.locator("#editor").input_value(), "দ")
                self.assertEqual(page.locator("#keystroke-log kbd").all_inner_texts(), ["q"])

                # Editing at the beginning invalidates the previous sequence.
                page.keyboard.press("k")
                self.assertEqual(page.locator("#editor").input_value(), "কদ")
                self.assertEqual(page.locator("#keystroke-log kbd").all_inner_texts(), ["k"])

                # Forward Delete removes text without a character keystroke.
                page.keyboard.press("Delete")
                self.assertEqual(page.locator("#editor").input_value(), "ক")
                self.assertEqual(page.locator("#keystroke-log kbd").count(), 0)

                # Pasting also changes the text without a physical key.
                page.locator("#editor").focus()
                page.keyboard.press("k")
                self.assertEqual(page.locator("#keystroke-log kbd").all_inner_texts(), ["k"])
                page.evaluate("""() => {
                    const editor = document.querySelector('#editor');
                    editor.dispatchEvent(new Event('paste', { bubbles: true }));
                    editor.value = 'পেস্ট';
                    editor.dispatchEvent(new InputEvent('input', {
                        bubbles: true, inputType: 'insertFromPaste', data: 'পেস্ট'
                    }));
                }""")
                self.assertEqual(page.locator("#keystroke-log kbd").count(), 0)
                self.assertTrue(page.locator("#keystroke-placeholder").is_visible())
            finally:
                browser.close()
