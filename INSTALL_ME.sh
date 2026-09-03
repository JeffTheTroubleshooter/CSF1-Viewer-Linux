#!/usr/bin/env bash
# Install CSF1 Viewer into ~/.local/bin and the app menu. No sudo.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
BIN_SRC=""
for c in "$DIR/CSF1-Viewer" "$DIR/dist/CSF1-Viewer"; do
  [[ -f "$c" ]] && BIN_SRC="$c" && break
done
if [[ -z "$BIN_SRC" ]]; then
  echo "CSF1-Viewer binary not found next to INSTALL_ME.sh"
  exit 1
fi
echo "WARNING: experimental program. Format / Install can erase a disk."
BIN_DIR="${HOME}/.local/bin"
APP_DIR="${HOME}/.local/share/applications"
mkdir -p "$BIN_DIR" "$APP_DIR"
install -m 0755 "$BIN_SRC" "$BIN_DIR/CSF1-Viewer"
if [[ -f "$DIR/CSF1-Viewer.desktop" ]]; then
  sed "s|^Exec=.*|Exec=${BIN_DIR}/CSF1-Viewer|" "$DIR/CSF1-Viewer.desktop" > "$APP_DIR/CSF1-Viewer.desktop"
  sed -i "s|^TryExec=.*|TryExec=${BIN_DIR}/CSF1-Viewer|" "$APP_DIR/CSF1-Viewer.desktop" || true
else
  printf '%s\n' '[Desktop Entry]' 'Type=Application' 'Name=CSF1 Viewer' \
    "Exec=${BIN_DIR}/CSF1-Viewer" 'Terminal=false' 'Categories=Utility;' > "$APP_DIR/CSF1-Viewer.desktop"
fi
echo "Installed $BIN_DIR/CSF1-Viewer"
echo "Start: CSF1-Viewer"
