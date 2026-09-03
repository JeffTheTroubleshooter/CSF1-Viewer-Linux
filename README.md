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

## Drag and drop (v0.3.7)

1. Mount the USB / CSF1 image.
2. Set dest path (default `/Base/Files`).
3. Drop files **or a whole folder** onto the second drop zone (web) or onto the window (desktop Tk).
4. Import file / Import folder buttons do the same thing.

CSF1 file cap is still 256 KiB per file.

## Related

JCkernel (OS) may stay private. These three Viewer repos stay public so Update works without a token.
