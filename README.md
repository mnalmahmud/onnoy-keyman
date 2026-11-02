# Onnoy · অন্বয়

**Write Bangla with the keys on your computer or phone.** Press a key to type a Bengali letter or vowel sign. Hold Shift or Right Alt for more characters. You don't have to spell words in English to convert them into Bangla.

[**Try Onnoy online**](https://mnalmahmud.github.io/onnoy-keyman/) · [Get the keyboard](https://github.com/mnalmahmud/onnoy-keyman/actions)

## Languages

Onnoy is made for **Bangla**. You can also use it to write these languages **with Bengali letters**:

- **Kokborok (Tripuri)** — including its special vowel combinations **অৗ** and **উা**.
- **Kurmali (Kudmali)** — the Bengali-script writing used in West Bengal.
- **Hajong** — the Bengali-script writing used in Bangladesh.
- **Meitei (Manipuri)** — its Bengali-script writing, distinct from the Meitei Mayek alphabet.

This is a Bengali-letter keyboard; it does not type other alphabets used for these languages. Bishnupriya Manipuri can be typed using the Bengali-র spelling convention. An alternate layout using Assamese-style **ৰ** in place of **র** may be added later; full Assamese support is deferred.

The language coverage is based on [Unicode's Kokborok spelling rules](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-12/), [SIL Bangladesh's language-writing projects](https://www.silbangladesh.org/language_education/orthography), [Kurmali writing samples](https://omniglot.com/writing/kurmali.htm), and [research on Bengali-script Manipuri](https://aclanthology.org/2026.wmt-main.200/).

## How to type

The layout follows the positions of the keys on a regular English keyboard.

- Press **K** for **ক**, or **Shift + K** for **খ**.
- The `\` `~` key (beside **1**) types **্**, the sign used to join consonants. Press **K**, that key, and **X** to type **ক্ষ**.
- The number keys type **০–৯**. Hold **Right Alt** (also called **AltGr**) to type **0–9**.
- The [online keyboard](https://mnalmahmud.github.io/onnoy-keyman/#workspace) shows all four layers (Base, Shift, AltGr and Shift + AltGr), lets you inspect individual keys, and includes Unicode details.

## Install

**Try it first:** You can type in your browser without installing anything.

For desktop and mobile, open a successful [build](https://github.com/mnalmahmud/onnoy-keyman/actions) and download the **onnoy-native-keyman-web** artifact.

- **Windows, macOS, Android, iPhone or iPad with Keyman:** Install [Keyman](https://keyman.com/), then import the included `keyman/onnoy.kmp` package.
- **Windows without Keyman:** Open `dist/onnoy.klc` in Microsoft Keyboard Layout Creator to build a Windows keyboard installer.
- **macOS without Keyman:** Copy `dist/onnoy.keylayout` into `~/Library/Keyboard Layouts/`, sign out and back in, then enable it in Keyboard settings.
- **Linux:** Install the `dist/onnoy.xkb_symbols` or `dist/onnoy.xkb_keymap` layout through your XKB configuration.

The native Windows, macOS and Linux installation methods still need testing on those systems.

## Build from source

You need Python 3.11+, Node.js 22 and pnpm 10.19.0.

```sh
python -m pip install kalamine==0.40
kalamine build layout.toml --qwerty-shortcuts
pnpm install --frozen-lockfile
pnpm run build:keyman
```

The native keyboard files appear in `dist/`; Keyman's files appear in `keyman/`. Run the tests with:

```sh
python -m unittest discover -s tests -p 'test_*.py'
```

To change which character a key types, edit [`layout.toml`](layout.toml). The Keyman keyboard is generated from it automatically. Mobile key placement and long-press options are in [`keyman/onnoy.keyman-touch-layout`](keyman/onnoy.keyman-touch-layout).

## License

[MIT](LICENSE).
