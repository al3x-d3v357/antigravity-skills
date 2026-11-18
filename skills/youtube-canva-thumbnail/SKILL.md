---
name: youtube-canva-thumbnail
description: Automates creating and exporting YouTube thumbnails from Alex's Canva template ("Canal capinha Arthur") via Canva MCP and preparing YouTube Studio uploads (title, description, thumbnail). Use whenever the user asks to create a thumbnail/capinha from Canva or publish a video to their YouTube channel.
---

# YouTube Thumbnail (Canva) & Upload Workflow

## 1. Canva Template Reference
- **Design Title:** `Canal capinha Arthur`
- **Design ID:** `DAHPkFMx6Sg` (5 pages, `1280x720` px)
- **Page IDs:**
  - Page 1: `PBQmftMdrnVzdQv9`
  - Page 2: `PBRc5Md5VZVyHhqv`
  - Page 3: `PBbJBlrFVgNfcP2D`
  - Page 4: `PBB0xN22PjHW7zhW`
  - Page 5: `PBGvsN4hW7NsR67q`

## 2. Editable Text Slots & Length Limits
Every page shares the exact same 9 text slots. Keep strings short to prevent line wrapping onto adjacent pills or icons:

| Slot | Role | Max Length (approx.) | Example |
|------|------|----------------------|---------|
| 1 | Top badge | ~18 chars | `3D DEV • BLENDER` |
| 2 | Main Title Line 1 (white) | ~7-8 chars | `RIFLE` |
| 3 | Main Title Line 2 (blue italic) | ~7-8 chars | `SCI-FI` |
| 4 | Left Pill (cyan) | ~9 chars | `BLENDER` |
| 5 | Right Pill (purple) | ~10 chars | `MODELO 3D` |
| 6 | Bottom Icon 1 (`</>`) | ~8-9 chars | `GIMP 3.2` |
| 7 | Bottom Icon 2 (brain) | ~9-10 chars | `IA NO 3D` |
| 8 | Bottom Icon 3 (`>_`) | ~9-10 chars | `AGY 2.0` |
| 9 | Bottom Icon 4 (rocket) | ~8-9 chars | `DO ZERO` |

## 3. Canva MCP Step-by-Step
1. Call `start-editing-transaction` with `design_id: "DAHPkFMx6Sg"`.
2. Identify the `element_id`s for the target page (default: Page 1 `PBQmftMdrnVzdQv9` or whichever page is least recently used).
3. Call `perform-editing-operations` with `replace_text` for the 9 text elements, passing the `pages` array returned by `start-editing-transaction`.
4. **Always inspect the preview image** (`media_0.png` in the tool output folder) with `read_file` to verify zero unwanted line wrapping or overlap. Adjust text or box width if needed.
5. Call `commit-editing-transaction` to save changes.
6. Call `export-design` with `format: { type: "png", width: 1280, height: 720, pages: [1] }` and download the resulting PNG URL locally (e.g., to `<Artifact Directory>/scratch/` and `<Artifact Directory>/browser_sandbox/uploads/`).

## 4. YouTube Studio Background Automation (OBRIGATÓRIO / MANDATORY)
- **NÃO usar o subagente `browser` (navegador na tela)** para configurar, enviar capinha ou agendar vídeos no YouTube Studio.
- **Executar obrigatoriamente em segundo plano via terminal (Python + Playwright headless)** usando o perfil persistente `~/.youtube_studio_profile` e os scripts de `D:\Projetos\automacao-unificada\youtube-creator-studio\` (por exemplo `browser.py`, `set_schedule_and_edit.py` ou script dedicado com `headless=True`).
- Seguir sempre as diretrizes de título, descrição, capítulos, CTAs, tags e hashtags de `D:\Projetos\automacao-unificada\youtube-seo-retencao\SKILL.md`.
- Se o perfil `~/.youtube_studio_profile` não estiver autenticado, executar `login.bat` em `D:\Projetos\automacao-unificada\youtube-creator-studio\` uma única vez.
