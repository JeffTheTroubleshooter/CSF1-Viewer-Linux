#!/usr/bin/env bash
# CSF1 Viewer Linux edition — public Update, no GitHub login.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
export CSF1_VIEWER_EDITION="${CSF1_VIEWER_EDITION:-Linux}"
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required."
  exit 1
fi
echo "CSF1 Viewer Linux  $(tr -d '\n' < VIEWER_VERSION 2>/dev/null || echo '?')"
python3 "$DIR/jck_version.py" || true
echo
if python3 -c "import tkinter" >/dev/null 2>&1; then
  exec python3 "$DIR/csf1_viewer.py" --tk "$@"
else
  echo "tkinter missing — browser UI on http://127.0.0.1:8765/"
  echo "Fedora: sudo dnf install python3-tkinter"
  exec python3 "$DIR/csf1_viewer.py" --web "$@"
fi
