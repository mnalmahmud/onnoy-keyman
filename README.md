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
| K / Shift+K | ক / খ | G / Shift+G | গ / ঘ |
| D / Shift+D | দ / ধ | T / Shift+T | ত / থ |
| F / Shift+F | ফ / — | X / Shift+X | ষ / ় |
| V / Shift+V | ভ / অ | B / Shift+B | ব / ৗ |
| E / Shift+E | ে / এ | I / Shift+I | ি / ই |
| O / Shift+O | ো / ও | Y / Shift+Y | ী / ঈ |
| [ / Shift+[ | ৈ / ঐ | ] / Shift+] | ূ / ঊ |
| ; / Shift+; | ৌ / ঔ | = / Shift+= | ৃ / ঋ |
| / / Shift+/ | ্ / ? | AltGr+/ | / |
| AltGr+` | ZWJ (U+200D) | Shift+AltGr+` | ZWNJ (U+200C) |

Space remains Space with every modifier. The ordinary slash character is on **AltGr+/**; **Shift+F is deliberately unassigned** rather than providing a duplicate virama shortcut. Backtick and tilde remain on their unmodified/Shift positions; ZWJ and ZWNJ use AltGr modifiers on the backtick key. ASCII bracket, semicolon and equals characters are available through AltGr layers. Number keys produce Bengali digits on the base layer.

**Explicit Unicode typing:** `K → / → X` produces ক্ষ, `/ → Z` produces ্য, and `Q → Shift+X` produces ড়. No background composition engine is necessary. Apps and fonts handle shaping.

## Native architecture

A single mapping (`layout/onnoy.json`) generates all three platform formats. There is no Keyman keyboard source in this project and no Keyman compiler in the build.

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
