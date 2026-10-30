"""
Lista e fotografa os videos do canal no YouTube Studio
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

async def check_channel():
    p = await async_playwright().start()
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(USER_DATA_DIR),
        channel="chrome",
        headless=False,
        user_agent=DEFAULT_USER_AGENT,
        viewport={"width": 1280, "height": 850},
        locale="pt-BR",
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()
    await page.goto("https://studio.youtube.com/channel/UCOaxMsFk9RYlHzkoCQ9c0lw/videos/upload", wait_until="networkidle")
    await page.wait_for_timeout(3000)
    await page.screenshot(path=r"D:\GitHub\youtube-mcp\current_content.png")
    print("Screenshot current_content.png salva!")
    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(check_channel())
