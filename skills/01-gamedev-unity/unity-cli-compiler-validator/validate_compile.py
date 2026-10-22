#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def validate(unity_path: str, project_path: str):
    log_file = Path(project_path) / "compile_check.log"
    cmd = [
        unity_path,
        "-batchmode",
        "-quit",
        "-projectPath", project_path,
        "-logFile", str(log_file)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Extrai o erro usando o log slicer se houver falha
    slicer_candidates = [
        Path(__file__).parent.parent / "log-slicer-diagnostic" / "slice_log.py",
        Path("agent_skills/log-slicer-diagnostic/slice_log.py"),
        Path("skills/01-gamedev-unity/log-slicer-diagnostic/slice_log.py")
    ]
    slicer = next((s for s in slicer_candidates if s.exists()), None)

    if slicer:
        check_out = subprocess.run(["python3", str(slicer), str(log_file)], capture_output=True, text=True).stdout
    else:
        check_out = "Log não filtrado."

    if "error CS" in check_out or result.returncode != 0:
        print(f"COMPILE_STATUS: FAILED\n{check_out}")
        sys.exit(1)
    else:
        print("COMPILE_STATUS: SUCCESS")
        sys.exit(0)

if __name__ == "__main__":
    u_path = sys.argv[1] if len(sys.argv) > 1 else "Unity"
    p_path = sys.argv[2] if len(sys.argv) > 2 else "."
    validate(u_path, p_path)
