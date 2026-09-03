# CSF1 Viewer — Linux

> **WARNING — EXPERIMENTAL SOFTWARE**
>
> This is an unfinished prototype for JCkernel / CSF1. It can mis-detect disks, refuse to mount, or (if you use Format / Install) **erase a storage device**. It is not a product, not audited, and not for production data.
>
> Use only on copies or media you can afford to lose. You are responsible for what you point it at.

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

**Update** checks this public repo's `VIEWER_VERSION` and can download `main`. No GitHub login.
