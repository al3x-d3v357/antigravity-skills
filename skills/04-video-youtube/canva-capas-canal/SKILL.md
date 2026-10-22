---
name: canva-capas-canal
description: >-
  Automação inteligente para atualização e geração de capas (thumbnails) do canal no Canva via Canva MCP. Permite alterar rapidamente textos, títulos, badges e pilares temáticos de acordo com o conteúdo de novos vídeos gravados, duplicar páginas e manter a consistência visual do projeto.
---

# Canva Capas do Canal (YouTube Thumbnails Automation)

Esta skill automatiza a atualização de capas (thumbnails 1280x720) do canal no Canva utilizando o servidor **Canva MCP** (`mcp-remote` / `https://mcp.canva.com/mcp`). Ela foi projetada para que o assistente altere com precisão estritamente os textos do layout oficial mantendo 100% da harmonia visual, tipográfica, composição de fundo, fotos e identidade visual originais.

---

## 🔗 Informações do Projeto no Canva

- **Link Direto de Edição:** [https://www.canva.com/design/DAHPkFMx6Sg/edit](https://www.canva.com/design/DAHPkFMx6Sg/edit)
- **Shortlink Oficial:** [https://canva.link/zg5n0ly78gj5zpf](https://canva.link/zg5n0ly78gj5zpf)
- **Design ID:** `DAHPkFMx6Sg`
- **Dimensões:** 1280 x 720 px (16:9)

---

## 📐 Regras Visuais Críticas & Mapeamento de Textos

> ⛔ **REGRA INEGOCIÁVEL:** NUNCA tente recriar a capa do zero ou alterar a foto, a lua, o fundo ou os elementos visuais gráficos. O template no Canva é a única fonte da verdade. O assistente deve **apenas manipular o texto central e o selo**, duplicando as páginas quando necessário.

A thumbnail possui uma hierarquia visual fixa com elementos posicionados estrategicamente:

| Posição no Layout | Descrição Visual | Regra Estrita de Caracteres | Exemplo Devlog IA | Exemplo Blender | Exemplo Speed Art | Exemplo Drift |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Subtítulo Topo** | Texto com tracinhos e ícone de lua | Máx. 20 caracteres | `GAME DEV • DEVLOG` | `TECH ART • BLENDER` | `TECH ART • BLENDER` | `GAME DEV • DEVLOG` |
| **Chamada Superior** | Tipografia branca grossa em destaque | **1 palavra curta (Máx. 7 caracteres)** | `CRIANDO` | `TEXTURA` | `ESPADA` | `DRIFT` |
| **Destaque Principal** | Tipografia gigante azul elétrico c/ borda | **1 ou 2 palavras (Máx. 7 a 8 caracteres)** | `COM IA` | `3D PRO` | `3D ART` | `UNITY 6` |
| **Badge Esquerdo** | Pílula ciano neon | 1 palavra curta (Máx. 8 carac.) | `DRIFT` | `MODDDIF` | `SPEED ART` | `DRIFT` |
| **Badge Direito** | Pílula roxa/azul | 1 ou 2 palavras curtas | `DESTRUIÇÃO` | `PBR SHADER` | `EEVEE/CYCLES` | `DESTRUIÇÃO` |
| **Pilar 1 (`</>`)** | Abaixo do ícone de código | Máx. 9 caracteres | `FÍSICA 3D` | `SETUP IA` | `SUBD MESH` | `FÍSICA 3D` |
| **Pilar 2 (Cérebro)**| Abaixo do ícone de IA | Máx. 11 caracteres | `DANOS REAIS` | `PROJEÇÃO IA` | `TOPOLOGIA` | `DANOS REAIS` |
| **Pilar 3 (Terminal)**| Abaixo do ícone de terminal | Máx. 10 caracteres | `IA INIMIGA` | `BLENDER 3D` | `SHADING PBR` | `IA INIMIGA` |
| **Pilar 4 (Foguete)** | Abaixo do ícone de velocidade | Máx. 11 caracteres | `PODERES HUD` | `RENDER PBR` | `3 MINUTOS` | `PODERES HUD` |
| **Selo Laranja** | Pincelada laranja no canto inferior | **Máx. 3 a 4 caracteres** | `#01` | `#02` | `#03` | `#04` |

> ⚠️ **Atenção Visual aos Limites de Largura:** O texto da **Chamada Superior** (ex: `CRIANDO`, `TEXTURA`, `ESPADA`, `DRIFT`) e o **Destaque Principal** (`COM IA`, `3D PRO`, `3D ART`, `UNITY 6`) possuem caixas de texto com largura restrita. Palavras com mais de 7-8 caracteres provocam quebra de linha indesejada sobrepondo as camadas inferiores.

---

## 🛠️ Procedimento Operacional Completo via Canva MCP

### 1. Iniciar Edição
Obtenha o `transaction_id` e a lista atual de páginas e elementos `richtexts`:
- Chamar `start-editing-transaction` passando `design_id: "DAHPkFMx6Sg"`.

### 2. Duplicar Página para Novos Vídeos
Para adicionar novas capas mantendo as anteriores intactas:
- Usar `merge-designs` com:
  ```json
  {
    "type": "modify_existing_design",
    "design_id": "DAHPkFMx6Sg",
    "operations": [
      {
        "type": "insert_pages",
        "after_page_number": 2,
        "source": {
          "type": "design",
          "design_id": "DAHPkFMx6Sg",
          "page_numbers": [1, 2]
        }
      }
    ],
    "user_intent": "Duplicate pages for new videos"
  }
  ```

### 3. Aplicar Alterações de Texto
- Chamar `perform-editing-operations` com operações `replace_text` para cada `element_id` de cada página.
- Validar se os textos respeitam estritamente a contagem de caracteres sem quebra de linha.

### 4. Salvar / Commit
- Chamar `commit-editing-transaction` com o `transaction_id` e `user_intent: "Save updated thumbnails"` para persistir as alterações permanentemente.

### 5. Exportação e Download em Alta Resolução (PNG 1280x720)
- Chamar `export-design` passando:
  ```json
  {
    "design_id": "DAHPkFMx6Sg",
    "format": { "type": "png" },
    "pages": [1, 2, 3, 4],
    "user_intent": "Export all thumbnail pages in PNG"
  }
  ```
- Baixar as URLs retornadas em `job.urls` salvando os arquivos `.png` com o nome exato de cada vídeo correspondente na pasta de postagem.

---

## 📋 Histórico de Capas Criadas no Projeto
- **Página 1 (#01):** `CRIANDO` / `COM IA` – Devlog IA Personagens 3D Pro.
- **Página 2 (#02):** `TEXTURA` / `3D PRO` – Escudo Capitão América 3D (Blender / Gemini / Affinity).
- **Página 3 (#03):** `ESPADA` / `3D ART` – Blender Sword (Speed Art 3 Min).
- **Página 4 (#04):** `DRIFT` / `UNITY 6` – Drift Projeto Timelapse (Unity 6 / Física).
