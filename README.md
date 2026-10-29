# অন্বয় · Onnoy

**A physical-key Unicode keyboard for Bengali script, built with [Keyman](https://keyman.com/).**

[**Try Onnoy**](https://mnalmahmud.github.io/onnoy-keyman/) · [Keyboard source](source/onnoy.kmn) · [Builds](../../actions) · [Report an issue](../../issues)

Onnoy uses predictable character groups on the standard US-QWERTY keyboard. It is a **fixed key layout**, not phonetic transliteration: pressing a key produces its assigned Unicode character, not a transliteration of an English spelling.

> **Project status:** The desktop and web keyboards compile in GitHub Actions. This is a prerelease project: compilation does not establish that every platform and modifier combination has been tested. Do not treat an untagged CI artifact as a stable release.

## Try it

Open the [live typing playground](https://mnalmahmud.github.io/onnoy-keyman/). It loads the actual compiled KeymanWeb keyboard produced by CI. Use a physical keyboard; the page is not a mobile touch keyboard.

If you are testing AltGr, use **Right Alt** where available. How Right Alt reaches Keyman depends on your operating system, browser and configured host keyboard. Report the environment alongside any discrepancy.

## Get the keyboard

- **Desktop:** Download the `onnoy.kmp` artifact from a successful [Actions build](../../actions), then open it with an installed [Keyman](https://keyman.com/) application. The package is intended for supported desktop Keyman installations; please report platform-specific installation results.
- **Web:** `onnoy.js` is the compiled KeymanWeb keyboard. The GitHub Pages deployment serves the same output.
- **Stable releases:** Version-tagged builds are published under [Releases](../../releases) after release testing. No stable release is implied until a version is explicitly published.

The raw `onnoy.kmx` is a compiled desktop component; most users should install the `.kmp` package instead.

## Keyboard layout

The columns represent **Base**, **Shift**, **AltGr**, and **AltGr + Shift**. A dash means Onnoy deliberately assigns nothing at that position.

| Key | Base | Shift | AltGr | AltGr + Shift |
|:--:|:--:|:--:|:--:|:--:|
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

**Numbers and punctuation:** Base number-row keys yield Bengali digits (`1` → ১ through `0` → ০); AltGr yields Latin digits. Most Shift number-row symbols follow US-QWERTY, except `Shift+4` → ৳; `AltGr+Shift+4` → `$`. The period key produces `।` on Base, `>` with Shift, and `.` with AltGr. Other punctuation is left to the host keyboard.

**Vowels:** E, I, U and O group each vowel's dependent and independent forms. **Conjuncts:** F inserts virama (`্`), so `K F X` yields `ক্ষ`. The font and shaping engine determine the rendered appearance.

### Sample keystrokes

| Output | Physical keys |
|---|---|
| বাংলা | `B A Shift+M L A` |
| ক্ষ | `K F X` |
| শিক্ষা | `Shift+S I K F X A` |
| ৳৪.৫০ | `Shift+4 4 AltGr+. 5 0` |

## Build from source

Requires Node.js, Python 3 and the [Keyman Developer CLI](https://help.keyman.com/developer/current-version/reference/kmc/cli/get-started):

```bash
npm install -g @keymanapp/kmc@18
bash scripts/build.sh
python3 scripts/verify_build.py
```

The outputs are `build/onnoy.kmx`, `build/onnoy.js` and `build/onnoy.kmp`. `verify_keyman.py` checks mapping invariants before compilation. The authoritative layout is `source/onnoy.kmn`; avoid maintaining another hand-written mapping for the website.

### Repository organization

| Path | Purpose |
|---|---|
| `source/onnoy.kmn` | Keyboard rules |
| `source/onnoy.kps` | Installable Keyman package definition |
| `web/` | GitHub Pages typing playground |
| `scripts/` | Build and artifact verification |
| `.github/workflows/build.yml` | Compile, test, publish CI artifacts and deploy Pages |

Changes to `main` rebuild the site from the compiled web keyboard. Tags matching `v*` trigger release asset publishing. Maintainers should use the [release checklist](RELEASE_CHECKLIST.md) before tagging.

## Known limitations

- **Physical desktop layout:** A mobile touch layout is not available.
- **AltGr:** Browser and OS modifier handling varies; a successful CI run does not prove cross-platform modifier behavior.
- **Composition:** Onnoy inserts Unicode characters. Rendering and conjunct formation depend on fonts and application text engines.
- **Coverage:** This is not a claim of complete coverage of every historical or modern character used in Bengali and Assamese. Character assignments, including ৰ and ৱ, are documented above.
- **Availability:** Web testing requires JavaScript and access to the KeymanWeb engine. A network or content blocker may prevent startup.

## Participate

Bug reports should state the physical keystrokes, expected output, actual Unicode output and environment. Mapping changes should have a clear rationale and regression tests. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License and credits

Copyright © 2026 **Muhtasham Nawr al-Mahmud**. Distributed under the [MIT License](LICENSE).

Onnoy's layout design draws from experience with Bengali keyboard traditions, including Probhat and KaGaPa. This acknowledgment is not a claim that either project's source code was incorporated verbatim. Any upstream source material added in future must retain its applicable notices.
