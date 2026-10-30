#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch TikTok Uploader
Publica todos os vídeos restantes de /home/alex/Videos/meus no TikTok Studio
com intervalo seguro anti-spam, legendas contextuais e ZERO emojis.
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Importar o post_tiktok do tiktok_poster
sys.path.append(str(Path(__file__).resolve().parent))
from tiktok_poster import post_tiktok, record_post_history, log

VIDEOS_DIR = Path("/home/alex/Videos/meus")
HISTORY_FILE = Path(os.path.expanduser("~/.social_sessions/tiktok_posts_history.json"))
if not HISTORY_FILE.exists():
    HISTORY_FILE = Path("/media/alex/alex/mcp-servers/social_sessions/tiktok_posts_history.json")

# Mapeamento contextual de legendas e hashtags (ZERO emojis)
METADATA_MAP = {
    "22gy.mp4": {
        "caption": "Gerando concept art de personagem em T-pose com IA para modelagem 3D.",
        "hashtags": "#gamedev #3d #ia #blender #characterdesign"
    },
    "ASU SpriteSlicer Pro Web • Ferramenta Completa para Fatiar Sprites e Criar Animações 2D.mp4": {
        "caption": "ASU SpriteSlicer Pro Web. Ferramenta completa para fatiar sprites e criar animações 2D.",
        "hashtags": "#gamedev #pixelart #sprites #indiedev #2d"
    },
    "BAIXADOR DE ISOS EM PYTHON_ Fox.iso Catalogo PSP sem Propaganda _ Devlog.mp4": {
        "caption": "Desenvolvi um baixador de ISOs de PSP em Python com catálogo limpo sem anúncios.",
        "hashtags": "#python #devlog #programacao #psp #opensource"
    },
    "COMO APRENDER A PROGRAMAR DO ZERO COM BLOCOS • Tutorial no mBlock IDE.mp4": {
        "caption": "Como aprender a programar do zero utilizando blocos lógicos no mBlock IDE.",
        "hashtags": "#programacao #tecnologia #aprendizagem #codigofonte #dev"
    },
    "COMO CRIAR APLICATIVOS COM IA DO ZERO • Tutorial de Desenvolvimento no OpenCode.mp4": {
        "caption": "Como desenvolver aplicativos completos utilizando inteligência artificial no OpenCode.",
        "hashtags": "#programacao #ia #desenvolvimento #software #tecnologia"
    },
    "COMO CRIAR UM SITE DE STREAMING DO ZERO • React & Next.js (Devlog Yakisoba Play).mp4": {
        "caption": "Criando uma plataforma de streaming completa do zero com React e Next.js.",
        "hashtags": "#react #nextjs #javascript #webdev #frontend"
    },
    "CRIANDO APP EM FLUTTER COM IA • Como Programar Mais Rápido em 2026.mp4": {
        "caption": "Criando aplicativo desktop no Linux utilizando Flutter, Dart e ferramentas de IA.",
        "hashtags": "#flutter #dart #linux #programacao #appdev"
    },
    "CRIANDO ASSETS EM PIXEL ART DO ZERO • Timelapse & Dicas para Jogos 2D.mp4": {
        "caption": "Criando assets e sprites em pixel art do zero para jogos 2D independentes.",
        "hashtags": "#pixelart #gamedev #indiedev #arte #jogos"
    },
    "CRIANDO JOGOS NA UNITY 6 DO ZERO • Guia Rápido para Iniciantes.mp4": {
        "caption": "Guia prático para iniciar no desenvolvimento de jogos utilizando a Unity 6.",
        "hashtags": "#unity #unity3d #gamedev #indiedev #jogos"
    },
    "CRIE ESPADA 3D NO BLENDER EM 3 MINUTOS • Speed Art & Hard Surface.mp4": {
        "caption": "Modelando uma espada estilizada no Blender 3D em 3 minutos com técnicas de hard surface.",
        "hashtags": "#blender #blender3d #b3d #3dart #gamedev"
    },
    "CRIE PERSONAGENS 3D PARA JOGOS COM IA • Hunyuan3D, Blender & Mixamo (Devlog #01).mp4": {
        "caption": "Pipeline de criação de personagens 3D para jogos unindo Hunyuan3D, Blender e Mixamo.",
        "hashtags": "#blender #3d #ia #mixamo #gamedev"
    },
    "CURSO DE HTML & CSS DO ZERO (PARTE 2) • Criando sua Primeira Página Web.mp4": {
        "caption": "Criando sua primeira página web responsiva com HTML5 e CSS3 moderno.",
        "hashtags": "#html #css #webdev #programacao #frontend"
    },
    "CURSO DE HTML DO ZERO PARA INICIANTES (PARTE 1) • Tags e Estrutura Básica.mp4": {
        "caption": "Introdução prática ao HTML. Estrutura básica e tags fundamentais para iniciantes.",
        "hashtags": "#html #webdesign #desenvolvimento #programacao #dev"
    },
    "Como Criar Jogo 2D no GameMaker Studio do Zero • Sprites, Objetos e Colisão.mp4": {
        "caption": "Como criar um jogo 2D completo no GameMaker Studio com sprites, objetos e física de colisão.",
        "hashtags": "#gamemaker #gamedev #indiedev #jogos #2d"
    },
    "Devlog Hi3D.ai IA 3D Studio Pro • Gerando Assets 3D com Inteligência Artificial.mp4": {
        "caption": "Testando geração de modelos e assets 3D em tempo real com o Hi3D.ai Studio Pro.",
        "hashtags": "#3d #ia #gamedev #blender #tecnologia"
    },
    "IA 3D É 10X MAIS RÁPIDA_ Gerei Modelos 3D com IA para Jogos no Blender!.mp4": {
        "caption": "Comparativo prático de velocidade gerando modelos 3D com IA para importação no Blender.",
        "hashtags": "#blender #ia #3dmodel #gamedev #indiedev"
    },
    "Showcase Blender Cyclop Cubo 3D • Modelagem Voxel & Estilo X-Men.mp4": {
        "caption": "Showcase de modelagem 3D em Voxel Art. Personagem Cyclop estilo X-Men feito no Blender.",
        "hashtags": "#voxel #voxelart #blender #xmen #3dart"
    },
    "Showcase Blender Ghost Isométrico 3D • Inimigo Estilizado para Jogos.mp4": {
        "caption": "Inimigo fantasma estilizado para jogo isométrico modelado e texturizado no Blender.",
        "hashtags": "#blender #3dart #isometric #gamedev #indiedev"
    },
    "Speed Modeling Retopologia ELEN 3D • Otimização de Malha e QuadFlow.mp4": {
        "caption": "Speed modeling e retopologia com malha quad limpa para animação no Blender 3D.",
        "hashtags": "#retopology #blender3d #b3d #3dmodeling #gamedev"
    },
    "TEXTURIZAÇÃO 3D ESTILIZADA COM IA NO BLENDER • Escudo Cel-Shaded & Affinity.mp4": {
        "caption": "Texturização cel-shaded estilizada para jogos unindo IA, Blender e Affinity Designer.",
        "hashtags": "#blender #celshaded #texturing #affinity #gamedev"
    }
}

def get_posted_filenames():
    posted = set()
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
                for entry in history:
                    if entry.get("success"):
                        p = Path(entry.get("video", "")).name
                        if p:
                            posted.add(p)
        except Exception:
            pass
    return posted

def run_batch(delay_seconds: int = 75):
    all_files = sorted(list(VIDEOS_DIR.glob("*.mp4")))
    posted = get_posted_filenames()
    to_post = [f for f in all_files if f.name not in posted]

    log(f"Iniciando lote de uploads no TikTok Studio.")
    log(f"Total de arquivos na pasta: {len(all_files)}")
    log(f"Já postados anteriormente: {len(posted)}")
    log(f"Restantes para publicar: {len(to_post)}")

    if not to_post:
        log("Todos os vídeos já foram publicados no TikTok!")
        return

    for index, video_path in enumerate(to_post, 1):
        filename = video_path.name
        log(f"\n========================================================")
        log(f"[{index}/{len(to_post)}] Processando: {filename}")
        log(f"========================================================")

        meta = METADATA_MAP.get(filename, {
            "caption": filename.replace(".mp4", "").replace("•", "-"),
            "hashtags": "#gamedev #linux #programacao #tecnologia"
        })

        full_caption = f"{meta['caption']}\n\n{meta['hashtags']}".strip()
        success = False

        try:
            success = post_tiktok(full_caption, str(video_path), headless=True)
        except Exception as e:
            log(f"Erro inesperado no envio de {filename}: {e}")
            success = False

        if success:
            log(f"SUCESSO no envio [{index}/{len(to_post)}]: {filename}")
        else:
            log(f"FALHA no envio [{index}/{len(to_post)}]: {filename}")

        if index < len(to_post):
            log(f"Aguardando intervalo de segurança anti-spam ({delay_seconds}s) antes do próximo...")
            time.sleep(delay_seconds)

    log("\nProcessamento do lote de vídeos concluído com sucesso!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Batch TikTok Uploader")
    parser.add_argument("--delay", type=int, default=75, help="Segundos de espera entre cada publicação")
    args = parser.parse_args()
    run_batch(delay_seconds=args.delay)
