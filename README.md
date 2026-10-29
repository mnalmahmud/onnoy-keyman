# অন্বয় · Onnoy

**A Unicode keyboard layout for Bengali, built with Keyman.** Onnoy combines predictable character relationships with a Bengali-first physical QWERTY layout.

**[Try Onnoy in your browser](https://mnalmahmud.github.io/onnoy-keyman/)** · [Full keymap](#layout) · [Build from source](#build) · [Contribute](CONTRIBUTING.md)

> **GitHub Pages:** In **Settings → Pages → Build and deployment**, select **GitHub Actions**. The browser typing test will become available at the link above after a successful deployment from `main`.

## Try in your browser

The GitHub Pages site uses **KeymanWeb** and the **compiled Onnoy keyboard** from this repository. It is a live typing playground—not a JavaScript mockup of the keymap. Type into the text field using a physical US-QWERTY keyboard, and use Right Alt (AltGr) or Shift to access other layers. There is also a Unicode inspector to help report issues.

It does not install a system-wide keyboard. Mobile touch input needs a separate design; the web playground is intended for physical keyboard testing.

## Downloads

A successful build creates:

- **`onnoy.kmp`** — installable Keyman keyboard package for supported desktop Keyman applications.
- **`onnoy.js`** — compiled KeymanWeb keyboard used by the GitHub Pages test site.
- **`onnoy.kmx`** — compiled desktop keyboard inside the package, also available for diagnosis.

Build artifacts are attached to successful GitHub Actions runs. When you push a `v*` tag, the workflow attaches the same files to a GitHub Release. No precompiled files are tracked in Git.

## Layout

Onnoy is a fixed Unicode layout, **not** English-to-Bengali transliteration. Letters use the 26 physical alphabet keys, with four modifier layers. Numbers and selected punctuation have their own conventional keys.

| Key | Normal | Shift | AltGr | AltGr+Shift |
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

The number keys produce Bengali digits directly and Latin digits through AltGr. `Shift+4` is **৳**; `AltGr+Shift+4` is **$**. `.` is **।**; `AltGr+.` is the ASCII period. Other punctuation retains its normal US-QWERTY behavior.

The E, I, U, O groups follow one pattern: normal **basic কার**, Shift **independent vowel**, AltGr **paired কার**, AltGr+Shift **paired independent vowel**.

## Build

Install Node.js 22 and the [Keyman Developer CLI](https://help.keyman.com/developer/current-version/reference/kmc/cli/get-started):

```bash
npm install -g @keymanapp/kmc@18
bash scripts/build.sh
python3 scripts/verify_build.py
```

This builds `build/onnoy.kmp`, `build/onnoy.kmx`, and `build/onnoy.js`. Compilation requires the Keyman CLI; `python3 verify_keyman.py` checks the textual mapping independently of compilation.

### Continuous integration and GitHub Pages

`.github/workflows/build.yml` runs on pull requests, pushes to `main`, and `v*` version tags.

1. Verify the Keyman source map and compile `.kmx`, `.js` and `.kmp`.
2. Check the compiled package and upload downloadable CI artifacts.
3. On `main`, deploy `web/index.html` and the freshly compiled `onnoy.js` together using GitHub Pages.
4. On a `v*` tag, attach `.kmp`, `.kmx` and `.js` to the GitHub release.

**Pages must use the GitHub Actions source**. No separate `preview.html`, `docs` branch, or committed compiled keyboard is needed. The test site only works after a successful compiled deployment, not by opening `web/index.html` as a local file.

## Scope and known limitations

- Desktop physical US-QWERTY keys are the reference. A touch layout has not been designed.
- The website is a browser test surface, not an OS keyboard installer.
- Input method shortcut handling (especially AltGr/Right Alt) varies by browser and operating system.
- Fonts/renderers shape conjuncts; Onnoy outputs Unicode code points.
- The source mapping is documented above; broader language coverage should be assessed through real-world testing.
- Some historical characters and the double danda are deliberately not assigned.
- Licensed under the [MIT License](LICENSE). Copyright © 2026 Muhtasham Nawr al-Mahmud. Any required upstream notices must also be preserved.

## Contributing

For a typing bug, provide the OS, browser or Keyman version, exact keystrokes, expected Unicode output, and actual result. See [CONTRIBUTING.md](CONTRIBUTING.md).