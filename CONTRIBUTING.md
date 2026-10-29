# Contributing

Contributions to Onnoy are welcome, especially reproducible typing bugs, corrections to the keymap, and fixes to installation or build problems.

## Report a problem

[Open an issue](https://github.com/mnalmahmud/onnoy-keyman/issues) and include:

1. **Environment:** operating system, browser (for the website) or Keyman version (for desktop).
2. **Keystrokes:** physical keys, in order, including Shift and Right Alt/AltGr.
3. **Expected output** and **actual output**. Include Unicode code points if the characters look identical.
4. **Reproduction:** whether the problem occurs in the [online test](https://mnalmahmud.github.io/onnoy-keyman/), an installed keyboard, or both.

For rendering defects, mention the application and font. For broken AltGr behavior, mention the host keyboard layout.

## Change a key assignment

Please start with an issue before moving existing assignments. Describe the existing mapping, the proposed mapping, the typing problem it solves, and any compatibility costs. Empty slots do not need to be filled without a practical reason.

The authoritative implementation is `source/onnoy.kmn`. When changing it, update the relevant table and examples in `README.md` and extend `verify_keyman.py` to cover the change. Avoid maintaining an independent JavaScript typing implementation: web input must use the compiled Keyman keyboard.

## Build and test

You need Node.js, Python 3, Bash, and Keyman Developer CLI 18.

```sh
npm install -g @keymanapp/kmc@18
python3 verify_keyman.py
bash scripts/build.sh
python3 scripts/verify_build.py
node --check web/app.js
```

The build should produce `build/onnoy.kmx`, `build/onnoy.js`, and `build/onnoy.kmp`. These are generated files; do not commit them.

The source mapping tests are static. For typing or UI changes, also test in Keyman or the deployed website. In particular, check base, Shift, AltGr and AltGr+Shift; conjuncts; numeric and punctuation keys; and behavior after switching keyboards.

## Pull requests

- Keep changes focused and describe the problem they address.
- List the tests you ran and the platforms you tested.
- Include screenshots for visual changes, not for ordinary mapping edits.
- Add required third-party copyright notices if you incorporate outside material.
- Don't describe a platform as supported solely because the package compiled.

CI runs on pull requests. The maintainer reviews changes before merging to `main`.

By contributing, you agree that your contribution may be distributed under the project's [MIT License](LICENSE).
