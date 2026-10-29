# Contributing

Onnoy has one authoritative mapping: [`layout/onnoy.json`](layout/onnoy.json). The Linux, macOS, Windows and Keyman sources are generated. Do not edit generated files to change a character assignment.

To change a key, explain the existing assignment, proposed assignment, affected modifiers and compatibility cost in an issue. Edit the JSON mapping and run:

```sh
python3 scripts/generate.py
python3 scripts/generate.py --check
```

For bugs, include the OS, application, physical key sequence, expected Unicode output and actual output. State whether the problem happens on a native desktop layout or in the KeymanWeb test site.

Native integration must be tested on its target OS; successful source generation or XML parsing is not sufficient. Windows requires MSKLC compilation and installer testing.

Pull requests should update tests when assignments change. The project uses the [MIT License](LICENSE).
