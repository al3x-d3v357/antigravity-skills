"""
Script para upload e agendamento automatico no YouTube Studio via Playwright
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
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

async def upload_and_schedule_video(
    video_path: str,
    thumbnail_path: Optional[str] = None,
    title: str = "",
    description: str = "",
    tags: str = "",
    schedule_date: str = "",  # e.g. "11 de nov. de 2026" or "11/11/2026"
    schedule_time: str = "13:15",  # e.g. "13:15"
    headless: bool = False,
) -> Dict[str, Any]:
    v_path = Path(video_path).resolve()
    if not v_path.exists():
        return {"success": False, "error": f"Video not found: {video_path}"}

    t_path = Path(thumbnail_path).resolve() if thumbnail_path else None

    p = await async_playwright().start()
    try:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            channel="chrome",
            headless=headless,
            user_agent=DEFAULT_USER_AGENT,
            args=CHROME_ARGS,
            viewport={"width": 1280, "height": 850},
            locale="pt-BR",
        )
    except Exception:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=headless,
            user_agent=DEFAULT_USER_AGENT,
            args=CHROME_ARGS,
            viewport={"width": 1280, "height": 850},
            locale="pt-BR",
        )

    page = context.pages[0] if context.pages else await context.new_page()

    try:
        print("[1/7] Acessando YouTube Studio...")
        await page.goto("https://studio.youtube.com/", wait_until="networkidle", timeout=60000)

        if "accounts.google.com" in page.url:
            await context.close()
            await p.stop()
            return {"success": False, "error": "Sessao nao autenticada."}

        print("[2/7] Abrindo modal de upload...")
        create_btn = page.locator("#create-icon, button[aria-label*='Criar'], button[aria-label*='Create'], ytcp-button#create-icon").first
        if await create_btn.count() > 0:
            await create_btn.click()
            await page.wait_for_timeout(1000)
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

        print("[4/7] Aguardando formulario de detalhes...")
        await page.wait_for_selector("#title-textarea, #textbox[aria-label*='título'], #textbox[aria-label*='title']", timeout=60000)
        await page.wait_for_timeout(2500)

        print("[5/7] Preenchendo metadados...")
        title_box = page.locator("#title-textarea #textbox, #textbox[aria-label*='título'], #textbox[aria-label*='title']").first
        await title_box.click()
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await title_box.evaluate(''' (el, text) => {
            el.innerText = text;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        } ''', title[:100])
        await page.wait_for_timeout(1000)

        # Descrição
        if description:
            desc_box = page.locator("#description-textarea #textbox, [aria-label*='descrição'], [aria-label*='description']").first
            if await desc_box.count() > 0:
                await desc_box.click()
                await desc_box.evaluate(''' (el, text) => {
                    el.innerText = text;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                } ''', description[:5000])
                await page.wait_for_timeout(1000)

        # Capa / Thumbnail
        if t_path and t_path.exists():
            print(f"  [+] Enviando capa: {t_path.name}...")
            try:
                thumb_input = page.locator("input[id='file-loader'], input[type='file'][accept*='image']").first
                if await thumb_input.count() > 0:
                    await thumb_input.set_input_files(str(t_path))
                    await page.wait_for_timeout(2500)
                else:
                    thumb_btn = page.locator("#select-button, ytcp-thumbnails-compact-editor-uploader").first
                    if await thumb_btn.count() > 0:
                        async with page.expect_file_chooser() as fc_info:
                            await thumb_btn.click()
                        file_chooser = await fc_info.value
                        await file_chooser.set_files(str(t_path))
                        await page.wait_for_timeout(2500)
            except Exception as e:
                print(f"  [!] Aviso ao enviar capa: {e}")

        # Classificação Etária (Não é para crianças)
        print("  [+] Configurando classificacao etaria...")
        not_for_kids = page.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK'], [name='VIDEO_MADE_FOR_KIDS_NOT_MFK']").first
        if await not_for_kids.count() > 0:
            await not_for_kids.click()
            await page.wait_for_timeout(500)

        # Tags
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
                print(f"  [!] Aviso tags: {e}")

        # Link do vídeo
        video_url = None
        try:
            link_elem = page.locator("a.ytcp-video-info, a[href*='youtu.be'], span.ytcp-video-info").first
            if await link_elem.count() > 0:
                video_url = await link_elem.get_attribute("href") or await link_elem.inner_text()
                if video_url and "youtu.be" in video_url:
                    video_url = video_url.strip()
        except Exception:
            pass

        print("[6/7] Avancando etapas de verificacao e visibilidade...")
        for step in range(3):
            next_btn = page.locator("#next-button, ytcp-button#next-button").first
            if await next_btn.count() > 0:
                await next_btn.click()
                await page.wait_for_timeout(1500)

        # Visibilidade e Agendamento
        print(f"[7/7] Configurando Agendamento para {schedule_date} as {schedule_time}...")
        
        # Clica na opcao Programar / Schedule
        schedule_radio = page.locator("#schedule-radio-button, tp-yt-paper-radio-button:has-text('Programar'), tp-yt-paper-radio-button:has-text('Schedule')").first
        if await schedule_radio.count() > 0:
            await schedule_radio.click()
            await page.wait_for_timeout(1500)
            
            # Seletor de data
            date_trigger = page.locator("#datepicker-trigger, ytcp-date-picker #picker, ytcp-date-picker input").first
            if await date_trigger.count() > 0:
                await date_trigger.click()
                await page.wait_for_timeout(800)
                # Tenta digitar ou preencher data
                date_input = page.locator("ytcp-date-picker input, #dialog input").first
                if await date_input.count() > 0:
                    await date_input.click()
                    await page.keyboard.press("Control+A")
                    await page.keyboard.type(schedule_date)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(800)
                else:
                    # Fecha datepicker pressionando Escape
                    await page.keyboard.press("Escape")

            # Seletor de horario
            time_trigger = page.locator("ytcp-time-picker input, ytcp-time-picker #input, #time-of-day-picker input").first
            if await time_trigger.count() > 0:
                await time_trigger.click()
                await page.keyboard.press("Control+A")
                await page.keyboard.type(schedule_time)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(800)
        else:
            print("[!] Opcao programar direta nao encontrada pelo seletor, salvando como Não-listado...")
            radio = page.locator("tp-yt-paper-radio-button[name='UNLISTED'], [name='UNLISTED']").first
            if await radio.count() > 0:
                await radio.click()
                await page.wait_for_timeout(1000)

        # Salvar / Programar
        done_btn = page.locator("#done-button, ytcp-button#done-button").first
        if await done_btn.count() > 0:
            await done_btn.click()
            print("[+] Botao Programar/Salvar clicado. Aguardando confirmacao...")
            await page.wait_for_timeout(6000)

        if not video_url:
            try:
                final_link = page.locator("a[href*='youtu.be'], #share-url, a.ytcp-video-share-dialog").first
                if await final_link.count() > 0:
                    video_url = await final_link.get_attribute("href") or await final_link.inner_text()
            except Exception:
                pass

        print("=======================================================")
        print(" [SUCESSO] Upload e configuracao concluidos!")
        print(f" Titulo: {title}")
        print(f" Video URL: {video_url}")
        print("=======================================================")

        await context.close()
        await p.stop()
        return {"success": True, "title": title, "video_url": video_url}

    except Exception as e:
        print(f"[-] Erro: {e}")
        try:
            await context.close()
            await p.stop()
        except Exception:
            pass
        return {"success": False, "error": str(e)}
