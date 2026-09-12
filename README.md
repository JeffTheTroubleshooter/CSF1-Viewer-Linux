# CSF1 Viewer — Linux

> **WARNING — EXPERIMENTAL SOFTWARE**
>
> Unfinished prototype. Format / Install can erase a disk. Not for production data.

Public host tool for [JCkernel](https://github.com/JeffTheTroubleshooter/JCkernel) CSF1 disks (`.img`, `.qcow2`, live USB).

This repo is the **Linux edition**. It is not the kernel.

Sister editions:

- [CSF1-Viewer-macOS](https://github.com/JeffTheTroubleshooter/CSF1-Viewer-macOS)
- [CSF1-Viewer-Windows](https://github.com/JeffTheTroubleshooter/CSF1-Viewer-Windows)

## Run

```bash
chmod +x CSF1-Viewer.sh
./CSF1-Viewer.sh
```

Needs `python3`. Fedora GUI: `sudo dnf install python3-tkinter`.

**Update** in the window checks this public repo’s `VIEWER_VERSION` and can download `main` over the local files. No GitHub login.

## Pull crash logs (v0.3.10)

Bootable USB layout: ESP + a **small CSF1 partition** (usually `/dev/sdX2`)
with the superblock at LBA 0 of that slice or LBA 4096 of the whole disk.

```bash
sudo ./CSF1-Viewer.sh
# Scan JCkernel USB → Mount / Detect CSF1 → Pull crash logs
```

Writes `~/Desktop/JCkernel-crash-logs/Base/BPL/` and
`~/Desktop/JCkernel-crash-logs/Base/Crash_Dump/`.

Mount tries **partition 2, then 1, then the whole disk**, so a tiny CSF1
slice is not skipped.

## Boot USB + BPL (v0.3.8)

`make bootable-usb` writes ESP + CSF1 partition 2 (origin LBA 4096).
After a 0.0.323+ boot, look at `/Base/BPL/` and `/Base/Crash_Dump/`.

## Related

JCkernel (OS) may stay private. These three Viewer repos stay public so Update works without a token.
