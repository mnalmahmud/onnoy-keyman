# Release checklist

Use this before publishing a version of Onnoy. **A green build is not a substitute for testing the keyboard.**

## 1. Verify the source

- [ ] Confirm the intended mappings in `source/onnoy.kmn` match `README.md`.
- [ ] Confirm the keyboard name, version, and language metadata in `source/onnoy.kmn` and `source/onnoy.kps`.
- [ ] Review third-party material and preserve any required license or attribution notices.
- [ ] Run the source checks and compiler:

  ```sh
  python3 verify_keyman.py
  bash scripts/build.sh
  python3 scripts/verify_build.py
  ```

- [ ] Confirm the build produced `onnoy.kmx`, `onnoy.js`, and `onnoy.kmp`, and that the `.kmp` includes the compiled keyboard.

## 2. Test typing

- [ ] Install `onnoy.kmp` in Keyman on each desktop platform you intend to claim as supported. Record the OS and Keyman versions.
- [ ] Verify base, Shift, AltGr and AltGr+Shift on a physical keyboard.
- [ ] Check vowels and vowel signs; virama and conjuncts; nukta; ZWNJ and ZWJ.
- [ ] Check Bengali and Latin digits, ৳, $, danda, and the literal period.
- [ ] Verify that unassigned combinations and host punctuation behave as documented.
- [ ] Open the [GitHub Pages test](https://mnalmahmud.github.io/onnoy-keyman/), confirm the compiled keyboard activates, and type the README examples.
- [ ] Test copy, clear, the Unicode inspector, and keyboard switching in the browser.
- [ ] Record known limitations rather than presenting untested combinations as supported.

## 3. Publish

- [ ] Confirm that the final `main` commit builds successfully and GitHub Pages deploys.
- [ ] Update `CHANGELOG.md` with the version, release date, and user-visible changes.
- [ ] Match the intended version in Keyman metadata before tagging.
- [ ] Create and push a version tag (for example, `v1.0.0`).
- [ ] Check the GitHub Release for the installable `onnoy.kmp` and accompanying compiled artifacts.
- [ ] Download the published `.kmp` and verify installation from the release asset itself.
- [ ] Confirm the README's release and testing links work.

Do not publish a stable release while a required platform test is outstanding; either finish the test or narrow the stated support.
