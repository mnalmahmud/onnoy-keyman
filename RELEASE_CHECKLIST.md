# Release checklist

This checklist is for maintainers. **A successful CI build is necessary, but not sufficient, for a release.**

## Source and metadata

- [x] MIT license present with copyright © 2026 Muhtasham Nawr al-Mahmud.
- [x] Repository on `main` with an automated Keyman build and Pages deployment.
- [ ] Review any copied or adapted upstream content and retain legally required notices.
- [ ] Check name, version and language metadata in `source/onnoy.kmn` and `source/onnoy.kps`.
- [ ] Check all documentation, example sequences and project URLs.

## Quality checks

- [ ] CI builds `onnoy.kmx`, `onnoy.js` and `onnoy.kmp` successfully.
- [ ] A maintainer opens the deployed website and types real text using KeymanWeb.
- [ ] Verify base, Shift, AltGr and AltGr+Shift layers with physical keys.
- [ ] Verify vowels, virama and conjuncts, Bengali/Latin digits, currency, danda, nukta and joiners.
- [ ] Check clipboard, clear, Unicode inspection and mobile-width layout on the website.
- [ ] Test `.kmp` installation and typing on each desktop OS claimed as supported.
- [ ] Confirm Pages does not deploy a stale or mocked keymap.

## Publish

- [ ] Inspect the compiled package and CI artifacts.
- [ ] Update `CHANGELOG.md` with the actual release date and tested platforms.
- [ ] Create a version tag such as `v1.0.0` only after checks pass.
- [ ] Confirm the GitHub Release contains the `.kmp`, `.kmx` and `.js` files.
- [ ] Verify installation and download links from the public release page.
