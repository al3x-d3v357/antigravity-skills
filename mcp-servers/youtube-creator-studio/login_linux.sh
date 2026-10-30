#!/usr/bin/env bash
# ==============================================================================
# YouTube Studio & Redes Sociais - Central de Conexão e Autenticação (Linux)
# ==============================================================================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BLENDER="/media/alex/alex/softwares/blender-5.2.2-linux-x64/5.2/python/bin/python3.13"

if [ -f "$PYTHON_BLENDER" ]; then
    PY_CMD="$PYTHON_BLENDER"
elif command -v python3 &>/dev/null; then
    PY_CMD="python3"
else
    echo "[ERRO] Python não encontrado no sistema."
    exit 1
fi

check_playwright() {
    "$PY_CMD" -c "import playwright" &>/dev/null
    return $?
}

install_playwright() {
    echo "================================================================="
    echo ">>> Instalando Playwright e Chromium no Python..."
    echo "================================================================="
    "$PY_CMD" -m pip install playwright
    "$PY_CMD" -m playwright install chromium
    "$PY_CMD" -m playwright install-deps 2>/dev/null || true
    echo ""
    echo "[SUCESSO] Instalação concluída!"
    read -p "Pressione ENTER para continuar..."
}

echo "================================================================="
echo "  🎬 YOUTUBE STUDIO & REDES SOCIAIS - GERENCIADOR DE LOGIN"
echo "================================================================="
echo " Utilizando Python: $PY_CMD"

if check_playwright; then
    echo " Status do Playwright: [OK] Instalado"
else
    echo " Status do Playwright: [NÃO INSTALADO] - Escolha a opção [i] primeiro"
fi

echo ""
echo " Escolha uma opção:"
echo " [i] INSTALAR DEPENDÊNCIAS (Playwright + Chromium)"
echo " [1] Fazer Login no YouTube Studio (Salvar sessão permanente)"
echo " [2] Verificar se a sessão do YouTube Studio está ativa"
echo " [3] Conectar no Threads (Meta / Instagram)"
echo " [4] Conectar no Instagram Web"
echo " [5] Fazer Upload de um Vídeo no YouTube Studio via Script"
echo " [w] Abrir YouTube Studio agora no Firefox (Upload manual imediato)"
echo " [0] Sair"
echo "================================================================="
read -p "Digite a opção desejada: " opt

case "$opt" in
    i|I)
        install_playwright
        exec "$0"
        ;;
    1)
        if ! check_playwright; then
            echo ""
            echo "[AVISO] O pacote 'playwright' ainda não está instalado!"
            read -p "Deseja instalar agora automaticamente? (s/n): " ans
            if [[ "$ans" =~ ^[sSyY]$ ]]; then
                install_playwright
            else
                exit 1
            fi
        fi
        echo ""
        echo ">>> Abrindo navegador para autenticação do YouTube Studio..."
        echo ">>> Digite seu e-mail e senha na janela que abrir."
        echo ">>> Quando o painel do YouTube Studio carregar, volte aqui e aperte ENTER."
        cd "$DIR" && "$PY_CMD" browser.py login
        ;;
    2)
        if ! check_playwright; then
            echo "[ERRO] Playwright não instalado. Escolha a opção [i] primeiro."
            exit 1
        fi
        echo ""
        echo ">>> Verificando integridade da sessão do YouTube Studio..."
        cd "$DIR" && "$PY_CMD" -c "import asyncio; from browser import verify_session; print('Resultado da sessão:', asyncio.run(verify_session()))"
        ;;
    3)
        if ! check_playwright; then
            echo "[ERRO] Playwright não instalado. Escolha a opção [i] primeiro."
            exit 1
        fi
        echo ""
        echo ">>> Conectando conta do Threads..."
        "$PY_CMD" /home/alex/.gemini/config/skills/social-auto-post/scripts/threads_poster.py --login
        ;;
    4)
        if ! check_playwright; then
            echo "[ERRO] Playwright não instalado. Escolha a opção [i] primeiro."
            exit 1
        fi
        echo ""
        echo ">>> Conectando conta do Instagram..."
        "$PY_CMD" /home/alex/.gemini/config/skills/social-auto-post/scripts/instagram_poster.py --login
        ;;
    5)
        if ! check_playwright; then
            echo "[ERRO] Playwright não instalado. Escolha a opção [i] primeiro."
            exit 1
        fi
        echo ""
        read -p "Caminho do arquivo de vídeo (.mp4/.mkv): " vpath
        read -p "Título do vídeo: " vtitle
        read -p "Caminho da capa/thumbnail (.png/.jpg) [opcional]: " vthumb
        read -p "Visibilidade (unlisted / public / private) [unlisted]: " vvis
        vvis=${vvis:-unlisted}
        cd "$DIR" && "$PY_CMD" browser.py upload "$vpath" "$vthumb" "$vtitle" "$vvis"
        ;;
    w|W)
        echo ""
        echo ">>> Abrindo https://studio.youtube.com/ no Firefox..."
        firefox "https://studio.youtube.com/" &
        ;;
    *)
        echo "Saindo."
        exit 0
        ;;
esac
