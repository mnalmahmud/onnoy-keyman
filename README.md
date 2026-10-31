# Onnoy (অন্বয়)

**Bengali Unicode typing, native to your operating system.**

A fixed physical-key Bengali layout built for **Linux, macOS and Windows**. Onnoy targets the operating system's native keyboard mechanisms—not Keyman, another input method, or a background keyboard application.

**[Keyboard layout demo](https://mnalmahmud.github.io/onnoy-keyman/)** · **[Native build artifacts](https://github.com/mnalmahmud/onnoy-keyman/actions)** · **[Issues](https://github.com/mnalmahmud/onnoy-keyman/issues)**

> The project is migrating from an older Keyman-first repository structure. The canonical keyboard mapping is preserved. The published repo name is pending change to `onnoy`; links retain the current working repository address.

## Download and install

| System | Native format | Install route | Status |
| --- | --- | --- | --- |
| Linux | XKB symbols | [Linux guide](docs/install-linux.md) | XKB build checked; desktop registration varies |
| macOS | `.keylayout`, `.pkg` | [macOS guide](docs/install-macos.md) | Unsigned package, device verification needed |
| Windows | `.klc` → compiled DLL/setup | [Windows guide](docs/install-windows.md) | Source available; verified installer still needed |

The native layouts **do not require Keyman** at runtime. Windows developers need MSKLC only while *building* a native installer; ordinary users should install a prebuilt verified keyboard once one is available. No platform is advertised as one-click installable without real testing.

## Keyboard basics

Onnoy uses a fixed US-QWERTY physical layout with four levels: Base, Shift, AltGr (Right Alt / macOS Option), and Shift+AltGr.

The complete, authoritative [layout definition](layout/onnoy.json) can be inspected in the [interactive keymap](https://mnalmahmud.github.io/onnoy-keyman/#keymap).

| Chord | Output | Chord | Output |
| --- | --- | --- | --- |
| T / Shift+T | ট / ঠ | AltGr+T | ৎ |
| F / Shift+F | ত / থ | Q / Shift+Q | দ / ধ |
| D / Shift+D | ড / ঢ | P / Shift+P | প / ফ |
| B / Shift+B | ব / ভ | V / Shift+V | অ / ৗ |
| R / Shift+R | র / ড় | X / Shift+X | শ / ঢ় |
| Z / Shift+Z | য / — | X | শ |
| M / Shift+M | ম / ঙ | AltGr+M / Shift+AltGr+M | ং / 𑷰 |
| N / Shift+N | ন / ণ | AltGr+N | ঞ |
| W / Shift+W | ূ / ঊ | AltGr+W | ৱ |
| E / Shift+E | ে / এ | I / Shift+I | ি / ই |
| O / Shift+O | ো / ও | Y / Shift+Y / AltGr+Y | ী / ঈ / য় |
| [ / Shift+[ | ৈ / ঐ | ] / Shift+] | ৌ / ঔ |
| ; / Shift+; | ৃ / ঋ | = / Shift+= | = / + (native US) |
| , / Shift+, | , / < | AltGr+, | ় |
| . / Shift+. | । / > | AltGr+. | . |
| / / Shift+/ | ্ / ? | AltGr+/ | / |
| AltGr+J | — (unassigned) | Shift+L | ঁ (AltGr+L unassigned) |

ZWJ (U+200D) and ZWNJ (U+200C) are currently unassigned, pending new shortcut placement. AltGr+apostrophe and Shift+AltGr+apostrophe are unassigned; Base/Shift apostrophe remain ordinary ASCII quotes. Space remains Space with every modifier. The backtick, minus, backslash and equals keys inherit platform-native US behavior. ASCII bracket, semicolon and slash characters remain available on AltGr. The comma retains ordinary Base/Shift punctuation while AltGr+comma continues to hold nukta; Shift+AltGr+comma is now unassigned. Shift+AltGr+M holds Bengali combining anusvara above (𑷰). Number keys produce Bengali digits on Base, English symbols on Shift and ASCII digits on AltGr.

**Explicit Unicode typing:** `K → / → Shift+S` produces ক্ষ; `/ → Z` produces ্য; `Shift+R` produces ড়; `Shift+X` produces ঢ়; and `AltGr+Y` produces য় (`Shift+Z` is unassigned). These mappings emit the specified Unicode scalars directly, without a background composition engine. Fonts and apps handle shaping and normalization.

## Native architecture

A minimal set of Onnoy overrides (`layout/onnoy.json`) generates all three native formats. Linux inherits `us(basic)` directly; macOS inherits unchanged keymaps inside its `.keylayout` from a pinned US reference; Windows overlays an exported US `.klc` at build time. Unchanged Space, Minus, Backslash, Comma and Backtick are not custom definitions. There is no Keyman keyboard source in this project and no Keyman compiler in the build.

```sh
python3 scripts/generate.py
python3 scripts/generate.py --check
bash scripts/build.sh
```

**Generator requirements:** Python 3. Running a native keyboard after installation does not require Python. Platform-specific packagers such as `pkgbuild` and MSKLC are only needed to build installers.

The [browser preview](https://mnalmahmud.github.io/onnoy-keyman/) uses a small self-contained JavaScript mapping only inside the demo textarea. It does not install a keyboard, intercept global shortcuts, or replace the OS-native layout.

For architecture, format limitations and release quality gates see [docs/architecture.md](docs/architecture.md). For original design experiments and corpus benchmarks see [docs/design-and-research.md](docs/design-and-research.md).

## Naming

The recommended repository name is **`onnoy`**. Changing a GitHub repository's public name and its GitHub Pages project URL requires a separate administrator action and link migration. No rename is implied by this code change.

## License

MIT © 2026 Muhtasham Nawr al-Mahmud.
