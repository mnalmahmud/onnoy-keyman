# Install Onnoy natively on macOS

Onnoy uses Apple's built-in keyboard-layout mechanism. It does not need Keyman or an input-method utility running in the background.

## Build and install locally

On macOS, run:

```sh
python3 scripts/build.py generate
bash scripts/package-macos.sh
```

This creates `build/onnoy-macos.pkg` using Apple's `pkgbuild`. It is currently unsigned, so macOS may block it depending on local security policy. Do not bypass security prompts for untrusted downloads.

For manual, per-user installation, copy `dist/macos/Onnoy.keylayout` to `~/Library/Keyboard Layouts/`, then log out and in if needed. Add Onnoy via System Settings → Keyboard → Input Sources.

The keyboard layout is native; the `pkgbuild` tool is needed only for packaging. Option corresponds to the AltGr layer. Test Command shortcuts and behavior in actual applications. No claim of macOS notarization or on-device verification is made.

The macOS ISO extra key (key code 10) and the grave position (key code 50) need real hardware validation. The grave position must produce virama while the extra ISO key produces backslash/pipe. A generated XML or unsigned package alone does not prove this.
