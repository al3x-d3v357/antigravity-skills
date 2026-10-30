"""
Extrai todos os videos da tabela de conteudo do YouTube Studio
"""
import os
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

USER_DATA_DIR = Path(os.path.expanduser("~/.youtube_studio_profile"))

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

async def dump_videos():
    p = await async_playwright().start()
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(USER_DATA_DIR),
        channel="chrome",
        headless=True,
        user_agent=DEFAULT_USER_AGENT,
        viewport={"width": 1280, "height": 850},
        locale="pt-BR",
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()
    await page.goto("https://studio.youtube.com/channel/UCOaxMsFk9RYlHzkoCQ9c0lw/videos/upload", wait_until="networkidle")
    await page.wait_for_timeout(3000)

    rows = page.locator("ytcp-video-row")
    count = await rows.count()
    print(f"Total rows encontradas: {count}")

    results = []
    for i in range(count):
        row = rows.nth(i)
        title = await row.locator("#video-title").inner_text() if await row.locator("#video-title").count() > 0 else ""
        vis = await row.locator("div.cell-body.tablecell-visibility").inner_text() if await row.locator("div.cell-body.tablecell-visibility").count() > 0 else ""
        date = await row.locator("div.cell-body.tablecell-date").inner_text() if await row.locator("div.cell-body.tablecell-date").count() > 0 else ""
        link_el = row.locator("a#video-title").first
        href = await link_el.get_attribute("href") if await link_el.count() > 0 else ""
        results.append({"title": title.strip(), "vis": vis.strip(), "date": date.strip(), "href": href})

    with open(r"D:\GitHub\youtube-mcp\all_channel_videos.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Salvo em D:\\GitHub\\youtube-mcp\\all_channel_videos.json")
    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(dump_videos())
