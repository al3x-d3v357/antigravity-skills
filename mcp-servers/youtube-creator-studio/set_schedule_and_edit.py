"""
Configura agendamento dos dois videos novos e otimiza o video 4tDqM8ZnSq4
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

CHROME_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-default-browser-check",
    "--no-first-run",
]

async def schedule_video_on_edit_page(page, video_id: str, target_date: str, target_time: str = "13:15"):
    print(f"\n[Agendando] Video {video_id} -> {target_date} as {target_time}...")
    await page.goto(f"https://studio.youtube.com/video/{video_id}/edit", wait_until="networkidle")
    await page.wait_for_timeout(3000)

    # Clicar no seletor de Visibilidade na coluna direita
    vis_trigger = page.locator("#visibility-container, [aria-label*='Visibilidade'], #basics-badge-visibility-label").first
    if await vis_trigger.count() == 0:
        vis_trigger = page.locator("tp-yt-paper-radio-group, #privacy-picker").first

    if await vis_trigger.count() > 0:
        await vis_trigger.click()
        await page.wait_for_timeout(1500)

        # Clicar em Programar / Schedule
        schedule_btn = page.locator("#schedule-radio-button, tp-yt-paper-radio-button:has-text('Programar')").first
        if await schedule_btn.count() > 0:
            await schedule_btn.click()
            await page.wait_for_timeout(1500)

            # Preencher data
            date_input = page.locator("#datepicker-trigger, ytcp-date-picker input").first
            if await date_input.count() > 0:
                await date_input.click()
                await page.wait_for_timeout(500)
                # Tenta digitar no input de data
                actual_input = page.locator("ytcp-date-picker input").first
                if await actual_input.count() > 0:
                    await actual_input.click()
                    await page.keyboard.press("Control+A")
                    await page.keyboard.type(target_date)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(500)
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(500)

            # Preencher horario
            time_input = page.locator("ytcp-time-picker input").first
            if await time_input.count() > 0:
                await time_input.click()
                await page.keyboard.press("Control+A")
                await page.keyboard.type(target_time)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(500)

            # Clicar em Concluido no dialog de visibilidade
            done_dialog = page.locator("#dialog-done-button, ytcp-button:has-text('Concluído'), ytcp-button:has-text('Done')").first
            if await done_dialog.count() > 0:
                await done_dialog.click()
                await page.wait_for_timeout(1000)

            # Clicar em Salvar no topo da pagina
            save_btn = page.locator("#save, ytcp-button#save, #save-button").first
            if await save_btn.count() > 0 and await save_btn.is_enabled():
                await save_btn.click()
                await page.wait_for_timeout(4000)
                print(f"[SUCESSO] Video {video_id} agendado para {target_date} as {target_time}!")
            else:
                print(f"[AVISO] Botao salvar desabilitado ou nao encontrado para {video_id}.")
        else:
            print(f"[AVISO] Opcao programar nao encontrada no dialog para {video_id}.")
    
    await page.screenshot(path=rf"D:\GitHub\youtube-mcp\scheduled_{video_id}.png")

async def update_video_4t(page):
    print("\n[Otimizando Video 4tDqM8ZnSq4]...")
    await page.goto("https://studio.youtube.com/video/4tDqM8ZnSq4/edit", wait_until="networkidle")
    await page.wait_for_timeout(3000)

    # Novo titulo com formula de acao + resultado (< 70 caracteres para alto CTR)
    new_title = "CRIE ESPADA 3D NO BLENDER EM 3 MINUTOS • Speed Art & Hard Surface"
    title_box = page.locator("#title-textarea #textbox").first
    if await title_box.count() > 0:
        await title_box.click()
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await title_box.evaluate(''' (el, text) => {
            el.innerText = text;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        } ''', new_title)
        await page.wait_for_timeout(1000)

    save_btn = page.locator("#save, ytcp-button#save, #save-button").first
    if await save_btn.count() > 0 and await save_btn.is_enabled():
        await save_btn.click()
        await page.wait_for_timeout(4000)
        print("[SUCESSO] Video 4tDqM8ZnSq4 atualizado com novo titulo de alto CTR!")
    else:
        print("[INFO] Titulo ja estava no formato ou botao salvar inativo.")

async def main():
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
        # 1. Agendar Video 1 (11 de Novembro)
        await schedule_video_on_edit_page(page, "dOiI_iUtgu4", "11 de nov. de 2026", "13:15")

        # 2. Agendar Video 2 (16 de Novembro)
        await schedule_video_on_edit_page(page, "GGOSX0DBMVo", "16 de nov. de 2026", "13:15")

        # 3. Otimizar video 4tDqM8ZnSq4
        await update_video_4t(page)

    finally:
        await context.close()
        await p.stop()

if __name__ == "__main__":
    asyncio.run(main())
