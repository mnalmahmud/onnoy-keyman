# Onnoy · অন্বয়

A **positional Unicode keyboard** for Bangla and Bengali-script Kokborok. Onnoy uses physical US-QWERTY key positions; it is **not** a phonetic input method.

**[Try it online](https://mnalmahmud.github.io/onnoy-keyman/)** · [Builds and downloads](https://github.com/mnalmahmud/onnoy-keyman/actions) · [Full layout](layout.toml)

## Typing

Use **Shift** for alternate characters and **Right Alt (AltGr)** for the additional layer. The layout works on ANSI and ISO keyboards.

| Keys | Output |
| --- | --- |
| `K` / `Shift+K` | ক / খ |
| `S` / `Shift+S` | স / শ |
| `F` / `Shift+F` / `AltGr+F` | ত / থ / ৎ |
| `Grave` / `Shift+Grave` | ্ (virama) / ় (nukta) |
| `AltGr+J` / `AltGr+D` | ZWJ / ZWNJ |
| `AltGr+W` | ৱ |

For example, `K → Grave → X` produces **ক্ষ**. The number row types Bengali numerals; use AltGr for ASCII digits. The extra ISO key types `\` and `|`.

The [online keyboard](https://mnalmahmud.github.io/onnoy-keyman/) shows the full layout and lets you type without installing anything.

## Install

Download the `onnoy-native-keyman-web` artifact from a successful [GitHub Actions build](https://github.com/mnalmahmud/onnoy-keyman/actions), or [build it yourself](#build).

- **Keyman (Windows, macOS, Linux, Android, iOS):** Install `keyman/onnoy.kmp` using [Keyman](https://keyman.com/). On mobile, enable the keyboard in your device settings.
- **Windows native:** Open `dist/onnoy.klc` in Microsoft Keyboard Layout Creator and build an installer.
- **macOS native:** Copy `dist/onnoy.keylayout` to `~/Library/Keyboard Layouts/`, log out and back in, then enable Onnoy in Keyboard settings.
- **Linux native:** Use `dist/onnoy.xkb_symbols` or `dist/onnoy.xkb_keymap` with your XKB configuration.

Native layouts do not require Keyman. Native installations have not yet been tested across all target operating systems.

## Build

Requires Python 3.11+, Node.js 22, and pnpm 10.19.0.

```sh
python -m pip install kalamine==0.40
kalamine build layout.toml --qwerty-shortcuts

pnpm install --frozen-lockfile
pnpm run build:keyman

python -m unittest discover -s tests -p 'test_*.py'
```

Kalamine creates the native layouts in `dist/`. The Keyman build generates `keyman/onnoy.kmn` from `layout.toml` and compiles the keyboard and `.kmp` package.

**To change the mapping, edit `layout.toml` only.** Do not edit the generated `.kmn`. Mobile key positions and long-press options are defined separately in [`keyman/onnoy.keyman-touch-layout`](keyman/onnoy.keyman-touch-layout).

## License

[MIT](LICENSE).
