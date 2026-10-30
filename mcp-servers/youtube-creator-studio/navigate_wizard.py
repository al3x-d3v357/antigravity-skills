"""
Abre o wizard pela tabela e navega ate Visibilidade
"""
import os
import asyncio
from pathlib import Path
from browser import get_browser_context

async def test_wizard():
    p, ctx = await get_browser_context(headless=False)
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    await page.goto("https://studio.youtube.com/channel/UCOaxMsFk9RYlHzkoCQ9c0lw/videos/upload", wait_until="networkidle")
    await page.wait_for_timeout(3000)

    # Clicar na linha do Yakisoba
    row = page.locator("ytcp-video-row:has-text('CRIANDO MEU STREAMING')").first
    await row.click()
    await page.wait_for_timeout(2000)

    # Clicar em Avancar 3 vezes
    for i in range(3):
        avancar = page.locator("ytcp-button:has-text('Avançar')").first
        await avancar.click()
        await page.wait_for_timeout(1500)

    await page.screenshot(path=r"D:\GitHub\youtube-mcp\step_visibilidade.png")
    print("Screenshot step_visibilidade.png salva!")

    # Clicar em Programar
    prog = page.locator("text='Programar'").first
    await prog.click()
    await page.wait_for_timeout(1500)

    await page.screenshot(path=r"D:\GitHub\youtube-mcp\step_programar_opened.png")
    print("Screenshot step_programar_opened.png salva!")

    # Inspecionar os elementos visiveis dentro do modal
    elements = await page.evaluate('''() => {
        const dialog = document.querySelector('ytcp-uploads-dialog') || document.querySelector('ytcp-dialog');
        const clickable = Array.from(dialog.querySelectorAll('button, input, [role="button"], ytcp-dropdown-trigger, tp-yt-paper-radio-button')).map(el => ({
            tag: el.tagName,
            id: el.id,
            text: el.innerText || el.value || '',
            ariaLabel: el.getAttribute('aria-label') || ''
        }));
        return clickable;
    }''')
    print("Clickable elements:", elements)

    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(test_wizard())
