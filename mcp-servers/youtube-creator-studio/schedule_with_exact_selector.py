"""
Programa os dois rascunhos usando seletores escopados em ytcp-uploads-dialog
"""
import os
import asyncio
from pathlib import Path
from browser import get_browser_context

async def schedule_draft_exact(video_id: str, target_day: str, target_month: str = "nov", target_time: str = "13:15"):
    print(f"\n==========================================")
    print(f"Programando {video_id} para dia {target_day} as {target_time}")
    print(f"==========================================")
    p, ctx = await get_browser_context(headless=False)
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    try:
        await page.goto(f"https://studio.youtube.com/video/{video_id}/edit", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Clicar em Editar rascunho
        edit_draft = page.locator("ytcp-button:has-text('Editar rascunho')").first
        if await edit_draft.count() > 0:
            await edit_draft.click()
            await page.wait_for_timeout(2500)

            # Avancar para a aba Visibilidade (clicando em Avancar ate a aba ficar REVIEW)
            for _ in range(3):
                next_btn = page.locator("ytcp-uploads-dialog #next-button").first
                if await next_btn.count() > 0:
                    await next_btn.click()
                    await page.wait_for_timeout(1200)

        dialog = page.locator("ytcp-uploads-dialog").first

        # Clicar em Programar dentro do dialog
        prog_header = dialog.locator("div.expand-header:has-text('Programar'), #second-container-expanders").first
        await prog_header.click()
        await page.wait_for_timeout(1500)

        # Clicar no dropdown de data dentro de ytcp-video-visibility-select
        date_trigger = dialog.locator("ytcp-video-visibility-select ytcp-dropdown-trigger").first
        await date_trigger.click()
        await page.wait_for_timeout(1000)

        # Screenshot do calendario aberto
        await page.screenshot(path=rf"D:\GitHub\youtube-mcp\calendar_{video_id}.png")
        print(f"Calendar screenshot salva: calendar_{video_id}.png")

        # No calendario que abre (ytcp-date-picker-dialog ou iron-dropdown):
        # Vamos tentar clicar no dia alvo
        # Procurar elemento com o texto do dia
        day_cell = page.locator(f"ytcp-date-picker-dialog tp-yt-paper-dialog span:has-text('{target_day}'), ytcp-date-picker-dialog [aria-label*='{target_day}'], ytcp-date-picker-dialog button:has-text('{target_day}')").first
        if await day_cell.count() > 0:
            await day_cell.click()
            print(f"Dia {target_day} clicado!")
            await page.wait_for_timeout(800)

        # Campo de Horario
        time_input = dialog.locator("ytcp-video-visibility-select ytcp-time-picker input, ytcp-video-visibility-select input[aria-label*='Horário']").first
        if await time_input.count() > 0:
            await time_input.click()
            await page.keyboard.press("Control+A")
            await page.keyboard.type(target_time)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(800)
            print(f"Horario {target_time} definido!")

        # Clicar em Programar
        done_btn = dialog.locator("#done-button, ytcp-button:has-text('Programar')").first
        if await done_btn.count() > 0:
            await done_btn.click()
            print("Botao Programar clicado com sucesso!")
            await page.wait_for_timeout(5000)

        await page.screenshot(path=rf"D:\GitHub\youtube-mcp\scheduled_final_{video_id}.png")
        print(f"Salvo scheduled_final_{video_id}.png")

    finally:
        await ctx.close()
        await p.stop()

async def main():
    await schedule_draft_exact("dOiI_iUtgu4", "11", "nov", "13:15")
    await schedule_draft_exact("GGOSX0DBMVo", "16", "nov", "13:15")

if __name__ == "__main__":
    asyncio.run(main())
