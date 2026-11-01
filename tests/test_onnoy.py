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
            ("M","shift_altgr"):"𑷰", ("W","altgr"):"ৱ",
            ("N","altgr"):"ঞ", ("4","shift"):"৳",
            ("4","shift_altgr"):"$"
        }
        for (key,layer), output in cases.items():
            with self.subTest(key=key,layer=layer):
                self.assertEqual(a[key][LAYERS.index(layer)],output)

    def test_symbol_and_alpha_omissions(self):
        a=resolve()
        self.assertEqual(a["Q"][2:], (None,None))
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

    def test_browser_visualizer_data(self):
        ref=json.loads(web.render(self.map))
        self.assertEqual(ref["keys"]["KeyJ"][2],"‍")
        self.assertEqual(ref["keys"]["KeyZ"][1],"য়")
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
