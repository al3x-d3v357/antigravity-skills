#!/usr/bin/env python3
"""
build_full_drift_project.py - Construtor de Projeto Nativo Drift Completo (+ Showcase 360 no Final)
Implementa:
- 49 Cortes Dinâmicos de Vídeo (604.42s)
- Clip 50: Showcase Turntable 360 do Personagem Dexter no Final da Faixa Principal (604.42s a 616.25s)
- 10 Cards Explicativos com Paleta Oficial
- 3 Lower-Thirds Estratégicos + Badge de Showcase
- Legendas Estilizadas com Background Box Glassmorphic Translúcido rebaixadas na margem inferior
- Trilha de Efeitos Sonoros (SFX Pop, Whoosh, Chime, Ding)
- Trilha Sonora Suave de Fundo (NCS Kawaii Mix) estendida até o encerramento do showcase
- Sincronização e Carregamento no Drift MCP
"""

import os
import sys
import uuid
import json
import struct
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import zstandard as zstd
import urllib.request

WORKSPACE_DIR = Path("D:/editaVideos/edita").resolve()
INPUT_VIDEO = str(WORKSPACE_DIR / "2026-09-29 23-03-30.mp4").replace("\\", "/")
DEX_360_VIDEO = str(WORKSPACE_DIR / "assets" / "dex_360_showcase_final.mp4").replace("\\", "/")
BGM_PATH = "C:/Users/alexa/Dropbox/song/NCS_Kawaii_Mix___NCS_-_Copyright_Free_Music_04_00-08-07-679.mp3"
OUTPUT_DRIFT = str(WORKSPACE_DIR / "projeto_edicao_personagens_3d.drift").replace("\\", "/")

# Drift MCP URL & Token
DRIFT_MCP_URL = "http://127.0.0.1:4731/mcp"
DRIFT_TOKEN = "1ffbdd396f91e311b43a816b266aaa1d221a5229264f2a601f902379cd58a1eb"

# 49 Cortes Refinados do Vídeo (start, duration, inPoint, outPoint, name)
CUTS_DATA = [
    (0.00, 9.50, 2.50, 12.00, "Clip 01 (01_hook)"),
    (9.50, 0.707, 279.293, 280.00, "Clip 02 (02_broll)"),
    (10.207, 21.482, 12.50, 33.982, "Clip 03 (03_affinity)"),
    (31.689, 21.178, 38.822, 60.00, "Clip 04 (03_affinity)"),
    (52.867, 5.768, 150.00, 155.768, "Clip 05 (04_export)"),
    (58.635, 3.251, 162.433, 165.684, "Clip 06 (04_export)"),
    (61.886, 1.277, 175.694, 176.971, "Clip 07 (04_export)"),
    (63.163, 10.529, 179.471, 190.00, "Clip 08 (04_export)"),
    (73.692, 18.188, 194.00, 212.188, "Clip 09 (05_hunyuan)"),
    (91.880, 2.052, 216.012, 218.064, "Clip 10 (05_hunyuan)"),
    (93.932, 5.556, 222.024, 227.580, "Clip 11 (05_hunyuan)"),
    (99.488, 2.648, 232.352, 235.00, "Clip 12 (05_hunyuan)"),
    (102.136, 2.361, 256.00, 258.361, "Clip 13 (06_unity_show)"),
    (104.497, 10.627, 262.102, 272.729, "Clip 14 (06_unity_show)"),
    (115.124, 0.601, 279.293, 279.894, "Clip 15 (06_unity_show)"),
    (115.725, 1.295, 284.406, 285.701, "Clip 16 (06_unity_show)"),
    (117.020, 9.288, 293.504, 302.792, "Clip 17 (06_unity_show)"),
    (126.308, 0.575, 306.719, 307.294, "Clip 18 (06_unity_show)"),
    (126.883, 24.298, 311.801, 336.099, "Clip 19 (06_unity_show)"),
    (151.181, 15.374, 340.942, 356.316, "Clip 20 (06_unity_show)"),
    (166.555, 2.798, 361.202, 364.00, "Clip 21 (06_unity_show)"),
    (169.353, 6.044, 369.00, 375.044, "Clip 22 (07_model_50k)"),
    (175.397, 54.013, 378.721, 432.734, "Clip 23 (07_model_50k)"),
    (229.410, 7.848, 436.152, 444.00, "Clip 24 (07_model_50k)"),
    (237.258, 0.923, 448.00, 448.923, "Clip 25 (08_segmentation)"),
    (238.181, 37.978, 452.022, 490.00, "Clip 26 (08_segmentation)"),
    (276.159, 22.942, 491.00, 513.942, "Clip 27 (09_retopology_mcp)"),
    (299.101, 22.879, 516.613, 539.492, "Clip 28 (09_retopology_mcp)"),
    (321.980, 1.908, 545.241, 547.149, "Clip 29 (09_retopology_mcp)"),
    (323.888, 26.453, 550.914, 577.367, "Clip 30 (09_retopology_mcp)"),
    (350.341, 6.135, 579.865, 586.00, "Clip 31 (09_retopology_mcp)"),
    (356.476, 28.283, 589.717, 618.00, "Clip 32 (09_retopology_mcp)"),
    (384.759, 10.609, 648.00, 658.609, "Clip 33 (10_gemini_bake)"),
    (395.368, 0.577, 661.362, 661.939, "Clip 34 (10_gemini_bake)"),
    (395.945, 19.271, 664.531, 683.802, "Clip 35 (10_gemini_bake)"),
    (415.216, 14.504, 688.184, 702.688, "Clip 36 (10_gemini_bake)"),
    (429.720, 1.374, 711.498, 712.872, "Clip 37 (10_gemini_bake)"),
    (431.094, 3.118, 715.875, 718.993, "Clip 38 (10_gemini_bake)"),
    (434.212, 0.552, 726.028, 726.580, "Clip 39 (10_gemini_bake)"),
    (434.764, 1.367, 736.633, 738.00, "Clip 40 (10_gemini_bake)"),
    (436.131, 2.639, 742.00, 744.639, "Clip 41 (11_mesh_result)"),
    (438.770, 7.375, 747.756, 755.131, "Clip 42 (11_mesh_result)"),
    (446.145, 1.246, 761.614, 762.860, "Clip 43 (11_mesh_result)"),
    (447.391, 47.643, 778.357, 826.00, "Clip 44 (11_mesh_result)"),
    (495.034, 1.121, 832.00, 833.121, "Clip 45 (12_uv_unwrap)"),
    (496.155, 34.675, 837.575, 872.250, "Clip 46 (12_uv_unwrap)"),
    (530.830, 35.097, 874.903, 910.00, "Clip 47 (12_uv_unwrap)"),
    (565.927, 27.886, 911.00, 938.886, "Clip 48 (13_outro)"),
    (593.813, 10.610, 941.890, 952.50, "Clip 49 (13_outro)")
]

# 10 Cards Explicativos (arquivo, nome, start, end)
CARDS_DATA = [
    ("assets/cards/card_01_hook.png", "Criação 3D com IA", 1.5, 8.5),
    ("assets/cards/card_02_concept.png", "Etapa 1: Conceito 2D", 14.0, 22.0),
    ("assets/cards/card_03_hunyuan.png", "Etapa 2: Tencent Hunyuan 3D", 75.0, 83.0),
    ("assets/cards/card_04_unity_gameplay.png", "Gameplay Unity 2.5D", 106.0, 114.0),
    ("assets/cards/card_05_segmentation.png", "Etapa 3: Pré-Segmentação", 240.0, 248.0),
    ("assets/cards/card_06_retopology.png", "Etapa 4: Retopologia IA", 280.0, 288.0),
    ("assets/cards/card_07_mixamo_mcp.png", "Mixamo MCP Agent + Unity", 326.0, 335.0),
    ("assets/cards/card_08_blender_gemini.png", "Blender Bake + Gemini Textura", 387.0, 395.0),
    ("assets/cards/card_09_benchmark.png", "Benchmark 50k -> 7.8k Quads", 449.0, 458.0),
    ("assets/cards/card_10_cta.png", "Encerramento: Like & Inscreva-se", 568.0, 578.0)
]

# 3 Lower-Thirds + Lower-Third de Showcase 360 no final
LOWER_THIRDS_DATA = [
    ("assets/lower_third_hunyuan.png", "Lower-Third: Hunyuan 3D", 85.0, 92.0),
    ("assets/lower_third_mixamo_mcp.png", "Lower-Third: Mixamo MCP", 340.0, 348.0),
    ("assets/lower_third_retopo.png", "Lower-Third: Retopologia 50k->7.8k", 462.0, 470.0),
    ("assets/lower_third.png", "Showcase 360: Modelo Dexter 3D", 605.0, 615.0)
]

# Efeitos Sonoros SFX (arquivo, nome, at, volume)
SFX_DATA = [
    ("assets/sfx/card_pop.wav", "SFX Card Pop 01", 1.5, 0.85),
    ("assets/sfx/card_pop.wav", "SFX Card Pop 02", 14.0, 0.85),
    ("assets/sfx/card_pop.wav", "SFX Card Pop 03", 75.0, 0.85),
    ("assets/sfx/whoosh_in.wav", "SFX Whoosh Hunyuan", 85.0, 0.75),
    ("assets/sfx/card_pop.wav", "SFX Card Pop 04", 106.0, 0.85),
    ("assets/sfx/card_pop.wav", "SFX Card Pop 05", 240.0, 0.85),
    ("assets/sfx/card_pop.wav", "SFX Card Pop 06", 280.0, 0.85),
    ("assets/sfx/ding_highlight.wav", "SFX Ding Retopo", 280.5, 0.70),
    ("assets/sfx/card_pop.wav", "SFX Card Pop 07", 326.0, 0.85),
    ("assets/sfx/whoosh_in.wav", "SFX Whoosh Mixamo", 340.0, 0.75),
    ("assets/sfx/card_pop.wav", "SFX Card Pop 08", 387.0, 0.85),
    ("assets/sfx/ding_highlight.wav", "SFX Ding Gemini", 387.5, 0.70),
    ("assets/sfx/card_pop.wav", "SFX Card Pop 09", 449.0, 0.85),
    ("assets/sfx/chime_benchmark.wav", "SFX Chime Benchmark", 449.2, 0.80),
    ("assets/sfx/whoosh_in.wav", "SFX Whoosh Retopo 50k", 462.0, 0.75),
    ("assets/sfx/card_pop.wav", "SFX Card Pop 10", 568.0, 0.85),
    ("assets/sfx/whoosh_in.wav", "SFX Whoosh 360 Final", 604.4, 0.85),
    ("assets/sfx/chime_benchmark.wav", "SFX Chime 360 Final", 604.8, 0.85)
]

# Legendas com Background Box (start, end, texto)
SUBTITLES_DATA = [
    (0.50, 4.20, "Hoje eu vou falar como que eu faço"),
    (4.20, 7.50, "para construir personagem 3D para jogos através de IA."),
    (7.50, 9.40, "Eles são construídos através de Inteligência Artificial."),
    (9.60, 10.20, "🎮 [Protótipo funcionando na Unity]"),
    (10.50, 16.00, "Eu peguei esse personagenzinho aqui que eu criei no Affinity,"),
    (16.00, 21.00, "que é um programa que eu uso para manipular imagem e vetores."),
    (21.00, 26.00, "Ele é da mesma empresa que comprou o Canva recentemente."),
    (26.00, 31.00, "Esse personagem eu peguei como referência lá do Pinterest."),
    (31.00, 37.00, "Joguei ele no Gemini e pedi para gerar um prompt"),
    (37.00, 43.00, "para criar um boneco semelhante, sem direitos autorais."),
    (43.00, 49.00, "Aí gerei através do Affinity essa arte base."),
    (49.00, 52.80, "Vou exportar essa imagem desse bonequinho."),
    (53.00, 58.50, "Eu gosto de deixar no formato JPG."),
    (58.60, 61.80, "Vou mudar o diretório e salvar na pasta Downloads."),
    (63.20, 68.00, "Vou colocar o nome de 'Bot'."),
    (68.00, 73.50, "Esse personagem lembra o bot do PlayStation 5, azul com branco."),
    (74.00, 80.00, "Agora vamos ver aqui no navegador a ferramenta de 3D."),
    (80.00, 88.00, "Eu utilizo o Hunyuan 3D Global da Tencent para gerar o modelo."),
    (88.00, 94.00, "Vamos clicar em 3D Studio, depois em Roles."),
    (94.00, 99.40, "Aqui foi um modelo que eu gerei para teste."),
    (99.50, 102.10, "Personagem Dexter... Aqui, esse modelinho!"),
    (102.50, 110.00, "Eu tô produzindo um joguinho curto com ele na Unity."),
    (110.00, 115.00, "Aqui tá ele certinho rodando na viewport 2.5D."),
    (117.00, 126.00, "Seguindo, vamos utilizar aquela imagem como referência."),
    (127.00, 138.00, "É só criar conta com e-mail e código de acesso."),
    (138.00, 150.00, "Vou selecionar a imagem e gerar o modelo 3D."),
    (151.20, 166.00, "Eu seleciono 50k faces para depois aplicar a retopologia."),
    (169.40, 175.00, "Voltamos aqui, galera! Aqui tá o modelo como ficou."),
    (175.40, 185.00, "Ele tá com 50.000 faces, o que é pesado para jogos."),
    (185.00, 200.00, "Você pode gerar por texto descritivo ou por imagem de referência."),
    (200.00, 215.00, "Pode usar várias fotos (frente, costas, lados) que fica ainda melhor."),
    (215.00, 229.00, "Seguindo, vamos agora clicar em Pre-segmented para dividir por cores."),
    (238.20, 248.00, "Voltei! Ele dividiu a face do personagem por cores anatômicas:"),
    (248.00, 258.00, "Barriguinha, orelhas, cabeça, bracinhos e anteninha."),
    (258.00, 276.00, "Fica muito mais fácil para gerar as texturas depois."),
    (276.20, 286.00, "Seguindo, vamos para a etapa de retopologia, clicando em Low."),
    (286.00, 299.00, "Esse processo leva uns 10 minutos, economizando horas de trabalho!"),
    (299.10, 312.00, "A IA é fantástica para quem tá criando jogos sozinho."),
    (323.90, 335.00, "Falando em animação, eu tava pesquisando o Mixamo MCP!"),
    (335.00, 348.00, "Muito legal conectar o MCP ao agente de IA para baixar animações"),
    (348.00, 356.40, "e transferir direto para a Unity de forma automatizada."),
    (356.50, 370.00, "Vou utilizar bastante esse pipeline nos próximos projetos."),
    (384.80, 395.00, "Sobre a textura, eu utilizo uma técnica com o Gemini!"),
    (396.00, 410.00, "Ativo o MCP do Blender, peço o bake e jogo no Gemini para texturizar."),
    (410.00, 425.00, "Fica super personalizado com o rostinho do boneco."),
    (436.10, 447.00, "Voltamos! Olha como ficou a distribuição dos quads!"),
    (447.40, 460.00, "Ele tinha 50.000 faces e reduziu para 7.887 faces otimizadas!"),
    (460.00, 475.00, "Diminuiu muito, perfeito para desempenho em jogos."),
    (475.00, 495.00, "Agora vamos ver o mapa UV otimizado."),
    (496.20, 510.00, "Olha que mapa UV bem distribuído e segmentado!"),
    (510.00, 530.00, "Fácil de ajustar no Blender e aplicar texturas personalizadas."),
    (530.80, 555.00, "Gostei bastante do resultado final desse pipeline."),
    (566.00, 575.00, "Para rigging e animação, eu prefiro utilizar o Mixamo."),
    (575.00, 585.00, "Espero que vocês tenham gostado! Deixem o like e se inscrevam!"),
    (585.00, 604.00, "Vou trazer mais novidades sobre jogos, IA e MCP. Valeu! 🚀"),
    (604.50, 615.50, "🎬 [Showcase 360: Modelo Dexter 3D Renderizado no Blender]")
]

def make_clip(clip_id, asset_id, name, path, clip_type, tl_start_us, tl_dur_us, src_in_us, src_out_us, volume=1.0, fade_in_us=80000, fade_out_us=80000):
    return {
        "id": clip_id,
        "assetId": asset_id,
        "name": name,
        "path": path,
        "type": clip_type,
        "timelineStartUs": tl_start_us,
        "timelineDurationUs": tl_dur_us,
        "srcInUs": src_in_us,
        "srcOutUs": src_out_us,
        "speed": 1.0,
        "speedCurve": [],
        "blendMode": "normal",
        "effects": [],
        "audioEffects": [],
        "audioStreamIndex": 0,
        "fadeInUs": fade_in_us,
        "fadeOutUs": fade_out_us,
        "fadeCurve": "smooth",
        "volume": {"keyframes": [{"timeUs": 0, "value": volume}]},
        "width": {"keyframes": [{"timeUs": 0, "value": 1920.0}]},
        "height": {"keyframes": [{"timeUs": 0, "value": 1080.0}]},
        "x": {"keyframes": [{"timeUs": 0, "value": 0.0}]},
        "y": {"keyframes": [{"timeUs": 0, "value": 0.0}]},
        "opacity": {"keyframes": []},
        "rotation": {"keyframes": []},
        "flipH": False,
        "flipV": False,
        "reverse": False,
        "suppressEmbeddedAudio": False,
        "subtitleCues": [],
        "mask": {"enabled": False}
    }

def make_text_clip(clip_id, text, start_s, end_s):
    tl_start_us = int(round(start_s * 1000000))
    tl_dur_us = int(round((end_s - start_s) * 1000000))
    
    return {
        "id": clip_id,
        "assetId": "",
        "name": text[:28] + ("..." if len(text) > 28 else ""),
        "path": "",
        "type": "text",
        "timelineStartUs": tl_start_us,
        "timelineDurationUs": tl_dur_us,
        "srcInUs": 0,
        "srcOutUs": tl_dur_us,
        "speed": 1.0,
        "speedCurve": [],
        "blendMode": "normal",
        "effects": [],
        "audioEffects": [],
        "fadeInUs": 120000,
        "fadeOutUs": 120000,
        "fadeCurve": "smooth",
        "textContent": text,
        "textStyle": {
            "align": "center",
            "valign": "center",
            "fontFamily": "Inter",
            "fontWeight": 700,
            "pixelSize": 34,
            "color": "#ffffffff",
            "boxColor": "#ea0a1020",
            "boxEnabled": True,
            "boxPadding": 10,
            "boxRadius": 8,
            "letterSpacing": 0,
            "lineHeight": 1.25,
            "wordWrap": True,
            "layers": [
                {
                    "blend": "normal",
                    "blur": 0,
                    "enabled": True,
                    "id": "fill",
                    "kind": "fill",
                    "offsetX": 0,
                    "offsetY": 0,
                    "opacity": 1,
                    "paint": {
                        "color": "#ffffffff",
                        "kind": "solid"
                    },
                    "scope": "all",
                    "spread": 0,
                    "width": 2
                }
            ],
            "accent": {
                "color": "#fff3be7a",
                "colorEnabled": True,
                "highlight": {
                    "color": "#ea0a1020",
                    "enabled": True,
                    "padding": 6,
                    "radius": 4
                },
                "n": 2,
                "outlineColor": "#ff000000",
                "outlineEnabled": False,
                "outlineWidth": 0,
                "phase": 0,
                "rule": "none",
                "sizeScale": 1
            }
        },
        "width": {"keyframes": [{"timeUs": 0, "value": 1700.0}]},
        "height": {"keyframes": [{"timeUs": 0, "value": 90.0}]},
        "x": {"keyframes": [{"timeUs": 0, "value": 0.0}]},
        "y": {"keyframes": [{"timeUs": 0, "value": 450.0}]},
        "volume": {"keyframes": [{"timeUs": 0, "value": 1.0}]}
    }

def build_full_project():
    proj_id = str(uuid.uuid4())
    video_asset_id = str(uuid.uuid4())
    dex_360_asset_id = str(uuid.uuid4())
    bgm_asset_id = str(uuid.uuid4())

    media_items = [
        {"id": video_asset_id, "path": INPUT_VIDEO, "name": "2026-09-29 23-03-30.mp4", "type": "video"},
        {"id": dex_360_asset_id, "path": DEX_360_VIDEO, "name": "dex_360_showcase_final.mp4", "type": "video"},
        {"id": bgm_asset_id, "path": BGM_PATH, "name": "NCS Kawaii Mix", "type": "audio"}
    ]

    # 1. Text / Subtitles Clips (Track 0)
    sub_clips = []
    for st_s, en_s, txt in SUBTITLES_DATA:
        cid = str(uuid.uuid4())
        sub_clips.append(make_text_clip(cid, txt, st_s, en_s))

    # 2. Cards & Lower-Thirds (Track 1)
    card_clips = []
    
    # 10 Cards
    for rel_path, cname, st_s, en_s in CARDS_DATA:
        aid = str(uuid.uuid4())
        full_path = str(WORKSPACE_DIR / rel_path).replace("\\", "/")
        media_items.append({"id": aid, "path": full_path, "name": Path(rel_path).name, "type": "image"})
        dur_us = int(round((en_s - st_s) * 1000000))
        st_us = int(round(st_s * 1000000))
        c = make_clip(str(uuid.uuid4()), aid, cname, full_path, "image", st_us, dur_us, 0, dur_us, volume=0.0, fade_in_us=350000, fade_out_us=350000)
        card_clips.append(c)

    # 3 Lower-Thirds + Showcase Lower Third
    for rel_path, cname, st_s, en_s in LOWER_THIRDS_DATA:
        aid = str(uuid.uuid4())
        full_path = str(WORKSPACE_DIR / rel_path).replace("\\", "/")
        media_items.append({"id": aid, "path": full_path, "name": Path(rel_path).name, "type": "image"})
        dur_us = int(round((en_s - st_s) * 1000000))
        st_us = int(round(st_s * 1000000))
        c = make_clip(str(uuid.uuid4()), aid, cname, full_path, "image", st_us, dur_us, 0, dur_us, volume=0.0, fade_in_us=350000, fade_out_us=350000)
        card_clips.append(c)

    # 3. 49 Video Cuts + Clip 50: Showcase 360 no Final (Track 2)
    video_clips = []
    for st_s, dur_s, in_s, out_s, name in CUTS_DATA:
        dur_us = int(round(dur_s * 1000000))
        st_us = int(round(st_s * 1000000))
        src_in_us = int(round(in_s * 1000000))
        src_out_us = int(round(out_s * 1000000))
        c = make_clip(str(uuid.uuid4()), video_asset_id, name, INPUT_VIDEO, "video", st_us, dur_us, src_in_us, src_out_us, volume=1.55, fade_in_us=60000, fade_out_us=60000)
        video_clips.append(c)

    # Inserção do Clip 50 (Showcase 360) no final da Faixa de Vídeo Principal
    showcase_start_s = 604.423
    showcase_dur_s = 11.83
    showcase_st_us = int(round(showcase_start_s * 1000000))
    showcase_dur_us = int(round(showcase_dur_s * 1000000))
    
    clip_50_showcase = make_clip(
        str(uuid.uuid4()), dex_360_asset_id, "Clip 50 (Showcase 360 Dexter Blender Studio)",
        DEX_360_VIDEO, "video", showcase_st_us, showcase_dur_us, 0, showcase_dur_us,
        volume=1.0, fade_in_us=250000, fade_out_us=800000
    )
    video_clips.append(clip_50_showcase)

    total_duration_us = showcase_st_us + showcase_dur_us # ~616.253s (10min 16s)

    # 4. SFX Clips (Track 3)
    sfx_clips = []
    for rel_path, sfx_name, at_s, vol in SFX_DATA:
        aid = str(uuid.uuid4())
        full_path = str(WORKSPACE_DIR / rel_path).replace("\\", "/")
        media_items.append({"id": aid, "path": full_path, "name": Path(rel_path).name, "type": "audio"})
        sfx_dur_us = 600000
        at_us = int(round(at_s * 1000000))
        c = make_clip(str(uuid.uuid4()), aid, sfx_name, full_path, "audio", at_us, sfx_dur_us, 0, sfx_dur_us, volume=vol, fade_in_us=10000, fade_out_us=80000)
        sfx_clips.append(c)

    # 5. BGM Audio Clip (Track 4)
    audio_clips = []
    if os.path.exists(BGM_PATH):
        bgm_clip = make_clip(str(uuid.uuid4()), bgm_asset_id, "NCS Kawaii Mix (BGM)", BGM_PATH, "audio", 0, total_duration_us, 0, total_duration_us, volume=0.018, fade_in_us=2000000, fade_out_us=3500000)
        audio_clips.append(bgm_clip)

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    doc = {
        "addons": [],
        "blobs": [],
        "format": {"app": "Drift", "appVersion": "0.7.0", "version": "1.1.0"},
        "project": {
            "author": "Alex",
            "createdAt": now_iso,
            "description": "Devlog Personagens 3D com IA - Edição Profissional Completa com Turntable 360",
            "id": proj_id,
            "modifiedAt": now_iso,
            "title": "Devlog IA Personagens 3D Pro"
        },
        "media": media_items,
        "document": {
            "allowClipOverlap": True,
            "assets": media_items,
            "author": "Alex",
            "background": {"blurStrength": 20, "color": "#ff000000", "kind": "color"},
            "binFolders": [],
            "bookmarks": [],
            "createdAt": now_iso,
            "description": "Devlog Personagens 3D Pro",
            "fps": 60,
            "height": 1080,
            "id": proj_id,
            "loopWorkArea": False,
            "mediaGridMode": True,
            "mediaViewMode": "grid",
            "modifiedAt": now_iso,
            "playheadUs": 0,
            "projectName": "Devlog IA Personagens 3D Pro",
            "rippleEnabled": False,
            "sampleRate": 48000,
            "snapEnabled": True,
            "version": 8,
            "width": 1920,
            "tracks": [
                {
                    "adjustmentScope": "allBelow",
                    "heightScale": 1,
                    "hidden": False,
                    "id": str(uuid.uuid4()),
                    "locked": False,
                    "muted": False,
                    "name": "Legendas Dinâmicas (Box Glassmorphic)",
                    "parentTrackId": "",
                    "showChannelWaveforms": False,
                    "showWaveform": False,
                    "transitions": [],
                    "type": "text",
                    "clips": sub_clips
                },
                {
                    "adjustmentScope": "allBelow",
                    "heightScale": 1,
                    "hidden": False,
                    "id": str(uuid.uuid4()),
                    "locked": False,
                    "muted": False,
                    "name": "10 Cards & Lower-Thirds (Paleta Oficial)",
                    "parentTrackId": "",
                    "showChannelWaveforms": False,
                    "showWaveform": False,
                    "transitions": [],
                    "type": "video",
                    "clips": card_clips
                },
                {
                    "adjustmentScope": "allBelow",
                    "heightScale": 1,
                    "hidden": False,
                    "id": str(uuid.uuid4()),
                    "locked": False,
                    "muted": False,
                    "name": "Vídeo Principal (50 Clipes - Inclui Showcase 360)",
                    "parentTrackId": "",
                    "showChannelWaveforms": False,
                    "showWaveform": False,
                    "transitions": [],
                    "type": "video",
                    "clips": video_clips
                },
                {
                    "adjustmentScope": "allBelow",
                    "heightScale": 1,
                    "hidden": False,
                    "id": str(uuid.uuid4()),
                    "locked": False,
                    "muted": False,
                    "name": "Efeitos Sonoros (SFX Pop/Whoosh/Chime)",
                    "parentTrackId": "",
                    "showChannelWaveforms": True,
                    "showWaveform": True,
                    "transitions": [],
                    "type": "audio",
                    "clips": sfx_clips
                },
                {
                    "adjustmentScope": "allBelow",
                    "heightScale": 1,
                    "hidden": False,
                    "id": str(uuid.uuid4()),
                    "locked": False,
                    "muted": False,
                    "name": "Trilha Sonora Suave (NCS Kawaii Mix)",
                    "parentTrackId": "",
                    "showChannelWaveforms": True,
                    "showWaveform": True,
                    "transitions": [],
                    "type": "audio",
                    "clips": audio_clips
                }
            ]
        }
    }

    # Salva arquivo nativo .drift
    json_bytes = json.dumps(doc, ensure_ascii=False, indent=None).encode("utf-8")
    cctx = zstd.ZstdCompressor(level=3)
    compressed = cctx.compress(json_bytes)
    header = (
        b"DRIFTPRJ"
        + struct.pack("<III", 1, len(compressed), len(json_bytes))
        + hashlib.sha256(json_bytes).digest()
    )

    with open(OUTPUT_DRIFT, "wb") as f:
        f.write(header + compressed)

    print(f"[DRIFT] Projeto nativo compilado com sucesso em '{OUTPUT_DRIFT}' ({len(header) + len(compressed)} bytes).")
    print(f"  - {len(sub_clips)} Legendas com Background Box")
    print(f"  - {len(card_clips)} Cards & Lower-Thirds")
    print(f"  - {len(video_clips)} Clipes de Vídeo Principais (Inclui Clip 50 Showcase 360)")
    print(f"  - {len(sfx_clips)} Efeitos Sonoros SFX sincronizados")
    print(f"  - {len(audio_clips)} Trilha BGM com Fade-In e Fade-Out")
    print(f"  - Duração Total da Timeline: {total_duration_us / 1000000:.2f}s ({total_duration_us / 60000000:.2f} min)")

    # Atualiza projeto no Drift Editor via MCP
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "load_project",
                "arguments": {"path": OUTPUT_DRIFT}
            }
        }
        headers = {
            "Authorization": f"Bearer {DRIFT_TOKEN}",
            "Content-Type": "application/json"
        }
        req = urllib.request.Request(DRIFT_MCP_URL, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            load_res = json.loads(resp.read().decode('utf-8'))
            print("[DRIFT MCP] load_project executado no Drift Video Editor:", json.dumps(load_res))
        
        # Salva o projeto carregado
        save_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "save_project",
                "arguments": {"path": OUTPUT_DRIFT}
            }
        }
        req_save = urllib.request.Request(DRIFT_MCP_URL, data=json.dumps(save_payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req_save, timeout=10) as resp_s:
            save_res = json.loads(resp_s.read().decode('utf-8'))
            print("[DRIFT MCP] save_project executado no Drift Video Editor:", json.dumps(save_res))

    except Exception as e:
        print(f"[DRIFT MCP] Erro ao sincronizar via MCP: {e}")

if __name__ == "__main__":
    build_full_project()
