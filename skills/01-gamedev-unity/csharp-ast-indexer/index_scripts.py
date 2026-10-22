#!/usr/bin/env python3
import re
import json
from pathlib import Path

SIGNATURE_REGEX = re.compile(
    r"((?:public|protected|private|static|override|virtual)\s+[\w<>\[\]]+\s+\w+\s*\([^)]*\))",
    re.MULTILINE
)
CLASS_REGEX = re.compile(r"(public|internal)?\s*(class|struct|interface|enum)\s+(\w+)")

def extract_api(scripts_dir: Path) -> dict:
    catalog = {}
    for cs_file in scripts_dir.rglob("*.cs"):
        content = cs_file.read_text(encoding="utf-8", errors="ignore")
        classes = CLASS_REGEX.findall(content)
        signatures = SIGNATURE_REGEX.findall(content)

        catalog[cs_file.name] = {
            "types": [c[2] for c in classes],
            "signatures": signatures[:10]  # Limita às 10 principais assinaturas
        }
    return catalog

if __name__ == "__main__":
    target_dir = Path("Assets/Scripts")
    output_file = Path("docs/scripts_api_index.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    data = extract_api(target_dir) if target_dir.exists() else {}
    output_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Indexados {len(data)} arquivos em {output_file}")
