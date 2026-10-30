#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Painel do Criador - Central Multi-Plataforma (YouTube, Kwai & TikTok)
Servidor Web Local e API de Automação para o Alex Sandro (@al3x-d3v357)
"""

import os
import sys
import json
import time
import subprocess
import threading
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 7890
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

PYTHON_BLENDER = "/media/alex/alex/softwares/blender-5.2.2-linux-x64/5.2/python/bin/python3.13"
PY_CMD = PYTHON_BLENDER if os.path.exists(PYTHON_BLENDER) else sys.executable

SESSIONS_DIR = Path(os.path.expanduser("~/.social_sessions"))
if not SESSIONS_DIR.exists():
    SESSIONS_DIR = Path("/media/alex/alex/mcp-servers/social_sessions")
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

YOUTUBE_PROFILE = Path(os.path.expanduser("~/.youtube_studio_profile"))

LOG_MESSAGES = []

def add_log(msg: str):
    timestamp = time.strftime("%H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    LOG_MESSAGES.append(formatted)
    if len(LOG_MESSAGES) > 50:
        LOG_MESSAGES.pop(0)
    print(formatted, flush=True)

def check_platforms_status():
    yt_ok = YOUTUBE_PROFILE.exists() and any(YOUTUBE_PROFILE.iterdir())
    kwai_file = SESSIONS_DIR / "session_kwai.json"
    kwai_ok = kwai_file.exists() and kwai_file.stat().st_size > 10
    tiktok_file = SESSIONS_DIR / "session_tiktok.json"
    tiktok_ok = tiktok_file.exists() and tiktok_file.stat().st_size > 10

    return {
        "youtube": {"active": yt_ok, "channel": "@al3x-d3v357", "name": "YouTube Studio"},
        "kwai": {"active": kwai_ok, "channel": "Kwai Creator", "name": "Kwai"},
        "tiktok": {"active": tiktok_ok, "channel": "@al3x_d3v357", "name": "TikTok Studio"}
    }

def run_cmd_async(cmd, name="Processo"):
    def worker():
        add_log(f"Iniciando: {name}...")
        env = os.environ.copy()
        env["WAYLAND_DISPLAY"] = env.get("WAYLAND_DISPLAY", "wayland-0")
        env["XDG_RUNTIME_DIR"] = env.get("XDG_RUNTIME_DIR", "/run/user/1000")
        env["DISPLAY"] = env.get("DISPLAY", ":0")
        try:
            proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in proc.stdout:
                line_str = line.strip()
                if line_str:
                    add_log(f"[{name}] {line_str}")
            proc.wait()
            add_log(f"{name} finalizado com código {proc.returncode}.")
        except Exception as e:
            add_log(f"Erro em {name}: {e}")
    t = threading.Thread(target=worker, daemon=True)
    t.start()

class PainelHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            data = check_platforms_status()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/logs":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"logs": LOG_MESSAGES}, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/" or self.path == "/index.html":
            self.path = "/index.html"
            super().do_GET()
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if self.path == "/api/login/kwai":
            add_log("Disparando navegador visível para criação de conta / login no Kwai...")
            cmd = [PY_CMD, "/home/alex/.gemini/config/skills/social-auto-post/scripts/kwai_poster.py", "--login"]
            run_cmd_async(cmd, "Login Kwai")
            self._send_json({"success": True, "message": "Janela do Kwai aberta na tela."})

        elif self.path == "/api/login/youtube":
            add_log("Disparando navegador visível para login no YouTube Studio...")
            cmd = [PY_CMD, "/media/alex/alex/mcp-servers/youtube-mcp/browser.py", "login"]
            run_cmd_async(cmd, "Login YouTube")
            self._send_json({"success": True, "message": "Janela do YouTube Studio aberta na tela."})

        elif self.path == "/api/login/tiktok":
            add_log("Disparando navegador visível para login no TikTok...")
            cmd = [PY_CMD, "/home/alex/.gemini/config/skills/social-auto-post/scripts/tiktok_poster.py", "--login"]
            run_cmd_async(cmd, "Login TikTok")
            self._send_json({"success": True, "message": "Janela do TikTok aberta na tela."})

        elif self.path == "/api/upload":
            video_path = payload.get("video_path", "").strip()
            title = payload.get("title", "").strip()
            caption = payload.get("caption", "").strip()
            hashtags = payload.get("hashtags", "").strip()
            platforms = payload.get("platforms", [])

            if not video_path or not os.path.exists(video_path):
                self._send_json({"success": False, "error": f"Arquivo de vídeo não encontrado: {video_path}"}, status=400)
                return

            add_log(f"Solicitação de upload recebida para: {', '.join(platforms)}")

            # 1. Kwai
            if "kwai" in platforms:
                cmd_kwai = [
                    PY_CMD, "/home/alex/.gemini/config/skills/social-auto-post/scripts/kwai_poster.py",
                    "--video", video_path,
                    "--post", caption or title,
                    "--hashtags", hashtags
                ]
                run_cmd_async(cmd_kwai, "Upload Kwai")

            # 2. TikTok
            if "tiktok" in platforms:
                cmd_tt = [
                    PY_CMD, "/home/alex/.gemini/config/skills/social-auto-post/scripts/tiktok_poster.py",
                    "--video", video_path,
                    "--post", caption or title,
                    "--hashtags", hashtags
                ]
                run_cmd_async(cmd_tt, "Upload TikTok")

            # 3. YouTube
            if "youtube" in platforms:
                cmd_yt = [
                    PY_CMD, "/media/alex/alex/mcp-servers/youtube-mcp/browser.py", "upload",
                    video_path, "", title or caption, "unlisted"
                ]
                run_cmd_async(cmd_yt, "Upload YouTube")

            self._send_json({"success": True, "message": "Uploads enfileirados com sucesso!"})

        else:
            self._send_json({"error": "Endpoint não encontrado"}, status=404)

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

def main():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, PainelHandler)
    add_log(f"Painel do Criador rodando em http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")

if __name__ == "__main__":
    main()
