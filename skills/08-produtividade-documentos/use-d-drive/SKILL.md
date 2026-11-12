---
name: use-d-drive
description: >-
  Enforces strict and exclusive use of the D: drive (D:\) for all project workspaces, repository clones, file operations, temporary scratchpads, builds, downloads, and media assets, keeping C: drive completely free and untouched. Triggers whenever files are created, projects are initiated, repositories are cloned, or working directories are configured.
---

# Use D: Drive Enforcement Skill

Garante a utilização obrigatória e exclusiva do disco secundário **D:** (`D:\`) para todas as atividades de desenvolvimento, manipulação de arquivos, criação de projetos, clones de repositórios Git, pastas de trabalho, compilações (builds) e armazenamento de mídias, preservando o disco C: livre e desobstruído.

---

## 1. Regras Mandatórias de Diretório

1. **Raiz de Projetos Centralizada em `D:\Projetos\`**:
   - Todo novo projeto, repositório clonado, aplicativo móvel (Flutter), jogo (Unity/Godot), software (C++/Desktop) ou modelo 3D deve ser criado dentro de `D:\Projetos\` na sua respectiva subpasta categorizada:
     - `D:\Projetos\Flutter\`: Aplicativos e testes Flutter/Dart.
     - `D:\Projetos\Unity\`: Projetos e assets da Unity Engine.
     - `D:\Projetos\Drift\`: Projetos, builds e assets do Drift Video Editor.
     - `D:\Projetos\3D\`: Arquivos do Blender (`.blend`), modelos `.fbx`, scripts de animação e assets 3D.
   - **Proibição Estrita no Disco C:**: É terminantemente proibido clonar repositórios, iniciar novos projetos ou salvar entregáveis no disco `C:\` ou em pastas de usuário (`C:\Users\...`), salvo se o usuário solicitar explicitamente uma configuração de sistema.

2. **Arquivos Temporários e Scratchpads**:
   - Qualquer processamento temporário, script descartável, exportação intermediária ou downloads temporários deve ser direcionado para `D:\temp\` ou para a pasta isolada do respectivo projeto em `D:\Projetos\<categoria>\<projeto>\`.

3. **Preservação e Limpeza da Raiz do Disco D:**:
   - A raiz `D:\` deve permanecer rigorosamente limpa e desobstruída.
   - NUNCA despejar arquivos soltos, instaladores `.zip`, instaladores `.exe` ou arquivos de log diretamente em `D:\`.
   - Pastas protegidas de inicializadores de jogos (ex: `D:\epicgames`) e pastas de sistema (`$RECYCLE.BIN`, `System Volume Information`) devem ser mantidas intactas e não devem ser misturadas com projetos.

4. **Remoção de Pastas Vazias**:
   - Pastas temporárias ou diretórios sem conteúdo que perderem utilidade devem ser limpos para evitar poluição visual no sistema de arquivos.
