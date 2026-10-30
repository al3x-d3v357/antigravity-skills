"""
Abre o wizard, avanca com #next-button e clica em #datepicker-trigger dentro de ytcp-uploads-dialog
"""
import os
import asyncio
from browser import get_browser_context

async def main():
    p, ctx = await get_browser_context(headless=False)
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    await page.goto("https://studio.youtube.com/channel/UCOaxMsFk9RYlHzkoCQ9c0lw/videos/upload", wait_until="networkidle")
    await page.wait_for_timeout(3000)

    # Clicar na linha do Yakisoba
    row = page.locator("ytcp-video-row:has-text('CRIANDO MEU STREAMING')").first
    await row.click()
    await page.wait_for_timeout(2000)

    dialog = page.locator("ytcp-uploads-dialog").first

    # Clicar em #next-button 3 vezes
    for i in range(3):
        btn = dialog.locator("#next-button").first
        await btn.click()
        await page.wait_for_timeout(1200)

    # Clicar em Programar
    prog = dialog.locator("text='Programar'").first
    await prog.click()
    await page.wait_for_timeout(1200)

    # Clicar no #datepicker-trigger dentro do dialog
    date_trig = dialog.locator("#datepicker-trigger").first
    await date_trig.click()
    await page.wait_for_timeout(1500)

    await page.screenshot(path=r"D:\GitHub\youtube-mcp\calendar_opened_success.png")
    print("Screenshot calendar_opened_success.png salva!")

    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(main())
