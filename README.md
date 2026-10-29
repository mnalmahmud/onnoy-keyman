# Onnoy (অন্বয়)

A fixed Bengali-script Unicode keyboard for physical US-QWERTY keys. All assignments live in **[`layout/onnoy.json`](layout/onnoy.json)**; platform files are generated, not maintained separately.

**[Try the keyboard](https://mnalmahmud.github.io/onnoy-keyman/)** · [Latest CI builds](https://github.com/mnalmahmud/onnoy-keyman/actions) · [Report an issue](https://github.com/mnalmahmud/onnoy-keyman/issues)

## Layout

The four layers are Base, Shift, AltGr (Right Alt; Option on macOS), and Shift+AltGr. A `null` mapping is unassigned, not necessarily an ASCII fallback.

| Key | Base | Shift | AltGr | Shift+AltGr |
| --- | --- | --- | --- | --- |
| Q | ড | ঢ | ড় | ঢ় |
| W | ট | ঠ | — | — |
| E | ে | এ | ৈ | ঐ |
| I | ি | ই | ী | ঈ |
| U | ু | উ | ূ | ঊ |
| O | ো | ও | ৌ | ঔ |
| R | র | ৃ | ঋ | ৰ |
| F | ্ | ় | — | — |
| X | ষ | **ক্ষ** | — | — |
| G | গ | ঘ | **জ্ঞ** | — |
| Y | য | য় | **্য** | — |

The three multi-code-point shortcuts output the exact sequences:

- **Shift+X:** ক্ষ = `U+0995 U+09CD U+09B7`
- **AltGr+G:** জ্ঞ = `U+099C U+09CD U+099E`
- **AltGr+Y:** য-ফলা = `U+09CD U+09AF` (no automatic ZWJ)

The [online keymap](https://mnalmahmud.github.io/onnoy-keyman/#keymap) shows every key and layer. ZWNJ (`U+200C`) and ZWJ (`U+200D`) have their own assignments on Z's AltGr layers.

## Platforms

| Platform | Generated artifact | Notes |
| --- | --- | --- |
| Web / Keyman | `build/onnoy.js`, `build/onnoy.kmp` | KeymanWeb runs the browser playground; the `.kmp` requires a Keyman runtime |
| Linux | `dist/linux/symbols/onnoy`, `dist/linux/Onnoy.XCompose` | Native XKB plus Compose; **no Keyman needed**; actual application support needs verification |
| macOS | `dist/macos/Onnoy.keylayout` | Native input source; XML is validated in CI; must also be tested installed |
| Windows | `dist/windows/onnoy.klc` | Source for MSKLC with ligatures; **not an installer** and not yet compiled/tested on Windows |

### Linux shortcut installation

Install and register the generated XKB symbols using your distribution's XKB configuration, then integrate the rules from `dist/linux/Onnoy.XCompose` into `~/.XCompose`. If needed, retain system Compose definitions using `include "%L"`. Restart affected applications. Onnoy maps F13–F15 internal keysyms to full Unicode strings; application, compositor and toolkit support can vary. Do not assume that a passing XKB compilation test proves all three shortcuts work everywhere.

### Other installation notes

- **macOS:** Install `Onnoy.keylayout` to `~/Library/Keyboard Layouts/`, then enable Onnoy in Keyboard → Input Sources (log out and back in if necessary).
- **Windows:** Compile `onnoy.klc` with MSKLC and test the resulting layout; no native installer is currently published.
- **Web:** Open the [typing playground](https://mnalmahmud.github.io/onnoy-keyman/) in a desktop browser.

## Build and test

Requirements: Python 3 and Node.js. Compiling Keyman additionally requires [Keyman Developer CLI 18](https://keyman.com/developer/).

```sh
python3 scripts/generate.py
python3 scripts/generate.py --check
npm install -g @keymanapp/kmc@18
bash scripts/build.sh
```

The generator writes `source/onnoy.kmn` and platform sources in `dist/`. The build script verifies the mapping, compiles the Keyman keyboard and package, and checks the outputs. `build/`, `dist/` and `site/` are generated and ignored by Git.

To test the browser locally:

```sh
mkdir -p site
cp web/index.html web/app.js web/style.css build/onnoy.js site/
cp layout/onnoy.json site/layout.json
python3 -m http.server 8000 --directory site
```

The CI workflow also runs Chromium smoke tests (Python Playwright). See **[CONTRIBUTING.md](CONTRIBUTING.md)** for source-tree structure, development practices and release validation.

## License

MIT © 2026 Muhtasham Nawr al-Mahmud. See [LICENSE](LICENSE).
