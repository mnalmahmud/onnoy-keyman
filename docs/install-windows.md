# Install Onnoy natively on Windows

Windows uses a compiled keyboard layout DLL and an OS-registered keyboard layout. Once installed, it works through Windows' built-in text input machinery and does not require Keyman or another background IME.

## Build the native setup

The repository currently generates **`dist/windows/onnoy.klc`**, a source file for Microsoft Keyboard Layout Creator (MSKLC). A .klc file is *not* itself installable.

On a Windows development machine with MSKLC 1.4 and `kbdutool.exe` available:

```powershell
python scripts/generate.py
powershell -ExecutionPolicy Bypass -File scripts/package-windows.ps1
```

Inspect the generated setup files and install them on a test Windows machine. Verify Unicode output, Ctrl+Alt/AltGr, ZWJ/ZWNJ, and the supplementary Unicode scalar U+11DF0. The project does **not yet provide a verified Windows installer**; an automated Windows CI job validates source generation but does not compile MSKLC.

Build-time MSKLC is not a required runtime dependency. If a release publishes a verified installer, ordinary users should need only that installer and Windows' language/keyboard settings.

### Shortcuts

AltGr may be exposed to applications as Ctrl+Alt. Windows and individual apps may intercept Ctrl+Alt+Z. Please report exact OS/app versions and actual Unicode output if this occurs.
