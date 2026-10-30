#!/usr/bin/env bash
# ==============================================================================
# Central do Criador (Linux) - YouTube, Kwai & TikTok
# Criado para Alex Sandro (@al3x-d3v357)
# ==============================================================================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BLENDER="/media/alex/alex/softwares/blender-5.2.2-linux-x64/5.2/python/bin/python3.13"

if [ -f "$PYTHON_BLENDER" ]; then
    PY_CMD="$PYTHON_BLENDER"
elif command -v python3 &>/dev/null; then
    PY_CMD="python3"
else
    echo "[ERRO] Python não encontrado."
    exit 1
fi

export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-0}"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/1000}"
export DISPLAY="${DISPLAY:-:0}"

SESSIONS_DIR="$HOME/.social_sessions"
[ -d "$SESSIONS_DIR" ] || SESSIONS_DIR="/media/alex/alex/mcp-servers/social_sessions"
mkdir -p "$SESSIONS_DIR"

clear
echo "================================================================="
echo "  🎬 CENTRAL DO CRIADOR - YOUTUBE • KWAI • TIKTOK"
echo "  Canal Oficial: Alex Sandro (@al3x-d3v357)"
echo "================================================================="
echo " Utilizando Python: $PY_CMD"
echo ""

# Status das sessões
check_status() {
    echo "--- STATUS DAS CONTAS CONECTADAS ---"
    if [ -d "$HOME/.youtube_studio_profile" ]; then
        echo " [YouTube Studio]  ● CONECTADO (@al3x-d3v357)"
    else
        echo " [YouTube Studio]  ○ NÃO CONECTADO"
    fi

    if [ -s "$SESSIONS_DIR/session_kwai.json" ]; then
        echo " [Kwai Creator]    ● CONECTADO"
    else
        echo " [Kwai Creator]    ○ NÃO CONECTADO (Criar conta ou logar)"
    fi

    if [ -s "$SESSIONS_DIR/session_tiktok.json" ]; then
        echo " [TikTok Studio]   ● CONECTADO (@al3x_d3v357)"
    else
        echo " [TikTok Studio]   ○ NÃO CONECTADO"
    fi
    echo "------------------------------------"
}

check_status

echo ""
echo " Escolha uma ação:"
echo " ---------------------------------------------------------------"
echo " [1] CRIAR CONTA / FAZER LOGIN NO KWAI (Abre navegador na tela)"
echo " [2] CONECTAR CANAL DO YOUTUBE STUDIO (Salvar sessão permanente)"
echo " [3] CONECTAR CONTA DO TIKTOK STUDIO (Salvar sessão permanente)"
echo " ---------------------------------------------------------------"
echo " [4] SUBIR VÍDEO NO KWAI (Com legenda e hashtags)"
echo " [5] SUBIR VÍDEO NO YOUTUBE STUDIO (Com thumbnail oficial)"
echo " [6] SUBIR VÍDEO NO TIKTOK (Com legenda e hashtags)"
echo " [7] MULTI-UPLOAD: Subir nos 3 de uma vez (YouTube + Kwai + TikTok)"
echo " ---------------------------------------------------------------"
echo " [w] ABRIR PAINEL VISUAL WEB NO NAVEGADOR (Dashboard Local)"
echo " [0] Sair"
echo "================================================================="
read -p "Digite a opção desejada: " opt

case "$opt" in
    1)
        echo ""
        echo ">>> Abrindo navegador para CRIAR CONTA ou fazer LOGIN no Kwai..."
        "$PY_CMD" /home/alex/.gemini/config/skills/social-auto-post/scripts/kwai_poster.py --login
        ;;
    2)
        echo ""
        echo ">>> Abrindo navegador para autenticação do YouTube Studio..."
        cd "$DIR" && "$PY_CMD" browser.py login
        ;;
    3)
        echo ""
        echo ">>> Abrindo navegador para autenticação do TikTok..."
        "$PY_CMD" /home/alex/.gemini/config/skills/social-auto-post/scripts/tiktok_poster.py --login
        ;;
    4)
        echo ""
        read -p "Caminho do vídeo (.mp4): " vpath
        read -p "Legenda (sem emojis): " vcaption
        read -p "Hashtags (#gamedev #b3d #linux): " vhash
        vhash=${vhash:-"#gamedev #b3d #linux"}
        "$PY_CMD" /home/alex/.gemini/config/skills/social-auto-post/scripts/kwai_poster.py --video "$vpath" --post "$vcaption" --hashtags "$vhash"
        ;;
    5)
        echo ""
        read -p "Caminho do vídeo (.mp4): " vpath
        read -p "Título do vídeo: " vtitle
        read -p "Caminho da thumbnail (.png) [opcional]: " vthumb
        read -p "Visibilidade (unlisted/public/private) [unlisted]: " vvis
        vvis=${vvis:-unlisted}
        cd "$DIR" && "$PY_CMD" browser.py upload "$vpath" "$vthumb" "$vtitle" "$vvis"
        ;;
    6)
        echo ""
        read -p "Caminho do vídeo (.mp4): " vpath
        read -p "Legenda (sem emojis): " vcaption
        read -p "Hashtags (#gamedev #b3d #linux): " vhash
        vhash=${vhash:-"#gamedev #b3d #linux"}
        "$PY_CMD" /home/alex/.gemini/config/skills/social-auto-post/scripts/tiktok_poster.py --video "$vpath" --post "$vcaption" --hashtags "$vhash"
        ;;
    7)
        echo ""
        read -p "Caminho do vídeo (.mp4): " vpath
        read -p "Título / Legenda: " vtext
        read -p "Caminho da thumbnail do YouTube (.png) [opcional]: " vthumb
        read -p "Hashtags (#gamedev #b3d #linux): " vhash
        vhash=${vhash:-"#gamedev #b3d #linux"}

        echo ""
        echo ">>> [1/3] Enviando para YouTube Studio..."
        cd "$DIR" && "$PY_CMD" browser.py upload "$vpath" "$vthumb" "$vtext" "unlisted"

        echo ""
        echo ">>> [2/3] Enviando para Kwai..."
        "$PY_CMD" /home/alex/.gemini/config/skills/social-auto-post/scripts/kwai_poster.py --video "$vpath" --post "$vtext" --hashtags "$vhash"

        echo ""
        echo ">>> [3/3] Enviando para TikTok..."
        "$PY_CMD" /home/alex/.gemini/config/skills/social-auto-post/scripts/tiktok_poster.py --video "$vpath" --post "$vtext" --hashtags "$vhash"

        echo ">>> MULTI-UPLOAD CONCLUÍDO!"
        ;;
    w|W)
        echo ""
        echo ">>> Iniciando Servidor do Painel do Criador em http://localhost:7890..."
        cd "$DIR/painel_web" && "$PY_CMD" app.py &
        sleep 2
        google-chrome "http://localhost:7890" >/dev/null 2>&1 &
        echo "[SUCESSO] Painel aberto no Google Chrome!"
        ;;
    *)
        echo "Saindo."
        exit 0
        ;;
esac
