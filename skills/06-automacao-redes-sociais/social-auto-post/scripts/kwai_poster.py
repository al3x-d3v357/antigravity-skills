# -*- coding: utf-8 -*-
"""
Kwai Auto-Poster & Session Manager
Parte do ecossistema de automação de redes sociais do Alex Sandro (@al3x_d3v357)
Suporta criação de conta, login persistente e upload de vídeos no Kwai.
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

SESSIONS_DIR = Path(os.path.expanduser("~/.social_sessions"))
try:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    SESSIONS_DIR = Path("/media/alex/alex/mcp-servers/social_sessions")
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
SESSION_FILE = SESSIONS_DIR / "session_kwai.json"
HISTORY_FILE = SESSIONS_DIR / "kwai_posts_history.json"

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)

def record_post_history(text: str, video_path: str, success: bool, details: str = ""):
    history = []
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "platform": "Kwai",
        "text": text,
        "video": video_path,
        "success": success,
        "details": details
    }
    history.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def launch_browser(p, headless: bool = False):
    common_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-infobars",
        "--disable-dev-shm-usage"
    ]
    try:
        return p.chromium.launch(
            channel="chrome",
            headless=headless,
            args=common_args
        )
    except Exception:
        return p.chromium.launch(
            headless=headless,
            args=common_args
        )

def interactive_login():
    """Abre o navegador visível para criar conta ou fazer login no Kwai e salva a sessão."""
    print("=" * 72)
    print("  [SOCIAL AUTO-POST] Configuração de Conta & Login - KWAI")
    print("=" * 72)
    print("1. O navegador será aberto na página inicial / login do Kwai.")
    print("2. Crie sua conta nova ou faça login com Google/Celular.")
    print("3. Acesse a Central do Criador (Kwai Creator Center).")
    print("4. Quando já estiver logado e no seu perfil do Kwai,")
    print("   volte aqui neste terminal e pressione ENTER para salvar a sessão.")
    print("=" * 72)

    with sync_playwright() as p:
        browser = launch_browser(p, headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 850},
            locale="pt-BR"
        )
        page = context.new_page()

        log("Navegando para https://studio.kwai.com/...")
        try:
            page.goto("https://studio.kwai.com/", timeout=45000)
        except Exception as e:
            log(f"Aviso de navegação: {e}")

        print("\n>>> Aguardando você criar a conta ou fazer login no Kwai Studio... <<<")
        input(">>> Pressione ENTER AQUI após concluir o login no Kwai Studio... <<<\n")

        context.storage_state(path=str(SESSION_FILE))
        log(f"SUCESSO! Sessão autenticada do Kwai Studio salva em: {SESSION_FILE}")
        browser.close()

def check_status() -> bool:
    """Verifica se existe sessão salva do Kwai e tenta validar."""
    if not SESSION_FILE.exists():
        print("[STATUS] Nenhuma sessão do Kwai salva. Use: python kwai_poster.py --login")
        return False
    print(f"[STATUS] Sessão do Kwai encontrada em: {SESSION_FILE}")
    return True

def post_kwai(text: str, video_path: str, headless: bool = True) -> bool:
    """Publica um vídeo no Kwai com legenda e hashtags (ZERO emojis)."""
    if not SESSION_FILE.exists():
        log("ERRO: Nenhuma sessão encontrada para o Kwai!")
        log("Execute primeiro o comando de criação/login: python kwai_poster.py --login")
        return False

    v_path = Path(video_path).resolve()
    if not v_path.exists():
        log(f"ERRO: Arquivo de vídeo não encontrado: {video_path}")
        return False

    abs_video_path = str(v_path)
    log(f"Iniciando publicação no Kwai... (Headless: {headless})")
    log(f"Legenda: {text[:80]}..." if len(text) > 80 else f"Legenda: {text}")
    log(f"Arquivo de vídeo: {abs_video_path}")

    with sync_playwright() as p:
        browser = launch_browser(p, headless=headless)
        context = browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            locale="pt-BR"
        )
        page = context.new_page()

        try:
            target_url = "https://www.kwai.com/creator"
            log(f"Acessando Central do Criador do Kwai: {target_url}...")
            page.goto(target_url, timeout=60000)
            page.wait_for_timeout(4000)

            if "login" in page.url.lower():
                log("ALERTA: Sessão expirada ou não autenticada no Kwai.")
                record_post_history(text, abs_video_path, False, "Sessão expirada")
                browser.close()
                return False

            # Procura botão de upload / enviar vídeo
            upload_btn = page.locator("button:has-text('Upload'), button:has-text('Enviar'), button:has-text('Publicar'), [aria-label*='upload']").first
            if upload_btn.is_visible(timeout=5000):
                upload_btn.click(force=True)
                page.wait_for_timeout(2000)

            # Input de arquivo
            file_input = page.locator('input[type="file"]').first
            log("Enviando arquivo de vídeo...")
            file_input.set_input_files(abs_video_path)
            page.wait_for_timeout(6000)

            # Preencher descrição / legenda
            caption_box = page.locator('textarea, div[contenteditable="true"], input[placeholder*="legenda"], input[placeholder*="descrição"]').first
            if caption_box.is_visible(timeout=8000):
                log("Preenchendo legenda e hashtags...")
                caption_box.click(force=True)
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                for line in text.split("\n"):
                    page.keyboard.type(line, delay=8)
                    page.keyboard.press("Shift+Enter")
                page.wait_for_timeout(1000)

            # Botão de Publicação final
            pub_btn = page.locator("button:has-text('Publicar'), button:has-text('Post'), button:has-text('Confirmar')").first
            for _ in range(25):
                if not pub_btn.get_attribute("disabled"):
                    log("Vídeo processado e pronto para publicação no Kwai!")
                    break
                page.wait_for_timeout(2000)

            pub_btn.click(force=True)
            page.wait_for_timeout(5000)
            log("SUCESSO: Post publicado no Kwai!")
            record_post_history(text, abs_video_path, True)
            browser.close()
            return True

        except Exception as e:
            err_msg = str(e)
            log(f"FALHA ao publicar no Kwai: {err_msg}")
            screenshot_path = str(SESSIONS_DIR / "kwai_post_error.png")
            try:
                page.screenshot(path=screenshot_path)
            except Exception:
                pass
            record_post_history(text, abs_video_path, False, err_msg)
            browser.close()
            return False

def show_history():
    if not HISTORY_FILE.exists():
        print("Nenhum histórico encontrado para o Kwai.")
        return
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)
    print("\n--- HISTÓRICO DE POSTAGENS NO KWAI ---")
    for p in posts[-5:]:
        status = "SUCESSO" if p.get("success") else "FALHA"
        print(f"[{p.get('timestamp')}] {status}: {p.get('video')} | {p.get('text')[:50]}...")
    print("--------------------------------------\n")

def main():
    parser = argparse.ArgumentParser(description="Kwai Auto-Poster & Account Manager")
    parser.add_argument("--login", action="store_true", help="Abre o navegador para criar conta ou fazer login no Kwai")
    parser.add_argument("--status", action="store_true", help="Verifica status da sessão do Kwai")
    parser.add_argument("--video", type=str, help="Caminho do arquivo de vídeo (.mp4, .mov)")
    parser.add_argument("--post", "--caption", dest="post", type=str, help="Texto da legenda (SEM emojis)")
    parser.add_argument("--hashtags", type=str, default="", help="Hashtags separadas por espaço (ex: #gamedev #b3d)")
    parser.add_argument("--visible", action="store_true", help="Executa com navegador visível")
    parser.add_argument("--history", action="store_true", help="Mostra histórico de postagens no Kwai")

    args = parser.parse_args()

    if args.login:
        interactive_login()
    elif args.status:
        check_status()
    elif args.history:
        show_history()
    elif args.video:
        text = args.post or ""
        if args.hashtags:
            text = f"{text}\n\n{args.hashtags}".strip() if text else args.hashtags.strip()
        post_kwai(text, args.video, headless=not args.visible)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
