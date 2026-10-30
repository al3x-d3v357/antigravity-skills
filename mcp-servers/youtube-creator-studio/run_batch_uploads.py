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

async def upload_video_item(
    video_path: str,
    thumbnail_path: str,
    title: str,
    description: str,
    tags: str,
    schedule_date_str: str, # e.g. "11 de nov. de 2026"
    schedule_time_str: str = "13:15"
):
    v_path = Path(video_path).resolve()
    t_path = Path(thumbnail_path).resolve()
    
    print(f"\n==========================================")
    print(f"Iniciando Upload: {v_path.name}")
    print(f"Capa: {t_path.name}")
    print(f"Data Alvo: {schedule_date_str} as {schedule_time_str}")
    print(f"==========================================")

    p = await async_playwright().start()
    context = await p.chromium.launch_persistent_context(
        user_data_dir=str(USER_DATA_DIR),
        channel="chrome",
        headless=False,
        user_agent=DEFAULT_USER_AGENT,
        args=CHROME_ARGS,
        viewport={"width": 1280, "height": 850},
        locale="pt-BR",
    )
    page = context.pages[0] if context.pages else await context.new_page()

    try:
        print("[Passo 1] Acessando studio.youtube.com...")
        await page.goto("https://studio.youtube.com/", wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(2000)

        print("[Passo 2] Abrindo modal de upload...")
        create_btn = page.locator("#create-icon, button[aria-label*='Criar'], ytcp-button#create-icon").first
        await create_btn.click()
        await page.wait_for_timeout(1000)

        upload_opt = page.locator("tp-yt-paper-item:has-text('Enviar'), #text-item-0").first
        await upload_opt.click()
        await page.wait_for_timeout(2000)

        print(f"[Passo 3] Enviando arquivo de video...")
        file_input = page.locator("input[type='file'][name='Filedata'], input[type='file']").first
        await file_input.set_input_files(str(v_path))

        print("[Passo 4] Aguardando tela de Detalhes...")
        await page.wait_for_selector("#title-textarea #textbox", timeout=60000)
        await page.wait_for_timeout(2500)

        # Titulo
        print("[Passo 5] Preenchendo Titulo...")
        title_box = page.locator("#title-textarea #textbox").first
        await title_box.click()
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await title_box.evaluate(''' (el, text) => {
            el.innerText = text;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        } ''', title[:100])
        await page.wait_for_timeout(1000)

        # Descricao
        print("[Passo 6] Preenchendo Descricao...")
        desc_box = page.locator("#description-textarea #textbox").first
        if await desc_box.count() > 0:
            await desc_box.click()
            await desc_box.evaluate(''' (el, text) => {
                el.innerText = text;
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            } ''', description[:5000])
            await page.wait_for_timeout(1000)

        # Capa / Thumbnail
        print(f"[Passo 7] Anexando Capa...")
        try:
            thumb_input = page.locator("input[id='file-loader'], input[type='file'][accept*='image']").first
            if await thumb_input.count() > 0:
                await thumb_input.set_input_files(str(t_path))
                await page.wait_for_timeout(2500)
            else:
                thumb_btn = page.locator("#select-button, ytcp-thumbnails-compact-editor-uploader").first
                async with page.expect_file_chooser() as fc_info:
                    await thumb_btn.click()
                fc = await fc_info.value
                await fc.set_files(str(t_path))
                await page.wait_for_timeout(2500)
            print("  [+] Capa anexada com sucesso!")
        except Exception as e:
            print(f"  [!] Aviso ao enviar capa: {e}")

        # Classificacao Etaria (Nao e para criancas)
        print("[Passo 8] Definindo classificacao etaria...")
        not_for_kids = page.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']").first
        if await not_for_kids.count() > 0:
            await not_for_kids.click()
            await page.wait_for_timeout(500)

        # Tags
        print("[Passo 9] Preenchendo Tags...")
        show_more = page.locator("ytcp-button:has-text('Mostrar mais'), #toggle-button").first
        if await show_more.count() > 0:
            await show_more.click()
            await page.wait_for_timeout(1000)
            tags_input = page.locator("#tags-container input").first
            if await tags_input.count() > 0:
                await tags_input.click()
                await tags_input.fill(tags)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(500)

        # Capturar Link do video
        video_url = None
        try:
            link_elem = page.locator("a.ytcp-video-info, a[href*='youtu.be']").first
            if await link_elem.count() > 0:
                video_url = await link_elem.get_attribute("href")
                if video_url:
                    video_url = video_url.strip()
                    print(f"  [+] Link do Video: {video_url}")
        except Exception:
            pass

        # Avancar pelos passos de Detalhes -> Elementos -> Verificacao -> Visibilidade
        print("[Passo 10] Avancando ate Visibilidade...")
        for i in range(3):
            next_btn = page.locator("#next-button, ytcp-button#next-button").first
            await next_btn.click()
            await page.wait_for_timeout(1500)

        print("[Passo 11] Selecionando Programar (Schedule)...")
        # Localiza o radio de programacao
        schedule_radio = page.locator("#schedule-radio-button, tp-yt-paper-radio-button:has-text('Programar')").first
        if await schedule_radio.count() > 0:
            await schedule_radio.click()
            await page.wait_for_timeout(1500)
            
            # Seletor de Data
            print(f"  [+] Configurando data: {schedule_date_str}...")
            date_trigger = page.locator("#datepicker-trigger, ytcp-date-picker #picker").first
            if await date_trigger.count() > 0:
                await date_trigger.click()
                await page.wait_for_timeout(1000)
                date_input = page.locator("ytcp-date-picker input, tp-yt-paper-dialog input").first
                if await date_input.count() > 0:
                    await date_input.click()
                    await page.keyboard.press("Control+A")
                    await page.keyboard.type(schedule_date_str)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(1000)
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(500)

            # Seletor de Horario
            print(f"  [+] Configurando horario: {schedule_time_str}...")
            time_input = page.locator("ytcp-time-picker input").first
            if await time_input.count() > 0:
                await time_input.click()
                await page.keyboard.press("Control+A")
                await page.keyboard.type(schedule_time_str)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(1000)

            await page.screenshot(path=rf"D:\GitHub\youtube-mcp\schedule_{v_path.stem}.png")
            print(f"  [+] Screenshot de confirmacao salva!")
        else:
            print("[!] Seletor direto de Programar nao localizado, marcando como Nao-listado...")
            unlisted_radio = page.locator("tp-yt-paper-radio-button[name='UNLISTED']").first
            if await unlisted_radio.count() > 0:
                await unlisted_radio.click()
                await page.wait_for_timeout(1000)

        # Clicar em Concluir / Programar
        print("[Passo 12] Clicando em Salvar / Programar...")
        done_btn = page.locator("#done-button, ytcp-button#done-button").first
        await done_btn.click()
        await page.wait_for_timeout(6000)

        if not video_url:
            try:
                final_link = page.locator("a[href*='youtu.be'], #share-url").first
                if await final_link.count() > 0:
                    video_url = await final_link.get_attribute("href")
            except Exception:
                pass

        print(f"\n[SUCESSO] Video {v_path.name} processado!")
        print(f"Titulo: {title}")
        print(f"Link: {video_url}")

        await context.close()
        await p.stop()
        return {"success": True, "title": title, "video_url": video_url}

    except Exception as e:
        print(f"[-] Erro ao processar video: {e}")
        try:
            await page.screenshot(path=rf"D:\GitHub\youtube-mcp\error_{v_path.stem}.png")
            await context.close()
            await p.stop()
        except Exception:
            pass
        return {"success": False, "error": str(e)}

async def main():
    # Video 1: Yakisoba Play
    desc_yakisoba = """🚀 Desenvolvi meu próprio streaming web de animes do zero! Conheça o Yakisoba Play, interface moderna com catálogo, player customizado e alta performance.
Neste vídeo de devlog, mostro toda a arquitetura da aplicação web, o design system estilizado em Dark Mode, o player de reprodução integrado e as decisões de engenharia full-stack no desenvolvimento frontend.

👇 RECURSOS & LINKS MENCIONADOS NO VÍDEO:
🔹 GitHub do Projeto: https://github.com/al3x-d3v357
🔹 Stack Tecnológica: React, Next.js, HTML5/CSS3 & TypeScript
🔹 Portfólio de Projetos: https://github.com/al3x-d3v357/projetos_unity

⏱️ CAPÍTULOS / TIMESTAMPS:
00:00 - Introdução & Visão Geral do Yakisoba Play
00:45 - Arquitetura Web & Player de Streaming
01:50 - Interface Moderna, Catálogo & Experiência de Usuário
03:10 - Responsividade, Dark Mode & Próximas Features
03:50 - Conclusão & Próximos Passos

💬 PERGUNTA DO VÍDEO:
Qual recurso você gostaria de ver na próxima versão do Yakisoba Play (sistema de favoritos, histórico ou recomendação)? Deixe seu comentário!

🔔 INSCREVA-SE & ACOMPANHE:
Se este conteúdo te inspirou, inscreva-se no canal, deixe seu like e ative o sininho para acompanhar todos os devlogs e projetos!

🔗 MINHAS REDES & COMUNIDADE:
🌐 GitHub: https://github.com/al3x-d3v357
🎮 Portfólio / Projetos: https://github.com/al3x-d3v357

#WebApp #Devlog #React #NextJS #Frontend #FullStack #Programação #IndieDev"""

    res1 = await upload_video_item(
        video_path=r"c:\Users\alexa\Videos\Yakisoba Play - Devlog Showcase.mp4",
        thumbnail_path=r"D:\GitHub\youtube-mcp\thumb_yakisoba_13.png",
        title="CRIANDO MEU STREAMING DE ANIMES DO ZERO • Yakisoba Play (Devlog Web App)",
        description=desc_yakisoba,
        tags="yakisoba play, web app, devlog, streaming anime, nextjs, react, frontend, fullstack, anime player, player web, alex sandro, al3x-d3v357",
        schedule_date_str="11 de nov. de 2026",
        schedule_time_str="13:15"
    )
    print("Resultado Video 1:", res1)

    await asyncio.sleep(5)

    # Video 2: UnoRouter OpenCode
    desc_unorouter = """🚀 Acelere seu fluxo de desenvolvimento criando ferramentas e interfaces completas com auxílio de Inteligência Artificial usando OpenCode, UnoRouter e Muse Spark!
Neste vídeo rápido, demonstro na prática a integração de assistentes de IA diretamente na criação de software, arquitetura modular em Python e boas práticas de prompting técnico para desenvolvimento ágil.

👇 RECURSOS & LINKS MENCIONADOS NO VÍDEO:
🔹 GitHub / Projetos: https://github.com/al3x-d3v357
🔹 Ferramentas: OpenCode, UnoRouter, Muse Spark, Python CustomTkinter
🔹 Portfólio & Repositórios: https://github.com/al3x-d3v357

⏱️ CAPÍTULOS / TIMESTAMPS:
00:00 - Introdução ao OpenCode & UnoRouter
00:25 - Demonstração da Interface Dark Mode & Chat com IA
00:50 - Prompting, Execução de Código & Muse Spark
01:15 - Conclusão & Otimização do Workflow Dev

💬 PERGUNTA DO VÍDEO:
Você já usa assistentes de IA no seu dia a dia de programação ou prefere escrever tudo manualmente? Comente aqui embaixo!

🔔 INSCREVA-SE & ACOMPANHE:
Gostou do tutorial? Inscreva-se no canal, deixe seu like e ative as notificações para receber novos conteúdos de programação, IA e GameDev!

🔗 MINHAS REDES & COMUNIDADE:
🌐 GitHub: https://github.com/al3x-d3v357
🎮 Projetos & Ferramentas: https://github.com/al3x-d3v357

#OpenCode #UnoRouter #InteligenciaArtificial #IACoding #Python #DevAI #MuseSpark #Tech"""

    res2 = await upload_video_item(
        video_path=r"c:\Users\alexa\Videos\unorouter_opencode_alex_editado.mp4",
        thumbnail_path=r"D:\GitHub\youtube-mcp\thumb_unorouter_14.png",
        title="PROGRAMANDO APPS COM IA NO OPENCODE • UnoRouter & Muse Spark (Tutorial Rápido)",
        description=desc_unorouter,
        tags="opencode, unorouter, muse spark, ia coding, programacao com ia, python dark mode, customtkinter, dev ai, llm code, alex sandro, al3x-d3v357",
        schedule_date_str="16 de nov. de 2026",
        schedule_time_str="13:15"
    )
    print("Resultado Video 2:", res2)

if __name__ == "__main__":
    asyncio.run(main())
