# Onnoy (অন্বয়)

Onnoy is a **Bengali keyboard layout for [Keyman](https://keyman.com/)**. It maps physical US-QWERTY keys directly to Unicode characters. It is not an English-to-Bengali transliteration input method.

[Try in your browser](https://mnalmahmud.github.io/onnoy-keyman/) · [Source](source/onnoy.kmn) · [Builds](https://github.com/mnalmahmud/onnoy-keyman/actions) · [Issues](https://github.com/mnalmahmud/onnoy-keyman/issues)

## Use Onnoy

### In a browser

Open the [typing test](https://mnalmahmud.github.io/onnoy-keyman/), focus the editor, and type with a physical keyboard. It uses the compiled KeymanWeb keyboard, not transliteration or a separately implemented keymap. The site does not install a system keyboard.

### On your computer

1. [Install Keyman](https://keyman.com/) for your operating system.
2. Open [GitHub Actions](https://github.com/mnalmahmud/onnoy-keyman/actions), select a run with a successful **Compile and verify Keyman artifacts** job, and download its **onnoy-keyman** artifact.
3. Extract the downloaded ZIP and open `onnoy.kmp` with Keyman.
4. Select **Onnoy** in Keyman's keyboard list.

The artifact from Actions is a development build, not a stable release. Once a tested release is published, its package will be available under [Releases](https://github.com/mnalmahmud/onnoy-keyman/releases).

The `.kmp` file is the installable desktop package. `.kmx` is the compiled desktop keyboard inside it; `.js` is the browser keyboard used by KeymanWeb. Platform-specific installation and AltGr behavior still need real-device testing.

## Keyboard layout

There are four layers: **Base**, **Shift**, **AltGr (Right Alt)**, and **AltGr + Shift**. The table follows the physical US-QWERTY letter rows. **—** means the key combination has no output assigned.

| Key | Base | Shift | AltGr | AltGr + Shift |
|:---:|:---:|:---:|:---:|:---:|
| Q | ট | ঠ | — | — |
| W | ড | ঢ | ড় | ঢ় |
| E | ে | এ | ৈ | ঐ |
| R | র | ৃ | ঋ | ৰ |
| T | ত | থ | ৎ | — |
| Y | য | য় | — | — |
| U | ু | উ | ূ | ঊ |
| I | ি | ই | ী | ঈ |
| O | ো | ও | ৌ | ঔ |
| P | প | ফ | — | — |
| A | া | আ | ঽ | — |
| S | স | শ | — | — |
| D | দ | ধ | — | — |
| F | ্ | ় | — | — |
| G | গ | ঘ | — | — |
| H | হ | ঃ | — | — |
| J | জ | ঝ | — | — |
| K | ক | খ | — | — |
| L | ল | — | — | — |
| Z | ঞ | ঙ | ZWNJ | ZWJ |
| X | ষ | — | — | — |
| C | চ | ছ | — | — |
| V | অ | ৱ | ৗ | — |
| B | ব | ভ | — | — |
| N | ন | ণ | — | — |
| M | ম | ং | ঁ | — |

### Number row and punctuation

- `1`–`0` produce **১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯ ০** on the base layer.
- **AltGr + 1–0** produces the corresponding Latin digits **1–0**.
- Shift produces the usual US number-row symbols, except **Shift + 4** produces **৳**. **AltGr + Shift + 4** produces **$**.
- The period key produces **।** (base), **>** (Shift), and **.** (AltGr).
- Other punctuation follows the host keyboard. Unassigned combinations in the table produce no character.

### Typing examples

| Result | Keystrokes |
|---|---|
| বাংলা | `B A Shift+M L A` |
| ক্ষ | `K F X` |
| শিক্ষা | `Shift+S I K F X A` |
| ৳৪.৫০ | `Shift+4 4 AltGr+. 5 0` |

`F` produces the virama (্), used to form conjuncts. `Shift+F` produces the nukta (়). `AltGr+Z` and `AltGr+Shift+Z` produce ZWNJ and ZWJ respectively; these format characters are normally invisible. The appearance of combining signs and conjuncts depends on the application's font and text-shaping support.

## Build from source

Requirements: **Node.js**, **Python 3**, a shell capable of running `bash`, and **Keyman Developer CLI 18**.

```sh
git clone https://github.com/mnalmahmud/onnoy-keyman.git
cd onnoy-keyman
npm install -g @keymanapp/kmc@18
bash scripts/build.sh
python3 scripts/verify_build.py
```

The build produces:

- `build/onnoy.kmp` — desktop package
- `build/onnoy.kmx` — compiled desktop keyboard
- `build/onnoy.js` — compiled KeymanWeb keyboard

`source/onnoy.kmn` defines the key mappings, and `source/onnoy.kps` defines the package. `verify_keyman.py` checks the source mappings before compilation; `scripts/verify_build.py` checks the generated files and package.

The [CI workflow](.github/workflows/build.yml) runs these checks on pushes and pull requests. It uploads the build artifacts, builds the GitHub Pages site from `web/` on `main`, and attaches compiled files to releases on version-tag pushes.

## Project status

The build pipeline compiles desktop and web targets. That does **not** by itself establish successful typing across Windows, macOS, Linux, and different browser/keyboard configurations. A dedicated mobile touch layout is not provided.

If a key behaves differently on your system, please [report the physical keystrokes, expected output, actual output, and environment](CONTRIBUTING.md).

## License

Copyright © 2026 **Muhtasham Nawr al-Mahmud**. Onnoy is released under the [MIT License](LICENSE).
