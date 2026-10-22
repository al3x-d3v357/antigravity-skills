# 🧊 Blender MCP Server

Conexão e controle total do Blender via MCP para modelagem, rigging, animação e renderização.

## 🚀 Instalação (Pós-Formatação)

1. **Instale o gerenciador UV (se não tiver)**:
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Instale o Addon no Blender**:
   - Baixe o addon `mcp-for-blender` ou instale via Preferences > Add-ons no Blender.
   - Ative o addon **BlenderMCP**.

3. **Configuração no Antigravity**:
   Adicione ao `~/.gemini/config/mcp_config.json`:
   ```json
   "blender": {
     "command": "uvx",
     "args": ["--python", "3.11", "mcp-for-blender"],
     "env": {
       "UV_PYTHON_PREFERENCE": "only-managed",
       "PYTHONIOENCODING": "utf-8"
     }
   }
   ```
