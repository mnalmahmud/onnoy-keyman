# Onnoy · অন্বয়

A direct, positional Unicode keyboard for **Bangla and Bengali-script Kokborok**, based on US-QWERTY physical key positions. [Try it online](https://mnalmahmud.github.io/onnoy-keyman/).

## Architecture

No custom OS-specific keyboard generators. The two upstream source formats are built by their respective compilers:

| Target | Source | Tool |
| --- | --- | --- |
| Linux XKB, Windows KLC/AHK, macOS keylayout | [layout.toml](layout.toml) | [Kalamine](https://github.com/OneDeadKey/kalamine) |
| Keyman desktop, Android, iOS, web text input | [keyman/onnoy.kmn](keyman/onnoy.kmn) and [touch layout](keyman/onnoy.keyman-touch-layout) | [Keyman Developer](https://keyman.com/developer/) |
| Web keyboard diagram | Kalamine-generated JSON | [x-keyboard](https://github.com/OneDeadKey/x-keyboard) |
| Web typing | Keyman-generated JavaScript | KeymanWeb |

Kalamine doesn't compile Keyman keyboards, and Keyman Developer doesn't read Kalamine TOML. The two editable keyboard sources are intentionally kept side by side; CI compares all physical keys and modifier layers to prevent drift. The visual diagram does not translate text: **KeymanWeb is the only web typing engine**.

## Build

Requires Python 3.11+ and Node.js.

```sh
python -m pip install 'kalamine==0.40'
kalamine build layout.toml --qwerty-shortcuts
npm install
npm run build:keyman
python -m unittest discover -s tests -p 'test_*.py' -v
```

Kalamine writes native layouts and `onnoy.json` into `dist/`. Keyman Developer writes `onnoy.kmx`, `onnoy.js`, and `onnoy.kmp` into `keyman/` (generated files are ignored). The `--qwerty-shortcuts` option keeps the physical US virtual-key assignments on Windows.

To preview the native layout while editing it, run `kalamine watch layout.toml`. GitHub Actions publishes a build artifact including native layouts, the Keyman package, and the hosted web site.

## Install

- **Linux:** Install `dist/onnoy.xkb_symbols` or `dist/onnoy.xkb_keymap` with your XKB setup. `xkalamine install layout.toml` can register the layout in supported desktop environments.
- **macOS:** Copy `dist/onnoy.keylayout` to `~/Library/Keyboard Layouts/`, log out and back in, then add it in Keyboard settings.
- **Windows:** Compile `dist/onnoy.klc` using Microsoft Keyboard Layout Creator. Alternatively, build an installer using `wkalamine build layout.toml` on Windows. The old project-specific DLL packaging scripts have been removed.
- **Keyman desktop, Android, iOS:** Install the compiled `keyman/onnoy.kmp`. The mobile touch layout has a Shift layer, numeric layer, long-press alternatives, and dedicated virama key.

Native OS layouts do **not** need the Keyman runtime.

## Mapping highlights

| Chord | Character |
| --- | --- |
| K / Shift+K | ক / খ |
| S / Shift+S | স / শ |
| Z / Shift+Z | য / ঈ |
| Grave / Shift+Grave | ্ / ় |
| AltGr+J / AltGr+D | ZWJ / ZWNJ |
| AltGr+W | ৱ |
| Shift+4 / AltGr+4 | ৳ / 4 |

Bengali digits are on the number row; AltGr accesses ASCII digits. K → Grave → X gives **ক্ষ**. The ISO extra key produces backslash / vertical bar, while ANSI key positions remain unchanged.

## Editing the keyboard

1. Update `layout.toml` (Kalamine) and `keyman/onnoy.kmn` (Keyman) together.
2. Rebuild both and run the contract tests to check every output, including empty AltGr combinations, ZWJ/ZWNJ and the layout's expected fixed mappings.
3. Edit the Keyman touch layout separately if the mobile placement or long-press options change.

All output generators, native packagers, and browser text translators previously implemented in Python/JavaScript have been removed.

[MIT License](LICENSE).
