"""
YouTube Studio Automation & Playwright Client
Gerencia perfil persistente e upload automático de vídeos com miniaturas (capas).
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, BrowserContext, Page

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


async def get_browser_context(headless: bool = False):
    """Inicia ou reutiliza o contexto persistente do navegador."""
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    p = await async_playwright().start()
    
    try:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            channel="chrome",
            headless=headless,
            user_agent=DEFAULT_USER_AGENT,
            args=CHROME_ARGS,
            viewport={"width": 1280, "height": 800},
            locale="pt-BR",
        )
    except Exception:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=headless,
            user_agent=DEFAULT_USER_AGENT,
            args=CHROME_ARGS,
            viewport={"width": 1280, "height": 800},
            locale="pt-BR",
        )
    return p, context


async def login():
    """Abre uma janela do navegador visível para login no YouTube Studio e salva o perfil."""
    print("=================================================================")
    print(" [YOUTUBE MCP] Autenticacao no YouTube Studio via Navegador")
    print("=================================================================")
    print(" 1. Uma janela do navegador vai abrir em https://studio.youtube.com/")
    print(" 2. Faca o login com a conta Google do seu canal.")
    print(" 3. Resolva o 2FA/Confirmacao no celular se solicitado.")
    print(" 4. Quando estiver logado no painel do YouTube Studio, volte aqui")
    print("    e pressione ENTER.")
    print("=================================================================")

    p, context = await get_browser_context(headless=False)
    page = context.pages[0] if context.pages else await context.new_page()

    await page.goto("https://studio.youtube.com/", wait_until="domcontentloaded")

    input("\n>>> Pressione ENTER neste terminal APOS concluir o login no navegador... <<<\n")

    current_url = page.url
    print(f"\n[INFO] Pagina atual: {current_url}")
    print(f"[SUCESSO] Perfil salvo com sucesso em: {USER_DATA_DIR}")
    
    await context.close()
    await p.stop()


async def verify_session() -> bool:
    """Verifica se o perfil persistente existe."""
    if not USER_DATA_DIR.exists() or not list(USER_DATA_DIR.iterdir()):
        print(f"[AVISO] Perfil de sessao nao encontrado em: {USER_DATA_DIR}")
        print("Execute: python browser.py login")
        return False
    return True


async def upload_video(
    video_path: str,
    thumbnail_path: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    visibility: str = "unlisted",  # "public", "unlisted", "private"
    made_for_kids: bool = False,
    headless: bool = False,
) -> Dict[str, Any]:
    """
    Realiza o upload completo de um vídeo no YouTube Studio com capa personalizada.
    """
    v_path = Path(video_path).resolve()
    if not v_path.exists():
        return {"success": False, "error": f"Arquivo de video nao encontrado: {video_path}"}

    t_path = Path(thumbnail_path).resolve() if thumbnail_path else None
    if t_path and not t_path.exists():
        print(f"[AVISO] Capa nao encontrada em: {thumbnail_path}. Upload continuara sem capa.")
        t_path = None

    if not title:
        title = v_path.stem

    p, context = await get_browser_context(headless=headless)
    page = context.pages[0] if context.pages else await context.new_page()

    try:
        print(f"[1/7] Acessando YouTube Studio...")
        await page.goto("https://studio.youtube.com/", wait_until="networkidle", timeout=60000)

        # Se redirecionou para login do Google
        if "accounts.google.com" in page.url:
            await context.close()
            await p.stop()
            return {
                "success": False,
                "error": "Sessao expirada ou nao autenticada. Execute o login primeiro com: python browser.py login"
            }

        print(f"[2/7] Abrindo modal de upload...")
        # Clica no botão 'Criar' ou 'Create'
        create_btn = page.locator("#create-icon, button[aria-label*='Criar'], button[aria-label*='Create'], ytcp-button#create-icon").first
        if await create_btn.count() > 0:
            await create_btn.click()
            await page.wait_for_timeout(1000)
            
            # Clica em 'Enviar vídeos' / 'Upload videos'
            upload_menu_item = page.locator("tp-yt-paper-item:has-text('Enviar'), tp-yt-paper-item:has-text('Upload'), #text-item-0").first
            await upload_menu_item.click()
        else:
            direct_upload = page.locator("#upload-button, ytcp-button#upload-button").first
            if await direct_upload.count() > 0:
                await direct_upload.click()

        await page.wait_for_timeout(2000)

        print(f"[3/7] Selecionando arquivo do video: {v_path.name}...")
        file_input = page.locator("input[type='file'][name='Filedata'], input[type='file']").first
        await file_input.set_input_files(str(v_path))

        print(f"[4/7] Aguardando formulario de detalhes...")
        await page.wait_for_selector("#title-textarea, #textbox[aria-label*='título'], #textbox[aria-label*='title']", timeout=60000)
        await page.wait_for_timeout(2000)

        # 1. Preencher Título
        print(f"[5/7] Preenchendo metadados...")
        title_box = page.locator("#title-textarea #textbox, #textbox[aria-label*='título'], #textbox[aria-label*='title']").first
        await title_box.click()
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await title_box.evaluate(''' (el, text) => {
            el.innerText = text;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        } ''', title[:100])
        await page.wait_for_timeout(500)

        # 2. Preencher Descrição
        if description:
            desc_box = page.locator("#description-textarea #textbox, [aria-label*='descrição'], [aria-label*='description']").first
            if await desc_box.count() > 0:
                await desc_box.click()
                await desc_box.evaluate(''' (el, text) => {
                    el.innerText = text;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                } ''', description[:5000])
                await page.wait_for_timeout(500)

        # 3. Anexar Capa / Thumbnail
        if t_path:
            print(f"  [+] Enviando capa (thumbnail): {t_path.name}...")
            try:
                thumb_input = page.locator("input[id='file-loader'], input[type='file'][accept*='image']").first
                if await thumb_input.count() > 0:
                    await thumb_input.set_input_files(str(t_path))
                    await page.wait_for_timeout(2000)
                else:
                    thumb_btn = page.locator("#select-button, ytcp-thumbnails-compact-editor-uploader").first
                    if await thumb_btn.count() > 0:
                        async with page.expect_file_chooser() as fc_info:
                            await thumb_btn.click()
                        file_chooser = await fc_info.value
                        await file_chooser.set_files(str(t_path))
                        await page.wait_for_timeout(2000)
            except Exception as e:
                print(f"  [!] Aviso ao enviar capa: {e}")

        # 4. Classificação Etária
        print(f"  [+] Configurando classificacao etaria...")
        not_for_kids = page.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK'], [name='VIDEO_MADE_FOR_KIDS_NOT_MFK']").first
        if await not_for_kids.count() > 0:
            await not_for_kids.click()
            await page.wait_for_timeout(500)

        # 5. Tags
        if tags:
            try:
                show_more_btn = page.locator("ytcp-button:has-text('Mostrar mais'), ytcp-button:has-text('Show more'), #toggle-button").first
                if await show_more_btn.count() > 0:
                    await show_more_btn.click()
                    await page.wait_for_timeout(1000)

                tags_input = page.locator("#tags-container input, input[aria-label*='Tags'], input[aria-label*='Marcadores']").first
                if await tags_input.count() > 0:
                    await tags_input.click()
                    await tags_input.fill(tags)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(500)
            except Exception as e:
                print(f"  [!] Aviso ao adicionar tags: {e}")

        # Capturar Link do vídeo
        video_url = None
        try:
            link_elem = page.locator("a.ytcp-video-info, a[href*='youtu.be'], span.ytcp-video-info").first
            if await link_elem.count() > 0:
                video_url = await link_elem.get_attribute("href") or await link_elem.inner_text()
                if video_url and "youtu.be" in video_url:
                    video_url = video_url.strip()
        except Exception:
            pass

        print(f"[6/7] Avancando etapas de verificacao e visibilidade...")
        for step in range(3):
            next_btn = page.locator("#next-button, ytcp-button#next-button").first
            if await next_btn.count() > 0:
                await next_btn.click()
                await page.wait_for_timeout(1500)

        # 6. Definir Visibilidade
        print(f"[7/7] Definindo visibilidade como '{visibility.upper()}'...")
        vis = visibility.lower()
        if vis == "public":
            radio = page.locator("tp-yt-paper-radio-button[name='PUBLIC'], [name='PUBLIC']").first
        elif vis == "private":
            radio = page.locator("tp-yt-paper-radio-button[name='PRIVATE'], [name='PRIVATE']").first
        else:  # unlisted
            radio = page.locator("tp-yt-paper-radio-button[name='UNLISTED'], [name='UNLISTED']").first

        if await radio.count() > 0:
            await radio.click()
            await page.wait_for_timeout(1000)

        # Salvar / Publicar
        done_btn = page.locator("#done-button, ytcp-button#done-button").first
        if await done_btn.count() > 0:
            await done_btn.click()
            print(f"[+] Botao Salvar/Publicar clicado. Aguardando confirmacao...")
            await page.wait_for_timeout(5000)

        if not video_url:
            try:
                final_link = page.locator("a[href*='youtu.be'], #share-url, a.ytcp-video-share-dialog").first
                if await final_link.count() > 0:
                    video_url = await final_link.get_attribute("href") or await final_link.inner_text()
            except Exception:
                pass

        print(f"\n=======================================================")
        print(f" [SUCESSO] Video enviado com sucesso!")
        print(f" Titulo: {title}")
        if video_url:
            print(f" Link: {video_url}")
        print(f" Visibilidade: {visibility}")
        print(f"=======================================================\n")

        await context.close()
        await p.stop()

        return {
            "success": True,
            "title": title,
            "video_url": video_url,
            "visibility": visibility,
            "has_thumbnail": bool(t_path),
        }

    except Exception as e:
        print(f"[-] Erro durante o upload: {e}")
        try:
            await context.close()
            await p.stop()
        except Exception:
            pass
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "login":
        asyncio.run(login())
    elif len(sys.argv) > 1 and sys.argv[1] == "upload":
        v = sys.argv[2] if len(sys.argv) > 2 else ""
        t = sys.argv[3] if len(sys.argv) > 3 else None
        tit = sys.argv[4] if len(sys.argv) > 4 else None
        res = asyncio.run(upload_video(video_path=v, thumbnail_path=t, title=tit))
        print(res)
    else:
        valid = asyncio.run(verify_session())
        if valid:
            print(f"[OK] Sessao YouTube Studio encontrada em: {USER_DATA_DIR}")
        else:
            print("Execute 'python browser.py login' para autenticar.")
