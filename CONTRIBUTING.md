# Contributing to Onnoy

Thanks for helping improve Onnoy. The goal is a predictable Unicode keyboard with a coherent physical-key layout, not simply filling every unused key combination.

## Before filing a bug

Check whether the problem occurs in the [live KeymanWeb test](https://mnalmahmud.github.io/onnoy-keyman/), the installed Keyman keyboard, or both. If possible, test on a physical US-QWERTY keyboard. Please include:

- Operating system and version; browser or Keyman version.
- Physical keys and modifiers pressed, in order (for example, `Shift+S I K F X A`).
- Expected text and actual text, ideally with Unicode code points.
- Whether Right Alt / AltGr works in other keyboard layouts.
- A minimal example, and a screenshot only if visual rendering matters.

Use [GitHub Issues](https://github.com/mnalmahmud/onnoy-keyman/issues) to report reproducible bugs.

## Proposing changes

Please open an issue before changing established mappings. Explain the typing problem, proposed assignment, alternatives considered, compatibility impact and any existing assignments that would move. Avoid inventing scores or declaring unused positions inherently problematic. A change should be justified by typing behavior, consistency or clear language coverage.

## Local development

Install Python 3, Node.js and the Keyman Developer CLI:

```sh
npm install -g @keymanapp/kmc@18
python3 verify_keyman.py
bash scripts/build.sh
python3 scripts/verify_build.py
```

The authoritative keyboard mapping is [`source/onnoy.kmn`](source/onnoy.kmn); package metadata lives in `source/onnoy.kps`. Update documentation and tests with mapping changes. Do not edit a nonexistent `audit.json` or add a second handwritten typing map.

The browser playground is in `web/`. It must load the **compiled KeymanWeb keyboard**, not replace it with custom JavaScript transliteration. Verify user-facing changes on a desktop and mobile viewport, and check that the editor still accepts genuine Keyman output.

## Pull requests

Keep each PR focused. Include a concise explanation, testing instructions, and screenshots for visible UI changes. Don't commit compiled `.kmx`, `.js` or `.kmp` output; the GitHub Actions workflow produces and publishes those artifacts.

Contributions are submitted for inclusion under the project's [MIT license](LICENSE). Include third-party attributions where applicable.

## Community expectations

Discuss ideas and defects respectfully. Review the proposal, not the person. Decisions should be based on reproducible behavior, clarity and maintainability.
