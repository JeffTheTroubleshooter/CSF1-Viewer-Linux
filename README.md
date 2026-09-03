# CSF1 Viewer — Linux

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

JCkernel (OS) may stay private. These three Viewer repos stay public so Update works without a token.
