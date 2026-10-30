# -*- coding: utf-8 -*-
import os
import asyncio
from browser import get_browser_context

async def save_unlisted(video_id: str):
    print(f"\nSalva video {video_id} como Não-listado...")
    p, ctx = await get_browser_context(headless=False)
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    try:
        await page.goto(f"https://studio.youtube.com/video/{video_id}/edit", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Clicar em Editar rascunho
        edit_draft = page.locator("text='Editar rascunho'").first
        if await edit_draft.count() > 0:
            await edit_draft.click()
            await page.wait_for_timeout(2000)

            # Avancar ate Visibilidade usando #next-button
            for _ in range(3):
                nxt = page.locator("#next-button").first
                if await nxt.count() > 0 and await nxt.is_visible():
                    await nxt.click()
                    await page.wait_for_timeout(1200)

        # Clicar no radio Nao listado
        unlisted_btn = page.locator("ytcp-video-visibility-select tp-yt-paper-radio-button[name='UNLISTED'], ytcp-video-visibility-select tp-yt-paper-radio-button:has-text('Não listado')").first
        if await unlisted_btn.count() > 0:
            print("  [+] Clicando em Não listado...")
            await unlisted_btn.click()
            await page.wait_for_timeout(1000)

        # Clicar no botao Salvar (#done-button)
        done_btn = page.locator("ytcp-uploads-dialog #done-button").first
        if await done_btn.count() > 0:
            print("  [+] Clicando no botao Salvar...")
            await done_btn.click()
            await page.wait_for_timeout(5000)

        await page.screenshot(path=rf"D:\GitHub\youtube-mcp\saved_unlisted_{video_id}.png")
        print(f"Salvo saved_unlisted_{video_id}.png!")

    finally:
        await ctx.close()
        await p.stop()

async def main():
    await save_unlisted("dOiI_iUtgu4")
    await save_unlisted("GGOSX0DBMVo")

if __name__ == "__main__":
    asyncio.run(main())
