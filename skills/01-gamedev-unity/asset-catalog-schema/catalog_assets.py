#!/usr/bin/env python3
import json
from pathlib import Path

def build_manifest(assets_root: Path) -> dict:
    manifest = {"models": [], "audio": [], "textures": []}

    ext_map = {
        ".fbx": "models", ".obj": "models", ".gltf": "models", ".glb": "models",
        ".wav": "audio", ".mp3": "audio", ".ogg": "audio",
        ".png": "textures", ".jpg": "textures", ".tga": "textures"
    }

    for file in assets_root.rglob("*.*"):
        ext = file.suffix.lower()
        if ext in ext_map:
            category = ext_map[ext]
            manifest[category].append({
                "name": file.stem,
                "path": str(file.as_posix())
            })

    return manifest

if __name__ == "__main__":
    root = Path("Assets")
    output = Path("docs/assets_manifest.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_manifest(root), indent=2), encoding="utf-8")
    print(f"Manifesto salvo em {output}")
