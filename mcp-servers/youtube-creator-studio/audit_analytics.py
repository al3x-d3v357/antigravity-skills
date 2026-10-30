# -*- coding: utf-8 -*-
"""
Audita métricas de inscritos, retenção, tráfego e conversão no YouTube Studio Analytics
"""
import os
import asyncio
from pathlib import Path
from browser import get_browser_context

async def audit_analytics():
    p, ctx = await get_browser_context(headless=False)
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    try:
        print("[1] Acessando Analytics do canal...")
        await page.goto("https://studio.youtube.com/channel/UCOaxMsFk9RYlHzkoCQ9c0lw/analytics", wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(4000)
        await page.screenshot(path=r"D:\GitHub\youtube-mcp\analytics_overview.png")
        print("  [+] Salvo analytics_overview.png")

        # Aba Conteúdo (para ver Impressões e CTR)
        content_tab = page.locator("tp-yt-paper-tab:has-text('Conteúdo'), #tabsContent tp-yt-paper-tab:has-text('Content')").first
        if await content_tab.count() > 0:
            await content_tab.click()
            await page.wait_for_timeout(3500)
            await page.screenshot(path=r"D:\GitHub\youtube-mcp\analytics_content_tab.png")
            print("  [+] Salvo analytics_content_tab.png")

        # Aba Público (Audience - para ver novos espectadores, recorrentes e inscritos)
        audience_tab = page.locator("tp-yt-paper-tab:has-text('Público'), #tabsContent tp-yt-paper-tab:has-text('Audience')").first
        if await audience_tab.count() > 0:
            await audience_tab.click()
            await page.wait_for_timeout(3500)
            await page.screenshot(path=r"D:\GitHub\youtube-mcp\analytics_audience_tab.png")
            print("  [+] Salvo analytics_audience_tab.png")

        # Extrair textos de métricas chave
        metrics = await page.evaluate('''() => {
            const cards = Array.from(document.querySelectorAll('ytcp-metric-card, .metric-card, ytcp-table-card')).map(c => c.innerText);
            return cards;
        }''')
        print(f"Metricas extraidas ({len(metrics)} cards)")

    finally:
        await ctx.close()
        await p.stop()

if __name__ == "__main__":
    asyncio.run(audit_analytics())
