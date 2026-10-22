#!/usr/bin/env bash
# Script de sincronizacao de Skills e MCPs para o Antigravity IDE (Linux)
set -e

DEST_DIR="$HOME/.gemini/config/skills"
OPENCODE_DIR="$HOME/.config/opencode/skills"
MCP_CONFIG="$HOME/.gemini/config/mcp_config.json"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$REPO_ROOT/skills"

echo "=========================================================="
echo "   Instalando Skills & MCPs no Google Antigravity IDE     "
echo "=========================================================="

# 1. Remover skill apagada (affinity-design)
echo "[1/3] Limpando skills removidas..."
rm -rf "$DEST_DIR/affinity-design"
rm -rf "$OPENCODE_DIR/affinity-design" 2>/dev/null || true
echo "[OK] affinity-design removido com sucesso."

# 2. Instalar todas as 45 skills ativas
echo "[2/3] Instalando 45 skills categorizadas..."
mkdir -p "$DEST_DIR"
mkdir -p "$OPENCODE_DIR" 2>/dev/null || true

installed_count=0
for skill_md in $(find "$SOURCE_DIR" -type f -name "SKILL.md" | sort); do
    skill_dir="$(dirname "$skill_md")"
    skill_name="$(basename "$skill_dir")"
    cp -r "$skill_dir" "$DEST_DIR/"
    cp -r "$skill_dir" "$OPENCODE_DIR/" 2>/dev/null || true
    installed_count=$((installed_count + 1))
    echo "  [+] $skill_name"
done
echo "[OK] $installed_count skills instaladas em $DEST_DIR"

# 3. Configurar mcp_config.json
echo "[3/3] Configurando MCP Servers em $MCP_CONFIG..."
cat << 'EOF' > "$MCP_CONFIG"
{
  "mcpServers": {
    "gamemaker": {
      "command": "node",
      "args": [
        "/media/alex/alex/mcp-servers/gamemaker-antigravity-mcp/dist/index.js"
      ]
    },
    "canva": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.canva.com/mcp"
      ]
    },
    "StitchMCP": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://stitch.googleapis.com/mcp",
        "--header",
        "X-Goog-Api-Key: ${STITCH_API_KEY:-YOUR_API_KEY}"
      ]
    },
    "blender": {
      "command": "uvx",
      "args": [
        "--python",
        "3.11",
        "mcp-for-blender"
      ],
      "env": {
        "UV_PYTHON_PREFERENCE": "only-managed",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
EOF

echo "[OK] mcp_config.json gerado com sucesso!"
echo "=========================================================="
echo " Instalacao concluida com sucesso!"
echo "=========================================================="
