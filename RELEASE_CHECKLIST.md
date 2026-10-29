# Release checks

- [ ] Verify all generated outputs match `layout/onnoy.json`.
- [ ] Compile XKB using `xkbcomp` on Linux and test it in a desktop session.
- [ ] Validate the `.keylayout` XML and test it as an installed macOS input source.
- [ ] Compile the Windows `.klc` with MSKLC, package a native Windows installer and test it before publishing Windows installation files.
- [ ] Compile and test KeymanWeb with physical key presses, including AltGr.
- [ ] Confirm downloads and GitHub Pages deployment.
- [ ] Review copyright notices, metadata and changelog.
- [ ] Tag a release only after platforms described as supported have been tested.
