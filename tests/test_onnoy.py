"""Unit regressions plus optional compiled-package and browser integration checks."""

import copy
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import unittest
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import ctypes
import os
import subprocess
import tempfile

from onnoy.backends import keyman, linux, macos, touch, web, windows
from onnoy.hardware import ALPHABET, BROWSER, ISO_EXTRA, KEYMAN, LAYERS, MAC, STANDARD, WINDOWS, XKB
from onnoy.model import load, resolve, validate
from tools.benchmark import onnoy as benchmark_layout

ROOT = Path(__file__).resolve().parents[1]


class MappingContractTests(unittest.TestCase):
    def test_sparse_schema(self):
        data = load()
        self.assertNotIn("passthrough", data)
        self.assertEqual(set(data), {"name","keys"})
        for fields in data["keys"].values():
            self.assertTrue(set(fields) <= set(LAYERS))
            self.assertNotIn(None, fields.values())

    def test_approved_sequences(self):
        a = resolve(geometry="ansi")
        cases = {
            ("GRAVE","base"):"্", ("GRAVE","shift"):"~",
            ("GRAVE","altgr"):"`", ("SLASH","base"):"/",
            ("SLASH","shift"):"?", ("COMMA","base"):",",
            ("COMMA","shift"):"<", ("S","shift"):"শ",
            ("X","base"):"ষ", ("X","shift"):"ঢ়",
            ("Z","shift"):"য়", ("Y","altgr"):"য়",
            ("J","altgr"):"‍", ("J","shift_altgr"):"‌",
            ("L","altgr"):"়", ("B","altgr"):"ৰ",
            ("V","altgr"):"ৱ",
            ("M","shift_altgr"):"𑷰",
            ("N","altgr"):"ঞ", ("4","shift"):"৳",
            ("4","shift_altgr"):"$"
        }
        for (key,layer), output in cases.items():
            with self.subTest(key=key,layer=layer):
                self.assertEqual(a[key][LAYERS.index(layer)],output)

    def test_symbol_and_alpha_omissions(self):
        a=resolve()
        self.assertEqual(a["Q"][2:], (None,None))
        self.assertEqual(a["W"][2:], (None, None))
        self.assertEqual(a["COMMA"], (",","<",None,None))
        self.assertEqual(a["SLASH"], ("/","?",None,None))
        self.assertEqual(a["MINUS"], ("-","_",None,None))
        self.assertEqual(a["SPACE"], (" "," "," "," "))
        self.assertNotIn(ISO_EXTRA,a)

    def test_iso(self):
        a=resolve(geometry="ansi")
        iso=resolve(geometry="iso")
        self.assertEqual(iso[ISO_EXTRA], ("\\","|",None,None))
        for key in STANDARD:
            self.assertEqual(a[key],iso[key])

    def test_reject_bad_scalars(self):
        d=load()
        for bad in (None,"", "abc", "\ud800"):
            clone=copy.deepcopy(d)
            clone["keys"]["J"]["base"]=bad
            with self.assertRaises(ValueError):
                validate(clone)

    def test_physical_tables_cover_all_positions(self):
        for target in (XKB,WINDOWS,MAC,KEYMAN,BROWSER):
            self.assertEqual(set(target), set(STANDARD)|{ISO_EXTRA})


def emit(*chords):
    mapping=resolve()
    result=[]
    for chord in chords:
        parts=chord.split("+")
        key=parts[-1]
        layer=(("Shift" in parts)*1)+(("AltGr" in parts)*2)
        value=mapping[key][layer]
        if value is not None:
            result.append(value)
    return "".join(result)

class TypingCases(unittest.TestCase):
    def test_bengali_words(self):
        cases={
            ("K","GRAVE","X"):"ক্ষ",
            ("Shift+S","I","K","GRAVE","X","A"):"শিক্ষা",
            ("B","A","AltGr+M","L","A"):"বাংলা",
            ("R","AltGr+J","GRAVE","Z"):"র‍্য",
            ("K","GRAVE","Shift+AltGr+J","X"):"ক্‌ষ",
            ("Shift+4","4","AltGr+PERIOD","5","0"):"৳৪.৫০",
            ("D","AltGr+L"):"ড়",
            ("Shift+D","AltGr+L"):"ঢ়",
        }
        for chords, expected in cases.items():
            with self.subTest(chords=chords):
                self.assertEqual(emit(*chords),expected)
    def test_alias_codepoint_exact(self):
        self.assertEqual(emit("Shift+Z"),chr(0x09DF))
        self.assertEqual(emit("AltGr+Y"),chr(0x09DF))
        self.assertEqual(emit("Shift+AltGr+M"),chr(0x11DF0))
        self.assertEqual(emit("AltGr+J"),chr(0x200D))
        self.assertEqual(emit("Shift+AltGr+J"),chr(0x200C))
    def test_punctuation_and_no_output(self):
        self.assertEqual(emit("SLASH","Shift+SLASH"),"/?")
        self.assertEqual(emit("COMMA","Shift+COMMA"),",<")
        self.assertEqual(emit("GRAVE","AltGr+GRAVE"),"্`")
        self.assertEqual(emit("AltGr+Z"),"")


class NativeLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map=resolve(load(), "iso")

    def test_xkb_iso_grave_and_layers(self):
        symbols=linux.render(self.map)
        self.assertIn('include "us(basic)"',symbols)
        self.assertIn('key <LSGT> { type[Group1]="FOUR_LEVEL", symbols[Group1]=[ U005C, U007C',symbols)
        self.assertIn('key <TLDE> { type[Group1]="FOUR_LEVEL", symbols[Group1]=[ U09CD, U007E, U0060',symbols)
        self.assertIn('key <AC07> { type[Group1]="FOUR_LEVEL", symbols[Group1]=[ U099C, U099D, U200D, U200C',symbols)
        self.assertIn('key <AC09> { type[Group1]="FOUR_LEVEL", symbols[Group1]=[ U09B2, U0981, U09BC',symbols)

    def test_windows_unicode_and_utf16_surrogates(self):
        text=windows.render(self.map)
        self.assertIn("29\tOEM_3\t0\t09cd\t007e\t-1\t0060",text)
        self.assertIn("56\tOEM_102\t0\t005c\t007c",text)
        self.assertIn("LIGATURE",text)
        # U+11DF0 is the surrogate pair D807 DDF0.
        self.assertIn("d807 ddf0",text.lower())

    def test_macos_self_contained(self):
        source=macos.render(self.map)
        root=ET.fromstring(source.split("\n",2)[2])
        self.assertIsNone(root.find("./keyMapSet[@id='OnnoyUSBase']"))
        keys=root.findall("./keyMapSet[@id='OnnoyMap']/keyMap")
        self.assertEqual(len(keys),6)
        def output(layer,code):
            return keys[layer].find(f"./key[@code='{code}']").get("output")
        self.assertEqual(output(0,50),"্")
        self.assertEqual(output(2,50),"`")
        self.assertEqual(output(0,10),"\\")
        self.assertEqual(output(1,10),"|")
        self.assertEqual(output(2,38),"‍")
        self.assertEqual(output(3,38),"‌")
        self.assertEqual(output(4,38),"j")

    def test_keyman_physical_rules(self):
        source=keyman.render(self.map)
        self.assertIn("+ [RALT K_J] > U+200D",source)
        self.assertIn("+ [SHIFT RALT K_J] > U+200C",source)
        self.assertIn("+ [RALT K_COLON] > U+003B",source)
        self.assertIn("+ [K_oE2] > U+005C",source)
        self.assertIn("+ [RALT K_Z] > nul",source)
        self.assertIn("+ [RALT K_V] > U+09F1", source)
        self.assertIn("+ [RALT K_W] > nul", source)

    def test_browser_visualizer_data(self):
        ref=json.loads(web.render(self.map))
        self.assertEqual(ref["keys"]["KeyJ"][2],"‍")
        self.assertEqual(ref["keys"]["KeyZ"][1],"য়")
        self.assertEqual(ref["keys"]["KeyV"][2], "ৱ")
        self.assertIsNone(ref["keys"]["KeyW"][2])
        self.assertEqual(ref["keys"]["IntlBackslash"][0],"\\")


class BuildTests(unittest.TestCase):
    def test_source_files_exist(self):
        for rel in ("dist/linux/symbols/onnoy","dist/macos/Onnoy.keylayout",
                    "dist/windows/onnoy.klc","dist/keyman/onnoy.kmn",
                    "dist/web/layout.json"):
            with self.subTest(rel=rel):
                f=ROOT/rel
                self.assertTrue(f.is_file())
                self.assertGreater(f.stat().st_size,100)

    def test_generated_macos_xml(self):
        root=ET.parse(ROOT/"dist/macos/Onnoy.keylayout").getroot()
        self.assertEqual(root.tag,"keyboard")
        self.assertEqual(len(root.findall("./keyMapSet[@id='OnnoyMap']/keyMap")),6)

    def test_benchmark_uses_printable_physical_key_names(self):
        layout = benchmark_layout()
        for key in ("\\", "`", "-", "=", "[", "]", ";", "'", ",", ".", "/", " "):
            self.assertIn(key, layout)
        self.assertNotIn("GRAVE", layout)
        self.assertEqual(layout["`"][0], "্")


class BrowserIntegrationSourceTests(unittest.TestCase):
    def test_uses_keymanweb_instead_of_second_translator(self):
        script=(ROOT/"web/app.js").read_text(encoding="utf-8")
        html=(ROOT/"web/index.html").read_text(encoding="utf-8")
        self.assertIn("engine.addKeyboards",script)
        self.assertIn("engine.setActiveKeyboard",script)
        self.assertIn("layout.keys",script)
        self.assertNotIn("function translateKey(",script)
        self.assertIn("keymanweb.js",html)
        self.assertNotIn("docs/install-", html)


class MobileTouchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping = resolve(load(), "iso")
        cls.layout = touch.render_data(cls.mapping)
        cls.layers = {
            layer["id"]: layer for layer in cls.layout["phone"]["layer"]
        }

    @staticmethod
    def flattened(layer):
        return [key for row in layer["row"] for key in row["key"]]

    @staticmethod
    def outputs(layer):
        return {
            key["id"] for key in MobileTouchTests.flattened(layer)
        } | {
            popup["id"]
            for key in MobileTouchTests.flattened(layer)
            for popup in key.get("sk", [])
        }

    def test_standard_three_phone_layers(self):
        self.assertEqual(set(self.layers), {"default", "shift", "numeric"})
        for layer in self.layers.values():
            self.assertEqual(len(layer["row"]), 4)
        self.assertEqual(
            [len(row["key"]) for row in self.layers["default"]["row"]],
            [10,9,9,7])
        self.assertEqual(
            [len(row["key"]) for row in self.layers["numeric"]["row"]],
            [10,10,10,7])

    def test_alphabet_keys_resolve_canonical_outputs(self):
        for layer_name, idx in (("default",0), ("shift",1)):
            for key in self.flattened(self.layers[layer_name]):
                if key["id"] not in {f"K_{letter}" for letter in ALPHABET}:
                    continue
                physical = key["id"].removeprefix("K_")
                output = self.mapping[physical][idx]
                self.assertEqual(key["text"],touch.caption(output))
                if idx:
                    self.assertEqual(key.get("layer"),"shift")

    def test_explicit_source_characters_are_all_reachable(self):
        # Primary virtual keys carry canonical Base/Shift outputs via KMN.
        # Direct U_xxxx keys include long-press alternatives and symbols.
        all_keys = set()
        for layer in self.layers.values():
            all_keys |= self.outputs(layer)
        reachable = {
            self.mapping[key][layer]
            for layer, _ in ((0,"base"),(1,"shift"))
            for key in ALPHABET
            if self.mapping[key][layer] is not None
        }
        reachable |= {
            chr(int(code[2:],16))
            for code in all_keys if code.startswith("U_")
        }
        expected = {
            value for mapping in load()["keys"].values()
            for value in mapping.values()
        }
        self.assertFalse(expected - reachable, f"Missing touch characters: {expected-reachable!r}")

    def test_critical_onscreen_keys(self):
        base=self.flattened(self.layers["default"])
        self.assertIn("U_09CD",{key["id"] for key in base})
        self.assertIn("K_SPACE",{key["id"] for key in base})
        self.assertIn("K_BKSP",{key["id"] for key in base})
        self.assertIn("K_ENTER",{key["id"] for key in base})
        for layer in self.layers.values():
            self.assertIn("K_LOPT",{key["id"] for key in self.flattened(layer)})
        self.assertTrue(any(k.get("nextlayer")=="numeric" for k in base))
        self.assertTrue(any(k.get("nextlayer")=="default" for k in self.flattened(self.layers["numeric"])))
        self.assertTrue(any(k.get("nextlayer")=="shift" for k in base))

    def test_joiners_nukta_assamese_and_supplementary(self):
        keys=set()
        for layer in self.layers.values():
            keys |= self.outputs(layer)
        for value in ("\u200D","\u200C","়","ৰ","ৱ","𑷰"):
            self.assertIn(touch.unicode_key(value),keys)

    def test_digits_and_ascii_fallbacks(self):
        numeric = self.layers["numeric"]
        all_keys=self.outputs(numeric)
        for ascii_digit in "0123456789":
            self.assertIn(touch.unicode_key(ascii_digit), all_keys)
        for bengali_digit in "০১২৩৪৫৬৭৮৯":
            self.assertIn(touch.unicode_key(bengali_digit), all_keys)

    def test_unicode_popups_not_alternative_character_source(self):
        rendered=json.loads(touch.render(self.mapping))
        self.assertEqual(rendered,self.layout)
        self.assertIn("store(&layoutfile) 'onnoy.keyman-touch-layout'",keyman.render(self.mapping))
        for layer in self.layers.values():
            for key in self.flattened(layer):
                self.assertTrue(key["id"].startswith(("K_","U_")))
                for popup in key.get("sk",[]):
                    self.assertTrue(popup["id"].startswith(("K_","U_")))

# Compiled Keyman package checks

PACKAGE = ROOT / "dist" / "keyman" / "onnoy.kmp"

def verify_mobile_package():
    assert PACKAGE.is_file(), "Missing compiled .kmp package"
    with ZipFile(PACKAGE) as archive:
        files = {name.rsplit("/",1)[-1]:name for name in archive.namelist()}
        for expected in ("onnoy.js","onnoy.kmx","kmp.json"):
            assert expected in files, f"Missing {expected} from mobile Keyman package"
        metadata=json.loads(archive.read(files["kmp.json"]).decode("utf-8-sig"))
        assert metadata.get("keyboards"), "Package does not declare a keyboard"
        javascript=archive.read(files["onnoy.js"])
        assert b"phone" in javascript, "Compiled mobile keyboard does not contain a phone layout"
        print("Validated KMP: desktop keyboard, mobile JS, embedded phone layout, metadata")

# Real KeymanWeb typing checks

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*_args):
        pass

def browser_smoke():
    from playwright.sync_api import sync_playwright
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
            try:
                page.locator('#keyboard .keyboard-key').first.wait_for(timeout=20000)
            except Exception as error:
                print("Keyboard status:", page.locator("#status-label").inner_text())
                print("Keyboard content:", page.locator("#keyboard").inner_text())
                print("Error detail:", page.locator("#error-detail").inner_text())
                print("Browser errors:",errors)
                raise AssertionError("Visualizer did not load") from error
            assert page.locator('#keyboard .keyboard-key').count() > 35, "Incomplete visualizer"
            page.select_option("#geometry","iso")
            assert page.locator('button.keyboard-key[data-key="§"]').count() == 1
            page.select_option("#geometry","ansi")
            assert page.locator('button.keyboard-key[data-key="§"]').count() == 0

            # Desktop editor and visual keyboard share the same horizontal row.
            bounds = page.evaluate("""() => {
                const editor = document.querySelector('.editor-pane').getBoundingClientRect();
                const keys = document.querySelector('.keyboard-pane').getBoundingClientRect();
                return { editorX: editor.x, keysX: keys.x, editorY: editor.y, keysY: keys.y };
            }""")
            assert bounds["keysX"] > bounds["editorX"], bounds
            assert abs(bounds["keysY"] - bounds["editorY"]) < 3, bounds

            # The selector exposes the canonical four layers, including relocated Assamese wa.
            page.locator('button.layer[data-layer="2"]').click()
            assert page.locator('button.keyboard-key[data-key="V"] .key-output').inner_text() == "ৱ"
            assert page.locator('button.keyboard-key[data-key="W"] .key-output').inner_text() == "—"
            page.locator('button.layer[data-layer="0"]').click()
            assert page.locator('button.keyboard-key[data-key="V"] .key-output').inner_text() == "অ"

            # Intercept editor key events as KeymanWeb may: the visualizer must
            # update immediately even when a downstream listener stops propagation.
            page.locator("#editor").focus()
            page.evaluate("""() => {
                const editor = document.getElementById('editor');
                editor.addEventListener('keydown', event => {
                    if (event.key === 'Shift' || event.code === 'AltRight') event.stopPropagation();
                });
                editor.addEventListener('keyup', event => {
                    if (event.key === 'Shift' || event.code === 'AltRight') event.stopPropagation();
                });
            }""")
            # The editor retains focus while we switch preview layers;
            # KeymanWeb must not prevent the visual keycaps from rendering.
            page.evaluate("""() => document.querySelector('[data-layer="2"]').click()""")
            assert page.locator('button.keyboard-key[data-key="V"] .key-output').inner_text() == "ৱ"
            page.evaluate("""() => document.querySelector('[data-layer="0"]').click()""")
            assert page.locator('button.keyboard-key[data-key="V"] .key-output').inner_text() == "অ"
            assert page.locator("#editor").evaluate("(element) => document.activeElement === element")

            # Physical modifiers must change the visual layer and restore it on release.
            page.keyboard.down("Shift")
            assert page.locator('button.keyboard-key[data-key="S"] .key-output').inner_text() == "শ"
            page.keyboard.up("Shift")
            assert page.locator('button.keyboard-key[data-key="S"] .key-output').inner_text() == "স"
            page.evaluate("""() => document.getElementById('editor').dispatchEvent(
                new KeyboardEvent('keydown', {key:'AltGraph', code:'AltRight', altKey:true, bubbles:true})
            )""")
            assert page.locator('button.keyboard-key[data-key="V"] .key-output').inner_text() == "ৱ"
            page.evaluate("""() => document.getElementById('editor').dispatchEvent(
                new KeyboardEvent('keyup', {key:'AltGraph', code:'AltRight', bubbles:true})
            )""")
            assert page.locator('button.keyboard-key[data-key="V"] .key-output').inner_text() == "অ"
            # Both modifiers held together must show the fourth layer.
            page.keyboard.down("Shift")
            page.evaluate("""() => document.getElementById('editor').dispatchEvent(
                new KeyboardEvent('keydown', {key:'AltGraph', code:'AltRight',
                  shiftKey:true, altKey:true, bubbles:true})
            )""")
            assert page.locator("#modifier-indicator").inner_text() == "SHIFT + ALTGR"
            page.evaluate("""() => document.getElementById('editor').dispatchEvent(
                new KeyboardEvent('keyup', {key:'AltGraph', code:'AltRight',
                  shiftKey:true, bubbles:true})
            )""")
            page.keyboard.up("Shift")
            assert page.locator("#modifier-indicator").inner_text() == "BASE"

            # Physical characters highlight as soon as pressed inside the editor.
            # The most recent key remains selected after release; no click required.
            page.locator("#editor").focus()
            page.keyboard.down("k")
            key_k = page.locator('button.keyboard-key[data-key="K"]')
            assert "pressed" in key_k.get_attribute("class").split()
            assert key_k.get_attribute("aria-pressed") == "true"
            page.keyboard.up("k")
            assert "pressed" not in key_k.get_attribute("class").split()
            assert "selected" in key_k.get_attribute("class").split()
            page.keyboard.down("Shift")
            page.keyboard.down("v")
            key_v = page.locator('button.keyboard-key[data-key="V"]')
            assert "pressed" in key_v.get_attribute("class").split()
            assert key_v.locator(".key-output").inner_text() == "ৗ"
            page.keyboard.up("v")
            page.keyboard.up("Shift")
            assert "selected" in key_v.get_attribute("class").split()
            assert key_v.locator(".key-output").inner_text() == "অ"

            # Clicking the visual keyboard selects a key without typing text.
            page.locator('button.keyboard-key[data-key="B"]').click()
            key_b = page.locator('button.keyboard-key[data-key="B"]')
            assert "selected" in key_b.get_attribute("class").split()
            assert key_b.get_attribute("aria-pressed") == "true"

            # Theme follows System initially, supports explicit Light/Dark, and persists.
            assert page.locator("#theme").input_value() == "system"
            page.select_option("#theme", "dark")
            assert page.locator("html").get_attribute("data-theme") == "dark"
            page.reload()
            page.wait_for_function(
                "() => document.getElementById('status-label').textContent === 'KeymanWeb ready'",
                timeout=45000)
            assert page.locator("#theme").input_value() == "dark"
            page.select_option("#theme", "light")
            assert page.locator("html").get_attribute("data-theme") == "light"
            page.select_option("#theme", "system")
            assert page.locator("html").get_attribute("data-theme") is None

            # The panes stack on mobile instead of overflowing the page.
            page.set_viewport_size({"width": 420, "height": 900})
            bounds = page.evaluate("""() => {
                const editor = document.querySelector('.editor-pane').getBoundingClientRect();
                const keys = document.querySelector('.keyboard-pane').getBoundingClientRect();
                return { editorBottom: editor.bottom, keysTop: keys.top };
            }""")
            assert bounds["keysTop"] >= bounds["editorBottom"], bounds
            page.set_viewport_size({"width": 1280, "height": 720})
            page.locator("#editor").focus()
            # KeymanWeb must not show its own floating OSK over the page;
            # our visual keyboard is the only desktop keyboard reference.
            assert page.evaluate("""() =>
                !(window.matchMedia('(hover: hover) and (pointer: fine)').matches &&
                  window.keyman.osk.isEnabled())
            """), "KeymanWeb floating OSK was not disabled for desktop"
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

def windows_smoke():
    """Install, exercise, upgrade and uninstall a compiled native Windows keyboard."""
    if os.name != "nt":
        raise RuntimeError("Windows-only smoke test")
    import winreg

    package = ROOT / "build/windows/onnoy-windows-native.zip"
    if not package.is_file():
        raise AssertionError(f"Windows installer missing: {package}")
    with tempfile.TemporaryDirectory() as temp:
        with ZipFile(package) as archive:
            archive.extractall(temp)
        root = Path(temp)
        for name in ("setup.ps1", "x64/onnoy.dll", "x86/onnoy.dll"):
            if not (root / name).is_file():
                raise AssertionError(f"Missing installer component: {name}")

        setup = root / "setup.ps1"
        command = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(setup)]
        registry_path = r"SYSTEM\\CurrentControlSet\\Control\\Keyboard Layouts\\A0010845"
        installed = False
        hkl = None
        user32 = ctypes.WinDLL("user32", use_last_error=True)
        user32.LoadKeyboardLayoutW.argtypes = (ctypes.c_wchar_p, ctypes.c_uint)
        user32.LoadKeyboardLayoutW.restype = ctypes.c_void_p
        user32.UnloadKeyboardLayout.argtypes = (ctypes.c_void_p,)
        user32.UnloadKeyboardLayout.restype = ctypes.c_int
        user32.ToUnicodeEx.argtypes = (
            ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_wchar_p, ctypes.c_int, ctypes.c_uint, ctypes.c_void_p,
        )
        user32.ToUnicodeEx.restype = ctypes.c_int
        try:
            subprocess.run(command, check=True)
            installed = True
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
                if winreg.QueryValueEx(key, "Layout File")[0] != "onnoy.dll":
                    raise AssertionError("Unexpected installed keyboard DLL")
            hkl = user32.LoadKeyboardLayoutW("A0010845", 0x1)
            if not hkl:
                raise AssertionError(f"Windows failed to load Onnoy keyboard ({ctypes.get_last_error()})")

            def type_key(vk, scan, *, shift=False, altgr=False):
                state = (ctypes.c_ubyte * 256)()
                if shift:
                    state[0x10] = 0x80
                if altgr:
                    state[0x11] = 0x80
                    state[0x12] = 0x80
                buffer = ctypes.create_unicode_buffer(16)
                length = user32.ToUnicodeEx(vk, scan, state, buffer, 16, 0, hkl)
                if length <= 0:
                    raise AssertionError(f"ToUnicodeEx failed for VK {vk:02X}: {length}")
                return buffer[:length].encode("utf-16-le", "surrogatepass").decode("utf-16-le")

            cases = (
                ((0x4B, 0x25), {}, "ক"),
                ((0x53, 0x1F), {"shift": True}, "শ"),
                ((0xC0, 0x29), {}, "্"),
                ((0x4A, 0x24), {"altgr": True}, "\u200d"),
                ((0x4A, 0x24), {"shift": True, "altgr": True}, "\u200c"),
                ((0x4D, 0x32), {"shift": True, "altgr": True}, "\U00011df0"),
            )
            for (vk, scan), modifiers, expected in cases:
                actual = type_key(vk, scan, **modifiers)
                if actual != expected:
                    raise AssertionError(f"VK {vk:02X} output {actual!r}, expected {expected!r}")
            # Reinstalling the same package should be safe.
            subprocess.run(command, check=True)
            print("Windows installation, Unicode typing and reinstall passed")
        finally:
            if hkl:
                user32.UnloadKeyboardLayout(hkl)
            if installed:
                subprocess.run(command + ["-Uninstall"], check=True)
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path):
                    raise AssertionError("Windows keyboard registry entry remains after uninstall")
            except FileNotFoundError:
                pass
