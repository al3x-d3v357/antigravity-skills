#!/usr/bin/env python3
"""Preflight check script for Kdenlive editor skill.

Validates:
1. Kdenlive installation path and executable status.
2. MLT engine (melt.exe) availability.
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

DEFAULT_KDENLIVE_PATHS = [
    r"D:\Programas\kdenlive-26.08.1_standalone\bin\kdenlive.exe",
    r"C:\Program Files\kdenlive\bin\kdenlive.exe",
]


def check_running_process(process_name: str = "kdenlive") -> bool:
    """Check if kdenlive process is actively running on Windows."""
    try:
        output = subprocess.check_output(
            ["tasklist", "/FI", f"IMAGENAME eq {process_name}.exe"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return f"{process_name}.exe" in output.lower()
    except Exception:
        return False


def locate_kdenlive_bin() -> tuple[Path | None, Path | None]:
    """Locate kdenlive.exe and melt.exe."""
    kdenlive_exe = None
    for p in DEFAULT_KDENLIVE_PATHS:
        path = Path(p)
        if path.is_file():
            kdenlive_exe = path
            break

    if not kdenlive_exe:
        which_path = shutil.which("kdenlive.exe") or shutil.which("kdenlive")
        if which_path:
            kdenlive_exe = Path(which_path)

    melt_exe = None
    if kdenlive_exe:
        candidate_melt = kdenlive_exe.parent / "melt.exe"
        if candidate_melt.is_file():
            melt_exe = candidate_melt

    if not melt_exe:
        which_melt = shutil.which("melt.exe") or shutil.which("melt")
        if which_melt:
            melt_exe = Path(which_melt)

    return kdenlive_exe, melt_exe


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight check for Kdenlive skill")
    parser.add_argument("--media", nargs="*", help="Media files or directories to validate")
    args = parser.parse_args()

    print("[*] Running Kdenlive Skill Preflight Check...")

    kdenlive_exe, melt_exe = locate_kdenlive_bin()
    if not kdenlive_exe:
        print("[!] ERROR: kdenlive.exe could not be located in standard paths.")
        return 2
    print(f"[+] Kdenlive binary: {kdenlive_exe}")

    if not melt_exe:
        print("[!] WARNING: melt.exe could not be found beside kdenlive.exe.")
    else:
        print(f"[+] MLT rendering engine: {melt_exe}")

    is_running = check_running_process("kdenlive")
    if is_running:
        print("[+] Kdenlive instance is currently RUNNING and ready.")
    else:
        print("[*] NOTICE: Kdenlive instance is NOT currently running. Launching may be required.")

    if args.media:
        missing = []
        for m in args.media:
            p = Path(m)
            if not p.exists():
                missing.append(m)
        if missing:
            print(f"[!] WARNING: The following media files were not found: {missing}")
            return 1
        else:
            print(f"[+] All {len(args.media)} media asset(s) validated successfully.")

    print("[+] Preflight check PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
