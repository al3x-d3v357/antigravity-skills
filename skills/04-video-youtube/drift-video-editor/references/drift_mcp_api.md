# Drift MCP Agent Guide & API Reference

Referência técnica completa para orquestração da API e timeline do **Drift Video Editor 0.7.5** via Model Context Protocol (MCP) e JSON-RPC 2.0.

---

## 1. Protocolo e Conexão

- **Endpoint HTTP**: `http://127.0.0.1:4731/mcp`
- **Transporte Alternativo (stdio)**: `D:/Programas/Drift/drift.exe --mcp-stdio`
- **Autenticação**: Header HTTP `Authorization: Bearer <TOKEN>`
- **Protocolo de Chamada**: JSON-RPC 2.0 com `tools/call` e REST `apply`

### Estrutura de Requisição JSON-RPC 2.0:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "inspect",
    "arguments": {
      "clips": true,
      "detail": true
    }
  }
}
```

---

## 2. Paleta de Cores Obrigatória & Identidade Visual

Toda criação de overlays, lower-thirds, badges, cards e caixas de texto explicativas deve utilizar estritamente a seguinte paleta de cores:

| Elemento | Código HEX | Finalidade Visual |
| :--- | :--- | :--- |
| **Azul Royal Profundo** | `#3852B4` | Fundo secundário, gradientes de sombra e molduras estruturais |
| **Azul Médio / Ardósia** | `#5E7AC4` | Bordas secundárias, linhas divisórias e ícones |
| **Dourado / Âmbar Quente** | `#F3BE7A` | Destaques de palavras-chave, subtítulos e badges de contexto |
| **Laranja Tangerina Vibrante** | `#F08D39` | Indicador de foco lateral, glow neon, tags de devlog e alertas |
| **Texto Obrigatório** | `#FFFFFF` | **Sempre branco puro** para máxima legibilidade contra fundos escuros |

---

## 3. Fluxo de Trabalho do Agente (Workflow)

1. **Catálogo de Operações**:
   - Chamar `catalog` para listar caixas de ferramentas (`toolboxes`) e suas operações.
   - Chamar `search({q})` para buscar uma operação por palavra-chave.
2. **Esquema de Ferramentas**:
   - Chamar `toolbox({name})` para obter schemas JSON detalhados.
3. **Mutações em Lote Atômicas**:
   - Chamar `apply({ops: [{tool, args}, ...]})` para aplicar edições com um único passo de desfazer (*undo step*).
4. **Inspeção de Estado**:
   - Chamar `inspect({clips: true, detail: true})` para obter UUIDs de clipes, pilhas de efeitos, máscaras, velocidade e estado de renderização.
5. **Inspeção Visual da Mídia**:
   - `activity()`: Localiza onde ocorrem mudanças bruscas na imagem.
   - `frames()`: Gera folha de contato (*contact sheet*) com momentos rotulados.
   - `capture()`: Gera snapshot still em resolução total no playhead.
6. **Reenquadramento e Inteligência Visual (0.7.5)**:
   - `auto_reframe({clip, aspect, mode})`: Ajuste de aspecto automático (ex: 9:16 vertical) ancorado em face (`mode: "face"`).
   - `list_face_track({track, clip})`: Rastreamento contínuo da posição do rosto.

---

## 4. Efeitos Especiais & Recursos 0.7.5

### Face Retouch (`face_retouch`):
Efeito nativo para tratamento facial profissional na câmera/webcam:
- `smoothing` (0.0 a 1.0, def: 0.6): suavização de pele.
- `sharpen` (0.0 a 1.0, def: 0.25): nitidez de contorno.
- `whitening` (0.0 a 1.0, def: 0.3): iluminação/clareamento suave.
- `skinTone` (0.0 a 1.0) e `toneColor` (hex, def: `#d9a982`).
- `slimFace` (0.0 a 1.0, def: 0.2) e `bigEyes` (0.0 a 1.0, def: 0.2).
- `faceIndex` (0 a 3): índice do rosto no enquadramento.

### Efeitos em People Cutouts:
- Na 0.7.5, efeitos aplicados a clipes com segmentação de pessoa/fundo transparente são renderizados corretamente no cutout.
- Uso recomendado: `edge_neon` com cor `#F08D39` ou `#5E7AC4` para dar contorno iluminado no apresentador.

### Authoring de Efeitos Customizados (.driftfx):
- `effect_authoring_guide({kind: "effect" | "transition" | "audio_effect"})`: Documentação e guias de criação.
- `create_effect({kind, id, displayName, ...})`: Cria novo efeito ou transição com shaders `.frag` ou pedais de áudio.
- `update_effect({kind, id, manifest, files})`: Atualiza código GLSL e propriedades.
- `get_effect_source({kind, id})`: Lê código-fonte de qualquer efeito do sistema.
- `export_effect({kind, id, path})`: Salva pacote `.driftfx` completo para reuso.

---

## 5. Toolboxes Principais (Drift 0.7.5)

| Toolbox | Principais Operações | Finalidade |
| :--- | :--- | :--- |
| **media** | `import_media`, `list_assets` | Importa e gerencia caminhos absolutos e assets |
| **timeline** | `place_clip`, `move_clip`, `split_clip`, `delete_clip`, `set_speed_curve` | Controle da linha do tempo e velocidade |
| **text** | `add_text`, `set_text`, `apply_text_look`, `set_text_animation` | Títulos, tipografia e animações |
| **shapes** | `list_shapes`, `add_shape`, `set_shape_style` | Retângulos, badges, containers glassmorphic |
| **effects** | `add_effect`, `set_effect_param`, `remove_effect` | Shaders GLSL, Face Retouch, Edge Neon, etc. |
| **transitions**| `add_transition`, `set_transition_param` | Transições de cena aceleradas por GPU |
| **authoring** | `create_effect`, `update_effect`, `get_effect_source`, `export_effect` | Criação e empacotamento de efeitos .driftfx |
| **vision / ai**| `auto_reframe`, `list_face_track`, `stabilize_clip`, `remove_stabilize` | Reenquadramento 9:16 e estabilização |
| **audio** | `detect_beats`, `detect_silence`, `set_volume`, `duck_under` | Sincronia de áudio e ritmo |
| **market** | `market_status`, `market_search`, `market_download` | Ativos da loja e nova aba Sound Effects |
| **voice** | `tts_generate`, `sfx_generate`, `list_voices` | Síntese de voz e efeitos sonoros |
| **addons** | `list_addons`, `install_addon`, `cancel_addon_install` | Gerenciamento de add-ons e modelos IA |
| **project** | `save_project`, `load_project`, `export_video`, `export_status` | Renderização e persistência |
