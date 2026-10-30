#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Thumbnails Profissionais no Estilo Oficial do Canva (@al3x-d3v357)
Resolução: 1280x720 (16:9)
Paleta Oficial:
- Azul Royal Profundo: #3852B4
- Azul Médio / Ardósia: #5E7AC4
- Dourado / Âmbar: #F3BE7A
- Laranja Tangerina Neon: #F08D39
- Texto Branco: #FFFFFF
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def create_gradient_overlay(width, height):
    """Cria sobreposição escura degradê da esquerda para direita para leitura perfeita dos textos."""
    gradient = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)
    for x in range(width):
        # Mais escuro à esquerda (alpha ~230) suavizando até à direita (alpha ~60)
        ratio = x / width
        alpha = int(235 * (1.0 - ratio * 0.75))
        draw.line([(x, 0), (x, height)], fill=(10, 15, 30, alpha))
    return gradient

def draw_pill_badge(draw, text, xy, bg_color, text_color=(255, 255, 255), font_size=20, font_path=FONT_BOLD):
    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 18, 8
    x0, y0 = xy
    x1, y1 = x0 + tw + (pad_x * 2), y0 + th + (pad_y * 2)
    radius = (y1 - y0) // 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=bg_color)
    draw.text((x0 + pad_x, y0 + pad_y - 2), text, font=font, fill=text_color)
    return x1

def generate_thumbnail(
    bg_frame_path: str,
    output_path: str,
    top_subtitle: str,
    upper_call: str,
    main_highlight: str,
    badge_left: str,
    badge_right: str,
    pillars: list,
    stamp_number: str
):
    w, h = 1280, 720
    
    # 1. Carregar frame de fundo e redimensionar
    if os.path.exists(bg_frame_path):
        base_img = Image.open(bg_frame_path).convert("RGBA")
        lanczos_filter = getattr(getattr(Image, 'Resampling', Image), 'LANCZOS', Image.LANCZOS)
        base_img = base_img.resize((w, h), lanczos_filter)
        # Leve aumento de contraste e saturação no fundo
        enhancer = ImageEnhance.Color(base_img)
        base_img = enhancer.enhance(1.2)
    else:
        # Fundo gradiente padrão se o frame não existir
        base_img = Image.new("RGBA", (w, h), (18, 24, 48, 255))

    # 2. Aplicar degradê escuro cinemático
    grad = create_gradient_overlay(w, h)
    base_img = Image.alpha_composite(base_img, grad)

    # 3. Canvas de desenho
    draw = ImageDraw.Draw(base_img)

    # 4. Linha de topo: Subtítulo (com pontinho dourado e cor #F3BE7A)
    f_sub = ImageFont.truetype(FONT_BOLD, 24)
    sub_text = f"●  {top_subtitle.upper()}"
    draw.text((60, 60), sub_text, font=f_sub, fill=(243, 190, 122)) # Dourado Âmbar

    # 5. Chamada Superior (Branco Gigante #FFFFFF)
    f_upper = ImageFont.truetype(FONT_BOLD, 92)
    # Sombra projetada
    draw.text((63, 113), upper_call.upper(), font=f_upper, fill=(0, 0, 0, 220))
    draw.text((60, 110), upper_call.upper(), font=f_upper, fill=(255, 255, 255))

    # 6. Destaque Principal (Azul Royal Neon c/ contorno branco e glow #3852B4 / #5E7AC4)
    f_main = ImageFont.truetype(FONT_BOLD, 88)
    y_main = 215
    # Contorno e sombra forte
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            if dx*dx + dy*dy <= 16:
                draw.text((60 + dx, y_main + dy), main_highlight.upper(), font=f_main, fill=(15, 25, 60, 255))
    # Brilho ciano/azul
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            draw.text((60 + dx, y_main + dy), main_highlight.upper(), font=f_main, fill=(94, 122, 196, 255))
    draw.text((60, y_main), main_highlight.upper(), font=f_main, fill=(240, 246, 255))

    # 7. Badges em Pílula
    y_badges = 345
    # Badge Esquerdo: Laranja Tangerina Neon (#F08D39)
    next_x = draw_pill_badge(draw, badge_left.upper(), (60, y_badges), bg_color=(240, 141, 57), text_color=(255, 255, 255), font_size=22)
    # Badge Direito: Azul Médio / Ardósia (#5E7AC4)
    draw_pill_badge(draw, badge_right.upper(), (next_x + 18, y_badges), bg_color=(56, 82, 180), text_color=(255, 255, 255), font_size=22)

    # 8. Os 4 Pilares Temáticos (Containers translúcidos inferiores)
    f_pilar_icon = ImageFont.truetype(FONT_BOLD, 16)
    f_pilar_text = ImageFont.truetype(FONT_BOLD, 17)
    icons = ["</>", "AI", "⚡", "🚀"]
    start_x = 60
    y_pilar = 430
    box_w = 150
    box_h = 75

    for i, p_text in enumerate(pillars[:4]):
        bx = start_x + (i * (box_w + 14))
        # Container com borda fina e fundo semi-transparente
        draw.rounded_rectangle([bx, y_pilar, bx + box_w, y_pilar + box_h], radius=8, fill=(20, 30, 60, 210), outline=(94, 122, 196, 180), width=2)
        # Ícone do pilar
        draw.text((bx + 14, y_pilar + 12), icons[i], font=f_pilar_icon, fill=(243, 190, 122))
        # Texto do pilar
        draw.text((bx + 14, y_pilar + 40), p_text.upper(), font=f_pilar_text, fill=(255, 255, 255))

    # 9. Sem numeração (removido a pedido do usuário)
    # Mantém a área limpa para destaque total da arte de fundo e dos títulos

    # 10. Salvar em PNG
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    base_img.convert("RGB").save(output_path, "PNG", quality=95)
    print(f"[SUCESSO] Thumbnail gerada: {output_path}")

def main():
    frames_dir = "/media/alex/alex/mcp-servers/youtube-mcp/frames"
    out_dir = "/media/alex/alex/mcp-servers/youtube-mcp/thumbs_novos"
    os.makedirs(out_dir, exist_ok=True)

    # 1. Capa #05: Baixa Games Flutter Linux
    generate_thumbnail(
        bg_frame_path=f"{frames_dir}/frame_baixa_games.png",
        output_path=f"{out_dir}/thumb_baixa_games_05.png",
        top_subtitle="APP DEV • FLUTTER",
        upper_call="FLUTTER",
        main_highlight="LINUX",
        badge_left="DESKTOP",
        badge_right="DART 3",
        pillars=["LINUX APP", "UBUNTU", "FLUTTER", "ALTA PERF"],
        stamp_number="#05"
    )

    # 2. Capa #06: Epic Games no Linux / Heroic
    generate_thumbnail(
        bg_frame_path=f"{frames_dir}/frame_heroic_epic.png",
        output_path=f"{out_dir}/thumb_epic_linux_06.png",
        top_subtitle="LINUX GAMING • EPIC",
        upper_call="JOGOS",
        main_highlight="NO LINUX",
        badge_left="HEROIC",
        badge_right="EPIC GAMES",
        pillars=["PROTON", "VULKAN", "WINE GE", "FPS ALTO"],
        stamp_number="#06"
    )

    # 3. Capa #07: Gamepad UI Showcase
    generate_thumbnail(
        bg_frame_path=f"{frames_dir}/frame_gamepad_ui.png",
        output_path=f"{out_dir}/thumb_gamepad_ui_07.png",
        top_subtitle="GAME DEV • UI/UX",
        upper_call="GAMEPAD",
        main_highlight="UI PRO",
        badge_left="CONTROLE",
        badge_right="NAVEGAÇÃO",
        pillars=["INPUT SYS", "CANVAS", "FEEDBACK", "100% FLUIDO"],
        stamp_number="#07"
    )

if __name__ == "__main__":
    main()
