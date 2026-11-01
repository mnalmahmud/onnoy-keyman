# Onnoy (অন্বয়)

**A fixed Unicode Bengali/Assamese keyboard, generated from one mapping.**

Onnoy provides **native Linux XKB, native macOS `.keylayout`, native Windows
KLC source, and Keyman**. Installing Keyman is optional: it is not required
for any native desktop implementation.

[Interactive visualizer and KeymanWeb playground](https://mnalmahmud.github.io/onnoy-keyman/) · [Build workflows](https://github.com/mnalmahmud/onnoy-keyman/actions) · [Source contract](docs/keyboard-contract.md)

## Key mappings

The authoritative source is [`layout/onnoy.json`](layout/onnoy.json). It
uses short key identifiers and sparse `base`, `shift`, `altgr`, and
`shift_altgr` entries. A single resolver applies ordinary US-QWERTY
symbol defaults; backend implementations cannot redefine characters.

| Chord | Output | Chord | Output |
| --- | --- | --- | --- |
| GRAVE / Shift+GRAVE | ্ / ~ | AltGr+GRAVE | \` |
| S / Shift+S | স / শ | X / Shift+X | ষ / ঢ় |
| Z / Shift+Z | য / য় | AltGr+Y | য় |
| AltGr+J | ZWJ U+200D | Shift+AltGr+J | ZWNJ U+200C |
| L / Shift+L | ল / ঁ | AltGr+L | ় |
| B / Shift+B | ব / ভ | AltGr+B | ৰ |
| AltGr+W | ৱ | AltGr+N | ঞ |
| / / Shift+/ | / / ? | , / Shift+, | , / < |
| M / Shift+M | ম / ঙ | AltGr+M / Shift+AltGr+M | ং / 𑷰 |

Common literal punctuation stays where available; brackets, semicolon
and full stop remain accessible through their assigned layers. ISO hardware
adds a Base backslash / Shift pipe key next to left Shift; it does not change
Bengali letter placements. QWERTZ and AZERTY are not supported profiles.

Example sequences: `K GRAVE X` → ক্ষ; `Shift+S I K GRAVE X A`
→ শিক্ষা; `R AltGr+J GRAVE Z` → র‍্য.
Unicode codepoints are emitted directly; no text normalization or
phonetic conversion is performed.

## Build

Python 3.12+ is used for the canonical mapping and native source generation:

```bash
python3 scripts/build.py validate
python3 scripts/build.py generate
python3 scripts/build.py check
python3 scripts/build.py test
```

Optional Keyman compilation (Node.js 20+):

```bash
npm install
npm run build:keyman
```

The compiler generates desktop `dist/keyman/onnoy.kmx`, installable
`dist/keyman/onnoy.kmp` and browser/mobile `dist/keyman/onnoy.js`.
The package contains a generated touch layout for Keyman on Android and iOS,
with Bengali letters, long-press variants, a permanent virama key, and a
numeric/symbol layer. Mobile device usability verification is still pending.
The KeymanWeb playground loads the compiled browser keyboard while
retaining a separate Onnoy visualizer.

Native outputs:

| OS | Generated artifact | Build/release status |
| --- | --- | --- |
| Linux | `dist/linux/symbols/onnoy` | XKB compilation in CI; desktop integration testing pending |
| macOS | `dist/macos/Onnoy.keylayout`, unsigned `.pkg` | Generated/package tested; ANSI/ISO installation tests pending |
| Windows | `dist/windows/onnoy.klc` | KLC source generated; MSKLC DLL/installer testing pending |
| Keyman desktop/mobile | `.kmn` + generated touch layout → `.kmx`, `.js`, `.kmp` | CI compilation; Android/iOS installation and typing tests pending |

See [Linux](docs/install-linux.md), [macOS](docs/install-macos.md),
[Windows](docs/install-windows.md), and
[Android/iOS](docs/install-mobile.md) installation guides.

## Architecture and contribution

`onnoy/model.py` resolves the canonical key map against one plain-US
reference. Independent backends in `onnoy/backends/` produce native
platform formats, Keyman and visualizer JSON. The old copied US keyboard
templates are no longer active build inputs.

- [Keyboard contract](docs/keyboard-contract.md)
- [Architecture](docs/architecture.md)
- [Contributing](CONTRIBUTING.md)
- [Design and research](docs/design-and-research.md)

All build outputs are generated; edit `layout/onnoy.json` for character
changes and update independently specified typing tests.

MIT licensed. See [LICENSE](LICENSE).
