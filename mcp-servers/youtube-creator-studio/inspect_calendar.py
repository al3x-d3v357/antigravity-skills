"""
Inspeciona e seleciona exatamente a data no dropdown do YouTube Studio
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

async def select_schedule(video_id: str, day_str: str, month_str: str = "nov", time_str: str = "13:15"):
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

        # Editar rascunho
        edit_draft = page.locator("ytcp-button:has-text('Editar rascunho')").first
        if await edit_draft.count() > 0:
            await edit_draft.click()
            await page.wait_for_timeout(2500)
            for step in range(3):
                next_btn = page.locator("#next-button, ytcp-button#next-button").first
                if await next_btn.count() > 0:
                    await next_btn.click()
                    await page.wait_for_timeout(1500)

        # Expandir Programar
        expand_prog = page.locator("div.expand-header:has-text('Programar'), #second-container-expanders").first
        await expand_prog.click()
        await page.wait_for_timeout(1500)

        # Clicar no dropdown de data
        # No screenshot vimos um botao com chevron mostrando '14 de out. de...'
        date_btn = page.locator("#datepicker-trigger, ytcp-dropdown-trigger, [aria-label*='data'], [aria-label*='Data']").first
        await date_btn.click()
        await page.wait_for_timeout(1000)

        await page.screenshot(path=rf"D:\GitHub\youtube-mcp\calendar_{video_id}.png")
        print("Calendar screenshot salva!")

        # No calendario, pesquisar por texto com a data ou dia
        # Ex: "11" de novembro
        # Vamos ver o screenshot
    finally:
        await context.close()
        await p.stop()

if __name__ == "__main__":
    asyncio.run(select_schedule("dOiI_iUtgu4", "11", "nov", "13:15"))
