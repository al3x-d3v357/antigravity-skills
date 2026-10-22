#!/usr/bin/env python3
"""
drift_project_builder.py - Construtor Universal e Empacotador de Projetos Nativos do Drift (.drift / .driftproj)

Gera arquivos binários nativos com compressão Zstandard e cabeçalho DRIFTPRJ de 52 bytes,
compatíveis com o manifest do Drift v0.6+ e v0.7+.
"""

import argparse
import copy
import hashlib
import json
import os
import struct
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import zstandard as zstd


def read_drift_project(path: str) -> dict:
    """Lê e descompacta um arquivo .drift ou .driftproj nativo."""
    with open(path, "rb") as f:
        data = f.read()
    decomp = zstd.ZstdDecompressor().decompress(data[52:], max_output_size=50 * 1024 * 1024)
    return json.loads(decomp)


def save_drift_project(doc: dict, output_path: str):
    """Compacta e grava um arquivo .drift ou .driftproj nativo com checksum SHA256."""
    json_bytes = json.dumps(doc, ensure_ascii=False, indent=None).encode("utf-8")
    cctx = zstd.ZstdCompressor(level=3)
    compressed = cctx.compress(json_bytes)
    header = (
        b"DRIFTPRJ"
        + struct.pack("<III", 1, len(compressed), len(json_bytes))
        + hashlib.sha256(json_bytes).digest()
    )
    out_p = Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with open(out_p, "wb") as f:
        f.write(header + compressed)
    print(f"[OK] Projeto Drift gravado: {output_path} ({len(header) + len(compressed)} bytes)")


def create_blank_project_document(
    project_name: str = "Novo Projeto Drift",
    width: int = 1920,
    height: int = 1080,
    fps: int = 60
) -> dict:
    """Cria um documento de projeto base com o schema exato do Drift."""
    proj_id = str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "addons": [],
        "blobs": [],
        "format": {
            "app": "Drift",
            "appVersion": "0.7.0",
            "version": "1.1.0"
        },
        "project": {
            "author": "Alex",
            "createdAt": now_iso,
            "description": "Projeto gerado via Drift MCP Agent Skill",
            "id": proj_id,
            "modifiedAt": now_iso,
            "title": project_name
        },
        "media": [],
        "document": {
            "allowClipOverlap": True,
            "assets": [],
            "author": "Alex",
            "background": {
                "blurStrength": 20,
                "color": "#ff000000",
                "kind": "color"
            },
            "binFolders": [],
            "bookmarks": [],
            "createdAt": now_iso,
            "description": "Projeto gerado via Drift MCP Agent Skill",
            "fps": fps,
            "height": height,
            "id": proj_id,
            "loopWorkArea": False,
            "mediaGridMode": True,
            "mediaViewMode": "grid",
            "modifiedAt": now_iso,
            "playheadUs": 0,
            "projectName": project_name,
            "rippleEnabled": False,
            "sampleRate": 48000,
            "snapEnabled": True,
            "version": 8,
            "width": width,
            "tracks": [
                {
                    "adjustmentScope": "allBelow",
                    "heightScale": 1,
                    "hidden": False,
                    "id": str(uuid.uuid4()),
                    "locked": False,
                    "muted": False,
                    "name": "Overlays & Badges",
                    "parentTrackId": "",
                    "showChannelWaveforms": False,
                    "showWaveform": False,
                    "transitions": [],
                    "type": "video",
                    "clips": []
                },
                {
                    "adjustmentScope": "allBelow",
                    "heightScale": 1,
                    "hidden": False,
                    "id": str(uuid.uuid4()),
                    "locked": False,
                    "muted": False,
                    "name": "Vídeo Principal",
                    "parentTrackId": "",
                    "showChannelWaveforms": False,
                    "showWaveform": False,
                    "transitions": [],
                    "type": "video",
                    "clips": []
                },
                {
                    "adjustmentScope": "allBelow",
                    "heightScale": 1,
                    "hidden": False,
                    "id": str(uuid.uuid4()),
                    "locked": False,
                    "muted": False,
                    "name": "Trilha Sonora",
                    "parentTrackId": "",
                    "showChannelWaveforms": True,
                    "showWaveform": True,
                    "transitions": [],
                    "type": "audio",
                    "clips": []
                }
            ]
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Construtor de Projetos Drift Video Editor")
    parser.add_argument("--output", "-o", default="edit.drift", help="Arquivo de saída (.drift ou .driftproj)")
    parser.add_argument("--name", default="Projeto Drift", help="Nome do projeto")

    args = parser.parse_args()
    proj = create_blank_project_document(args.name)
    save_drift_project(proj, args.output)


if __name__ == "__main__":
    main()
