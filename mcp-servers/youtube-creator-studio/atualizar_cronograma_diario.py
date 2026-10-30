# -*- coding: utf-8 -*-
"""
Script de Automação de Agendamento Diário e Otimização de Metadados
Canal Alex Sandro (@al3x-d3v357)
Ajustado para publicação diária (todos os dias às 13:13).
"""

import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

USER_DATA_DIR = Path(os.path.expanduser("~/.youtube_studio_profile"))
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

# Cronograma Diário Atualizado (Outubro / Novembro 2026)
DAILY_SCHEDULE = [
    {
        "id": "N3dGCCcy0R0",
        "date_str": "28 de out. de 2026",
        "day_num": "28",
        "weekday": "Quarta-feira (Amanhã)",
        "old_title": "Speed Modeling Retopologia ELEN 3D • Otimização de Malha e QuadFlow",
        "new_title": "Retopologia 3D no Blender: Como Fazer QuadFlow Perfeito para Jogos",
        "tags": "blender retopologia, quadflow blender, retopologia 3d jogos, otimizacao de malha 3d, blender 3d tutorial, gamedev brasil, alex sandro, al3x-d3v357"
    },
    {
        "id": "sSshCFDfjr8",
        "date_str": "29 de out. de 2026",
        "day_num": "29",
        "weekday": "Quinta-feira",
        "old_title": "ASU SpriteSlicer Pro Web • Ferramenta Completa para Fatiar Sprites e Criar Animações 2D",
        "new_title": "Como Fatiar Sprites e Criar Animações 2D no Navegador (SpriteSlicer Web)",
        "tags": "spriteslicer web, fatiar sprites, animacao 2d jogos, spritesheet slicer, gamedev 2d ferramentas, pixel art animation, alex sandro, al3x-d3v357"
    },
    {
        "id": "ahVYK3sHzhE",
        "date_str": "30 de out. de 2026",
        "day_num": "30",
        "weekday": "Sexta-feira",
        "old_title": "Como Criar Jogo 2D no GameMaker Studio do Zero • Sprites, Objetos e Colisão",
        "new_title": "Criando Jogo 2D no GameMaker do Zero • Movimentação e Colisão Fácil",
        "tags": "gamemaker tutorial iniciante, criar jogo 2d gamemaker, gml do zero, colisao gamemaker studio, indie game dev, alex sandro, al3x-d3v357"
    },
    {
        "id": "HZ4s069FouA",
        "date_str": "31 de out. de 2026",
        "day_num": "31",
        "weekday": "Sábado",
        "old_title": "Gerando Personagem 3D com IA em 1 Minuto no Tripo3D • Imagem para Modelo 3D",
        "new_title": "Gerei Personagem 3D Completo com IA em 60 Segundos! (Tripo3D para Jogos)",
        "tags": "tripo3d tutorial, ia 3d para jogos, criar modelos 3d com ia, imagem para 3d, blender ia, gamedev ia 2026, alex sandro, al3x-d3v357"
    },
    {
        "id": "dOiI_iUtgu4",
        "date_str": "1 de nov. de 2026",
        "day_num": "1",
        "weekday": "Domingo",
        "old_title": "CRIANDO MEU STREAMING DE ANIMES DO ZERO • Yakisoba Play (Devlog Web App)",
        "new_title": "Criei Meu Próprio Streaming de Animes do Zero! (React & Next.js Devlog)",
        "tags": "yakisoba play, streaming anime devlog, criar web app react, nextjs projeto completo, frontend portfolio, alex sandro, al3x-d3v357"
    },
    {
        "id": "GGOSX0DBMVo",
        "date_str": "2 de nov. de 2026",
        "day_num": "2",
        "weekday": "Segunda-feira",
        "old_title": "PROGRAMANDO APPS COM IA NO OPENCODE • UnoRouter & Muse Spark (Tutorial Rápido)",
        "new_title": "Programando Softwares com IA 10x Mais Rápido • OpenCode & Muse Spark",
        "tags": "opencode tutorial, unorouter muse spark, programar com ia, dev ai python, desenvolvimento agil ia, alex sandro, al3x-d3v357"
    }
]

# Vídeo recente com visualizações baixas para otimização imediata
VIDEO_FLOP_OPTIMIZATION = {
    "id": "4tDqM8ZnSq4",
    "old_title": "CRIE ESPADA 3D NO BLENDER EM 3 MINUTOS • Speed Art & Hard Surface",
    "new_title": "Blender 3D: Como Modelar uma Espada para Jogos em Minutos (Hard Surface Fácil)",
    "tags": "blender 3d espada, modelagem hard surface iniciante, criar armas 3d jogos, tutorial blender modelagem, blender low poly sword, alex sandro, al3x-d3v357, gamedev brasil",
    "description": """🗡️ Aprenda como modelar uma espada estilizada para jogos no Blender de forma rápida e eficiente usando técnicas essenciais de Hard Surface!
Neste vídeo prático, demonstro o fluxo completo de criação da lâmina, guarda e cabo, com foco em topologia limpa, modificadores essenciais e otimização para engines como Unity e Godot.

👇 RECURSOS & LINKS DO CANAL:
🔹 GitHub do Canal: https://github.com/al3x-d3v357
🔹 Projetos de GameDev: https://github.com/al3x-d3v357/projetos_unity
🔹 Minha Comunidade Dev: Inscreva-se para novos tutoriais diários!

⏱️ CAPÍTULOS / TIMESTAMPS:
00:00 - Introdução: O que vamos criar
00:20 - Modelando a Lâmina e chanfros (Hard Surface)
01:10 - Construção da Guarda e Detalhes
02:00 - Cabo e Pomo estilizado
02:40 - Polimento da Malha e Resultado Final

💬 PERGUNTA DO VÍDEO:
Qual próxima arma ou equipamento medieval você quer aprender a modelar no Blender (machado, escudo ou cajado)? Comente abaixo!

🔔 INSCREVA-SE & ATIVE AS NOTIFICAÇÕES:
Vídeos novos TODOS OS DIAS às 13:13 sobre GameDev, Blender 3D e IA!

#Blender3D #HardSurface #Modelagem3D #GameDev #IndieDev #3DArt #BlenderTutorial"""
}

print("Configuração de agendamento diário e metadados carregada com sucesso.")
