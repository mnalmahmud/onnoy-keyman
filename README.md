# Onnoy (অন্বয়)

A Unicode keyboard for Bengali and Assamese, based on US-QWERTY positions.
The [layout.json](layout.json) defines characters for the native Linux,
Windows and macOS keyboards, Keyman, and the mobile touch layout.

[Try the keyboard](https://mnalmahmud.github.io/onnoy-keyman/) · [Releases](https://github.com/mnalmahmud/onnoy-keyman/releases) · [Builds](https://github.com/mnalmahmud/onnoy-keyman/actions)

## Layout

| Key | Base | Shift | Other |
| --- | --- | --- | --- |
| Grave | ্ | ~ | AltGr: backtick |
| S | স | শ | |
| X | ষ | ঢ় | |
| Z | য | য় | |
| Y | ী | ঈ | AltGr: য় |
| J | জ | ঝ | AltGr: ZWJ, Shift+AltGr: ZWNJ |
| L | ল | ঁ | AltGr: ় (nukta) |
| B | ব | ভ | AltGr: ৰ |
| W | ূ | ঊ | AltGr: ৱ |
| M | ম | ঙ | AltGr: ং, Shift+AltGr: 𑷰 |

`K GRAVE X` → **ক্ষ** · `Shift+S I K GRAVE X A` → **শিক্ষা**.

Use Shift and Right Alt (AltGr) for alternate characters. Ordinary US
punctuation such as `/` and `?` remains available; the extra ISO key
outputs backslash/pipe. Text is emitted as exact Unicode characters.

## Install

Generate platform sources first with `python -m onnoy generate`.
Native desktop layouts do not require Keyman.

### Linux

```sh
python -m onnoy package --target linux
```

Extract `build/onnoy-linux-native.tar.gz` and run the bundled `install.sh`.
This installs user-local XKB symbols in `~/.config/xkb/symbols/`.
On X11, try `setxkbmap -I"$HOME/.config/xkb" -layout onnoy -variant basic`.
Wayland desktop integration may require additional XKB registration.

### macOS

```sh
python -m onnoy package --target macos
```

This produces an unsigned `build/onnoy-macos.pkg`. Alternatively, copy
`dist/macos/Onnoy.keylayout` into `~/Library/Keyboard Layouts/` and enable
it under System Settings → Keyboard → Input Sources.

### Windows

Generate `dist/windows/onnoy.klc` and compile a native installer on Windows
using Microsoft Keyboard Layout Creator 1.4 and `kbdutool.exe`:

```powershell
python -m onnoy package --target windows
```

The `.klc` file alone is not installable.

### Keyman (desktop, Android, iOS)

```sh
npm install
python -m onnoy package --target keyman
```

Import `dist/keyman/onnoy.kmp` in Keyman. On Android, install from a local
package in Keyman's settings. On iPhone/iPad, use Keyman's *Install From File*
option and enable Keyman under iOS keyboard settings.

The touch keyboard includes long-press alternatives, Shift, Bengali digits,
a numeric/symbol page, and a dedicated virama key.

## Development

Python 3.12+ is required. Keyman compilation uses Node.js.

```sh
python -m onnoy validate
python -m onnoy generate
python -m onnoy check
python -m onnoy test
python -m onnoy test --package-check
python tools/benchmark.py
```

The package check requires a compiled Keyman `.kmp`. For the browser test,
build and stage `site/`, install Playwright/Chromium, then run
`python -m onnoy test --browser`.

[MIT License](LICENSE).
