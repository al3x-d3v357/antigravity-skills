#!/usr/bin/env python3
import sys
import re
from pathlib import Path

ERROR_PATTERN = re.compile(r"(error CS\d+|Exception|NullReferenceException|Failed to compile|Error:)", re.IGNORECASE)

def slice_unity_log(log_path: Path, max_lines: int = 15) -> str:
    if not log_path.exists():
        return f"LOG_ERRO: Arquivo {log_path} não encontrado."

    lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    error_lines = []

    for idx, line in enumerate(lines):
        if ERROR_PATTERN.search(line):
            # Pega 1 linha antes e até 2 depois para contexto
            start = max(0, idx - 1)
            end = min(len(lines), idx + 3)
            error_lines.extend(lines[start:end])
            if len(error_lines) >= max_lines:
                break

    if not error_lines:
        return "LOG_STATUS: NENHUM_ERRO_CRITICO_ENCONTRADO"

    return "\n".join(list(dict.fromkeys(error_lines))[:max_lines])

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("Editor.log")
    print(slice_unity_log(target))
