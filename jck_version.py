#!/usr/bin/env python3
"""Public-repo version check for CSF1 Viewer editions. No GitHub login."""

from __future__ import annotations

import json
import os
import re
import ssl
import sys
import tempfile
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OWNER = os.environ.get("CSF1_VIEWER_OWNER", "JeffTheTroubleshooter")
EDITION = os.environ.get("CSF1_VIEWER_EDITION", "Linux")
REPO = os.environ.get("CSF1_VIEWER_REPO", "CSF1-Viewer-" + EDITION)
FAMILY = ("CSF1-Viewer-Linux", "CSF1-Viewer-macOS", "CSF1-Viewer-Windows")
KERNEL_REPO = "JeffTheTroubleshooter/JCkernel"


def parse_ver(s):
    s = (s or "").strip().lstrip("vV")
    nums = re.findall(r"\d+", s)
    if not nums:
        return (0, 0, 0)
    while len(nums) < 3:
        nums.append("0")
    return tuple(int(x) for x in nums[:3])


def viewer_version():
    p = os.path.join(HERE, "VIEWER_VERSION")
    if os.path.isfile(p):
        try:
            return open(p, "r", encoding="utf-8").read().strip().split()[0].lstrip("v")
        except OSError:
            pass
    return "0.3.6"


def bundled_version():
    return viewer_version()


def _ssl():
    try:
        return ssl.create_default_context()
    except Exception:
        return ssl._create_unverified_context()


def _http_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "CSF1-Viewer"})
    with urllib.request.urlopen(req, timeout=12, context=_ssl()) as r:
        return r.read().decode("utf-8", "replace")


def _http_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": "CSF1-Viewer"})
    with urllib.request.urlopen(req, timeout=30, context=_ssl()) as r:
        return r.read()


def fetch_latest():
    raw = "https://raw.githubusercontent.com/%s/%s/main/VIEWER_VERSION" % (OWNER, REPO)
    errors = []
    try:
        ver = _http_text(raw).strip().split()[0].lstrip("v")
        if parse_ver(ver) > (0, 0, 0):
            return {"ok": True, "version": ver, "source": "public-VIEWER_VERSION",
                    "message": "Public %s/%s is %s" % (OWNER, REPO, ver),
                    "url": "https://github.com/%s/%s" % (OWNER, REPO)}
    except Exception as e:
        errors.append("raw: " + str(e))
    local = bundled_version()
    return {"ok": False, "version": local, "source": "offline",
            "message": "Public edition repo not reachable yet. Bundled Viewer %s. (%s)" % (local, "; ".join(errors)[:200]),
            "url": "https://github.com/%s/%s" % (OWNER, REPO)}


def compare_report():
    latest = fetch_latest()
    local = bundled_version()
    lv, bv = parse_ver(latest.get("version") or ""), parse_ver(local)
    newer = bool(latest.get("ok") and lv > bv)
    same = bool(latest.get("ok") and lv == bv and bv > (0, 0, 0))
    if newer:
        verdict = "Update available: Viewer %s -> %s" % (local, latest["version"])
    elif same:
        verdict = "Viewer is current: %s" % local
    elif latest.get("ok"):
        verdict = "Local Viewer %s is ahead of public %s" % (local, latest["version"])
    else:
        verdict = latest.get("message") or "offline"
    latest["local"] = local
    latest["viewer"] = local
    latest["newer"] = newer
    latest["verdict"] = verdict
    latest["edition"] = EDITION
    latest["family"] = list(FAMILY)
    latest["kernel_repo"] = KERNEL_REPO
    return latest


def apply_update_zip(zip_path):
    if not zip_path or not os.path.isfile(zip_path):
        return {"ok": False, "message": "No zip selected."}
    names = []
    allow = {"VIEWER_VERSION", "JCKERNEL_VERSION", "csf1_core.py", "csf1_viewer.py",
             "jck_version.py", "jck_install.py", "host_usb.py", "qcow2io.py",
             "CSF1-Viewer.sh", "CSF1-Viewer.bat", "CSF1-Viewer.command", "README.md"}
    with zipfile.ZipFile(zip_path, "r") as z:
        for info in z.infolist():
            base = os.path.basename(info.filename)
            if info.is_dir() or base not in allow:
                continue
            with open(os.path.join(HERE, base), "wb") as out:
                out.write(z.read(info.filename))
            names.append(base)
    if not names:
        return {"ok": False, "message": "Zip had no Viewer files."}
    return {"ok": True, "message": "Updated %s. Restart the Viewer." % ", ".join(names), "files": names}


def pull_github_version():
    r = compare_report()
    if not r.get("ok"):
        return r
    url = "https://codeload.github.com/%s/%s/zip/refs/heads/main" % (OWNER, REPO)
    try:
        blob = _http_bytes(url)
    except Exception as e:
        r["applied"] = False
        r["message"] = "Download failed: %s" % e
        return r
    tmp = os.path.join(tempfile.gettempdir(), "csf1-viewer-update.zip")
    with open(tmp, "wb") as f:
        f.write(blob)
    applied = apply_update_zip(tmp)
    try:
        os.remove(tmp)
    except OSError:
        pass
    applied["version"] = r.get("version")
    applied["viewer"] = viewer_version()
    return applied


def main():
    r = compare_report()
    print("CSF1 Viewer — public edition check")
    print("  Edition  : %s" % EDITION)
    print("  Repo     : %s/%s" % (OWNER, REPO))
    print("  Local    : %s" % (r.get("local") or "?"))
    print("  Public   : %s  (%s)" % (r.get("version") or "?", r.get("source") or ""))
    print("  %s" % r.get("verdict"))
    print("  Family   : %s" % ", ".join(FAMILY))
    if r.get("url"):
        print("  %s" % r["url"])
    return 0

if __name__ == "__main__":
    sys.exit(main())
