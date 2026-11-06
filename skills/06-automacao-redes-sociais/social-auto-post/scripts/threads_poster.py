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
SESSION_FILE = SESSIONS_DIR / "session_threads.json"
HISTORY_FILE = SESSIONS_DIR / "threads_posts_history.json"


def resolve_session_file() -> Path:
    if SESSION_FILE.exists():
        return SESSION_FILE
    alt_threads = FALLBACK_SESSIONS_DIR / "session_threads.json"
    if alt_threads.exists():
        return alt_threads
    ig_home = SESSIONS_DIR / "session_instagram.json"
    if ig_home.exists():
        return ig_home
    alt_ig = FALLBACK_SESSIONS_DIR / "session_instagram.json"
    if alt_ig.exists():
        return alt_ig
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
        "platform": "Threads (Meta / Instagram)",
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


def auto_sso_login_if_needed(page, context) -> bool:
    """Realiza login SSO de 1 clique no Threads usando a sessão conectada do Instagram."""
    body_text = page.locator("body").inner_text()
    if "login" in page.url.lower() or "Log in or join" in body_text or "Continue with Instagram" in body_text:
        log("Detectada tela de login no Threads. Acionando SSO automático via conta Instagram conectada...")
        if "login" not in page.url.lower():
            page.goto("https://www.threads.com/login", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3500)

        sso_selectors = [
            'div[role="button"]:has-text("arthursantos.real")',
            'span:has-text("arthursantos.real")',
            'div[role="button"]:has-text("al3x_d3v357")',
            'div[role="button"]:has-text("Continue with Instagram")',
            'div[role="button"]:has-text("Continuar com o Instagram")',
            'button:has-text("Continue with Instagram")',
            'button:has-text("Continuar com o Instagram")'
        ]
        for sel in sso_selectors:
            loc = page.locator(sel).first
            if loc.is_visible(timeout=1500):
                log(f"Autenticando com 1 clique via SSO: {sel}")
                loc.click(force=True)
                page.wait_for_timeout(7000)
                break

        try:
            context.storage_state(path=str(SESSION_FILE))
            if FALLBACK_SESSIONS_DIR.exists():
                context.storage_state(path=str(FALLBACK_SESSIONS_DIR / "session_threads.json"))
        except Exception:
            pass
    return "login" not in page.url.lower()


def interactive_login():
    """Autentica no Threads (tenta SSO automático primeiro com a sessão do Instagram ou abre navegador)."""
    active_sess = resolve_session_file()
    if active_sess.exists():
        log(f"Verificando login SSO automático no Threads a partir de: {active_sess}")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                channel="chrome",
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            context = browser.new_context(
                storage_state=str(active_sess),
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 850}
            )
            page = context.new_page()
            page.goto("https://www.threads.com/login", wait_until="domcontentloaded", timeout=35000)
            page.wait_for_timeout(3500)
            if auto_sso_login_if_needed(page, context):
                log(f"SUCESSO! Conta do Threads autenticada e salva em: {SESSION_FILE}")
                browser.close()
                return
            browser.close()

    print("=" * 72)
    print("  [SOCIAL AUTO-POST] Configuração de Login - THREADS (Instagram)")
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
        log("Navegando para https://www.threads.com/login...")
        page.goto("https://www.threads.com/login")
        input(">>> Pressione ENTER AQUI após concluir o login e estar no Feed do Threads... <<<\n")
        context.storage_state(path=str(SESSION_FILE))
        log(f"SUCESSO! Credenciais e sessão do Threads salvas em: {SESSION_FILE}")
        browser.close()


def post_thread(text: str, hashtags: str = "", media_paths: Optional[List[str]] = None, headless: bool = True, live_trends: bool = False) -> bool:
    """Analisa tendências internacionais antes de publicar um post no Threads."""
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
        log("ERRO: Nenhuma sessão encontrada para o Threads!")
        log("Execute primeiro o comando de login: python threads_poster.py --login")
        return False

    media_paths = media_paths or []
    valid_medias = []
    for m in media_paths:
        p = Path(m)
        if p.exists():
            valid_medias.append(str(p.resolve()))
        else:
            log(f"AVISO: Arquivo de mídia não encontrado: {m}")

    log(f"Iniciando publicação no Threads... (Headless: {headless})")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=headless,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        context = browser.new_context(
            storage_state=str(active_session),
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 850}
        )
        page = context.new_page()

        try:
            log("Acessando https://www.threads.com...")
            page.goto("https://www.threads.com/", wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(3500)

            if not auto_sso_login_if_needed(page, context):
                log("ERRO: A sessão expirou no Threads. Execute 'python threads_poster.py --login'.")
                record_post_history(full_text, valid_medias, False, "Sessão expirada", trend_report)
                browser.close()
                return False

            create_btn = None
            selectors = [
                '[aria-label="New thread"]',
                '[aria-label="Nova thread"]',
                'svg[aria-label="New thread"]',
                'svg[aria-label="Nova thread"]',
                'svg[aria-label="Criar"]',
                'svg[aria-label="Create"]',
                '[aria-label="Criar"]',
                '[aria-label="Create"]',
                'span:has-text("What\'s new?")',
                'span:has-text("Quais são as novidades?")',
                'div[role="button"]:has-text("Iniciar uma thread")',
                'div[role="button"]:has-text("Start a thread")',
            ]
            for sel in selectors:
                loc = page.locator(sel).first
                if loc.is_visible(timeout=1000):
                    create_btn = loc
                    break

            if create_btn:
                log("Abrindo formulário de criação de thread...")
                create_btn.click(force=True)
                page.wait_for_timeout(1500)

            editors = page.locator('div[contenteditable="true"]').all()
            if not editors:
                log("ERRO: Não foi possível localizar a caixa de texto do Threads.")
                record_post_history(full_text, valid_medias, False, "Editor não encontrado", trend_report)
                browser.close()
                return False

            active_editor = editors[-1]
            log("Inserindo legenda adaptada (ZERO emojis) e hashtags internacionais...")
            active_editor.click()
            page.wait_for_timeout(300)
            page.keyboard.insert_text(full_text)
            page.wait_for_timeout(1000)

            if valid_medias:
                log(f"Fazendo upload de {len(valid_medias)} arquivo(s) de mídia...")
                file_inputs = page.locator('input[type="file"]').all()
                if not file_inputs:
                    attach_icon = page.locator('svg[aria-label="Anexar mídia"], svg[aria-label="Attach media"], [aria-label="Anexar mídia"], [aria-label="Attach media"]').first
                    if attach_icon.is_visible():
                        attach_icon.click()
                        page.wait_for_timeout(500)
                    file_inputs = page.locator('input[type="file"]').all()

                if file_inputs:
                    file_inputs[-1].set_input_files(valid_medias)
                    log("Aguardando upload e renderização da mídia pelo Threads...")
                    page.wait_for_timeout(4000)

            is_video = any(m.lower().endswith(('.mp4', '.mov', '.webm', '.mkv')) for m in valid_medias)
            wait_sec = 60 if is_video else 20
            log("Aguardando liberação do botão Postar do popup...")

            for _ in range(wait_sec):
                btn_state = page.evaluate("""() => {
                    const btns = Array.from(document.querySelectorAll('div[role="button"], button')).filter(e => {
                        const t = (e.innerText || '').trim();
                        return (t === 'Post' || t === 'Postar');
                    });
                    if (btns.length === 0) return null;
                    const target = btns[btns.length - 1];
                    return {
                        disabled: target.getAttribute('aria-disabled'),
                        y: target.getBoundingClientRect().y
                    };
                }""")
                if btn_state and btn_state.get("disabled") != "true" and btn_state.get("y", 0) > 150:
                    break
                page.wait_for_timeout(1000)

            log("Enviando post para o Threads...")
            clicked = page.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('div[role="button"], button')).filter(e => {
                    const t = (e.innerText || '').trim();
                    return (t === 'Post' || t === 'Postar');
                });
                if (btns.length > 0) {
                    btns[btns.length - 1].click();
                    return true;
                }
                return false;
            }""")

            if not clicked:
                log("ERRO: Não foi possível clicar no botão Postar do popup!")
                record_post_history(full_text, valid_medias, False, "Botão Postar não clicado", trend_report)
                browser.close()
                return False

            log("Aguardando processamento e confirmação dos servidores da Meta...")
            for sec in range(90):
                page.wait_for_timeout(1000)
                status = page.evaluate("""() => {
                    const body = document.body.innerText;
                    const hasPosting = body.includes('Posting...') || body.includes('Publicando...');
                    const hasPosted = body.includes('Posted') || body.includes('Publicado') || body.includes('View');
                    return { posting: hasPosting, posted: hasPosted };
                }""")
                if status.get("posted"):
                    log("Confirmação recebida: 'Posted'!")
                    break
                if not status.get("posting") and sec > 8:
                    break

            page.wait_for_timeout(3000)
            log("SUCESSO: Post publicado com êxito no Threads!")
            record_post_history(full_text, valid_medias, True, "Publicado com sucesso no Threads", trend_report)

            context.storage_state(path=str(SESSION_FILE))
            browser.close()
            return True

        except Exception as e:
            log(f"ERRO durante a publicação no Threads: {str(e)}")
            record_post_history(full_text, valid_medias, False, str(e), trend_report)
            try:
                page.screenshot(path=str(SESSIONS_DIR / "threads_post_error.png"))
            except Exception:
                pass
            browser.close()
            return False


def show_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            hist = json.load(f)
        print(f"\n--- HISTÓRICO DE POSTAGENS THREADS ({len(hist)}) ---")
        for h in hist[-5:]:
            print(f"[{h['timestamp']}] Sucesso: {h['success']} | Mídia: {len(h.get('media', []))} arquivos")
            print(f"Texto: {h['text'][:100]}...\n")
    else:
        print("Nenhum histórico encontrado para o Threads.")


def main():
    parser = argparse.ArgumentParser(description="Social Auto-Post - Automação de Postagens no THREADS com Análise Internacional")
    parser.add_argument("--login", action="store_true", help="Autentica e salva sua conta do Threads (SSO com Instagram)")
    parser.add_argument("--analyze-only", action="store_true", help="Apenas executa a análise de tendências internacionais sem publicar")
    parser.add_argument("--live-trends", action="store_true", help="Consulta as páginas do exterior ao vivo antes de postar")
    parser.add_argument("--post", type=str, help="Texto ou legenda da postagem")
    parser.add_argument("--hashtags", type=str, default="", help="Hashtags adicionais separadas por espaço")
    parser.add_argument("--media", nargs="+", help="Caminhos de imagens ou vídeos para anexar ao post")
    parser.add_argument("--visible", action="store_true", help="Roda o navegador visível para acompanhar")
    parser.add_argument("--history", action="store_true", help="Exibe o histórico de postagens realizadas no Threads")

    args = parser.parse_args()

    if args.login:
        interactive_login()
        return

    if args.history:
        show_history()
        return

    if args.analyze_only:
        report = trend_analyzer.analyze_and_adapt(args.post or "", args.hashtags, args.media, live=args.live_trends)
        trend_analyzer.print_trend_report(report)
        return

    if args.post:
        success = post_thread(
            text=args.post,
            hashtags=args.hashtags,
            media_paths=args.media,
            headless=not args.visible,
            live_trends=args.live_trends
        )
        if success:
            print("\n[OK] Publicação realizada com sucesso no Threads!")
        else:
            print("\n[FALHA] Não foi possível publicar no Threads. Verifique o log acima.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
