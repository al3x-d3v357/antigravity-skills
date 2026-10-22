---
name: blender-mcp-batch-runner
description: Agrupa comandos do Blender em um único script Python (bpy) atômico para execução via MCP, eliminando vaivém de turnos.
---

# Blender MCP Batch Runner

Toda manipulação no Blender deve ocorrer em uma única chamada via MCP. É estritamente proibido fragmentar operações.

## Estrutura do Script bpy Obrigatório
1. **Reset da Cena:** Limpeza de malhas orfãs e coleções temporárias.
2. **Geração/Transformação:** Modelagem procedural, aplicação de chanfros (*bevel*) e ajuste de origem no pivô/base.
3. **Unwrap e Materiais:** Atribuição de paleta de cores básicas em nós de material principiado.
4. **Exportação Automática:** Exportar diretamente para `Assets/Models/<nome_asset>.fbx` com `apply_unit_scale=True`.

## Formato de Entrega
- **Prompt Executivo para o Agente**
- **Script Python (bpy) Completo** (autocontido, com tratamento `try/except`)
- **Resumo Operacional** (3 linhas com nomes de malhas geradas e caminho do arquivo)
