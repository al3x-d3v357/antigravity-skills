#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Foreign Benchmark & Trend Analyzer (Instagram & Threads)
Analisa páginas internacionais de referência (@polygonrunway, @southernshotty, @megavoxels, @imphenzia)
para extrair tendências de legendas, hashtags globais e músicas antes de cada postagem do Alex.
Regra Estrita: Apenas referências do exterior (ZERO páginas brasileiras e ZERO emojis).
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = SCRIPT_DIR / "config.json"

SESSIONS_DIR = Path(os.path.expanduser("~/.social_sessions"))
try:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    SESSIONS_DIR = Path("/media/alex/alex/mcp-servers/social_sessions")
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

TREND_CACHE_FILE = SESSIONS_DIR / "latest_trend_analysis.json"


def strip_emojis(text: str) -> str:
    """Remove qualquer emoji do texto para cumprir a diretriz absoluta ZERO emojis do Alex."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"
        "\U0001FA70-\U0001FAFF"
        "\u2600-\u26FF"
        "\u2700-\u27BF"
        "]+",
        flags=re.UNICODE,
    )
    cleaned = emoji_pattern.sub("", text)
    # Remove múltiplos espaços gerados pela remoção
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    return cleaned.strip()


def load_config() -> Dict[str, Any]:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def detect_category(text: str, media_paths: Optional[List[str]] = None) -> str:
    """Detecta a categoria técnica do post para escolher o cluster gringo ideal."""
    combined = (text or "").lower()
    if media_paths:
        combined += " " + " ".join(str(m).lower() for m in media_paths)

    if any(k in combined for k in ["voxel", "goxel", "magicavoxel", "toycube", "cubo", "cyclop"]):
        return "voxel_art"
    if any(k in combined for k in ["godot", "gdscript"]):
        return "gamedev_godot"
    if any(k in combined for k in ["unity", "csharp", "c#", "drift", "veicular", "car", "gameplay", "hud", "ia inimiga"]):
        return "gamedev_unity"
    if any(k in combined for k in ["pixel", "sprite", "libresprite", "2d", "gamemaker"]):
        return "pixel_art"
    return "blender_3d"


def select_music_category(category: str, text: str) -> str:
    combined = (text or "").lower()
    if category in ["gamedev_unity", "gamedev_godot"] or any(k in combined for k in ["fisica", "física", "colisao", "colisão", "drift", "combate", "laser", "ataque"]):
        return "gamedev_action_vehicle"
    if category == "voxel_art" or any(k in combined for k in ["walk", "idle", "anim", "personagem", "character", "toycube"]):
        return "voxel_and_character_anim"
    if any(k in combined for k in ["codigo", "código", "script", "python", "flutter", "react", "sistema"]):
        return "devlog_and_code"
    return "blender_timelapse_3d"


def fetch_live_foreign_benchmarks() -> List[Dict[str, Any]]:
    """Coleta dados ao vivo das páginas gringas no Instagram via Playwright se disponível."""
    live_data = []
    session_ig = SESSIONS_DIR / "session_instagram.json"
    if not session_ig.exists():
        alt_ig = Path("/media/alex/alex/mcp-servers/social_sessions/session_instagram.json")
        if alt_ig.exists():
            session_ig = alt_ig
        else:
            return live_data

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(
                channel="chrome",
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            context = browser.new_context(
                storage_state=str(session_ig),
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 850}
            )
            page = context.new_page()
            for handle in ["polygonrunway", "southernshotty", "megavoxels", "imphenzia"]:
                try:
                    page.goto(f"https://www.instagram.com/{handle}/", wait_until="domcontentloaded", timeout=25000)
                    page.wait_for_timeout(3000)
                    info = page.evaluate("""() => {
                        const metaDesc = document.querySelector('meta[name="description"]')?.content || '';
                        const imgs = Array.from(document.querySelectorAll('article img, main img')).map(i => i.alt).filter(Boolean).slice(1, 5);
                        return { metaDesc, sample_captions: imgs };
                    }""")
                    live_data.append({"handle": f"@{handle}", **info})
                except Exception:
                    pass
            browser.close()
    except Exception:
        pass
    return live_data


def analyze_and_adapt(
    raw_text: str,
    custom_hashtags: str = "",
    media_paths: Optional[List[str]] = None,
    live: bool = False
) -> Dict[str, Any]:
    """
    Executa a análise de tendências das páginas internacionais (@polygonrunway, @southernshotty,
    @megavoxels, @imphenzia), sugere música em alta, seleciona hashtags internacionais e
    limpa/adapta a legenda garantindo ZERO emojis.
    """
    cfg = load_config()
    benchmarks = cfg.get("foreign_benchmarks", [])
    category = detect_category(raw_text, media_paths)
    music_cat = select_music_category(category, raw_text)

    # 1. Hashtags baseadas nas páginas do exterior (sem tags brasileiras)
    hashtag_map = cfg.get("hashtags", {})
    recommended_tags = hashtag_map.get(category, hashtag_map.get("blender_3d", "#blender3d #b3d #gamedev #indiegamedev #3dart"))

    if custom_hashtags:
        # Filtra tags brasileiras caso tenham sido passadas por engano e mescla com as internacionais
        br_tags = {"#jogosbrasileiros", "#gamesbr", "#jogosindies", "#jogos", "#programacao", "#desenvolvimento"}
        custom_list = [t for t in custom_hashtags.split() if t.lower() not in br_tags]
        rec_list = recommended_tags.split()
        merged = []
        for t in custom_list + rec_list:
            if t.lower() not in [m.lower() for m in merged]:
                merged.append(t)
        final_hashtags = " ".join(merged[:14])
    else:
        final_hashtags = recommended_tags

    # 2. Músicas em alta nas páginas do exterior para esta categoria
    music_map = cfg.get("trending_music", {})
    recommended_music = music_map.get(music_cat, [
        "Hotel Pools - Eclipse (Chill Synthwave)",
        "Lo-Fi Girl / Chillhop Instrumental 90 BPM",
        "Narvent - Fainted (Synthwave / Retrowave)"
    ])

    # 3. Adaptação da legenda para o padrão internacional (Hook direto + Técnico + ZERO emojis)
    clean_caption = strip_emojis(raw_text or "")
    # Substituir bullets com símbolos especiais por traço limpo padrão devlog gringo
    clean_caption = clean_caption.replace("•", "-").replace("🔹", "-").replace("🔸", "-")

    live_snapshots = fetch_live_foreign_benchmarks() if live else []

    report = {
        "timestamp": datetime.now().isoformat(),
        "detected_category": category,
        "foreign_pages_analyzed": [b.get("handle") for b in benchmarks],
        "foreign_benchmarks_summary": benchmarks,
        "live_snapshots": live_snapshots,
        "recommended_music_tracks": recommended_music,
        "recommended_international_hashtags": final_hashtags,
        "adapted_caption_zero_emojis": clean_caption,
    }

    try:
        with open(TREND_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

    return report


def print_trend_report(report: Dict[str, Any]):
    print("=" * 76)
    print("  [TREND ANALYZER] ANÁLISE PRÉ-POSTAGEM (BENCHMARK INTERNACIONAL / EXTERIOR)")
    print("=" * 76)
    print(f"  Categoria Detectada : {report['detected_category']}")
    print(f"  Páginas Analisadas  : {', '.join(report['foreign_pages_analyzed'])} (100% Exterior)")
    print("-" * 76)
    print("  [MÚSICAS / ÁUDIOS EM ALTA RECOMENDADOS PARA ESTE POST]:")
    for idx, m in enumerate(report["recommended_music_tracks"], 1):
        print(f"    {idx}. {m}")
    print("-" * 76)
    print("  [HASHTAGS INTERNACIONAIS SELECIONADAS]:")
    print(f"    {report['recommended_international_hashtags']}")
    print("-" * 76)
    print("  [LEGENDA ADAPTADA (ESTILO DEVLOG GRINGO | ZERO EMOJIS)]:")
    for line in report["adapted_caption_zero_emojis"].splitlines():
        print(f"    {line}")
    print("=" * 76)


def main():
    parser = argparse.ArgumentParser(description="Analisador de Tendências Internacionais para Instagram e Threads")
    parser.add_argument("--post", type=str, default="Testando novo sistema e assets 3D no Blender e Unity 6.", help="Texto base ou tema da postagem")
    parser.add_argument("--hashtags", type=str, default="", help="Hashtags opcionais")
    parser.add_argument("--media", nargs="+", help="Arquivos de mídia")
    parser.add_argument("--live", action="store_true", help="Consulta as páginas do exterior ao vivo via Playwright")
    args = parser.parse_args()

    report = analyze_and_adapt(args.post, args.hashtags, args.media, live=args.live)
    print_trend_report(report)


if __name__ == "__main__":
    main()
