# -*- coding: utf-8 -*-
"""
Script final para definir agendamento dos dois videos no YouTube Studio
"""
import os
import asyncio
from pathlib import Path
from browser import get_browser_context

async def configure_video_schedule(video_id: str, target_day: str, target_time: str = "13:15"):
    print(f"\n==========================================")
    print(f"Configurando video {video_id}...")
    print(f"==========================================")
    p, ctx = await get_browser_context(headless=False)
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    try:
        await page.goto(f"https://studio.youtube.com/video/{video_id}/edit", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Clicar em Editar rascunho
        edit_draft = page.locator("text='Editar rascunho'").first
        if await edit_draft.count() > 0:
            await edit_draft.click()
            await page.wait_for_timeout(2500)

            # Avancar ate Visibilidade usando #next-button
            for _ in range(3):
                nxt = page.locator("#next-button").first
                if await nxt.count() > 0 and await nxt.is_visible():
                    await nxt.click()
                    await page.wait_for_timeout(1200)

        # Agora estamos na tela de Visibilidade
        # Clicar no acordeon Programar
        print("  [+] Clicando em Programar...")
        prog_card = page.locator("text='Programar'").first
        await prog_card.click()
        await page.wait_for_timeout(1500)

        # Clicar no trigger de data (mostra '14 de out' ou similar)
        date_btn = page.locator("#datepicker-trigger, [id*='datepicker'], ytcp-text-dropdown-trigger").first
        if await date_btn.count() > 0:
            print("  [+] Abrindo seletor de data...")
            await date_btn.click()
            await page.wait_for_timeout(1000)
            
            # Clicar no dia no popup/dialog
            # O alvo e o numero do dia (11 ou 16)
            day_target = page.locator(f"tp-yt-paper-dialog span:has-text('{target_day}'), tp-yt-paper-dialog [aria-label*='{target_day}'], [role='dialog'] span:has-text('{target_day}')").first
            if await day_target.count() > 0:
                print(f"  [+] Dia {target_day} selecionado no calendario!")
                await day_target.click()
                await page.wait_for_timeout(500)
            else:
                await page.keyboard.press("Escape")

        # Campo de Horario
        time_field = page.locator("ytcp-uploads-dialog input[aria-label*='Horário'], ytcp-uploads-dialog input[value*='00:00'], ytcp-uploads-dialog ytcp-time-picker input").first
        if await time_field.count() > 0:
            print(f"  [+] Definindo horario: {target_time}...")
            await time_field.click()
            await page.keyboard.press("Control+A")
            await page.keyboard.type(target_time)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(500)

        # Clicar no botao Programar / Salvar (#done-button)
        done_btn = page.locator("#done-button").first
        if await done_btn.count() > 0:
            print("  [+] Clicando no botao Programar (#done-button)...")
            await done_btn.click()
            await page.wait_for_timeout(6000)

        await page.screenshot(path=rf"D:\GitHub\youtube-mcp\result_{video_id}.png")
        print(f"[SUCESSO] Processado {video_id}!")

    finally:
        await ctx.close()
        await p.stop()

async def main():
    # Video 1: 11 de Novembro (Quarta-feira)
    await configure_video_schedule("dOiI_iUtgu4", "11", "13:15")
    # Video 2: 16 de Novembro (Segunda-feira)
    await configure_video_schedule("GGOSX0DBMVo", "16", "13:15")

if __name__ == "__main__":
    asyncio.run(main())
