"""
Inspeciona e otimiza o video 4tDqM8ZnSq4 no YouTube Studio
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

async def inspect_and_optimize():
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

    await page.goto("https://studio.youtube.com/video/4tDqM8ZnSq4/edit", wait_until="networkidle")
    await page.wait_for_timeout(3000)

    # Pegar titulo atual
    title_el = page.locator("#title-textarea #textbox, [aria-label*='título'], [aria-label*='title']").first
    current_title = await title_el.inner_text() if await title_el.count() > 0 else "N/A"
    print("Titulo atual:", current_title)

    # Pegar descricao atual
    desc_el = page.locator("#description-textarea #textbox, [aria-label*='descrição'], [aria-label*='description']").first
    current_desc = await desc_el.inner_text() if await desc_el.count() > 0 else "N/A"
    print("Descricao atual (primeiras 100 letras):", current_desc[:100])

    await page.screenshot(path=r"D:\GitHub\youtube-mcp\video_4tDq_inspect.png")
    print("Screenshot salva!")

    await context.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(inspect_and_optimize())
