"""End-to-end KeymanWeb typing using the generated website and keyboard."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*_args):
        pass

def main():
    handler=partial(QuietHandler,directory=str(ROOT/"site"))
    server=ThreadingHTTPServer(("127.0.0.1",0),handler)
    thread=Thread(target=server.serve_forever,daemon=True)
    thread.start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            page=browser.new_page()
            errors=[]
            page.on("pageerror",lambda error:errors.append(str(error)))
            page.goto(f"http://127.0.0.1:{server.server_port}/")
            page.wait_for_function(
                "() => document.getElementById('status-label').textContent === 'KeymanWeb ready'",
                timeout=45000)
            assert page.locator('#keyboard .keyboard-key').count() > 35, "Visualizer did not load"
            page.select_option("#geometry","iso")
            assert page.locator('button.keyboard-key[data-key="§"]').count() == 1
            page.select_option("#geometry","ansi")
            assert page.locator('button.keyboard-key[data-key="§"]').count() == 0
            page.locator("#editor").focus()
            page.keyboard.press("k")
            page.wait_for_function("() => document.getElementById('editor').value === 'ক'")
            page.keyboard.press("Shift+z")
            page.wait_for_function("() => document.getElementById('editor').value === 'কয়'")
            assert not errors, errors
            print("KeymanWeb typing and generated visualizer passed")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
if __name__=="__main__": main()
