"""
Publica os dois videos rascunho salvando a visibilidade corretamente
"""
import os
import asyncio
from pathlib import Path
from browser import get_browser_context

async def publish_draft(video_id: str):
    print(f"\n[Processando] Video {video_id}...")
    p, ctx = await get_browser_context(headless=False)
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    try:
        await page.goto(f"https://studio.youtube.com/video/{video_id}/edit", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Clicar em Editar rascunho
        edit_draft = page.locator("ytcp-button:has-text('Editar rascunho')").first
        if await edit_draft.count() > 0:
            print("  [+] Abrindo modal de rascunho...")
            await edit_draft.click()
            await page.wait_for_selector("ytcp-uploads-dialog", timeout=30000)
            await page.wait_for_timeout(2000)

            # Clicar em Avancar ate a aba de Visibilidade
            for step in range(3):
                next_btn = page.locator("ytcp-uploads-dialog #next-button").first
                if await next_btn.count() > 0 and await next_btn.is_visible():
                    await next_btn.click()
                    await page.wait_for_timeout(1500)

            print("  [+] Selecionando Visibilidade Não-Listado...")
            # Clica no radio Não listado
            unlisted = page.locator("ytcp-uploads-dialog tp-yt-paper-radio-button[name='UNLISTED']").first
            if await unlisted.count() > 0:
                await unlisted.click()
                await page.wait_for_timeout(1000)

            # Clica no botao Salvar no rodape do modal
            save_btn = page.locator("ytcp-uploads-dialog #done-button").first
            if await save_btn.count() > 0:
                print("  [+] Clicando no botao Salvar...")
                await save_btn.click()
                await page.wait_for_timeout(6000)

        await page.screenshot(path=rf"D:\GitHub\youtube-mcp\saved_{video_id}.png")
        print(f"  [SUCESSO] Rascunho finalizado para {video_id}!")

    finally:
        await ctx.close()
        await p.stop()

async def main():
    await publish_draft("dOiI_iUtgu4")
    await publish_draft("GGOSX0DBMVo")

if __name__ == "__main__":
    asyncio.run(main())
