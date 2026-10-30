"""
Descobre as tags e botoes do modal que abre ao clicar na tabela
"""
import os
import asyncio
import json
from browser import get_browser_context

async def inspect():
    p, ctx = await get_browser_context(headless=False)
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    await page.goto("https://studio.youtube.com/channel/UCOaxMsFk9RYlHzkoCQ9c0lw/videos/upload", wait_until="networkidle")
    await page.wait_for_timeout(3000)

    row = page.locator("ytcp-video-row:has-text('CRIANDO MEU STREAMING')").first
    await row.click()
    await page.wait_for_timeout(2500)

    data = await page.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('ytcp-button, button')).filter(b => b.innerText && b.innerText.trim().length > 0).map(b => ({
            tag: b.tagName,
            id: b.id,
            text: b.innerText.trim(),
            className: b.className
        }));
        return btns;
    }''')

    with open(r"D:\GitHub\youtube-mcp\draft_modal_buttons.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Salvo draft_modal_buttons.json!")
    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(inspect())
