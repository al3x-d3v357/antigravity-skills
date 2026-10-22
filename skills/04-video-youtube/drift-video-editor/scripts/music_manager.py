#!/usr/bin/env python3
"""
music_manager.py - Gerenciador Inteligente de Trilha Sonora para o Drift Video Editor

Localiza, analisa e seleciona automaticamente faixas de áudio livres de direitos autorais (NCS)
a partir do diretório padrão 'C:/Users/alexa/Dropbox/song'.
"""

import argparse
import glob
import json
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

DEFAULT_MUSIC_DIR = "C:/Users/alexa/Dropbox/song"


def scan_music_library(music_dir: str = DEFAULT_MUSIC_DIR) -> List[Dict[str, Any]]:
    """Escaneia a biblioteca de músicas e retorna lista estruturada com durações e metadados."""
    p = Path(music_dir)
    if not p.exists():
        return []

    files = sorted(p.glob("*.mp3"))
    tracks = []

    for f in files:
        f_path = str(f).replace("\\", "/")
        name = f.name
        dur_sec = 0.0

        # ffprobe para obter duração exata
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration:stream=sample_rate,channels",
            "-of", "json", f_path
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            info = json.loads(res.stdout)
            dur_sec = float(info["format"]["duration"])
            sr = int(info["streams"][0].get("sample_rate", 44100)) if info.get("streams") else 44100
            ch = int(info["streams"][0].get("channels", 2)) if info.get("streams") else 2
        except Exception:
            dur_sec = 180.0
            sr = 44100
            ch = 2

        m, s = int(dur_sec // 60), int(dur_sec % 60)
        tracks.append({
            "name": name,
            "path": f_path,
            "duration_sec": round(dur_sec, 2),
            "duration_formatted": f"{m:02d}:{s:02d}",
            "sample_rate": sr,
            "channels": ch
        })

    return tracks


def recommend_track(target_duration_sec: float, tracks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Recomenda a faixa mais adequada com base na duração desejada do vídeo."""
    if not tracks:
        return None

    # Se for um vídeo longo (mais de 15 minutos), recomenda o mix completo (Track 01)
    if target_duration_sec >= 900.0:
        for t in tracks:
            if "01_00-00-00" in t["name"]:
                return t

    # Procura a faixa individual cuja duração seja >= target_duration_sec com o menor excesso
    candidates_longer = [t for t in tracks if t["duration_sec"] >= target_duration_sec and "01_00-00-00" not in t["name"]]
    if candidates_longer:
        candidates_longer.sort(key=lambda x: x["duration_sec"])
        return candidates_longer[0]

    # Se nenhuma faixa individual for longa o suficiente, busca a mais próxima ou o mix
    non_full_mix = [t for t in tracks if "01_00-00-00" not in t["name"]]
    if non_full_mix:
        non_full_mix.sort(key=lambda x: abs(x["duration_sec"] - target_duration_sec))
        return non_full_mix[0]

    return tracks[0]


def main():
    parser = argparse.ArgumentParser(description="Gerenciador de Trilha Sonora Drift Video Editor")
    parser.add_argument("--dir", default=DEFAULT_MUSIC_DIR, help="Diretório da biblioteca de músicas")
    parser.add_argument("--target-duration", type=float, help="Duração do vídeo em segundos para recomendação automática")
    parser.add_argument("--json", action="store_true", help="Saída em formato JSON")

    args = parser.parse_args()
    tracks = scan_music_library(args.dir)

    if args.target_duration:
        chosen = recommend_track(args.target_duration, tracks)
        if args.json:
            print(json.dumps(chosen, indent=2, ensure_ascii=False))
        else:
            if chosen:
                print(f"[RECOMENDAÇÃO] Para vídeo de {args.target_duration:.1f}s ({args.target_duration/60:.1f} min):")
                print(f"  Faixa: {chosen['name']}")
                print(f"  Duração: {chosen['duration_formatted']} ({chosen['duration_sec']}s)")
                print(f"  Caminho: {chosen['path']}")
            else:
                print("[AVISO] Nenhuma faixa encontrada.")
        return

    if args.json:
        print(json.dumps(tracks, indent=2, ensure_ascii=False))
    else:
        print(f"\n=======================================================")
        print(f"BIBLIOTECA DE MÚSICAS: {args.dir}")
        print(f"Total de Faixas Encontradas: {len(tracks)}")
        print("-------------------------------------------------------")
        for idx, t in enumerate(tracks):
            print(f"[{idx+1:02d}] {t['duration_formatted']} | {t['name']}")
        print("=======================================================\n")


if __name__ == "__main__":
    main()
