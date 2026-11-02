# Onnoy · অন্বয়

Onnoy is a keyboard for writing Bangla and other languages using Bengali letters. It works on computers and phones, with Shift and Right Alt giving access to additional characters.

[**Try the keyboard**](https://mnalmahmud.github.io/onnoy-keyman/) · [Download builds](https://github.com/mnalmahmud/onnoy-keyman/actions)

## Languages

Onnoy is designed for **Bangla** and also supports writing **Kokborok, Bishnupriya Manipuri, Kurmali (Kudmali), Hajong, and Meitei (Manipuri)** in Bengali script.

## How to type

The layout follows the positions of the keys on a regular English keyboard.

- Press **K** for **ক**, or **Shift + K** for **খ**.
- The **Grave** key (immediately left of **1**) types **্**, which joins consonants. Press **K**, **Grave**, then **X** to type **ক্ষ**.
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
