---
name: code-patch-diff-engine
description: Aplica alterações cirúrgicas de código via SEARCH/REPLACE para evitar a reescrita de arquivos inteiros e economizar tokens.
---

# Code Patch Diff Engine

NUNCA reescreva classes inteiras ou repita métodos inalterados ao modificar scripts (.cs, .py, .json, .shader).

## Formato Obrigatório do Bloco

<<<<<<< SEARCH
// 2 a 3 linhas idênticas do arquivo original para servir de âncora
=======
// Código novo ou alterado
>>>>>>> REPLACE

## Regras
1. Mantenha 2 linhas de contexto antes e depois da modificação.
2. Não altere indentação das linhas de âncora.
3. Se houver mudanças em pontos distantes do mesmo arquivo, emita múltiplos blocos separados.

## Execução Local
```bash
cat << 'EOF' | python skills/09-ia-workflows-antigravity/code-patch-diff-engine/patch_engine.py "caminho/do/arquivo"
<<<<<<< SEARCH
float speed = 10f;
=======
float speed = 25f;
>>>>>>> REPLACE
EOF
```
