# Contributing to Onnoy

Please open an issue before making a major key reassignment. Include physical key sequences, the expected Unicode string, actual output, OS/browser, and (for desktop) Keyman version. Use the live GitHub Pages test site to reproduce web issues. For mapping changes, update `audit.json` and `source/onnoy.kmn` together and ensure `python3 verify_keyman.py` passes. The CI workflow compiles and packages the Keyman artifacts, then deploys the real web keyboard to Pages on `main`.

No extra keys should be assigned merely because slots are vacant. Focus changes on reproducible problems and predictable typing.