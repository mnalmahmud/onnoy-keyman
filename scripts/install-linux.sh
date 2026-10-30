#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
target="${XDG_DATA_HOME:-$HOME/.local/share}/onnoy"
mkdir -p "$target"
cp onnoy Onnoy.XCompose "$target/"
echo "Onnoy files installed in $target"
echo "To register a native XKB layout, copy $target/onnoy into the XKB symbols directory"
echo "(usually /usr/share/X11/xkb/symbols/, requiring administrator privileges),"
echo "and add an XKB rules entry for onnoy(basic) using your distribution's procedure."
echo "Add this line to ~/.XCompose if your Compose configuration supports includes:"
echo "include \"$target/Onnoy.XCompose\""
echo "Then select the layout and restart affected applications."
echo "NOTE: This installer does not automatically change global XKB or user Compose settings."
