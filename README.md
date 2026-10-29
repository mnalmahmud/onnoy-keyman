# Onnoy (অন্বয়)

A fixed, Unicode Bengali-script keyboard layout for physical US-QWERTY keys. **One source of truth:** [`layout/onnoy.json`](layout/onnoy.json). The Linux, macOS, Windows and Keyman sources are all generated from it.

**[Try Onnoy in your browser](https://mnalmahmud.github.io/onnoy-keyman/)** · [Builds](https://github.com/mnalmahmud/onnoy-keyman/actions) · [Issues](https://github.com/mnalmahmud/onnoy-keyman/issues)

## What works

| Platform | Output | Status |
| --- | --- | --- |
| Browser | KeymanWeb (`onnoy.js`) | Compiled in CI; physical-key input is intended for desktop browsers |
| Linux | XKB + XCompose (`dist/linux/Onnoy.XCompose`) | Native shortcuts for multi-character output; application support must be tested |
| macOS | Native `.keylayout` | Generated and XML-validated in CI; installed input source must be tested |
| Windows | `.klc` source | Includes ligature entries; must be compiled and tested with MSKLC; **not an installer** |
| Keyman desktop | `.kmp` package | Compiled in CI; requires Keyman and target-OS testing |

CI artifacts (including the Linux Compose file) are downloadable from a successful [workflow run](https://github.com/mnalmahmud/onnoy-keyman/actions). There are currently no published GitHub Releases. A successful CI build does not certify that a layout installs correctly on every operating system.

## Keyboard layout

The 26 letter positions, 10 number positions and period key have four layers: Base, Shift, AltGr (Right Alt / macOS Option) and Shift+AltGr. Unassigned outputs are `null` in [the canonical mapping](layout/onnoy.json); they do not imply ASCII fallback on every platform.

The [canonical layout definition](layout/onnoy.json) lists every assignment. Q carries ড/ঢ/ড়/ঢ় and W carries ট/ঠ, keeping each consonant family together while placing the more frequent ট/ঠ on W. In particular, the vowel groups are E (ে এ ৈ ঐ), I (ি ই ী ঈ), U (ু উ ূ ঊ) and O (ো ও ৌ ঔ). F produces virama (্); Shift+F produces nukta (়). The number row yields Bengali digits; AltGr gives ASCII digits. Shift+4 gives ৳ and AltGr+Shift+4 gives $. The period key yields । (base), > (Shift), and . (AltGr).

**Approved shortcuts:** Shift+X → ক্ষ (ক + ্ + ষ), AltGr+G → জ্ঞ (জ + ্ + ঞ), AltGr+Y → য-ফলা (্ + য). The default ya-phala sequence does not include ZWJ.

**Linux, no Keyman required:** The generator creates both `dist/linux/symbols/onnoy` and `dist/linux/Onnoy.XCompose`. The XKB symbols assign internal F13–F15 keysyms to these shortcuts; the Compose file maps them to full Unicode strings. Keysyms are generated in physical-key order, rather than shortcut approval order. Merge the Onnoy Compose rules into `~/.XCompose` (keeping `include "%L"` if appropriate), and reload/restart applications to make them effective. Compose processing varies among desktop environments, Wayland compositors and applications, so verify on your Linux setup. F13–F15 should be reserved for Onnoy; software using those function keys may conflict.

**Windows:** the KLC contains `%%` entries and corresponding `LIGATURE` rules for these sequences; MSKLC compatibility must be verified on Windows. macOS emits the Unicode strings directly. Keyman supports these sequences, too.

The [browser playground](https://mnalmahmud.github.io/onnoy-keyman/) displays **all four layers** and shows the Unicode code points of text entered into its editor. ZWNJ (U+200C) and ZWJ (U+200D) are invisible characters, not blank assignments.

## Install or test

- **Browser:** Open the playground in a desktop browser. It loads the compiled Keyman keyboard; if the remote engine fails, ordinary typing and the visual key reference remain usable.
- **Linux (XKB):** Copy `dist/linux/symbols/onnoy` into the relevant XKB symbols directory, then register `onnoy(basic)` in your desktop's XKB configuration. Desktop layout registration differs across distributions.
- **macOS:** Copy `dist/macos/Onnoy.keylayout` to `~/Library/Keyboard Layouts/`, log out and back in if necessary, then enable Onnoy from **System Settings → Keyboard → Input Sources**.
- **Windows:** `dist/windows/onnoy.klc` is *source* for Microsoft Keyboard Layout Creator (MSKLC). Compile and test it using MSKLC; no native installer is provided.
- **Keyman desktop:** The generated `build/onnoy.kmp` is a Keyman package, not a native Windows installer. It requires a compatible Keyman runtime.

## Development

Prerequisites: Python 3 and Node.js. Building Keyman additionally requires [Keyman Developer CLI 18](https://keyman.com/developer/). The generator itself has no third-party Python dependencies.

```sh
python3 scripts/generate.py
python3 scripts/generate.py --check
python3 -m unittest discover -s tests -p 'test_layout.py'
npm install -g @keymanapp/kmc@18
bash scripts/build.sh
```

`generate.py` produces:

```text
source/onnoy.kmn              Keyman keyboard source
dist/linux/symbols/onnoy      Linux XKB
dist/linux/Onnoy.XCompose     Linux Unicode sequence shortcuts
dist/macos/Onnoy.keylayout    macOS native input source
dist/windows/onnoy.klc        Windows MSKLC source
```

`build.sh` compiles `build/onnoy.kmx`, `build/onnoy.js` and `build/onnoy.kmp`. Both `dist/` and `build/` are generated and ignored by Git.

To stage the test website locally:

```sh
mkdir -p site
cp web/index.html web/app.js web/style.css build/onnoy.js site/
cp layout/onnoy.json site/layout.json
python3 -m http.server 8000 --directory site
```

Browse to http://localhost:8000. Optional real-browser smoke tests use Python Playwright and Chromium:

```sh
python3 -m pip install playwright==1.56.0
python3 -m playwright install chromium
python3 -m unittest discover -s tests -p 'test_browser.py'
```

## Contributing

Make mapping edits **only** in `layout/onnoy.json`; regenerate and test all affected platforms. Do not edit generated sources directly. See [CONTRIBUTING.md](CONTRIBUTING.md) and [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md). When reporting a bug, include the operating system, application, physical key, modifiers, expected Unicode and actual Unicode.

MIT licensed. Copyright © 2026 Muhtasham Nawr al-Mahmud. See [LICENSE](LICENSE).
