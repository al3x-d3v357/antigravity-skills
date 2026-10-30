"""
Clica no rascunho diretamente na tabela de conteudo
"""
import os
import asyncio
from pathlib import Path
from browser import get_browser_context

async def click_draft_in_table():
    p, ctx = await get_browser_context(headless=False)
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    await page.goto("https://studio.youtube.com/channel/UCOaxMsFk9RYlHzkoCQ9c0lw/videos/upload", wait_until="networkidle")
    await page.wait_for_timeout(3000)

    # Localizar a linha com o texto do video
    draft_link = page.locator("ytcp-video-row:has-text('CRIANDO MEU STREAMING') #video-title, ytcp-video-row:has-text('CRIANDO MEU STREAMING') a").first
    print("Clicando no draft na tabela...")
    await draft_link.click()
    await page.wait_for_timeout(3000)

    await page.screenshot(path=r"D:\GitHub\youtube-mcp\clicked_draft_table.png")
    print("Screenshot salva: clicked_draft_table.png")

    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(click_draft_in_table())
