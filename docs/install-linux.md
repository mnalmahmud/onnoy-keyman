# Install Onnoy natively on Linux

Onnoy is an XKB layout, **not** an input method: no Keyman, Fcitx, IBus, or background process is needed to interpret the keys. You still need your desktop's standard keyboard-layout chooser and an XKB configuration that loads the generated symbols.

## Build

```sh
python3 scripts/build.py generate
bash scripts/package-linux.sh
```

The package is `build/onnoy-linux-native.tar.gz`. It contains an XKB symbols file and `install.sh`. The installer only copies the layout into `~/.config/xkb/symbols/onnoy`; it does **not** register a system-wide layout or modify XKB rules.

## Test X11 first

Once the XKB symbols are accessible to the X server, on traditional X11 you may use:

```sh
setxkbmap -I"$HOME/.config/xkb" -layout onnoy -variant basic
```

Some X11 servers do not honor the per-user XKB include path. If the command fails, install `dist/linux/symbols/onnoy` as `/usr/share/X11/xkb/symbols/onnoy` (requires administrator permissions) and then reload the XKB layout.

### Desktop integration

GNOME, KDE, and other Wayland compositors usually select layouts through XKB rules/desktop settings, not `setxkbmap`. Installing an unregistered symbols file alone does not make Onnoy appear in the graphical keyboard list. A distribution package may need to register `onnoy(basic)` in the system XKB rules and restart the session or compositor.

The Linux archive is currently **a native-layout bundle, not a one-click installer**. Avoid replacing OS files silently: follow your distribution's documented XKB registration process. Record X11/Wayland desktop and application when reporting a typing problem.

## Known modifier caveats

Right Alt acts as AltGr where supported; a compositor or application may intercept its own shortcuts. ZWJ and ZWNJ are `AltGr+J` and `Shift+AltGr+J`. The Space key always outputs a space.
