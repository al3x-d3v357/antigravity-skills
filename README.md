# ⚡ Antigravity Skills & MCP Hub

> Hub unificado e definitivo de **Skills** e **MCP Servers** (Model Context Protocol) para o **Google Antigravity IDE** e **OpenCode**.
> Desenvolvido e mantido por **Alex Sandro ([@al3x-d3v357](https://github.com/al3x-d3v357))**.

---

## 📦 Lista de Skills Organizadas por Categoria (55 Skills Ativas)

Todas as skills estão estruturadas em 8 categorias temáticas dentro de [`skills/`](./skills/):

### 🎮 01. Game Development - Unity (`01-gamedev-unity/`)
| Skill | Descrição |
| :--- | :--- |
| **`game-design-entre-blender-e-unity-cli`** | Pipeline de Game Design unindo Blender via MCP e Unity Engine operada via CLI (batchmode/headless). |
| **`unity-cli-compiler-validator`** | Valida a compilação do projeto Unity via CLI e retorna apenas status booleano e a linha de falha. |
| **`log-slicer-diagnostic`** | Filtra logs brutos da Unity e do compilador, isolando apenas a linha exata do erro e economizando contexto. |
| **`csharp-ast-indexer`** | Fornece assinaturas e métodos de scripts C# existentes sem carregar o código-fonte completo no prompt. |
| **`fsm-logic-decoupler`** | Modela lógica de movimentação, bots e regras de jogo em C# puro desconectado de MonoBehaviour para economia de tokens. |
| **`asset-catalog-schema`** | Lê e mantém o manifesto de assets disponíveis (modelos, áudios, texturas) evitando comandos repetidos de listagem. |
| **`unity-gameplay-systems`** | Arquitetura, Player Controllers 2D/3D, Cinemachine, combat systems e UI TMP. |
| **`unity-cli`** | Controle do Unity Editor via linha de comando, testes, builds e automações. |
| **`unity-docs-first`** | Workflow mandatório de consulta prévia à documentação oficial do Unity 6. |
| **`unity-mcp`** | Orquestração do Unity Editor via MCP (GameObjects, cenas, componentes e testes). |
| **`unity-pipeline`** | Loop de testes headless, compilação de scripts e hot reload C# em runtime. |
| **`unity-probuilder`** | Grayboxing, modelagem procedural e criação de fases 3D com ProBuilder. |
| **`mcp-source`** | Alternância rápida de versões e branches do pacote MCP for Unity. |

### 👾 02. Game Development - Godot (`02-gamedev-godot/`)
| Skill | Descrição |
| :--- | :--- |
| **`godot-multigenre-antigravity`** | Scaffolding para Tower Defense, jogos táticos por turnos e naves/veículos antigravitacionais. |
| **`godot-autochess-battle-logic`** | Combate automático em grelha com AStarGrid2D, FSM de gladiadores e fases da partida. |
| **`godot-data-driven-architecture`** | Arquitetura orientada a dados via Custom Resources (.tres), Event Bus global e nós modulares. |
| **`godot-isometric-vehicle-physics`** | Física arcade de veículos em perspectiva isométrica (2.5D/3D) com drift e suspensão suave. |

### 🎨 03. Modelagem e Animação 3D (`03-3d-blender/`)
| Skill | Descrição |
| :--- | :--- |
| **`blender-mcp-batch-runner`** | Agrupa comandos do Blender em um único script Python (bpy) atômico para execução via MCP, eliminando vaivém de turnos. |
| **`blender-affinity-texturing`** | Extração de mapas UV de faces no Blender, pintura no Serif Affinity e aplicação direta no Base Color. |
| **`blender-to-unity`** | Handoff e importação direta de modelos do Blender para a Unity via MCP. |
| **`toycub-blender-animator`** | Pacote com 8 ações de animações procedurais estilizadas para personagens ToyCube no Blender. |

### 🎬 04. Vídeo e Produção Audiovisual (`04-video-youtube/`)
| Skill | Descrição |
| :--- | :--- |
| **`drift-video-editor`** | Pós-produção avançada no Drift MCP: remoção acústica de silêncios, punch-in e timelapses. |
| **`kdenlive-editor`** | Montagem e edição de vídeo profissional na timeline do Kdenlive via MCP. |
| **`youtube-studio-uploader`** | Upload automatizado de vídeos completos, miniaturas, títulos, tags e agendamento no YouTube Studio. |
| **`youtube-seo-retencao`** | Estratégia completa de SEO, CTR magnético, retenção e roteirização para o canal do YouTube. |
| **`youtube-thumbnail-designer`** | Criação e design de capas profissionais de alta conversão para o YouTube. |
| **`canva-capas-canal`** | Automação e geração de thumbnails para o YouTube via Canva MCP. |

### 📈 05. Marketing, SEO e Copywriting (`05-marketing-seo-copy/`)
| Skill | Descrição |
| :--- | :--- |
| **`ab-copy-variants-generator`** | Geração de 5 variantes testáveis de copy com diferentes alavancas de conversão. |
| **`cta-optimizer`** | Reescrita e otimização de chamadas para ação (CTAs) em e-mails e páginas de vendas. |
| **`hook-engineer`** | Criação de 10 ganchos de abertura irresistíveis para capturar a atenção imediata. |
| **`content-optimizer`** | Otimização de SEO on-page, legibilidade e densidade de palavras-chave. |
| **`seo-intent-analyzer`** | Análise de intenção de busca para ranqueamento na primeira página do Google. |
| **`linkedin-post-generator`** | Redação de publicações de alto engajamento no LinkedIn usando padrões comprovados. |
| **`campaign-retrospective-builder`** | Retrospectiva estruturada de resultados e hipóteses pós-campanha de marketing. |
| **`partnership-proposal-writer`** | Redação e resposta de propostas comerciais de patrocínio e parcerias. |

### 🤖 06. Automação e Redes Sociais (`06-automacao-redes-sociais/`)
| Skill | Descrição |
| :--- | :--- |
| **`social-auto-post`** | Publicação autônoma de artes 3D e novidades no Threads, Instagram, X e TikTok via Playwright. |
| **`blogspot-automation-pipeline`** | Publicação autônoma de artigos técnicos e renders 3D no Blogger com captura via Playwright. |
| **`curriculo-auto-apply`** | Busca e candidatura automática a vagas de TI (InfoJobs, LinkedIn, Gupy). |
| **`ong-triagem-cadastro`** | Triagem e cadastro automatizado de dados da ONG One by One (WhatsApp -> Google Sheets). |

### 📄 08. Produtividade e Documentação (`08-produtividade-documentos/`)
| Skill | Descrição |
| :--- | :--- |
| **`csv-to-presentations`** | Conversão de dados tabulares (CSV/Excel) em apresentações PowerPoint formatadas. |
| **`document-converter`** | Conversor universal de documentos entre Markdown, DOCX e PDF com extração de texto. |
| **`meeting-notes-extractor`** | Extração estruturada de atas, decisões e itens de ação a partir de reuniões. |
| **`notes-to-powerpoint`** | Transformação de rascunhos, anotações e tópicos em pitch decks profissionais. |
| **`writing-partner`** | Assistente de redação, citações, melhoria estrutural e escrita colaborativa. |
| **`career-ladder-builder`** | Construção de matriz e framework de progressão de carreira em 4 níveis. |
| **`job-description-optimizer`** | Otimização e reescrita de descrições de vagas para recrutamento assertivo. |
| **`decision-logger`** | Registro formal de decisões técnicas e de arquitetura (ADRs) para wikis de equipe. |
| **`project-changelog-tracker`** | Documentação incremental de versões e histórico de entregas de projetos. |
| **`comprehensive-research`** | Sistema avançado de pesquisa, síntese e investigação em múltiplos níveis. |

### 🧠 09. IA, Workflows & Antigravity (`09-ia-workflows-antigravity/`)
| Skill | Descrição |
| :--- | :--- |
| **`code-patch-diff-engine`** | Aplica alterações cirúrgicas de código via SEARCH/REPLACE para evitar a reescrita de arquivos inteiros e economizar tokens. |
| **`atomic-step-scaffolder`** | Fraciona planos complexos de jogos em microetapas sequenciais estritas, impedindo a geração de respostas gigantescas. |
| **`session-delta-tracker`** | Registra um resumo operacional de 5 linhas ao final de cada execução para manter contexto persistente entre sessões. |
| **`architect-agent-bridge`** | Orquestração em duas fases (extração de contexto e execução estrita) com modelo Gemini arquiteto. |
| **`ask-matt`** | Roteador inteligente para escolher qual skill ou workflow melhor se aplica à tarefa. |
| **`token-budget-optimizer`** | Otimização inteligente de consumo de tokens, contexto e chamadas de MCP. |

---

## 🔌 MCP Servers Integrados

| Servidor MCP | Tipo / Protocolo | Finalidade Principal |
| :--- | :--- | :--- |
| **`canva`** | Remote / `mcp-remote` | Automação de design, geração de posts, capas de canal e busca de assets no Canva. |
| **`blender`** (`mcp-for-blender`) | `uvx` / Python | Automação de modelagem, execução de scripts e rigging no Blender. |
| **`unity-mcp`** | Stdio / Node (Unity MCP) | Criação de GameObjects, gerenciamento de cenas, componentes e build no Unity. |
| **`gamemaker`** | Python/Node MCP | Manipulação de assets, scripts GML e salas no GameMaker Studio. |
| **`StitchMCP`** | NPX / Google Stitch | Integração de design, prototipação e layout de interfaces. |

---

## 🚀 Instalação e Restauração Rápida (1 Clique)

### No Linux/macOS:
```bash
./install_in_antigravity.sh
```

### No Windows (PowerShell):
```powershell
powershell.exe -ExecutionPolicy Bypass -File .\install.ps1
```

---

## 📁 Estrutura do Repositório

```text
antigravity-skills/
├── .agents/
│   └── skills.json                      (mapeamento de categorias para Antigravity IDE)
├── skills/                              (55 skills divididas em 8 categorias)
│   ├── README.md                        (índice detalhado de skills)
│   ├── 01-gamedev-unity/                (13 skills Unity, Game Design CLI, Parsers & AST)
│   ├── 02-gamedev-godot/                (4 skills Godot)
│   ├── 03-3d-blender/                   (4 skills Blender, Batch Runner & 3D)
│   ├── 04-video-youtube/                (6 skills de vídeo, edição e canal)
│   ├── 05-marketing-seo-copy/           (8 skills de copy, SEO e marketing)
│   ├── 06-automacao-redes-sociais/      (4 skills de redes sociais e automação)
│   ├── 08-produtividade-documentos/     (10 skills de docs, slides e pesquisa)
│   └── 09-ia-workflows-antigravity/     (6 skills de IA, Diff Engine, Atomic Scaffolder e otimização)
├── mcp-servers/                         (servidores MCP integrados e configuradores)
├── opencode.jsonc                       (declaração de categorias de skills e MCPs)
├── install_in_antigravity.sh            (instalador Linux Antigravity)
├── install.ps1                          (instalador PowerShell Windows)
├── install.sh                           (instalador Bash genérico)
├── .gitignore
└── README.md
```

---

## 📄 Licença
Distribuído sob a licença MIT. Criado e mantido por **Alex Sandro ([@al3x-d3v357](https://github.com/al3x-d3v357))**.
