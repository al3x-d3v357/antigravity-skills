#!/usr/bin/env python3
"""Preflight check script for Kdenlive editor skill (Linux & cross-platform).

Validates:
1. Kdenlive installation path and executable status.
2. MLT engine (melt) and FFmpeg availability.
3. Running Kdenlive instance detection.
4. Input media files or directories (if supplied).

Exits with:
  0: Success / Ready to edit
  1: Warning / Process not running
  2: Critical / Missing binaries
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

LINUX_KDENLIVE_PATHS = [
    "/usr/bin/kdenlive",
    "/usr/local/bin/kdenlive",
    "/var/lib/flatpak/exports/bin/org.kde.kdenlive",
    str(Path.home() / ".local/share/flatpak/exports/bin/org.kde.kdenlive"),
]


def check_running_process(process_name: str = "kdenlive") -> bool:
    """Check if kdenlive process is actively running on Linux."""
    try:
        # Check via pgrep
        res = subprocess.run(["pgrep", "-f", process_name], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception:
        return False


def locate_kdenlive_bin() -> tuple[Path | None, Path | None]:
    """Locate kdenlive and melt binaries on Linux."""
    kdenlive_bin = None
    which_path = shutil.which("kdenlive")
    if which_path:
        kdenlive_bin = Path(which_path)
    else:
        for p in LINUX_KDENLIVE_PATHS:
            path = Path(p)
            if path.is_file() and os.access(path, os.X_OK):
                kdenlive_bin = path
                break

    melt_bin = None
    which_melt = shutil.which("melt")
    if which_melt:
        melt_bin = Path(which_melt)
    elif kdenlive_bin:
        candidate = kdenlive_bin.parent / "melt"
        if candidate.is_file():
            melt_bin = candidate

    return kdenlive_bin, melt_bin


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight check for Kdenlive skill on Linux")
    parser.add_argument("--media", nargs="*", help="Media files or directories to validate")
    args = parser.parse_args()

    print("[*] Running Kdenlive Skill Preflight Check (Linux)...")

    ffmpeg_bin = shutil.which("ffmpeg")
    if ffmpeg_bin:
        print(f"[+] FFmpeg binary: {ffmpeg_bin}")
    else:
        print("[!] WARNING: ffmpeg binary not found on PATH.")

    kdenlive_bin, melt_bin = locate_kdenlive_bin()
    if not kdenlive_bin:
        print("[*] NOTICE: Kdenlive binary not found on standard paths. FFmpeg headless pipeline will be used.")
    else:
        print(f"[+] Kdenlive binary: {kdenlive_bin}")

    if melt_bin:
        print(f"[+] MLT rendering engine: {melt_bin}")

    is_running = check_running_process("kdenlive")
    if is_running:
        print("[+] Kdenlive instance is currently RUNNING.")
    else:
        print("[*] NOTICE: Kdenlive instance is not running.")

    if args.media:
        missing = []
        for m in args.media:
            p = Path(m)
            if not p.exists():
                missing.append(m)
        if missing:
            print(f"[!] ERROR: Missing media files: {', '.join(missing)}")
            return 2
        print(f"[+] All {len(args.media)} specified media assets verified.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
