---
name: social-auto-post
description: >-
  Automação inteligente e silenciosa para publicação de conteúdos, renders 3D, vídeos turntable e devlogs no Kwai, TikTok, YouTube, Threads, Instagram e X em segundo plano via Playwright. Inclui análise obrigatória pré-postagem de páginas internacionais do exterior (@polygonrunway, @southernshotty, @megavoxels, @imphenzia) para adaptação de legendas, hashtags globais e músicas em alta, mantendo linguagem casual de dev e ZERO emojis.
---

# Social Auto-Post - Automação de Publicações & Inteligência de Tendências do Exterior (Threads, Instagram, TikTok, Kwai, YouTube & X)

Esta skill automatiza a análise de tendências internacionais e a publicação de artes 3D, demonstrações técnicas, vídeos de gameplay/turntable e devlogs diretamente no **Instagram**, **Threads**, **TikTok**, **Kwai**, **YouTube** e **X (Twitter)** de forma autônoma e em segundo plano (**"por trás dos panos"**) via Playwright.

---

## 🌍 1. Protocolo Obrigatório Pré-Postagem: Análise de Tendências do Exterior

**REGRA DE OURO:** Sempre que o Alex pedir para postar qualquer conteúdo no **Instagram** ou no **Threads**, o assistente **DEVE PRIMEIRO** executar a análise de tendências (`trend_analyzer.py`) baseada **exclusivamente em páginas do exterior** (proibido usar páginas brasileiras ou hashtags nacionais como `#jogosbrasileiros` ou `#gamesbr`).

### As 4 Páginas Internacionais de Referência (Benchmarks Oficiais)

1. **`@polygonrunway` (Roman Klco — Eslováquia | 366K+ seguidores)**
   - **Foco:** Modelagem 3D estilizada, Low-Poly, Isométrico, Hard Surface e Geometry Nodes no Blender.
   - **Estrutura de Legenda:** Gancho inicial ultra-curto e direto (*"Works like a charm..."*, *"Just slap it on the surface!"*), seguido de 1 frase técnica direta sobre o modificador ou técnica usada no Blender.
   - **Hashtags que utiliza:** `#blender3d #blendertips #hardsurface #lowpoly #lowpolyart #b3d #3dmodeling #isometricart #stylizedart`
   - **Músicas / Áudios:** Lo-Fi Chillhop minimalista, Synthwave suave instrumental ou ASMR limpo da viewport.

2. **`@southernshotty` (SouthernShotty3D — EUA | 92K+ seguidores)**
   - **Foco:** Animação de personagens 3D estilizados no Blender, ferramentas de Pixel-Art / 3D (`Blender Pixel Kit`), shaders estilo clay/toon e VFX.
   - **Estrutura de Legenda:** Abertura em estilo devlog pessoal (*"Been working on..."*), seguida de 2 a 3 frases explicando a pipeline técnica exata (câmera isométrica, preview em tempo real, rig ou shader) e fechando com uma pergunta aberta para engajamento técnico.
   - **Hashtags que utiliza:** `#blender3d #tutorials #animationfilm #3dart #pixelart #gamedev #b3d #stylized3d`
   - **Músicas / Áudios:** Cozy Indie Game OST / Upbeat Lo-Fi Beats sincronizados com o loop da animação.

3. **`@megavoxels` (Mega Voxels — EUA | 74K+ seguidores)**
   - **Foco:** Voxel Art 3D, personagens blocados (estilo ToyCube/Voxel), construções isométricas e Pixel Art.
   - **Estrutura de Legenda:** Pergunta de curiosidade técnica ou convite ao processo (*"How many voxels do you think it took to make this?"*), créditos da ferramenta utilizada e bloco denso de hashtags globais de Voxel/3D.
   - **Hashtags que utiliza:** `#voxelart #3dart #magicavoxel #voxels #voxel #voxelartist #processart #pixelart #3dmodel #gamedev`
   - **Músicas / Áudios:** Rock/Eletrônico energético em timelapses rápidos (ex: *Linkin Park - Burn It Down*) ou Chiptune / Synthwave 8-Bit.

4. **`@imphenzia` (Stefan Persson — Suécia / Austrália | Referência Global Indie GameDev)**
   - **Foco:** Low-Poly Speed Modeling no Blender (*10 Minute Modeling Challenge*) e desenvolvimento de jogos indie e física veicular na Unity.
   - **Estrutura de Legenda:** Contextualiza o desafio técnico, iluminação/compositing (Eevee / Cycles) e integração com a engine (Unity/Godot) em tom 100% autêntico de desenvolvedor.
   - **Hashtags que utiliza:** `#lowpoly #lowpolyart #3d #blender3d #blender #3dart #gamedev #indiegamedev #cgi #3dmodeling #3dmodel #characterdesign #dailyrender #gameart #unity #unity3d #indiegame #indiedev #3drender #eevee`
   - **Músicas / Áudios:** Synthwave / Retrowave anos 80 de ritmo marcado (*Narvent*, *Hotel Pools*, *Krosia*, *Forhill*, *The Midnight*).

---

## 🎯 2. Diretrizes Obrigatórias de Publicação do Alex

1. **PROIBIDO O USO DE EMOJIS (Regra Absoluta):**
   - Nunca insira nenhum tipo de emoji no texto ou na legenda das postagens. O `trend_analyzer.py` remove automaticamente qualquer emoji ou bullet colorido antes do envio.

2. **Adaptação da Legenda (Fórmula Internacional para o Conteúdo do Alex):**
   - **Linha 1 (Hook Direto estilo `@polygonrunway`):** Frase curta destacando o resultado visual ou mecânica principal.
   - **Corpo Técnico (Estilo `@southernshotty` + Devlog do Alex):** Lista enxuta com traços simples (`-`) detalhando o que foi implementado (ex: física de impacto, rig de 3 ossos ToyCube, iluminação de estúdio, shader ou IA inimiga).
   - **Fechamento (Engajamento Dev estilo `@megavoxels`):** Comentário ou pergunta técnica casual sobre o projeto.

3. **Clusters de Hashtags 100% Internacionais (Sem Tags Brasileiras):**
   - **Unity / GameDev:** `#madewithunity #unity3d #unity6 #gamedev #indiegamedev #indiegame #gamedevelopment #gamedesign #csharp #3dart #lowpoly #b3d #devlog #gameart`
   - **Godot / GameDev:** `#godotengine #godot4 #gamedev #indiegamedev #indiegame #gamedevelopment #gamedesign #b3d #blender3d #lowpoly #gameart #devlog`
   - **Blender 3D / Low-Poly:** `#blender3d #b3d #blendertips #lowpoly #lowpolyart #3dmodeling #3dart #3dmodel #stylizedart #hardsurface #characterdesign #3drender #gameart #indiegamedev`
   - **Voxel Art / ToyCube:** `#voxelart #voxels #voxel #voxelartist #magicavoxel #3dart #lowpoly #blender3d #b3d #3dmodel #gameart #indiegamedev #characterdesign #processart`
   - **Pixel Art / 2D:** `#pixelart #2dart #sprites #gamedev #indiegamedev #indiegame #gameart #retrogame #gamedevelopment #pixelartist`

4. **Tendências de Músicas Recomendadas por Categoria:**
   - **Gameplay de Ação / Física Veicular / Unity 6:**
     1. *Narvent - Fainted* (Synthwave / Dark Retrowave — alta retenção em física e veículos)
     2. *Synthwave Outrun 120 BPM / Phonk Instrumental Suave* (cortes dinâmicos de gameplay)
     3. *Linkin Park - Burn It Down* (usado por `@megavoxels` em showcases rápidos)
   - **Blender 3D / Speed Modeling / Turntable:**
     1. *Hotel Pools - Eclipse* (Chill Synthwave — padrão gringo para modelagem e hard surface)
     2. *Krosia - Azur* (Ambient Synthwave — excelente para turntables 360 e clay render)
     3. *Forhill - Odyssey* (Retrowave Atmosférico — transição wireframe para render final)
   - **Animação de Personagens / Voxel / ToyCube:**
     1. *Lo-Fi Girl / Chillhop Beats Instrumental 90 BPM* (padrão `@polygonrunway` e `@southernshotty`)
     2. *Chiptune / Cozy Arcade Instrumental* (ideal para ciclos de walk, attack e skill cast)

5. **Cadência de Postagem (Um de Cada Vez):**
   - Sempre disparar **uma postagem por vez**, executando a análise de tendências antes de cada envio.

---

## 🔐 3. Sessões Conectadas (Instagram & Threads)

- **Conta Conectada:** `@arthursantos.real` / `@al3x_d3v357` (*"Alex RJ, apenas um desenvolvedor de jogos."*)
- **Arquivos de Sessão Persistente:**
  - Instagram: `~/.social_sessions/session_instagram.json` (e espelho em `/media/alex/alex/mcp-servers/social_sessions/session_instagram.json`)
  - Threads: `~/.social_sessions/session_threads.json` (autenticado via SSO de 1 clique com a conta do Instagram em `https://www.threads.com/`)
  - Relatório da Última Análise de Tendências: `~/.social_sessions/latest_trend_analysis.json`

---

## 🛠️ 4. Comandos de Execução (Linux)

Interpretador Python recomendado com Playwright:
`/media/alex/alex/softwares/blender-5.2.2-linux-x64/5.2/python/bin/python3.13`
Scripts localizados em: `/home/alex/.gemini/config/skills/social-auto-post/scripts/`

### Passo 1 (Obrigatório antes de postar): Analisar Tendências de Tags, Música e Legenda
```bash
/media/alex/alex/softwares/blender-5.2.2-linux-x64/5.2/python/bin/python3.13 /home/alex/.gemini/config/skills/social-auto-post/scripts/trend_analyzer.py --post "Texto base do post" --media "/caminho/arquivo.mp4"
```
*(Adicione `--live` para consultar as páginas gringas ao vivo no Instagram via Playwright antes de gerar a recomendação).*

### Passo 2: Publicar no Threads (Executa a análise de tendências automaticamente)
```bash
/media/alex/alex/softwares/blender-5.2.2-linux-x64/5.2/python/bin/python3.13 /home/alex/.gemini/config/skills/social-auto-post/scripts/threads_poster.py --post "Texto casual adaptado" --media "/caminho/render.png"
```

### Passo 3: Publicar no Instagram (Executa a análise de tendências automaticamente)
```bash
/media/alex/alex/softwares/blender-5.2.2-linux-x64/5.2/python/bin/python3.13 /home/alex/.gemini/config/skills/social-auto-post/scripts/instagram_poster.py --post "Texto casual adaptado" --media "/caminho/render.png"
```

---

## 📋 Resumo das Regras para o Assistente

| Critério | Instrução Estrita |
| :--- | :--- |
| **Análise Pré-Post** | **Obrigatória.** Sempre rodar `trend_analyzer.py` antes de postar no Instagram ou Threads. |
| **Referências** | **100% Exterior** (`@polygonrunway`, `@southernshotty`, `@megavoxels`, `@imphenzia`). Zero páginas brasileiras. |
| **Emojis** | **ZERO emojis.** Banido totalmente das postagens. |
| **Tom da Legenda** | Hook técnico curto + lista limpa com `-` + pergunta casual de dev (adaptado das páginas gringas). |
| **Hashtags** | Exclusivamente tags internacionais de alto alcance no nicho (`#blender3d #b3d #indiegamedev #voxelart #madewithunity`). |
| **Músicas** | Sempre apresentar as 3 faixas internacionais em alta recomendadas para o estilo do vídeo/post. |
