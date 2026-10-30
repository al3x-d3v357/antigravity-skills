"""
Completa o rascunho e programa o video no YouTube Studio
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

CHROME_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-default-browser-check",
    "--no-first-run",
]

async def finish_draft(video_id: str, schedule_date: str, schedule_time: str = "13:15"):
    print(f"\n[Finalizando Rascunho] {video_id} -> {schedule_date} as {schedule_time}...")
    p = await async_playwright().start()
    context = await p.chromium.launch_persistent_context(
        user_data_dir=str(USER_DATA_DIR),
        channel="chrome",
        headless=False,
        user_agent=DEFAULT_USER_AGENT,
        args=CHROME_ARGS,
        viewport={"width": 1280, "height": 850},
        locale="pt-BR",
    )
    page = context.pages[0] if context.pages else await context.new_page()

    try:
        await page.goto(f"https://studio.youtube.com/video/{video_id}/edit", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Clicar em "Editar rascunho"
        edit_draft_btn = page.locator("ytcp-button:has-text('Editar rascunho'), button:has-text('Editar rascunho')").first
        if await edit_draft_btn.count() > 0:
            print("  [+] Clicando em 'Editar rascunho'...")
            await edit_draft_btn.click()
            await page.wait_for_timeout(2500)

            # Avancar pelos passos
            for step in range(3):
                next_btn = page.locator("#next-button, ytcp-button#next-button").first
                if await next_btn.count() > 0:
                    await next_btn.click()
                    await page.wait_for_timeout(1500)

            # Agora na aba Visibilidade
            print("  [+] Na tela de Visibilidade, clicando em Programar...")
            # Clicar no radio button de programar
            sched_radio = page.locator("#schedule-radio-button, tp-yt-paper-radio-button[name='SCHEDULE'], tp-yt-paper-radio-button:has-text('Programar')").first
            if await sched_radio.count() > 0:
                await sched_radio.click()
                await page.wait_for_timeout(1500)

                # Seletor de Data
                date_trigger = page.locator("#datepicker-trigger, ytcp-date-picker #picker").first
                if await date_trigger.count() > 0:
                    await date_trigger.click()
                    await page.wait_for_timeout(800)
                    date_input = page.locator("ytcp-date-picker input, tp-yt-paper-dialog input").first
                    if await date_input.count() > 0:
                        await date_input.click()
                        await page.keyboard.press("Control+A")
                        await page.keyboard.type(schedule_date)
                        await page.keyboard.press("Enter")
                        await page.wait_for_timeout(800)
                    await page.keyboard.press("Escape")
                    await page.wait_for_timeout(500)

                # Seletor de Horario
                time_input = page.locator("ytcp-time-picker input").first
                if await time_input.count() > 0:
                    await time_input.click()
                    await page.keyboard.press("Control+A")
                    await page.keyboard.type(schedule_time)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(800)

                # Clicar em Programar / Salvar
                done_btn = page.locator("#done-button, ytcp-button#done-button").first
                if await done_btn.count() > 0:
                    await done_btn.click()
                    print(f"  [+] Botao Programar clicado com sucesso para {video_id}!")
                    await page.wait_for_timeout(5000)
            else:
                print("  [!] Radio Programar nao encontrado no modal.")

        await page.screenshot(path=rf"D:\GitHub\youtube-mcp\final_{video_id}.png")

    finally:
        await context.close()
        await p.stop()

async def main():
    await finish_draft("dOiI_iUtgu4", "11 de nov. de 2026", "13:15")
    await finish_draft("GGOSX0DBMVo", "16 de nov. de 2026", "13:15")

if __name__ == "__main__":
    asyncio.run(main())
