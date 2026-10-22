#!/usr/bin/env bash
# Script para criar repositorios no GitHub por Categoria via GitHub CLI (gh)
set -e

export PATH="/media/alex/alex/bin:$PATH"

if ! gh auth status >/dev/null 2>&1; then
    echo "[!] Voce ainda nao esta autenticado no GitHub CLI."
    echo "Execute primeiro no seu terminal: gh auth login"
    exit 1
fi

REPO_ROOT="/media/alex/alex/antigravity-skills/al3x-antigravity-skills"
SKILLS_DIR="$REPO_ROOT/skills"
GITHUB_USER="$(gh api user -q .login)"
echo "[+] Autenticado no GitHub como: @$GITHUB_USER"

# Mapeamento de Categorias para Nomes de Repositorios no GitHub
declare -A CATEGORIES=(
    ["01-gamedev-unity"]="antigravity-skills-unity"
    ["02-gamedev-godot"]="antigravity-skills-godot"
    ["03-3d-blender"]="antigravity-skills-blender"
    ["04-video-youtube"]="antigravity-skills-video-youtube"
    ["05-marketing-seo-copy"]="antigravity-skills-marketing-seo"
    ["06-automacao-redes-sociais"]="antigravity-skills-automacao-social"
    ["08-produtividade-documentos"]="antigravity-skills-produtividade-documentos"
    ["09-ia-workflows-antigravity"]="antigravity-skills-ia-workflows"
)

TEMP_EXPORT_DIR="/tmp/antigravity_github_repos"
rm -rf "$TEMP_EXPORT_DIR"
mkdir -p "$TEMP_EXPORT_DIR"

for cat_folder in "${!CATEGORIES[@]}"; do
    repo_name="${CATEGORIES[$cat_folder]}"
    source_cat="$SKILLS_DIR/$cat_folder"
    target_repo="$TEMP_EXPORT_DIR/$repo_name"

    if [ -d "$source_cat" ]; then
        echo "=========================================================="
        echo " Preparando repositorio: $repo_name (Categoria: $cat_folder)"
        echo "=========================================================="
        mkdir -p "$target_repo"
        cp -r "$source_cat"/* "$target_repo/"

        # Criar README do repositorio da categoria
        cat << EOF > "$target_repo/README.md"
# ⚡ $repo_name

> Pacote de Skills para o **Google Antigravity IDE** e **OpenCode**.
> Categoria: \`$cat_folder\`
> Mantido por [@$GITHUB_USER](https://github.com/$GITHUB_USER).

## 📦 Skills Inclusas neste Pacote

EOF
        for s in "$target_repo"/*/; do
            if [ -d "$s" ]; then
                s_name=$(basename "$s")
                echo "- **\`$s_name\`**" >> "$target_repo/README.md"
            fi
        done

        cat << EOF >> "$target_repo/README.md"

## 🚀 Como Usar no Antigravity IDE
Copie as pastas das skills para o seu diretorio global de skills:
- **Linux/macOS:** \`~/.gemini/config/skills/\`
- **Windows:** \`%USERPROFILE%\\.gemini\\config\\skills\\\`

---
Distribuido sob a licenca MIT.
EOF

        # Inicializar Git e Criar no GitHub
        cd "$target_repo"
        git init -b main
        git config user.name "Alex Sandro"
        git config user.email "alex.sandro.dev@gmail.com"
        git add -A
        git commit -m "feat: release inicial das skills da categoria $cat_folder"

        echo "[+] Criando repositorio remoto no GitHub: $GITHUB_USER/$repo_name..."
        if gh repo view "$GITHUB_USER/$repo_name" >/dev/null 2>&1; then
            echo "[INFO] Repositorio $repo_name ja existe no GitHub. Atualizando remote e enviando commits..."
            git remote add origin "https://github.com/$GITHUB_USER/$repo_name.git" 2>/dev/null || git remote set-url origin "https://github.com/$GITHUB_USER/$repo_name.git"
            git push -u origin main --force
        else
            gh repo create "$GITHUB_USER/$repo_name" --public --source=. --remote=origin --push
        fi
        echo "[OK] Repositorio $repo_name publicado com sucesso!"
    fi
done

echo "=========================================================="
echo " Todos os repositorios foram criados e publicados no GitHub!"
echo "=========================================================="
