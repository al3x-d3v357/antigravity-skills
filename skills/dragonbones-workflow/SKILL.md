---
name: dragonbones-workflow
description: >-
  Automatiza o fluxo completo de criação de personagens 2D para o DragonBones Pro no disco D:
  remoção precisa de fundo com Pillow, segmentação de partes articuladas (cabeça, cabelo, olhos,
  membros, cauda e efeitos), empacotamento de atlas (*_tex.png / *_tex.json), geração de esqueleto
  e animações suaves (*_ske.json em DragonBones 5.5) e integração via servidor MCP dragonbones.
---

# DragonBones Pro Workflow (2D Rigging & Animation)

Fluxo padrão para transformar imagens individuais ou sprite sheets modulares em projetos prontos para o **DragonBones Pro** (`D:\Programas\Egret\DragonBonesPro\DragonBonesPro.exe`).

---

## 1. Diretórios e Ferramentas MCP
- **Projetos em `D:\Projetos\2D\<Nome_Do_Projeto>\`** (seguindo `use-d-drive`):
  - `source.jpg` / `*_nobg.png` (imagem original e versão com fundo transparente)
  - `parts\*.png` (peças individuais recortadas)
  - `<Nome>_tex.png` e `<Nome>_tex.json` (atlas empacotado)
  - `<Nome>_ske.json` (esqueleto, skins e animações no formato DragonBones 5.5)
- **Servidor MCP `dragonbones`** (`D:\Projetos\2D\dragonbones-mcp\server.py`):
  - `get_dragonbones_info`, `list_dragonbones_projects`, `inspect_dragonbones_data`, `create_dragonbones_project`, `add_dragonbones_animation`, `open_in_dragonbones`.

---

## 2. Remoção de Fundo e Segmentação Segura (Python + Pillow)
1. **Use Flood-Fill a partir das bordas** (nunca substituição global de cor) para preservar cores internas parecidas com o fundo (ex.: olhos vermelhos em fundo vermelho, roupas brancas em fundo branco).
2. **Preserve sombreamentos próximos ao fundo**: ajuste a tolerância de distância de cor e limite por canal para não apagar pernas/pele sombreadas.
3. **Limpe bolhas fechadas e ruídos**: remova bolsões internos grandes de fundo (entre pernas, braços ou cauda), sombra do chão e partículas desconexas (< 120 px), aplicando suavização alpha de 1–2 px nas bordas.
4. **Detecção exata em Sprite Sheets**: use análise de componentes conectados para obter os bounding boxes reais antes de recortar cada peça.

---

## 3. Regras de Rigging e Animação Suave (DragonBones 5.5)
- **Olhos e Piscadas (`eyes`)**:
  - Recorte **100% da altura do olho** (cílios superiores até ~4–6 px abaixo da base da íris) para evitar que a parte inferior da íris fique visível ao piscar.
  - Mantenha o osso `eyes` **sem `translateFrame`** (alinhado pixel a pixel com `head`); anime o olhar gerando variações (`eyes_look_l`, `eyes_look_r`) que deslocam apenas a íris dentro da esclera, e `eyes_blink` cobrindo toda a abertura ocular com o tom de pele + cílio curvado.
- **Cabelo e Orelhas**:
  - Mantenha orelhas e brincos presos ao osso `head`; isole apenas as mechas laterais externas (`hair_left`, `hair_right`) com rotação suave (`±1.8°` a `±2.5°`) para não invadir a orelha.
- **Cadeias Articuladas (Cauda, Capa, Asas)**:
  - Divida caudas em 2–3 ossos (`tail_base` → `tail_mid` → `tail_tip`) com defasagem de fase (`π/3`) para movimento fluido em onda.
- **Keyframes Senoidais**:
  - Gere keyframes a cada 4–6 frames com `tweenEasing: 0` seguindo curvas cossenoidais contínuas, evitando transições bruscas de apenas 2 keyframes.

---

## 4. Validação Visual Obrigatória
Antes de concluir qualquer entrega:
1. Inspecione visualmente com `read_file` o `*_nobg.png`, o atlas `*_tex.png` e peças críticas (`head.png`, `eyes_blink.png`, `eyes_look_l.png`).
2. Confirme que não há cortes no rosto/focinho, sobras de fundo ou partes transparentes indevidas.
3. Inicie ou oriente a importação de `<Nome>_ske.json` no **DragonBones Pro** (`File → Import Data...`).
