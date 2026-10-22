#!/usr/bin/env bash
# Script de Instalacao de Skills para macOS e Linux (Antigravity + OpenCode)
# Autor: Alex Sandro (@al3x-d3v357)

set -e

DEST_DIR="$HOME/.gemini/config/skills"
OPENCODE_DIR="$HOME/.config/opencode/skills"
CLAUDE_DIR="$HOME/.claude/skills"
AGENTS_DIR="$HOME/.agents/skills"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills"

echo "=========================================================="
echo "   Instalador de Skills - Antigravity + OpenCode           "
echo "=========================================================="

mkdir -p "$DEST_DIR" "$OPENCODE_DIR"
mkdir -p "$CLAUDE_DIR" "$AGENTS_DIR" 2>/dev/null || true

for skill_md in $(find "$SOURCE_DIR" -type f -name "SKILL.md" | sort); do
    skill=$(dirname "$skill_md")
    skill_name=$(basename "$skill")
    cp -r "$skill" "$DEST_DIR/"
    cp -r "$skill" "$OPENCODE_DIR/" 2>/dev/null || true
    cp -r "$skill" "$CLAUDE_DIR/" 2>/dev/null || true
    cp -r "$skill" "$AGENTS_DIR/" 2>/dev/null || true
    echo "[OK] Skill instalada: $skill_name (gemini + opencode + compat)"
done

echo "=========================================================="
echo " Todas as skills foram instaladas com sucesso!"
echo "  - Antigravity: $DEST_DIR"
echo "  - OpenCode:    $OPENCODE_DIR"
echo "  - Compat:      $CLAUDE_DIR, $AGENTS_DIR"
echo "=========================================================="
