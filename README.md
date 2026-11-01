# Onnoy · অন্বয়

A Unicode keyboard for **Bangla and Assamese**, built around the familiar US-QWERTY key positions.

Onnoy maps physical keys directly to Unicode characters. It works as a native keyboard layout on Linux, Windows, and macOS, or through Keyman on desktop and mobile.

[**Try Onnoy online**](https://mnalmahmud.github.io/onnoy-keyman/) · [Keyboard mapping](layout.json) · [Builds](https://github.com/mnalmahmud/onnoy-keyman/actions)

## Keyboard layout

The layout stays in the same positions on ANSI and ISO keyboards. Use **Shift** for alternate letters and **Right Alt (AltGr)** for additional characters.

| Key | Output |
| --- | --- |
| `K` / `Shift+K` | ক / খ |
| `S` / `Shift+S` | স / শ |
| `Z` / `Shift+Z` | য / য় |
| `Grave` | ্ (virama) |
| `AltGr+J` / `Shift+AltGr+J` | ZWJ / ZWNJ |
| `AltGr+L` | ় (nukta) |
| `AltGr+B` / `AltGr+V` | ৰ / ৱ |

For example, `K → Grave → X` produces **ক্ষ**, and `Shift+S → I → K → Grave → X → A` produces **শিক্ষা**.

Number keys produce Bengali digits; AltGr gives access to ASCII digits. The extra ISO key provides `\` and `|`. See the [interactive keyboard](https://mnalmahmud.github.io/onnoy-keyman/#keymap) or [layout.json](layout.json) for every assignment.

## Install

Native desktop layouts require **no Keyman or background input method**. The commands below run from the repository root.

### Linux

```sh
python -m onnoy package --target linux
```

Extract `build/onnoy-linux-native.tar.gz` and run its `install.sh`. This installs the XKB symbols under `~/.config/xkb/symbols/`. On X11, you can try:

```sh
setxkbmap -I"$HOME/.config/xkb" -layout onnoy -variant basic
```

Some desktops, particularly on Wayland, also require registering the layout in their keyboard settings.

### macOS

```sh
python -m onnoy package --target macos
```

This creates `build/onnoy-macos.pkg` (unsigned). To install manually, copy `dist/macos/Onnoy.keylayout` to `~/Library/Keyboard Layouts/`, then add Onnoy in **System Settings → Keyboard → Input Sources**.

### Windows

```powershell
python -m onnoy package --target windows
```

Requires **Microsoft Keyboard Layout Creator 1.4** with `kbdutool.exe` installed. This generates `build/windows/onnoy-windows-native.zip` with native x64/x86 keyboard DLLs and an install/uninstall script. Extract the archive, then run `setup.ps1` in elevated 64-bit PowerShell (use `-Uninstall` to remove Onnoy). No Keyman runtime is needed. The standalone `.klc` file is only source; new packages require Windows installation testing before release.

### Keyman · Desktop / Android / iOS

```sh
npm install
python -m onnoy package --target keyman
```

Install `dist/keyman/onnoy.kmp` with Keyman. On Android and iOS, import the package through Keyman's keyboard installation settings; enable Keyman in the device's keyboard settings when needed.

The mobile layout includes long-press variants, Bengali numerals, Shift, and a dedicated virama key.

## Build and test

Requires **Python 3.12+**. Building Keyman also requires Node.js.

```sh
python -m onnoy validate
python -m onnoy generate
python -m onnoy check
python -m onnoy test
```

Generated files are written to `dist/`. Packaging creates artifacts under `build/`. Both directories are ignored by Git.

## License

[MIT](LICENSE).
