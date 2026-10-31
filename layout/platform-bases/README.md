# Pinned platform US reference sources

These are **build-time inputs only** for `scripts/generate.py`. They are not
runtime keyboard dependencies and they are not custom Onnoy assignments.

- `windows-us.klc`: a Microsoft Keyboard Layout Creator export of the standard
  US layout, originally saved as `keymap/klc/409 US.klc` in
  [commanderx16/x16-rom](https://github.com/commanderx16/x16-rom/blob/master/keymap/klc/409%20US.klc)
  (upstream blob `8ee6a5e2c0e6cac036e8188849d81d1f8f9a19a9`). The generator patches physical KLC
  rows, keeping Windows-native scan/VK and Control outputs.
- `macos-us.keylayout`: a minimal U.S.-style keymap of only five *unchanged*
  keys, extracted from a U.S.-derived Ukelele keyboard reference in
  [ministryofprogramming/bosnian-macos-keyboard](https://github.com/ministryofprogramming/bosnian-macos-keyboard/blob/master/src/Bosnian%20-%20U.S..keylayout)
  (upstream blob `a67605fd05384a36d8bf152aab49517d253aa1a7`). The five key outputs were compared with
  [an exported macOS U.S. keyboard layout](https://gist.github.com/paiv/a396403b890647e0faa22b03d7d5f573).
  For active keys, the Onnoy keymap uses Apple's `baseMapSet`/`baseIndex`
  to inherit from this reference set and overrides only Onnoy-specific keys.
  It includes the ordinary macOS Option punctuation behavior for these five
  keys, including the Option+Backtick dead-key action.

The reference snapshots are pinned so native files can be generated offline
and reproducibly on any host. They are not automatically refreshed from the
user's installed OS keyboard layout; importing a new version is a deliberate
reviewed change.

`layout/onnoy.json` remains the sole source of **Onnoy overrides**, while
these two files supply platform-specific ordinary keyboard behavior.

The macOS reference stores a single complete ordinary-US mapping for Command
and Control (base index 4), shared by both Onnoy shortcut layers.
The normal Space character is retained on all four Onnoy typing layers,
including Option: U.S. Option+Space nonbreaking space is deliberately normalized
to ASCII Space for Onnoy.
