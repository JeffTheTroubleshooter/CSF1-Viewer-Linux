#!/usr/bin/env python3
"""Put Crash_Dump / BPL log files onto an existing USB CSF1 volume.

Usage (Linux, as root if the target is a real disk):

  python3 seed_crashdump.py /dev/sdX
  python3 seed_crashdump.py /dev/sdX2
"""
from __future__ import annotations

import os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from csf1_core import RawBlockDev, CSF1Volume

DEST = "/Base/Crash_Dump"
BPL = "/Base/BPL"
FILES = {
    "README.txt": "Crash_Dump (CD disk)\nDIAG writes diag_log.txt here.\nboot_stuck_log.txt if a step sits still 15s.\n",
    "boot_stuck_log.txt": "JCkernel boot_stuck_log.txt\nstatus=waiting\npercent=\nstep=\n",
    "boot_ok.log": "# boot_ok.log\n",
    "boot_fail.log": "# boot_fail.log\n",
    "diag_log.txt": "JCkernel DIAG log\nstatus=placeholder\n",
}
BPL_FILES = {
    "README.txt": "BPL - Boot Process Logs\nboot_passed.log\nboot_failed.log\nboot_passed_with_warnings.log\n",
    "boot_passed.log": "# boot_passed.log\n",
    "boot_failed.log": "# boot_failed.log\n",
    "boot_passed_with_warnings.log": "# boot_passed_with_warnings.log\n",
}

def put(vol, name, text, dest=DEST):
    data = text.encode("utf-8")
    for e in vol.files:
        if e.path.rstrip("/") == dest and e.name == name:
            vol.replace_file_content(e.index, data)
            return "replaced"
    tmp = os.path.join(tempfile.gettempdir(), name)
    open(tmp, "wb").write(data)
    try:
        vol.add_file(tmp, dest)
    finally:
        try: os.remove(tmp)
        except OSError: pass
    return "added"

def ensure_folder(vol, parent, name):
    parent = parent.rstrip("/") or "/"
    for e in vol.folders:
        if e.name == name and (e.path.rstrip("/") or "/") == parent:
            return
    vol.add_folder(parent, name)

def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__.strip()); return 1
    target = sys.argv[1]
    if not os.path.exists(target):
        print("not found:", target); return 1
    dev = RawBlockDev(target, writable=True)
    vol = CSF1Volume(dev)
    if not vol.detect_and_mount():
        print("no CSF1 on", target); print(vol.message); dev.close(); return 2
    print("mounted:", vol.sb.disk_name if vol.sb else "?")
    ensure_folder(vol, "/", "Base")
    ensure_folder(vol, "/Base", "Crash_Dump")
    ensure_folder(vol, "/Base", "BPL")
    for name, text in FILES.items():
        print(" ", put(vol, name, text, DEST), DEST + "/" + name)
    for name, text in BPL_FILES.items():
        print(" ", put(vol, name, text, BPL), BPL + "/" + name)
    dev.flush(); dev.close()
    print("done.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
