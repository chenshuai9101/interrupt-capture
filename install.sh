#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TARGET="$HOME/bin/ic"

mkdir -p "$HOME/bin"
ln -sfn "$SCRIPT_DIR/interrupt_capture.py" "$TARGET"
chmod +x "$SCRIPT_DIR/interrupt_capture.py"

echo "Installed ic -> $TARGET"
echo
echo "Add this alias to your shell profile if you want a shorter restore command:"
echo "  alias resume='ic resume'"
echo
echo "Make sure ~/bin is on PATH. For zsh:"
echo "  export PATH=\"\$HOME/bin:\$PATH\""
