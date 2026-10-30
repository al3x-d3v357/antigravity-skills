"""
Inspeciona os seletores exatos dentro de #schedule-content
"""
import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from browser import get_browser_context

async def inspect_schedule():
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
    expand_prog = page.locator("div.expand-header:has-text('Programar'), #second-container-expanders").first
    await expand_prog.click()
    await page.wait_for_timeout(1500)

    # Inspecionar elementos em #schedule-content
    info = await page.evaluate('''() => {
        const sc = document.querySelector('#schedule-content') || document.querySelector('#second-container');
        if (!sc) return { found: false };
        
        const inputs = Array.from(sc.querySelectorAll('input, ytcp-dropdown-trigger, [role="button"], button')).map(el => ({
            tag: el.tagName,
            id: el.id,
            className: el.className,
            text: el.innerText || el.value || '',
            ariaLabel: el.getAttribute('aria-label') || ''
        }));
        
        const bottomBtns = Array.from(document.querySelectorAll('#dialog ytcp-button, ytcp-uploads-dialog ytcp-button, .button-area ytcp-button')).map(el => ({
            id: el.id,
            text: el.innerText,
            ariaLabel: el.getAttribute('aria-label') || ''
        }));

        return { found: true, inputs, bottomBtns };
    }''')

    print("Schedule Info:", info)
    await ctx.close()
    await p.stop()

asyncio.run(inspect_schedule())
