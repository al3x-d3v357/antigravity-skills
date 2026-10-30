"""
Expande o card 'Programar', preenche data e horario e clica em Salvar/Programar.
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

async def schedule_video_draft(video_id: str, date_str: str, time_str: str = "13:15"):
    print(f"\n==========================================")
    print(f"Programando {video_id} para {date_str} as {time_str}")
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
        await page.goto(f"https://studio.youtube.com/video/{video_id}/edit", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Clicar em "Editar rascunho" se estiver visivel
        edit_draft_btn = page.locator("ytcp-button:has-text('Editar rascunho')").first
        if await edit_draft_btn.count() > 0:
            print("  [+] Abrindo wizard de rascunho...")
            await edit_draft_btn.click()
            await page.wait_for_timeout(2500)

            # Avancar ate a aba Visibilidade
            for step in range(3):
                next_btn = page.locator("#next-button, ytcp-button#next-button").first
                if await next_btn.count() > 0:
                    await next_btn.click()
                    await page.wait_for_timeout(1500)

        # Agora estamos na tela de Visibilidade!
        # Clicar no card/acordeon 'Programar'
        print("  [+] Clicando no container 'Programar'...")
        # Localiza o container que tem o texto 'Programar' e o icone de expandir
        expand_prog = page.locator("#second-container-expanders, ytcp-video-visibility-select #second-container, div.expand-header:has-text('Programar')").first
        if await expand_prog.count() == 0:
            expand_prog = page.locator("text='Programar'").first

        await expand_prog.click()
        await page.wait_for_timeout(1500)

        # Screenshot para inspecionar os seletores abertos
        await page.screenshot(path=rf"D:\GitHub\youtube-mcp\expanded_{video_id}.png")
        print("  [+] Screenshot do acordeon expandido salva!")

        # Preencher Data
        # Clica no seletor de data
        date_el = page.locator("#datepicker-trigger, ytcp-date-picker #picker, input.style-scope.ytcp-date-picker").first
        if await date_el.count() > 0:
            await date_el.click()
            await page.wait_for_timeout(800)
            date_inp = page.locator("ytcp-date-picker input").first
            if await date_inp.count() > 0:
                await date_inp.click()
                await page.keyboard.press("Control+A")
                await page.keyboard.type(date_str)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(800)
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(500)

        # Preencher Horario
        time_el = page.locator("ytcp-time-picker input").first
        if await time_el.count() > 0:
            await time_el.click()
            await page.keyboard.press("Control+A")
            await page.keyboard.type(time_str)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(800)

        # Clicar no botao Programar (que agora substitui o botao Salvar)
        done_btn = page.locator("#done-button, ytcp-button#done-button, ytcp-button:has-text('Programar')").first
        if await done_btn.count() > 0:
            await done_btn.click()
            print("  [+] Botao Programar clicado!")
            await page.wait_for_timeout(5000)

        await page.screenshot(path=rf"D:\GitHub\youtube-mcp\done_{video_id}.png")
        print(f"  [SUCESSO] Finalizado {video_id}!")

    finally:
        await context.close()
        await p.stop()

async def main():
    # Video 1: 11 de Novembro
    await schedule_video_draft("dOiI_iUtgu4", "11 de nov. de 2026", "13:15")
    # Video 2: 16 de Novembro
    await schedule_video_draft("GGOSX0DBMVo", "16 de nov. de 2026", "13:15")

if __name__ == "__main__":
    asyncio.run(main())
