#!/usr/bin/env python3
"""
generate_lower_third.py - Deterministic Lower-Third & Card Graphic Generator

Generates transparent 1920x1080 PNG overlays with the mandatory color palette:
#3852B4 (Deep Royal Blue), #5E7AC4 (Medium Slate Blue), #F3BE7A (Warm Amber Gold), #F08D39 (Vibrant Orange).
Text is ALWAYS 100% white (#FFFFFF).
"""

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def hex_to_rgb(hex_str: str):
    h = hex_str.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


# Mandatory Palette
COLOR_DEEP_BLUE = hex_to_rgb("#3852B4")       # (56, 82, 180)
COLOR_SLATE_BLUE = hex_to_rgb("#5E7AC4")      # (94, 122, 196)
COLOR_WARM_GOLD = hex_to_rgb("#F3BE7A")       # (243, 190, 122)
COLOR_VIBRANT_ORANGE = hex_to_rgb("#F08D39")  # (240, 141, 57)
COLOR_TEXT_WHITE = (255, 255, 255, 255)       # Mandatory pure white

# Fox.iso brand variant (opt-in via --palette fox)
FOX_CORAL = hex_to_rgb("#FF7F50")
FOX_SUNGLOW = hex_to_rgb("#FFD166")
FOX_MINT = hex_to_rgb("#06D6A0")
FOX_TEAL = hex_to_rgb("#118AB2")


def get_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    """Attempts to find a clean system sans-serif font, falling back to default."""
    font_candidates = []
    if sys.platform == "win32":
        font_candidates = [
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
        ]
    elif sys.platform == "darwin":
        font_candidates = [
            "/System/Library/Fonts/SFProText-Bold.otf" if bold else "/System/Library/Fonts/SFProText-Regular.otf",
            "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        ]
    else:
        font_candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ]

    for font_path in font_candidates:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue

    return ImageFont.load_default()


def render_lower_third(
    name: str,
    role: str,
    desc: str,
    output_path: str,
    highlight: str = "",
    width: int = 1920,
    height: int = 1080,
    accent: str = "orange"
):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")

    # Dimensions & Positioning - Centered Bottom Card
    card_w = 1360
    card_h = 190
    card_x = (width - card_w) // 2
    card_y = height - 250
    radius = 16

    accent_rgb = COLOR_VIBRANT_ORANGE if accent == "orange" else (COLOR_WARM_GOLD if accent == "gold" else COLOR_SLATE_BLUE)

    # 1. Subtle Glow Underlay with Palette Color
    glow_box = [card_x - 4, card_y - 4, card_x + card_w + 4, card_y + card_h + 4]
    draw.rounded_rectangle(glow_box, radius=radius + 3, fill=(*accent_rgb, 40))

    # 2. Main Glassmorphic Dark Container
    bg_color = (10, 16, 32, 240)
    border_color = (*accent_rgb, 200)
    card_box = [card_x, card_y, card_x + card_w, card_y + card_h]
    draw.rounded_rectangle(card_box, radius=radius, fill=bg_color, outline=border_color, width=3)

    # 3. Left Accent Strip
    strip_w = 8
    strip_box = [card_x + 8, card_y + 12, card_x + 8 + strip_w, card_y + card_h - 12]
    draw.rounded_rectangle(strip_box, radius=4, fill=(*accent_rgb, 255))

    # Fonts
    font_badge = get_font(18, bold=True)
    font_title = get_font(34, bold=True)
    font_desc = get_font(23, bold=False)
    font_highlight = get_font(21, bold=True)

    text_x = card_x + 36

    # Tag / Role Badge
    tag_y = card_y + 18
    if role:
        draw.text((text_x, tag_y), role.upper(), font=font_badge, fill=(*COLOR_WARM_GOLD, 255))

    # Main Title (MANDATORY WHITE)
    title_y = tag_y + 28 if role else card_y + 26
    draw.text((text_x, title_y), name, font=font_title, fill=COLOR_TEXT_WHITE)

    # Description (MANDATORY WHITE)
    if desc:
        desc_y = title_y + 44
        draw.text((text_x, desc_y), desc, font=font_desc, fill=COLOR_TEXT_WHITE)

    # Highlight (Warm Gold #F3BE7A)
    if highlight:
        hl_y = title_y + 78
        draw.text((text_x, hl_y), f"💡 {highlight}", font=font_highlight, fill=(*COLOR_WARM_GOLD, 255))

    # Save artifact
    output_dir = Path(output_path).parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    img.save(output_path, "PNG")
    print(f"[SUCCESS] Lower-third rendered to: {output_path} ({width}x{height})")


def main():
    parser = argparse.ArgumentParser(description="Mandatory Palette Lower-Third Overlay Generator")
    parser.add_argument("--name", default="PROTÓTIPO GODOT", help="Main title name")
    parser.add_argument("--role", default="DEVLOG // GAMEPLAY", help="Badge / category")
    parser.add_argument("--desc", default="Jogo de Carro desenvolvido na Godot Engine", help="Explanatory description")
    parser.add_argument("--highlight", default="Cenário e mecânicas criados com apoio de IA", help="Highlight text")
    parser.add_argument("--accent", choices=["orange", "gold", "blue", "deep_blue"], default="orange", help="Accent color")
    parser.add_argument("--output", "-o", default="lower_third.png", help="Output PNG path")

    args = parser.parse_args()
    render_lower_third(args.name, args.role, args.desc, args.output, highlight=args.highlight, accent=args.accent)


if __name__ == "__main__":
    main()
