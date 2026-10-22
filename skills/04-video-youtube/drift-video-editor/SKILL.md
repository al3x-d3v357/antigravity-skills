---
name: drift-video-editor
description: >-
  Automates end-to-end video post-production for devlogs, gameplay demos, and technical showcases. Orchestrates the Drift Video Editor MCP timeline, 5-track structured projects, subtitle styling with glassmorphic backgrounds, acoustic SFX synchronization, Blender 360 studio turntable renders, FFmpeg automations, and Drift 0.7.5 enhancements (Face Retouch beauty shader, AI upscaling, composite clip speed ramps, MCP custom effect authoring, auto reframe, video stabilization, and people cutout styling). Triggers whenever the user requests video editing, silence removal, dynamic framing, timelapse creation, music integration, or timeline manipulation via Drift MCP.
---

# Drift Video Editor Skill

Orquestra pipelines automatizados de edição de vídeo profissional em 1080p60 para apresentações técnicas, devlogs de jogos, timelapses e redes sociais, utilizando o **Drift Video Editor 0.7.5 (MCP)**, integrações com **Blender 3D Studio** e automações **FFmpeg**.

---

## 0. Isolamento e Organização Estrutural de Pastas de Projetos (REGRA MANDATÓRIA)

Para manter a integridade, organização e limpeza do ambiente de trabalho do criador:

1. **Criação Obrigatória de Pasta Dedicada por Projeto**:
   - Sempre que o usuário solicitar a edição de um vídeo, **é terminantemente proibido despejar arquivos soltos na raiz do diretório `Videos` (`/home/alex/Videos`)**.
   - O agente **deve obrigatoriamente criar uma pasta dedicada e isolada com o nome do projeto** no diretório de vídeos (Exemplo: `/home/alex/Videos/<nome_do_projeto>/`).
   - Todo o ciclo de vida do projeto — mídias de trabalho, arquivos intermediários de renderização, speed ramps, crops, cards gráficos, trilhas sonoras, o arquivo de projeto `.driftproj` e o master final — **deve obrigatoriamente residir dentro desta pasta dedicada**.

2. **Localização e Ingestão do Avatar Oficial do Alex**:
   - O avatar e foto oficial do criador fica localizado no diretório Pictures: `/home/alex/Pictures/Avata.jpeg` (ou variações `avatar*`).
   - O agente deve buscar o arquivo original diretamente em `Pictures/`, aplicar o recorte circular supersample com contorno neon `#F08D39` (3px) e salvá-lo dentro da pasta do projeto em `/home/alex/Videos/<nome_do_projeto>/avatar.png`.

3. **Política de Higienização de Intermediários**:
   - Ao concluir e confirmar a renderização final ou a versão selecionada pelo usuário, todos os arquivos temporários e intermediários (`ramped_*`, `framed_*`, `pipeline_ident_*`, frames avulsos) devem ser devidamente excluídos, mantendo a pasta limpa apenas com os entregáveis definitivos e o `.driftproj`.

---

## 1. Identidade Visual & Paleta de Cores Obrigatória

Toda e qualquer composição de elementos gráficos (cards explicativos, caixas de informação, lower-thirds, bordas luminosas, badges e legendas) **deve obrigatoriamente** seguir a paleta corporativa:

| Cor | HEX | Uso Recomendado |
| :--- | :--- | :--- |
| **Azul Royal Profundo** | `#3852B4` | Gradientes escuros de container e fundos secundários |
| **Azul Médio / Ardósia** | `#5E7AC4` | Divisórias sutis, contornos estruturais e badges secundários |
| **Dourado / Âmbar Quente** | `#F3BE7A` | Subtítulos, destaques de texto e pontos de atenção |
| **Laranja Tangerina Vibrante** | `#F08D39` | Faixa indicadora lateral, glow neon, tags de status e botões de ação |
| **Texto Obrigatório** | `#FFFFFF` | **Texto sempre 100% branco** para garantia total de contraste e legibilidade |

### Regras de Design para Cards Explicativos:
1. **Container Glassmorphic**: Fundo escuro translúcido (`rgba(10, 16, 32, 0.94)`), cantos arredondados (`radius: 16px`) e contorno de 3px com gradiente/cor de destaque da paleta.
2. **Faixa Indicadora Lateral**: Faixa de 8px em `#F08D39` ou `#5E7AC4` na lateral esquerda do card.
3. **Texto de Alto Contraste**: Títulos e corpo sempre em `#FFFFFF`, com palavras-chave de destaque em `#F3BE7A`.
4. **Card Obrigatório de Apresentação Inicial do Alex (NOVA ATUALIZAÇÃO OBRIGATÓRIA)**:
   - Todo vídeo apresentado ou narrado **deve obrigatoriamente** iniciar apresentando o criador: **"ALEX | DESENVOLVEDOR & CRIADOR"**.
   - Posicionamento inferior (lower-third / bottom card), exibido entre `1.0s` e `7.5s`.
   - **Animação Padronizada**: Entrada com animação suave de subida/slide + fade (`0.35s`) acompanhado de **SFX whoosh/pop**, sustentação clara, e saída com slide/fade suave acompanhado de efeito sonoro.
5. **Animação Obrigatória em TODOS os Elementos Gráficos & Efeitos Sonoros (SFX)**:
   - **TODOS os elementos visuais em tela** (cards explicativos, caixas de informação, lower-thirds, badges e banners) **devem obrigatoriamente conter animação de entrada e de saída** (transições, slide-in, fade-in de 350ms, fade-out de 350ms).
   - Nenhum elemento pode aparecer ou sumir de forma estática/"cortada".
   - Cada entrada e saída gráfica deve ser sincronizada no milissegundo com **efeito sonoro dedicado (SFX pop, whoosh_in, chime ou ding)**.
6. **Avatar + Visualizador de Ondas Sonoras Sincronizado (DIRETRIZ MANDATÓRIA)**:
   - Todo vídeo narrado **deve obrigatoriamente** exibir avatar do criador no **canto inferior esquerdo em moldura circular compacta (~120x120px)** com contorno neon `#F08D39` (3px) e sombra suave.
   - À direita do avatar, **visualizador de ondas sonoras sincronizado** (linha ou barras estilizadas, ~300x80px, cor `#F08D39` / `#F3BE7A`) reagindo em tempo real ao áudio vocal (FFmpeg `showwaves`/`avectorscope` ou efeito Drift dedicado).
   - Se a interface possuir barra de status inferior (ex.: progresso de download), elevar o conjunto com **offset de ~40px da borda** para nunca cobrir informações.
   - Exibição contínua durante toda a narração, com fade-in/out de 350ms + SFX pop na entrada/saída.

---

## 1.2 Variante de marca Fox.iso (opcional)

Para projetos Fox.iso, pode-se usar a variante `brand_fox_iso` do `style_guide.json`:
coral `#FF7F50` (ação/perigo), sunglow `#FFD166` (highlight), mint `#06D6A0` (sucesso), teal `#118AB2` (info), texto sempre `#FFFFFF`.
Assets: `D:/GitHub/baixa_games/imgs/logo_full.png`, `logo_icon.png`, `logo_badge.png`, `brand_sheet.png`.
A paleta Drift padrão (seção 1) segue obrigatória por default; Fox.iso é opt-in por projeto.

---

## 1.1 Regra Obrigatória de Remoção Dinâmica de Silêncio (Frases Completas)
1. **Preservação Total da Fala**:
   - Os cortes acústicos devem eliminar tempos mortos do OBS (início e fim) e silêncios intermediários longos (>0.75s).
   - **É estritamente proibido cortar palavras ou final de frases**: aplicar sempre margem de respiro generosa nas bordas (`pad_in >= 0.18s` a `0.20s` e `pad_out >= 0.30s` a `0.35s`).
   - Toda frase deve ser falada e concluída completamente com dicção natural.
2. **Ganho Vocal e Presença**:
   - Em vídeos com microfone rebaixado (`mean_volume < -35dB`), aplicar **obrigatoriamente ganho acústico compensatório (+10dB a +14dB / volume 2.5x a 3.0x)**.
   - Trilha sonora BGM sempre suave e atenuada (`0.020` a `0.022`) para nunca mascarar a fala.

---

## 2. Arquitetura Padrão da Linha do Tempo (5 Faixas de Produção)

Os projetos no Drift Video Editor devem ser estruturados deterministamente em 5 faixas hierárquicas:

```text
┌─────────────────────────────────────────────────────────────┐
│ Track 0 [TEXT]:  Legendas Dinâmicas com Box Glassmorphic    │
├─────────────────────────────────────────────────────────────┤
│ Track 1 [VIDEO]: Cards Explicativos, Badges & Lower-Thirds  │
├─────────────────────────────────────────────────────────────┤
│ Track 2 [VIDEO]: Vídeo Principal (Face Retouch, IA & Zooms) │
├─────────────────────────────────────────────────────────────┤
│ Track 3 [AUDIO]: Efeitos Sonoros (SFX Pop, Whoosh, Chime)   │
├─────────────────────────────────────────────────────────────┤
│ Track 4 [AUDIO]: Trilha Sonora Suave BGM (NCS Kawaii Mix)   │
└─────────────────────────────────────────────────────────────┘
```

### Especificações Técnicas de Cada Faixa:
1. **Track 0 (Text / Subtitles)**:
   - Legendas sincronizadas com fala natural.
   - `boxColor`: `#ea0a1020` (fundo translúcido escuro de alto contraste).
   - `boxEnabled`: `true`, `boxRadius: 10`, `boxPadding: 12`.
   - `color`: `#ffffffff` (100% branco puro), `fontFamily: "Inter"`, `pixelSize: 36`.
   - `accent.color`: `#fff3be7a` (Dourado Âmbar para palavras-chave).
   - Posicionamento inferior seguro: `y: 410`, `w: 1700`, `h: 110`.
2. **Track 1 (Graphics / Overlays & Cutouts)**:
   - Cards estruturais em `assets/cards/` + 3 Lower-Thirds.
   - Fade-in de `350ms` e Fade-out de `350ms`.
   - **People Cutouts (0.7.5)**: Em camadas de webcam recortada (fundo transparente), aplicar contorno luminoso neon (`edge_neon` em tom `#F08D39` ou `#5E7AC4`, largura 3px) e sombra projetada suave.
3. **Track 2 (Main Video Footage & Processamento IA 0.7.5)**:
   - Cortes acústicos de silêncio eliminando pausas e ruídos de gravação.
   - Zooms contextuais de 10% a 25% em momentos de demonstração técnica e viewport.
   - **Face Retouch (Drift 0.7.5 Beauty Effect)**: Sempre que houver câmera do apresentador ou webcam na cena, aplicar o efeito `face_retouch` com parâmetros calibrados para transmissão profissional:
     - `smoothing: 0.45` (suavização sutil da textura da pele)
     - `sharpen: 0.20` (preservação de nitidez de olhos e boca)
     - `whitening: 0.15` (equilíbrio de luminosidade do rosto)
     - `skinTone: 0.0` e `toneColor: "#d9a982"` (tom natural)
     - `slimFace: 0.05` e `bigEyes: 0.0` (sem distorção artificial)
     - `faceIndex: 0` (ou índice do apresentador detectado)
   - **Speed Control em Clipes Compostos (Composite Clips 0.7.5)**:
     - Agrupar trechos multi-camada (ex: webcam + tela + gráficos de código) em Composite Clips e modular a curva de velocidade de forma unificada (timelapses e speed ramps sincronizados).
   - **Snapping e Ripple Edit (0.7.5)**:
     - Utilizar snapping sensível ao nível de zoom e ripple em trims de borda para manter perfeita integridade temporal entre fala, música e transições.
4. **Track 3 (SFX / Sound Design)**:
   - Sincronização no milissegundo de entrada de cada card: `card_pop.wav`, `whoosh_in.wav`.
   - Destaque em marcos de benchmark e técnicas: `chime_benchmark.wav`, `ding_highlight.wav`.
   - Acesso à nova aba de **Sound Effects** no Marketplace do Drift para busca e variações de áudio.
5. **Track 4 (BGM Trilha Sonora)**:
   - Biblioteca local: `C:/Users/alexa/Dropbox/song` (*NCS Kawaii Mix*).
   - Volume ajustado suave: `0.018` a `0.022`.
   - Micro-fade inicial de `2.0s` e fade-out gradual de encerramento de `3.5s`.

---

## 3. Pipeline de Renderização 3D Studio Turntable (Blender)

Para apresentação de modelos 3D desenvolvidos em devlogs:
1. **Configuração de Estúdio em 3 Pontos**:
   - **Key Light**: 850W, suave (tamanho 2.5m), cor quente (`1.0, 0.95, 0.88`).
   - **Fill Light**: 400W, suave (tamanho 3.5m), cor ardósia azul (`0.75, 0.85, 1.0`).
   - **Rim Light**: 1100W, recorte de borda (tamanho 2.0m), dourado quente (`0.95, 0.75, 0.48`).
   - **Pedestal**: Base cilíndrica com material escuro metálico (`#0a101f`).
2. **Câmera & Órbita 360°**:
   - Lente retrato de 65mm com enquadramento de corpo inteiro.
   - Rotação suave de 360 graus via Empty Rig ou frame-handler.
3. **Exportação & Ingestão no Drift**:
   - Renderização EEVEE-Next em sequência PNG / MP4 H.264.
   - Inserção automática como clipe final de apresentação do projeto.

---

## 4. Orquestração MCP do Drift Video Editor (0.7.5)

- **Endpoint HTTP**: `http://127.0.0.1:4731/mcp`
- **Operações Principais**:
  - `import_media`: Importação em lote de caminhos absolutos para a lixeira de mídia.
  - `load_project`: Carregamento do projeto `.drift` nativo em tempo real no editor aberto.
  - `save_project`: Persistência imediata das alterações.
  - `apply_text_look`: Aplicação instantânea do look `background` e shading em legendas.
  - `auto_reframe`: Reenquadramento inteligente com `mode: "face"` para aspect ratio 9:16 vertical.
  - `list_face_track`: Rastreamento facial em tempo real para ancoragem de enquadramento.
  - `stabilize_clip`: Estabilização de vídeo gravado em campo com salvamento direto no media bin.
  - `detect_beats`: Mapeamento de transições e cortes rítmicos alinhados à trilha sonora.

### Authoring de Efeitos Customizados & Shaders (.driftfx via MCP 0.7.5):
O Drift 0.7.5 permite aos agentes criar, atualizar, inspecionar e exportar efeitos de vídeo e pedais de áudio:
- `effect_authoring_guide({kind})`: Obtém a especificação e schema para `effect`, `transition` ou `audio_effect`.
- `create_effect({kind, id, displayName, manifest, files})`: Cria um pacote completo em tempo real.
- `update_effect({kind, id, manifest, files})`: Atualiza shaders fragment (`.frag`) e parâmetros.
- `get_effect_source({kind, id})`: Inspeciona código GLSL e manifesto de qualquer efeito existente.
- `export_effect({kind, id, path})`: Empacota e exporta um arquivo `.driftfx` para distribuição.
- `list_addons` e `install_addon`: Gerencia pacotes instalados e modelos adicionais.

---

## 5. Estrutura de Arquivos da Skill

```text
skills/drift-video-editor/
├── SKILL.md                          # Guia orquestrador e protocolo de decisão
├── scripts/
│   ├── drift_client.py              # Cliente MCP desacoplado (JSON-RPC 2.0, Bearer Token & 0.7.5 tools)
│   ├── build_full_drift_project.py  # Construtor nativo de 5 faixas e sincronizador MCP
│   ├── render_turntable_360.py      # Pipeline de estúdio 360 no Blender EEVEE-Next
│   ├── music_manager.py             # Gerenciador da biblioteca de músicas (Dropbox/song)
│   ├── generate_lower_third.py      # Gerador de cards e overlays com paleta oficial
│   └── auto_edit_video.py           # Pipeline unificado de processamento FFmpeg
└── references/
    ├── drift_mcp_api.md             # Guia completo da API Drift MCP e toolboxes (atualizado para 0.7.5)
    ├── ffmpeg_recipes.md            # Receitas de filtros de vídeo, speed ramps e áudio
    └── style_guide.json             # Paleta oficial, dimensões e tokens visuais
```

---

## 6. Protocolo Obrigatório de Análise e Edição em Lote (Batch Workflow)

Sempre que um lote de vídeos for submetido para edição, o agente deve seguir estritamente o seguinte fluxo determinístico:

1. **Inspeção Acústica e Diagnóstico Pré-Edição**:
   - Inspecionar cada arquivo do lote via `ffprobe` e `ffmpeg -af volumedetect`.
   - Se o volume vocal estiver rebaixado (`mean_volume < -40dB`), aplicar **obrigatoriamente ganho acústico compensatório (+12dB a +14dB / volume 2.2x)** na faixa vocal.
   - Se o vídeo for uma sessão silenciosa (`mean_volume <= -90dB`, sem áudio gravado), converter obrigatoriamente para **Speed Modeling / Timelapse Acelerado (12x a 15x)** com marcadores de etapas na Track 0 e destaque musical na Track 4.
2. **Cortes Acústicos Inteligentes**:
   - Detectar pausas e silêncios superiores a `1.2s` (`silencedetect=noise=-32dB:d=0.75`), preservando margem de segurança de `0.15s` nas bordas para manter a respiração natural.
   - Eliminar os tempos mortos de início e encerramento da captura de tela (OBS).
3. **Otimizações IA e Pós-Processamento Visual (Drift 0.7.5)**:
   - **Estabilização**: Se a gravação apresentar trepidação, aplicar `stabilize_clip` gerando novo ativo estabilizado.
   - **AI Video Upscaling**: Se houver clipes de baixa resolução (<1080p) ou trechos recortados, usar upscaling por IA com seleção de modelo e preview ao vivo.
   - **Face Retouch**: Em trechos com apresentador/webcam, injetar o efeito `face_retouch` calibrado (`smoothing: 0.45`, `whitening: 0.15`, `sharpen: 0.20`).
   - **People Cutouts**: Inserir iluminação de borda neon (`edge_neon` em `#F08D39`) ao redor da pessoa recortada.
4. **Mapeamento Neural de Legendas com Whisper**:
   - Transcrever as falas do vídeo com Whisper (`language="pt"`).
   - Remapear milimetricamente os timestamps para os novos tempos da timeline após a eliminação de silêncios.
5. **Construção e Carregamento Deterministico no Drift MCP**:
   - Montar o arquivo nativo `.drift` comprimido em Zstandard (nível 3) com cabeçalho `DRIFTPRJ`.
   - Carregar e persistir imediatamente no Drift MCP em execução (`http://127.0.0.1:4731/mcp`) via chamadas JSON-RPC `load_project` e `save_project`.

---

## 7. Pipeline de Trailers Verticais para Redes Sociais (Shorts / Reels / TikTok)

Para cada projeto principal finalizado, deve ser disponibilizado o pipeline de geração do trailer vertical de alta retenção:

1. **Auto Reframe com Rastreamento Facial IA (Drift 0.7.5)**:
   - Utilizar a ferramenta MCP `auto_reframe` com `aspect: 0.5625` (9:16) e `mode: "face"`.
   - Utilizar `list_face_track` para manter o apresentador ou elemento principal perfeitamente centralizado em cenas de ação móvel.
2. **Especificações Técnicas de Vídeo**:
   - Resolução: `1080x1920 (9:16) @ 60fps`.
   - Duração ótima: `30s a 45s`.
   - Composição Visual Alternativa: Fundo ampliado com desfoque dinâmico (`boxblur=25:5`), vídeo principal centralizado e nítido (`1080x608 pad 1080:614`) com moldura ardósia (`#5E7AC4`).
3. **Composição Gráfica Glassmorphic**:
   - **Top Card**: Container escuro translúcido com faixa lateral laranja (`#F08D39`), título em `#FFFFFF` (46px bold) e subtítulo em `#F3BE7A`.
   - **Bottom Card (CTA)**: Chamada de ação magnética para o canal com glow laranja e destaque para inscrição.
4. **Sound Design & Mixagem Vertical**:
   - Ganho vocal aumentado para dispositivos móveis (`+2dB` a `+3dB`).
   - Trilha sonora BGM atenuada com ducking suave e fades de entrada/saída.
   - Disparo sincronizado de SFX de impacto (`card_pop.wav`, `whoosh_in.wav`, `chime_benchmark.wav`).

---

## 8. Protocolo de Operação e Versionamento

Sempre que a skill for aprimorada ou modificada, suas alterações devem ser sincronizadas com o repositório central:
- **Repositório Git**: `D:\GitHub\antigravity-skills`
- **Comandos**: `git add .`, `git commit -m "..."`, `git push origin main`.
