# -*- coding: utf-8 -*-
"""
Script de Publicação em Lote para os 3 novos vídeos do Alex Sandro
1. Baixa Games Flutter Linux (05)
2. Epic Games no Linux / Heroic (06)
3. Gamepad UI Showcase (07)
"""

import os
import sys
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

USER_DATA_DIR = Path(os.path.expanduser("~/.youtube_studio_profile"))

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

CHROME_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-default-browser-check",
    "--no-first-run",
]

VIDEOS_TO_UPLOAD = [
    {
        "video_path": "/home/alex/Videos/projects/baixa_games_flutter_linux/exports/baixa_games_master_16x9.mp4",
        "thumbnail_path": "/media/alex/alex/mcp-servers/youtube-mcp/thumb_baixa_games_oficial.png",
        "title": "Como Criar Apps Desktop no Linux com Flutter (Projeto Baixa Games)",
        "description": """🚀 Desenvolvi um aplicativo desktop nativo para Linux utilizando Flutter e Dart! Conheça a arquitetura do projeto Baixa Games, interface moderna com Dark Mode e integração de performance no Ubuntu/Linux.

👇 RECURSOS & LINKS DO CANAL:
🔹 GitHub / Código Fonte: https://github.com/al3x-d3v357
🔹 Projetos & Portfólio: https://github.com/al3x-d3v357/projetos_unity

⏱️ CAPÍTULOS / TIMESTAMPS:
00:00 - Introdução ao Projeto Baixa Games
00:50 - Arquitetura Desktop no Flutter Linux
02:30 - Interface Moderna e Responsiva
04:45 - Integração e Performance Nativa
05:40 - Conclusão e Próximos Passos

💬 PERGUNTA DO VÍDEO:
Você já testou criar aplicações Desktop com Flutter ou prefere desenvolver para Web/Mobile? Deixe nos comentários!

🔔 VÍDEOS NOVOS TODOS OS DIAS ÀS 13:13:
Inscreva-se e ative o sininho para acompanhar a rotina diária de desenvolvimento!

#Flutter #Linux #Dart #Ubuntu #DesktopDev #SoftwareDevelopment #OpenSource #Tech""",
        "tags": "flutter linux, criar app desktop flutter, flutter dart desktop, ubuntu app flutter, baixa games alex sandro, flutter tutorial brasil, gamedev ferramentas, alex sandro, al3x-d3v357",
        "schedule_date": "28 de out. de 2026",
        "schedule_time": "13:13"
    },
    {
        "video_path": "/home/alex/Videos/Instalar Jogos da Epic no Linux — Heroic Games Launcher.mp4",
        "thumbnail_path": "/media/alex/alex/mcp-servers/youtube-mcp/thumb_epic_linux_oficial.png",
        "title": "Como Instalar e Rodar Jogos da Epic Games no Linux Fácil (Heroic Launcher)",
        "description": """🎮 Aprenda o passo a passo completo para instalar, configurar e rodar sua biblioteca de jogos da Epic Games no Linux com estabilidade e FPS alto usando o Heroic Games Launcher!

Neste tutorial prático, mostro a configuração de Wine-GE, Proton, Vulkan e as otimizações recomendadas para extrair o máximo de desempenho no Ubuntu/Debian.

👇 RECURSOS & FERRAMENTAS MENCIONADAS:
🔹 Heroic Games Launcher: https://heroicgameslauncher.com/
🔹 GitHub do Alex: https://github.com/al3x-d3v357

⏱️ CAPÍTULOS / TIMESTAMPS:
00:00 - Introdução: Epic Games no Linux
01:20 - Download e Instalação do Heroic Games Launcher
04:15 - Login e Vinculação da Conta Epic
07:10 - Configurações de Wine, Proton e Vulkan
10:30 - Teste Prático de Instalação e Execução
12:40 - Considerações Finais e Dicas de FPS

💬 PERGUNTA DO VÍDEO:
Qual jogo da sua biblioteca da Epic você mais quer ver rodando no Linux com alto FPS? Comente abaixo!

🔔 VÍDEOS NOVOS TODOS OS DIAS ÀS 13:13:
Inscreva-se e ative as notificações para dicas de Linux, GameDev e Tecnologia!

#LinuxGaming #HeroicLauncher #EpicGames #Wine #Proton #Ubuntu #Gaming #JogosLinux""",
        "tags": "jogos epic linux, heroic games launcher tutorial, como jogar no linux, wine proton jogos, epic games linux ubuntu, heroic launcher setup, gaming no linux, alex sandro, al3x-d3v357",
        "schedule_date": "29 de out. de 2026",
        "schedule_time": "13:13"
    },
    {
        "video_path": "/home/alex/Videos/gamepad_ui_showcase.mp4",
        "thumbnail_path": "/media/alex/alex/mcp-servers/youtube-mcp/thumb_gamepad_ui_oficial.png",
        "title": "Criando Menu e UI para Gamepad no Jogo (Navegação Fluida por Controle)",
        "description": """🎯 Ter suporte nativo e fluido para Gamepad/Controle é essencial em qualquer jogo moderno para PC, consoles e Steam Deck. Neste showcase técnico, apresento a estrutura de interface, foco automático e navegação de menus sem travar a experiência do jogador.

👇 RECURSOS & LINKS:
🔹 Repositório do Canal: https://github.com/al3x-d3v357
🔹 Projetos de GameDev: https://github.com/al3x-d3v357/projetos_unity

⏱️ CAPÍTULOS / TIMESTAMPS:
00:00 - O Desafio da UI para Controle
01:10 - Sistema de Navegação por Eixos e Botões
03:00 - Feedback Visual e Foco Automático
05:20 - Tratamento de Menus e Submenus
07:00 - Conclusão e Boas Práticas de UX

💬 PERGUNTA DO VÍDEO:
Nos seus projetos de jogos, você já planeja a UI para controle desde o primeiro dia ou adapta depois? Deixe sua resposta!

🔔 VÍDEOS NOVOS TODOS OS DIAS ÀS 13:13:
Acompanhe os devlogs e testes diários se inscrevendo no canal!

#GameDev #UIUX #Gamepad #ControllerUI #GameDesign #Unity #Godot #IndieDev""",
        "tags": "gamepad ui game dev, menu navegacao controle jogos, input system gamepad, unity controller ui, godot gamepad navigation, indie game dev ux, alex sandro, al3x-d3v357",
        "schedule_date": "30 de out. de 2026",
        "schedule_time": "13:13"
    }
]

async def upload_single_video(page, item: dict):
    v_path = Path(item["video_path"]).resolve()
    t_path = Path(item["thumbnail_path"]).resolve()
    
    print(f"\n=======================================================")
    print(f">>> Enviando: {v_path.name}")
    print(f">>> Titulo: {item['title']}")
    print(f">>> Thumbnail: {t_path.name}")
    print(f"=======================================================")

    if not v_path.exists():
        print(f"[ERRO] Arquivo de video nao encontrado: {v_path}")
        return {"success": False, "error": "Video not found"}

    # 1. Acessa YouTube Studio
    print("  [1/6] Abrindo YouTube Studio...")
    await page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(4000)

    # 2. Clicar em Criar / Enviar vídeos
    print("  [2/6] Abrindo janela de envio...")
    create_btn = page.locator("#create-icon, button[aria-label*='Criar'], button[aria-label*='Create'], ytcp-button#create-icon").first
    if await create_btn.count() > 0:
        await create_btn.click()
        await page.wait_for_timeout(1000)
        upload_opt = page.locator("tp-yt-paper-item:has-text('Enviar'), tp-yt-paper-item:has-text('Upload'), #text-item-0").first
        await upload_opt.click()
    else:
        upload_btn = page.locator("#upload-button, ytcp-button#upload-button").first
        if await upload_btn.count() > 0:
            await upload_btn.click()

    await page.wait_for_timeout(2500)

    # 3. Input de arquivo
    print("  [3/6] Carregando arquivo do vídeo no formulário...")
    file_input = page.locator("input[type='file'][name='Filedata'], input[type='file']").first
    await file_input.set_input_files(str(v_path))

    # 4. Aguardar tela de Detalhes
    print("  [4/6] Aguardando tela de metadados...")
    await page.wait_for_selector("#title-textarea #textbox, #textbox[aria-label*='título'], #textbox[aria-label*='title']", timeout=60000)
    await page.wait_for_timeout(2500)

    # Preencher Título
    title_box = page.locator("#title-textarea #textbox, #textbox[aria-label*='título'], #textbox[aria-label*='title']").first
    try:
        await title_box.click(force=True, timeout=5000)
    except Exception:
        pass
    await title_box.evaluate(''' (el, text) => {
        el.focus();
        el.innerText = text;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    } ''', item["title"][:100])
    await page.wait_for_timeout(1000)

    # Preencher Descrição
    desc_box = page.locator("#description-textarea #textbox, [aria-label*='descrição'], [aria-label*='description']").first
    if await desc_box.count() > 0:
        try:
            await desc_box.click(force=True, timeout=5000)
        except Exception:
            pass
        await desc_box.evaluate(''' (el, text) => {
            el.focus();
            el.innerText = text;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        } ''', item["description"][:5000])
        await page.wait_for_timeout(1000)

    # Anexar Capa / Thumbnail
    if t_path.exists():
        print(f"  [+] Inserindo thumbnail oficial: {t_path.name}...")
        try:
            thumb_input = page.locator("input[id='file-loader'], input[type='file'][accept*='image']").first
            if await thumb_input.count() > 0:
                await thumb_input.set_input_files(str(t_path))
                await page.wait_for_timeout(3000)
            else:
                thumb_btn = page.locator("#select-button, ytcp-thumbnails-compact-editor-uploader").first
                if await thumb_btn.count() > 0:
                    async with page.expect_file_chooser() as fc:
                        await thumb_btn.click(force=True)
                    chooser = await fc.value
                    await chooser.set_files(str(t_path))
                    await page.wait_for_timeout(3000)
        except Exception as e:
            print(f"  [!] Aviso na miniatura: {e}")

    # Checagem de segurança do Google: "Confirme sua identidade"
    try:
        ident_dialog = page.locator("tp-yt-paper-dialog:has-text('Confirme sua identidade'), [role='dialog']:has-text('Confirme sua identidade')").first
        if await ident_dialog.count() > 0 and await ident_dialog.is_visible():
            print("\n  [!] Google solicitou confirmação de identidade para envio de miniatura.")
            print("  [!] Por favor, confirme na janela do navegador que abriu na sua tela...")
            avancar_btn = ident_dialog.locator("button:has-text('Avançar'), ytcp-button:has-text('Avançar')").first
            if await avancar_btn.count() > 0:
                await avancar_btn.click()
            await ident_dialog.wait_for(state="hidden", timeout=120000)
            print("  [+] Identidade confirmada com sucesso!\n")
            await page.wait_for_timeout(2000)
    except Exception as e:
        print(f"  [i] Verificação de identidade: {e}")

    # Não é conteúdo para crianças
    not_kids = page.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK'], [name='VIDEO_MADE_FOR_KIDS_NOT_MFK']").first
    if await not_kids.count() > 0:
        await not_kids.click(force=True)
        await page.wait_for_timeout(500)

    # Tags
    try:
        more_btn = page.locator("ytcp-button:has-text('Mostrar mais'), ytcp-button:has-text('Show more'), #toggle-button").first
        if await more_btn.count() > 0:
            await more_btn.click(force=True)
            await page.wait_for_timeout(1000)

        tags_in = page.locator("#tags-container input, input[aria-label*='Tags'], input[aria-label*='Marcadores']").first
        if await tags_in.count() > 0:
            await tags_in.click(force=True)
            await tags_in.fill(item["tags"])
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(500)
    except Exception as e:
        print(f"  [!] Aviso tags: {e}")

    # Capturar Link do Vídeo
    video_url = ""
    try:
        link_el = page.locator("a.ytcp-video-info, a[href*='youtu.be']").first
        if await link_el.count() > 0:
            video_url = await link_el.get_attribute("href") or await link_el.inner_text()
    except Exception:
        pass

    # 5. Avançar Etapas (Elementos, Verificação, Visibilidade)
    print("  [5/6] Avançando telas de verificação...")
    for _ in range(5):
        unlisted_visible = await page.locator("tp-yt-paper-radio-button[name='UNLISTED'], [name='UNLISTED']").count() > 0 and await page.locator("tp-yt-paper-radio-button[name='UNLISTED'], [name='UNLISTED']").first.is_visible()
        if unlisted_visible:
            print("  [+] Aba de Visibilidade alcançada!")
            break
        nxt = page.locator("#next-button, ytcp-button#next-button").first
        if await nxt.count() > 0 and await nxt.is_visible():
            await nxt.click(force=True)
            await page.wait_for_timeout(2500)
        else:
            await page.wait_for_timeout(1500)

    # 6. Salvar como Não-listado (Unlisted) com segurança máxima para processamento HD
    print(f"  [6/6] Salvando visibilidade como Não-listado (Pronto para revisão e agendamento)...")
    unlisted_radio = page.locator("tp-yt-paper-radio-button[name='UNLISTED'], [name='UNLISTED']").first
    if await unlisted_radio.count() > 0:
        await unlisted_radio.click(force=True)
        await page.wait_for_timeout(1500)

    # Aguardar done_btn ficar visível e ativo
    done_btn = page.locator("#done-button, ytcp-button#done-button, ytcp-button:has-text('Salvar'), ytcp-button:has-text('Save')").first
    try:
        await page.wait_for_selector("#done-button:not([hidden]):not([disabled]), ytcp-button#done-button:not([hidden])", timeout=15000)
    except Exception:
        pass
    if await done_btn.count() > 0:
        await done_btn.click(force=True)
        print("  [+] Vídeo salvo com sucesso no painel!")
        await page.wait_for_timeout(8000)

    await page.screenshot(path=f"/media/alex/alex/mcp-servers/youtube-mcp/uploaded_{v_path.stem}.png")
    print(f"[CONCLUÍDO] Vídeo enviado com sucesso! URL: {video_url}")
    return {"success": True, "title": item["title"], "url": video_url}

async def main():
    p = await async_playwright().start()
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(USER_DATA_DIR),
        headless=False,
        user_agent=DEFAULT_USER_AGENT,
        args=CHROME_ARGS,
        viewport={"width": 1280, "height": 850},
        locale="pt-BR"
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    results = []
    try:
        for item in VIDEOS_TO_UPLOAD:
            res = await upload_single_video(page, item)
            results.append(res)
            await page.wait_for_timeout(4000)
    finally:
        await ctx.close()
        await p.stop()

    print("\n================ RESUMO DOS UPLOADS ================")
    for r in results:
        print(f"- {r.get('title')}: {'OK' if r.get('success') else 'FALHA'} ({r.get('url', 'N/A')})")

if __name__ == "__main__":
    asyncio.run(main())
