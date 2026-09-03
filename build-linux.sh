#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
python3 -m PyInstaller --noconfirm --clean --onefile --name CSF1-Viewer \
  --add-data "VIEWER_VERSION:." --add-data "JCKERNEL_VERSION:." --add-data "WARNING.md:." \
  --hidden-import csf1_core --hidden-import host_usb --hidden-import jck_version \
  --hidden-import jck_install --hidden-import qcow2io csf1_viewer.py
echo "Binary: $DIR/dist/CSF1-Viewer"
