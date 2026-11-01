# Install Onnoy in Keyman for Android or iPhone/iPad

Onnoy's **Keyman package** is shared between desktop Keyman and Android/iOS.
The package contains a compiled JavaScript keyboard with a generated touch
interface. No separately maintained mobile Unicode mapping is required.

## Build a development package

From the repository:

```bash
python3 scripts/build.py generate
npm install
npm run build:keyman
python3 tests/check_mobile_package.py
```

The resulting installable file is `dist/keyman/onnoy.kmp`. This is a
developer build, not yet a real-device-verified public release.

## Android

Install the Keyman app. Transfer the `.kmp` file to the phone, open Keyman,
choose its keyboard settings, then **Install from local file** (menu wording
may vary). Select the package and confirm installation.

Keyman documentation:
https://help.keyman.com/products/android/current-version/basic/config/install-keyboard-or-dictionary

## iPhone and iPad

Install the Keyman app, put the `.kmp` in Files or download it on the device,
then choose **Settings → Install From File** in Keyman. Approve installation.
To use Keyman outside its own app, enable the Keyman keyboard in iOS keyboard
settings.

Keyman documentation:
https://help.keyman.com/products/iphone-and-ipad/18.0/basic/config/

## Touch layout

- Default: QWERTY-row ordering of Bengali and Assamese signs.
- **Shift:** alternate Bengali character assignments.
- **Long press:** alternate letters, vowel signs and less-used characters.
- **Virama:** dedicated key next to space on every page.
- **?123:** Bengali digits, punctuation and Latin digits by long press.
- **Globe/menu:** change installed languages/keyboards.
- **Backspace** and **Enter:** native input actions.

Dots shown before vowel marks are visual aids only; they are not inserted.
The special alternatives labelled ZWJ and ZWNJ insert U+200D and U+200C.

## Device acceptance checklist

Before publishing a mobile-compatible release, test the package on real
Android and iOS devices, including narrow and wide screens, portrait and
landscape orientation. Check all layers, long-press popup selection, typed
codepoint sequences, conjuncts, deletion, Assamese letters, keyboard switching,
iOS third-party keyboard activation, and language-menu behavior.

CI confirms touch-layout character coverage, Keyman compilation, package
contents and desktop-browser typing. Those checks **do not establish** that
the full touch UX functions correctly in Android and iOS applications.
