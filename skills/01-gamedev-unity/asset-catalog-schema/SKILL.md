---
name: asset-catalog-schema
description: Lê e mantém o manifesto de assets disponíveis (modelos, áudios, texturas) evitando comandos repetidos de listagem.
---

# Asset Catalog Schema

1. Nunca execute `ls`, `dir` ou `Get-ChildItem` repetidamente para encontrar arquivos de malha ou som.
2. Leia o arquivo `docs/assets_manifest.json` para obter os caminhos relativos exatos de modelos e áudios disponíveis.
3. Ao adicionar um novo asset externo, rode:
   `python skills/01-gamedev-unity/asset-catalog-schema/catalog_assets.py`
