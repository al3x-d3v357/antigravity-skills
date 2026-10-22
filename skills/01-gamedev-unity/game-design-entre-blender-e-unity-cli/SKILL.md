---
name: game-design-entre-blender-e-unity-cli
description: Pipeline de Game Design unindo Blender via MCP para modelagem/rigging procedural e Unity Engine operada via CLI (batchmode/headless).
---

# Game Design entre Blender e Unity CLI

Pipeline profissional de desenvolvimento de jogos integrando a criação e tratamento de malhas no Blender (via MCP) com a gestão, importação e compilação automatizada na Unity Engine diretamente pelo terminal (CLI headless/batchmode).

## 1. Escopo e Diretrizes
- **Engine Alvo:** Unity Engine (versão 6 ou LTS), operada estritamente via terminal/CLI (`-batchmode`, `-quit`).
- **Criação de Modelos 3D:** Blender operado atomicamente via Blender MCP com scripts Python (`bpy`).
- **Automação sem Interface:** Todo o ciclo de vida do projeto pode ser executado e validado em segundo plano.

## 2. Automação Unity via CLI
- **Setup e Inicialização:**
  ```bash
  "<UNITY_PATH>" -batchmode -quit -createProject "<PROJECT_PATH>" -logFile "<PROJECT_PATH>/create_project.log"
  ```
- **Pipeline de Importação Automatizada:**
  Rotinas C# de editor acionadas via `-executeMethod`:
  ```bash
  "<UNITY_PATH>" -batchmode -quit -projectPath "<PROJECT_PATH>" -executeMethod AssetImportAutomator.ProcessAssets -logFile "<PROJECT_PATH>/import.log"
  ```
- **Compilação e Build Headless (Windows/Linux):**
  ```bash
  "<UNITY_PATH>" -batchmode -quit -projectPath "<PROJECT_PATH>" -buildWindows64Player "<BUILD_OUTPUT_PATH>/Game.exe" -logFile "<PROJECT_PATH>/build.log"
  ```

## 3. Integração com Blender via MCP
- **Modelagem e Tratamento:**
  Geração procedural de arenas, ajuste de escala, configuração de pontos de pivô e centralização de centro de massa diretamente no Blender via scripts Python (`bpy`).
- **Exportação Direta para Unity:**
  Todos os modelos gerados são exportados como `.fbx` ou `.glb` diretamente para a pasta `Assets/Models/` do projeto Unity com `apply_unit_scale=True`.
- **Estrutura de Execução:**
  1. Prompt Executivo para o Agente.
  2. Script Python (`bpy`) Completo e autocontido.
  3. Resumo Operacional informando nome das malhas geradas e destino no projeto.
