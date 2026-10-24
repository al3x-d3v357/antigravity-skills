---
name: voxel-character-craft
description: Pipeline ultra-otimizado em tokens para criação, parametrização e escultura de personagens em Voxel Art 3D utilizando o Goxel via servidor MCP, exportação automática (.vox/.obj) e visualização direta em GUI. Use sempre que o usuário solicitar novos heróis, modelos de voxel, ou personagens para jogos com consumo mínimo de tokens.
---

# Voxel Character Craft (Low-Token Architecture)

Skill especializada na criação ultra-rápida e econômica de modelos em **Voxel Art 3D** para personagens de jogos (Unity, Godot, Blender). Reduz drasticamente o consumo de tokens de contexto e resposta ao delegar a escultura volumétrica para rotinas procedurais no servidor MCP `goxel` em vez de gerar milhares de coordenadas brutas no prompt.

---

## 1. Princípios de Economia de Tokens

* **Zero Coordenadas Verbosas no Chat:** Nunca despeje blocos gigantescos de arrays `[x, y, z, r, g, b]` na resposta ao usuário. A geração deve ser executada atomicamente pelo servidor MCP.
* **Arquétipos Paramétricos:** Utilize as classes procedurais registradas no MCP (`cyberpunk_archer`, `archer`, `tank`, `mage`, `support`, `elf_healer`) ou envie micro-scripts QuickJS estruturados com funções utilitárias (`setBox`).
* **Saída Estruturada e Concisa:** Retorne apenas um resumo operacional com:
  - Nome do Personagem e Arquétipo
  - Paleta de Cores Chave (RGBA)
  - Caminhos dos Arquivos Gerados (`.vox` e `.obj`)
  - Status da GUI (se foi aberta na tela para inspeção)

---

## 2. Paletas e Arquétipos Padronizados

| Arquétipo | Cores Principais | Acessórios Característicos |
| :--- | :--- | :--- |
| **Cyberpunk Archer** | Laranja Neon (`#FF7300`), Azul Elétrico/Ciano (`#00E1FF`), Preto Carbono (`#181B24`) | Arco composto tech, corda laser cyan, visor holográfico, prótese biônica |
| **Mage** | Púrpura Imperial (`#55238C`), Ouro Místico (`#FAC32D`), Cristal Magenta (`#D737FF`) | Túnica longa com runas, chapéu cônico, barba volumosa, cajado com cristal |
| **Tank / Warrior** | Aço Polido (`#415573`), Dourado (`#E1B92D`), Azul Néon (`#2DDCFF`) | Armadura pesada, elmo com visor iluminado, escudo torre e espada larga |
| **Elf Healer / Support** | Branco Sagrado (`#F0F0F5`), Menta/Esmeralda (`#4BE1EB`), Dourado Divino (`#FFD732`) | Orelhas élficas longas, asas de espírito, cajado da árvore da vida, orbe de cura |

---

## 3. Diretórios Padrão

* **Pasta de Avaliação Rápida (Desktop/Inspeção):**
  `/home/alex/Documents/voxel_art/`
* **Pasta de Assets do Jogo (Unity BlockTactics):**
  `/media/alex/alex/pro_unity/block_tactics/blocktactics/Assets/BlockTactics/VoxelCharacters/`
* **Binário Goxel:**
  `/media/alex/alex/softwares/goxel-0.15.1-extracted/AppRun`

---

## 4. Fluxo de Execução com MCP

### Chamada Padrão de Criação (`goxel_create_character`):
```json
{
  "name": "goxel_create_character",
  "arguments": {
    "character_class": "cyberpunk_archer",
    "output_dir": "/home/alex/Documents/voxel_art",
    "export_obj": true,
    "open_in_gui": true
  }
}
```

### Formato de Arquivos:
1. **`.vox` (MagicaVoxel):** Formato padrão leve, exportado sem sobrecarga de renderizador headless.
2. **`.obj` (Wavefront 3D):** Malha tridimensional pronta para arrastar para a Unity/Godot.
3. **Visualização `.gox`:** No Goxel manual, use o filtro `MagicaVoxel (*.vox)` no diálogo de abertura (`Ctrl+O`) ou salve com `Ctrl+S` para salvar as camadas nativas.

---

## 5. Delegação via OpenCode

Quando delegado ao OpenCode para economizar contexto no agente principal:
```bash
opencode run --auto "Crie o personagem <classe> no Goxel Art e salve em ~/Documents/voxel_art"
```
