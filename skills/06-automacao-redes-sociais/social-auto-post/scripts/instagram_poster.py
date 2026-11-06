import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

sys.path.append(str(Path(__file__).resolve().parent))
import trend_analyzer

SESSIONS_DIR = Path(os.path.expanduser("~/.social_sessions"))
try:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    SESSIONS_DIR = Path("/media/alex/alex/mcp-servers/social_sessions")
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

FALLBACK_SESSIONS_DIR = Path("/media/alex/alex/mcp-servers/social_sessions")
SESSION_FILE = SESSIONS_DIR / "session_instagram.json"
HISTORY_FILE = SESSIONS_DIR / "instagram_posts_history.json"


def resolve_session_file() -> Path:
    if SESSION_FILE.exists():
        return SESSION_FILE
    alt_ig = FALLBACK_SESSIONS_DIR / "session_instagram.json"
    if alt_ig.exists():
        return alt_ig
    threads_session = SESSIONS_DIR / "session_threads.json"
    if threads_session.exists():
        return threads_session
    alt_threads = FALLBACK_SESSIONS_DIR / "session_threads.json"
    if alt_threads.exists():
        return alt_threads
    return SESSION_FILE


def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)


def record_post_history(text: str, media_paths: List[str], success: bool, details: str = "", trend_report: Optional[dict] = None):
    history = []
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []

    entry = {
        "timestamp": datetime.now().isoformat(),
        "platform": "Instagram",
        "text": text,
        "media": media_paths,
        "success": success,
        "details": details,
        "recommended_music": (trend_report or {}).get("recommended_music_tracks", []),
        "foreign_benchmarks": (trend_report or {}).get("foreign_pages_analyzed", [])
    }
    history.append(entry)
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def interactive_login():
    """Abre o navegador visível para autenticar na conta do Instagram e salva a sessão."""
    print("=" * 72)
    print("  [SOCIAL AUTO-POST] Configuração de Login - INSTAGRAM")
    print("=" * 72)
    print("1. O navegador será aberto na página de login do Instagram.")
    print("2. Faça o login com sua conta do Instagram (@arthursantos.real / @al3x_d3v357).")
    print("3. Quando já estiver logado e no Feed do Instagram,")
    print("   volte aqui neste terminal e pressione a tecla ENTER para salvar a sessão.")
    print("=" * 72)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 850}
        )
        page = context.new_page()

        log("Navegando para https://www.instagram.com/accounts/login/...")
        page.goto("https://www.instagram.com/accounts/login/")

        print("\n>>> Aguardando você fazer login no navegador aberto... <<<")
        input(">>> Pressione ENTER AQUI após concluir o login e estar no Feed do Instagram... <<<\n")

        context.storage_state(path=str(SESSION_FILE))
        if FALLBACK_SESSIONS_DIR.exists():
            context.storage_state(path=str(FALLBACK_SESSIONS_DIR / "session_instagram.json"))
        log(f"SUCESSO! Credenciais e sessão do Instagram salvas em: {SESSION_FILE}")
        browser.close()


def post_instagram(text: str, media_paths: Optional[List[str]] = None, hashtags: str = "", headless: bool = True, live_trends: bool = False) -> bool:
    """Analisa tendências internacionais antes de publicar um post no Instagram."""
    # 1. Análise Obrigatória de Tendências do Exterior (Tags, Música e Legenda)
    trend_report = trend_analyzer.analyze_and_adapt(
        raw_text=text,
        custom_hashtags=hashtags,
        media_paths=media_paths,
        live=live_trends
    )
    trend_analyzer.print_trend_report(trend_report)

    clean_caption = trend_report["adapted_caption_zero_emojis"]
    final_hashtags = trend_report["recommended_international_hashtags"]
    full_text = f"{clean_caption}\n\n{final_hashtags}".strip()

    active_session = resolve_session_file()
    if not active_session.exists():
        log("ERRO: Nenhuma sessão encontrada para o Instagram!")
        log("Execute primeiro o comando de login: python instagram_poster.py --login")
        return False

    media_paths = media_paths or []
    valid_medias = []
    for m in media_paths:
        p = Path(m)
        if p.exists():
            valid_medias.append(str(p.resolve()))
        else:
            log(f"AVISO: Arquivo de mídia não encontrado: {m}")

    if not valid_medias:
        log("ERRO: O Instagram requer pelo menos uma imagem ou vídeo para publicar!")
        return False

    log(f"Iniciando publicação no Instagram... (Headless: {headless})")
    log(f"Mídias ({len(valid_medias)}): {valid_medias}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        context = browser.new_context(
            storage_state=str(active_session),
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            page.goto("https://www.instagram.com/", timeout=45000)
            page.wait_for_timeout(3000)

            if "accounts/login" in page.url:
                log("ALERTA: Sessão expirada ou redirecionada para tela de login.")
                record_post_history(full_text, valid_medias, False, "Sessao expirada", trend_report)
                browser.close()
                return False

            create_btn = page.locator('svg[aria-label="Nova publicação"], svg[aria-label="New post"], a[href="#"][role="link"]:has-text("Criar"), span:has-text("Criar")').first
            if not create_btn.is_visible(timeout=5000):
                create_btn = page.locator('svg[aria-label="Criar"], svg[aria-label="Create"]').first

            create_btn.click()
            page.wait_for_timeout(2000)

            try:
                page.evaluate('''() => {
                    const spans = Array.from(document.querySelectorAll('span')).filter(el => el.textContent.trim() === 'Post' || el.textContent.trim() === 'Publicação');
                    if (spans.length === 0) return;
                    let target = spans[0];
                    while (target && target.tagName !== 'A' && target.tagName !== 'BUTTON' && !target.getAttribute('role')) {
                        target = target.parentElement;
                    }
                    if (target) { target.click(); }
                    else { spans[0].click(); }
                }''')
                page.wait_for_timeout(2500)
            except Exception as e_menu:
                log(f"Aviso submenu post: {e_menu}")

            file_input = page.locator('input[type="file"]')
            file_input.set_input_files(valid_medias[0])
            page.wait_for_timeout(4000)

            try:
                ok_btn = page.locator('button:has-text("OK"), div[role="button"]:has-text("OK"), button:has-text("Entendi")').first
                if ok_btn.is_visible(timeout=3000):
                    log("Fechando modal de aviso do Reels ('OK')...")
                    ok_btn.click(force=True)
                    page.wait_for_timeout(1000)
            except Exception as ok_err:
                log(f"Aviso popup reels: {ok_err}")

            try:
                crop_btn = page.locator('button:has(svg[aria-label="Selecionar corte"]), button:has(svg[aria-label="Select crop"]), svg[aria-label="Selecionar corte"], svg[aria-label="Select crop"]').first
                if crop_btn.is_visible(timeout=3000):
                    crop_btn.click(force=True)
                    page.wait_for_timeout(600)
                    orig_opt = page.locator('button:has-text("Original"), span:has-text("Original"), div[role="button"]:has-text("Original"), button:has-text("16:9"), span:has-text("16:9")').first
                    if orig_opt.is_visible(timeout=2000):
                        orig_opt.click(force=True)
                        page.wait_for_timeout(600)
            except Exception as crop_err:
                log(f"Aviso ajuste de corte: {crop_err}")

            for step in range(3):
                try:
                    ok_btn = page.locator('button:has-text("OK"), div[role="button"]:has-text("OK")').first
                    if ok_btn.is_visible(timeout=1000):
                        ok_btn.click(force=True)
                        page.wait_for_timeout(500)
                except Exception:
                    pass

                next_btn = page.locator('div[role="button"]:has-text("Avançar"), div[role="button"]:has-text("Next"), button:has-text("Avançar"), button:has-text("Next")').first
                if next_btn.is_visible(timeout=3000):
                    next_btn.click(force=True)
                    page.wait_for_timeout(2500)
                caption_area = page.locator('div[aria-label="Add a caption..."], div[aria-label="Write a caption..."], div[aria-label="Escreva uma legenda..."], div[role="textbox"]').first
                if caption_area.is_visible(timeout=1500):
                    break

            caption_area = page.locator('div[aria-label="Add a caption..."], div[aria-label="Write a caption..."], div[aria-label="Escreva uma legenda..."], div[role="textbox"]').first
            if caption_area.is_visible(timeout=5000):
                caption_area.click(force=True)
                caption_area.fill(full_text)
                page.wait_for_timeout(1000)

            dialog = page.locator('div[role="dialog"]').last
            share_btn = dialog.locator('div[role="button"]:has-text("Compartilhar"), div[role="button"]:has-text("Share"), button:has-text("Compartilhar"), button:has-text("Share")').first
            share_btn.click(force=True)
            log("Botão de compartilhar clicado. Aguardando conclusão do envio...")

            try:
                page.wait_for_selector('text="Your reel has been shared.", text="Your reel has been shared", text="Your post has been shared.", text="Your post has been shared", text="Sua publicação foi compartilhada", text="Seu reel foi compartilhado", svg[aria-label="Animated checkmark"]', timeout=60000)
                log("SUCESSO: Post publicado com sucesso no Instagram!")
                record_post_history(full_text, valid_medias, True, "Publicado com sucesso", trend_report)
                browser.close()
                return True
            except Exception as wait_err:
                if page.locator('div[role="dialog"]:has-text("New reel"), div[role="dialog"]:has-text("Create new post")').count() == 0:
                    log("SUCESSO: Modal de publicação concluído e fechado no Instagram!")
                    record_post_history(full_text, valid_medias, True, "Modal concluído", trend_report)
                    browser.close()
                    return True
                raise wait_err

        except Exception as e:
            err_msg = str(e)
            log(f"FALHA ao publicar no Instagram: {err_msg}")
            screenshot_path = str(SESSIONS_DIR / "instagram_post_error.png")
            try:
                page.screenshot(path=screenshot_path)
            except Exception:
                pass
            record_post_history(full_text, valid_medias, False, err_msg, trend_report)
            browser.close()
            return False


def show_history():
    if not HISTORY_FILE.exists():
        print("Nenhum histórico encontrado para o Instagram.")
        return
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)
    print("\n--- HISTÓRICO DE POSTAGENS NO INSTAGRAM ---")
    for p in posts[-5:]:
        status = "SUCESSO" if p.get("success") else "FALHA"
        print(f"[{p.get('timestamp')}] {status}: {p.get('text')[:60]}...")
    print("-------------------------------------------\n")


def main():
    parser = argparse.ArgumentParser(description="Instagram Auto-Poster com Análise de Tendências do Exterior")
    parser.add_argument("--login", action="store_true", help="Login interativo no Instagram")
    parser.add_argument("--analyze-only", action="store_true", help="Apenas executa a análise de tendências internacionais sem publicar")
    parser.add_argument("--live-trends", action="store_true", help="Consulta as páginas do exterior ao vivo antes de postar")
    parser.add_argument("--post", type=str, help="Texto da legenda")
    parser.add_argument("--hashtags", type=str, default="", help="Hashtags separadas por espaço")
    parser.add_argument("--media", nargs="+", help="Arquivos de imagem ou vídeo")
    parser.add_argument("--visible", action="store_true", help="Executa com navegador visível")
    parser.add_argument("--history", action="store_true", help="Histórico de postagens")

    args = parser.parse_args()

    if args.login:
        interactive_login()
    elif args.history:
        show_history()
    elif args.analyze_only:
        report = trend_analyzer.analyze_and_adapt(args.post or "", args.hashtags, args.media, live=args.live_trends)
        trend_analyzer.print_trend_report(report)
    elif args.post:
        post_instagram(args.post, args.media, hashtags=args.hashtags, headless=not args.visible, live_trends=args.live_trends)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
