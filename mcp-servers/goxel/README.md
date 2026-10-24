# 🧱 Goxel Voxel Art MCP Server

Servidor de automação e modelagem 3D em Voxel Art utilizando o **Goxel (0.15.1)** via Model Context Protocol (MCP) para o **Antigravity IDE**.

Permite a criação procedural de personagens (Arqueiro, Tanque, Mago, Suporte), itens, armas e cenários, exportação automática para `.vox` e `.obj`, além de abertura interativa na interface visual.

---

## 🛠️ Ferramentas Disponíveis

1. `goxel_create_character`: Constrói classes de heróis em Voxel Art 3D com exportação `.vox` e `.obj`.
2. `goxel_create_object`: Constrói armas (espadas, cajados, arcos, escudos), baús, poções e tochas.
3. `goxel_run_custom_script`: Executa scripts procedurais QuickJS internamente no Goxel.
4. `goxel_export_model`: Converte modelos para `.vox`, `.obj`, `.gltf` e `.png`.
5. `goxel_open_gui`: Abre a interface visual do Goxel na tela para edição manual.

---

## 🚀 Configuração no Antigravity

Adicione ao seu arquivo de configuração de MCP (`mcp_config.json` ou `opencode.jsonc`):

```json
"goxel": {
  "command": "node",
  "args": ["/media/alex/alex/antigravity-skills/al3x-antigravity-skills/mcp-servers/goxel/server.js"]
}
```
