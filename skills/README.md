# 📚 Índice de Skills por Categoria

Este diretório contém todas as **55 Skills** do ecossistema Antigravity & OpenCode, devidamente separadas e organizadas por pilares temáticos:

---

### 🎮 01. Game Development - Unity (`01-gamedev-unity/`)
> Ferramentas, automações, arquitetura profissional e otimização para desenvolvimento na **Unity Engine 6**.

- **`game-design-entre-blender-e-unity-cli`**: Pipeline de Game Design unindo Blender via MCP e Unity Engine operada via CLI (batchmode/headless).
- **`unity-cli-compiler-validator`**: Valida a compilação do projeto Unity via CLI e retorna apenas status booleano e a linha de falha.
- **`log-slicer-diagnostic`**: Filtra logs brutos da Unity e do compilador, isolando apenas a linha exata do erro e economizando contexto.
- **`csharp-ast-indexer`**: Fornece assinaturas e métodos de scripts C# existentes sem carregar o código-fonte completo no prompt.
- **`fsm-logic-decoupler`**: Modela lógica de movimentação, bots e regras de jogo em C# puro desconectado de MonoBehaviour para economia de tokens.
- **`asset-catalog-schema`**: Lê e mantém o manifesto de assets disponíveis (modelos, áudios, texturas) evitando comandos repetidos de listagem.
- **`unity-gameplay-systems`**: Arquitetura desacoplada, Player Controllers 2D/3D, Cinemachine, sistemas de vida/combate e UI TextMeshPro.
- **`unity-cli`**: Controle do Unity Editor via CLI/terminal, compilação, testes automatizados e builds headless.
- **`unity-docs-first`**: Workflow mandatório de consulta à documentação local oficial do Unity 6 antes da implementação.
- **`unity-mcp`**: Manipulação e criação de GameObjects, componentes e cenas na Unity via Model Context Protocol.
- **`unity-pipeline`**: Loop automatizado de compilação, execução de testes e recarregamento C# em tempo de execução.
- **`unity-probuilder`**: Modelagem 3D, graybox, blocking e criação procedural de fases com ProBuilder via MCP.
- **`mcp-source`**: Alternância rápida de versões e branches do pacote oficial `mcp-for-unity`.

---

### 👾 02. Game Development - Godot (`02-gamedev-godot/`)
> Scaffolding, física arcade e arquitetura de dados para a **Godot Engine 4**.

- **`godot-multigenre-antigravity`**: Scaffolding para Tower Defense, jogos táticos por turnos e veículos antigravitacionais.
- **`godot-autochess-battle-logic`**: Lógica de combate automático em grelha AStarGrid2D, FSM de gladiadores e fases da partida.
- **`godot-data-driven-architecture`**: Estrutura orientada a dados via Custom Resources (.tres), Event Bus global e nós modulares.
- **`godot-isometric-vehicle-physics`**: Física arcade 2.5D/3D para veículos em visão isométrica com drift e amortecimento suave.

---

### 🎨 03. Modelagem e Animação 3D (`03-3d-blender/`)
> Automações de rigging, UV unwrapping e handoff entre **Blender**, **Affinity** e **Engines**.

- **`blender-mcp-batch-runner`**: Agrupa comandos do Blender em um único script Python (bpy) atômico para execução via MCP, eliminando vaivém de turnos.
- **`blender-affinity-texturing`**: Workflow de exportação de UV de faces no Blender, pintura no Affinity e texturização no Base Color.
- **`blender-to-unity`**: Pipeline de exportação e handoff direto de modelos 3D do Blender para a Unity via MCP.
- **`toycub-blender-animator`**: Pacote de 8 animações procedurais e estilizadas para rigs verticais de 3 ossos estilo ToyCube.

---

### 🎬 04. Vídeo e Produção Audiovisual (`04-video-youtube/`)
> Edição, montagem, criação de capas e publicação para **YouTube**, **Drift** e **Kdenlive**.

- **`drift-video-editor`**: Pós-produção avançada no Drift MCP: remoção acústica de silêncios, punch-in dinâmico e timelapses.
- **`kdenlive-editor`**: Montagem profissional de vídeo, corte de timeline, aplicação de efeitos e renderização via MCP.
- **`youtube-studio-uploader`**: Upload automatizado de vídeos completos, capas, descrições, tags e agendamento no YouTube Studio.
- **`youtube-seo-retencao`**: Otimização completa de SEO, CTR magnético, retenção e roteirização para o canal do YouTube.
- **`youtube-thumbnail-designer`**: Design de capas de alta conversão como arquivos PNG para o YouTube.
- **`canva-capas-canal`**: Atualização e geração dinâmica de capas/thumbnails no Canva via Canva MCP.

---

### 📈 05. Marketing, SEO e Copywriting (`05-marketing-seo-copy/`)
> Estratégia de conteúdo, redação persuasiva e otimização para mecanismos de busca.

- **`ab-copy-variants-generator`**: Geração de 5 variantes testáveis de copy com diferentes alavancas de conversão.
- **`cta-optimizer`**: Otimização e reescrita de chamadas para ação (CTAs) em landing pages e e-mails.
- **`hook-engineer`**: Criação de 10 ganchos de abertura irresistíveis para prender a atenção do leitor.
- **`content-optimizer`**: Otimização de SEO on-page, densidade de palavras-chave e legibilidade de textos.
- **`seo-intent-analyzer`**: Análise de intenção de busca para ranqueamento nos primeiros resultados do Google.
- **`linkedin-post-generator`**: Redação de publicações de alto engajamento no LinkedIn usando padrões comprovados.
- **`campaign-retrospective-builder`**: Retrospectiva estruturada pós-campanha para extração de métricas e hipóteses.
- **`partnership-proposal-writer`**: Redação e respostas formais para propostas de patrocínio e parcerias comerciais.

---

### 🤖 06. Automação e Redes Sociais (`06-automacao-redes-sociais/`)
> Automações inteligentes em segundo plano com Playwright e integração de serviços.

- **`social-auto-post`**: Publicação silenciosa de artes 3D e novidades no Threads, Instagram, X e TikTok via Playwright.
- **`blogspot-automation-pipeline`**: Publicação e formatação autônoma de tutoriais e renders no Blogger.
- **`curriculo-auto-apply`**: Busca e envio inteligente de currículos para vagas de TI (InfoJobs, LinkedIn, Gupy).
- **`ong-triagem-cadastro`**: Triagem e cadastro automático de pacientes da ONG One by One do WhatsApp para Google Sheets.

---

### 📄 08. Produtividade e Documentação (`08-produtividade-documentos/`)
> Gestão de conhecimento, relatórios, apresentações e conversão de arquivos.

- **`csv-to-presentations`**: Conversão de dados tabulares (CSV/Excel) em apresentações PowerPoint formatadas com gráficos.
- **`document-converter`**: Conversor universal entre Markdown, DOCX e PDF com extração de texto.
- **`meeting-notes-extractor`**: Extração estruturada de atas, decisões e itens de ação a partir de transcrições de reuniões.
- **`notes-to-powerpoint`**: Transformação de rascunhos, anotações e tópicos em pitch decks e apresentações profissionais.
- **`writing-partner`**: Co-autor e revisor para pesquisa, citações, melhoria de estrutura e escrita técnica.
- **`career-ladder-builder`**: Construção de plano de progressão de carreira com competências e níveis claros.
- **`job-description-optimizer`**: Otimização de anúncios de vagas para atrair os melhores candidatos.
- **`decision-logger`**: Registro formal de decisões técnicas e arquiteturais (ADRs) para wikis de equipe.
- **`project-changelog-tracker`**: Documentação incremental de versões e histórico de entregas de projetos.
- **`comprehensive-research`**: Sistema avançado de pesquisa, coleta de fontes e análise de conteúdo em múltiplos níveis.

---

### 🧠 09. IA, Workflows & Antigravity (`09-ia-workflows-antigravity/`)
> Orquestração de modelos, roteamento e otimização máxima de tokens do agente Antigravity.

- **`code-patch-diff-engine`**: Aplica alterações cirúrgicas de código via SEARCH/REPLACE para evitar a reescrita de arquivos inteiros e economizar tokens.
- **`atomic-step-scaffolder`**: Fraciona planos complexos de jogos em microetapas sequenciais estritas, impedindo a geração de respostas gigantescas.
- **`session-delta-tracker`**: Registra um resumo operacional de 5 linhas ao final de cada execução para manter contexto persistente entre sessões.
- **`architect-agent-bridge`**: Fluxo em duas fases (extração de contexto e execução estrita) entre modelo local e modelo arquiteto (Gemini).
- **`ask-matt`**: Roteador inteligente para escolher qual skill ou workflow melhor se aplica ao seu objetivo atual.
- **`token-budget-optimizer`**: Monitoramento e economia inteligente de tokens, limites de contexto e chamadas de MCP.
