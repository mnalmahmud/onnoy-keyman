# Onnoy (অন্বয়)

A fixed, Unicode Bengali-script keyboard layout for physical US-QWERTY keys. **One source of truth:** [`layout/onnoy.json`](layout/onnoy.json). The Linux, macOS, Windows and Keyman sources are all generated from it.

**[Try Onnoy in your browser](https://mnalmahmud.github.io/onnoy-keyman/)** · [Builds](https://github.com/mnalmahmud/onnoy-keyman/actions) · [Issues](https://github.com/mnalmahmud/onnoy-keyman/issues)

## What works

| Platform | Output | Status |
| --- | --- | --- |
| Browser | KeymanWeb (`onnoy.js`) | Compiled in CI; physical-key input is intended for desktop browsers |
| Linux | XKB (`dist/linux/symbols/onnoy`) | Generated and syntax-compiled in CI; desktop integration must be tested |
| macOS | Native `.keylayout` | Generated and XML-validated in CI; installed input source must be tested |
| Windows | `.klc` source | Generated only; **not an installer** |
| Keyman desktop | `.kmp` package | Compiled in CI; requires Keyman and target-OS testing |

CI artifacts are downloadable from a successful [workflow run](https://github.com/mnalmahmud/onnoy-keyman/actions). There are currently no published GitHub Releases. A successful CI build does not certify that a layout installs correctly on every operating system.

## Keyboard layout

The 26 letter positions, 10 number positions and period key have four layers: Base, Shift, AltGr (Right Alt / macOS Option) and Shift+AltGr. Unassigned outputs are `null` in [the canonical mapping](layout/onnoy.json); they do not imply ASCII fallback on every platform.

Key examples:

| Key | Base | Shift | AltGr | Shift+AltGr |
| --- | --- | --- | --- | --- |
| E | ে | এ | ৈ | ঐ |
| I | ি | ই | ী | ঈ |
| U | ু | উ | ূ | ঊ |
| O | ো | ও | ৌ | ঔ |
| F | ্ | ় | — | — |
| Z | ঞ | ঙ | ZWNJ | ZWJ |
| 4 | ৪ | ৳ | 4 | $ |
| . | । | > | . | — |

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
