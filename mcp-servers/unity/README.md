# 🎮 Unity MCP Server

Orquestração e automação do Unity Editor via Model Context Protocol.

## 🚀 Instalação (Pós-Formatação)

1. **Instale o pacote MCP for Unity no projeto Unity**:
   - No Unity Editor, abra **Window > Package Manager**.
   - Adicione via git URL: `https://github.com/Unity-Technologies/com.unity.ai.assistant.git` (ou pacote local em `D:\GitHub\unity-mcp`).

2. **Relay Executável**:
   - O executável do relay fica localizado em `%USERPROFILE%\.unity\relay\relay_win.exe`.

3. **Configuração no Antigravity**:
   Adicione ao `~/.gemini/config/mcp_config.json`:
   ```json
   "unity-mcp": {
     "command": "C:\\Users\\alexa\\.unity\\relay\\relay_win.exe",
     "args": ["--mcp"]
   }
   ```
