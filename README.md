# Onnoy (অন্বয়)

A positional Unicode keyboard for Bengali and Assamese, based on physical
US-QWERTY key positions. One [layout.json](layout.json) supplies the same
character assignments to native desktop layouts, Keyman, and mobile touch
keys. ANSI and ISO keyboards are supported.

[Try Onnoy](https://mnalmahmud.github.io/onnoy-keyman/) · [Releases](https://github.com/mnalmahmud/onnoy-keyman/releases) · [Builds](https://github.com/mnalmahmud/onnoy-keyman/actions)

## Keyboard

| Key | Base | Shift | Additional |
| --- | --- | --- | --- |
| GRAVE | ্ (virama) | ~ | AltGr: backtick |
| S | স | শ | |
| X | ষ | ঢ় | |
| Z | য | য় | |
| Y | ী | ঈ | AltGr: য় |
| J | জ | ঝ | AltGr: ZWJ (U+200D), Shift+AltGr: ZWNJ (U+200C) |
| L | ল | ঁ | AltGr: nukta ় |
| B | ব | ভ | AltGr: Assamese ৰ |
| W | ূ | ঊ | AltGr: Assamese ৱ |
| M | ম | ঙ | AltGr: ং, Shift+AltGr: 𑷰 |

`K GRAVE X` produces **ক্ষ**; `Shift+S I K GRAVE X A` produces
**শিক্ষা**. Common punctuation such as `/` and `?` retains its US
position. The ISO extra key produces backslash/pipe.

## Installation

Generate sources with `python -m onnoy generate`. Native desktop keyboards
do **not** require Keyman.

### Linux

Run `python -m onnoy package --target linux`, extract
`build/onnoy-linux-native.tar.gz`, and run the bundled `install.sh`.
This puts the XKB symbols in `~/.config/xkb/symbols`. X11 users can try
`setxkbmap -I"$HOME/.config/xkb" -layout onnoy -variant basic`.
Wayland desktop environments generally need additional XKB rules/desktop
registration for Onnoy to appear in keyboard settings.

### macOS

On macOS, run `python -m onnoy package --target macos` to create the
unsigned `build/onnoy-macos.pkg`. Alternatively, put
`dist/macos/Onnoy.keylayout` in `~/Library/Keyboard Layouts/` and
enable it in **System Settings → Keyboard → Input Sources**. Log out/in if
needed. The package is not signed or notarized.

### Windows

Run `python -m onnoy generate`. The resulting
`dist/windows/onnoy.klc` is **source, not an installer**. To compile
the native DLL and installer on Windows, install Microsoft Keyboard Layout
Creator 1.4 with `kbdutool.exe` on PATH, then run
`python -m onnoy package --target windows`.

### Keyman (desktop, Android, iOS)

Run `python -m onnoy generate`, `npm install`, and
`python -m onnoy package --target keyman`. Import
`dist/keyman/onnoy.kmp` into Keyman. On Android, select the local package
in Keyman's keyboard installation settings. On iPhone/iPad, use Keyman's
**Install From File** option and enable Keyman in iOS keyboard settings.

The generated mobile touch layout has Bengali digits, Shift and long-press
alternatives, a dedicated virama key, and a numeric/symbol page.

## Build and test

Use Python 3.12+. Keyman compilation additionally requires Node.js and the
dependencies in `package.json`.

```sh
python -m onnoy validate
python -m onnoy generate
python -m onnoy check
python -m onnoy test
python -m onnoy package --target keyman
python -m onnoy test --package-check
python tools/benchmark.py --corpus tests/data/demo-bengali.txt
```

After staging the compiled website under `site/`, run
`python -m onnoy test --browser` with Playwright/Chromium installed.
Generated directories `build/`, `dist/`, and `site/` are ignored by Git.

[MIT licensed](LICENSE).
