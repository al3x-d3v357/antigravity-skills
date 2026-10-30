"""
Abre o datepicker trigger e fotografa o menu/calendario
"""
import os
import asyncio
from pathlib import Path
from browser import get_browser_context

async def open_calendar():
    p, ctx = await get_browser_context(headless=False)
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    await page.goto("https://studio.youtube.com/video/dOiI_iUtgu4/edit", wait_until="networkidle")
    await page.wait_for_timeout(3000)

    edit_draft = page.locator("ytcp-button:has-text('Editar rascunho')").first
    if await edit_draft.count() > 0:
        await edit_draft.click()
        await page.wait_for_timeout(2000)

        for _ in range(3):
            next_btn = page.locator("#next-button, ytcp-button#next-button").first
            if await next_btn.count() > 0:
                await next_btn.click()
                await page.wait_for_timeout(1000)

    # Clicar em Programar
    prog_card = page.locator("text='Programar'").first
    await prog_card.click()
    await page.wait_for_timeout(1500)

    # Clicar no datepicker trigger
    trigger = page.locator("#datepicker-trigger, ytcp-text-dropdown-trigger").first
    print("Clicando no trigger de data...")
    await trigger.click()
    await page.wait_for_timeout(1500)

    await page.screenshot(path=r"D:\GitHub\youtube-mcp\calendar_opened.png")
    print("Screenshot calendar_opened.png salva!")

    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(open_calendar())
