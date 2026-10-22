# 🕹️ GameMaker MCP Server

Automação e controle de projetos GameMaker via Model Context Protocol.

## 🚀 Instalação (Pós-Formatação)

1. **Clone e Instale dependências**:
   ```bash
   cd D:\GitHub\gamemaker-antigravity-mcp
   npm install
   npm run build
   ```

2. **Configuração no Antigravity**:
   Adicione ao `~/.gemini/config/mcp_config.json`:
   ```json
   "gamemaker": {
     "command": "node",
     "args": ["D:\\GitHub\\gamemaker-antigravity-mcp\\dist\\index.js"]
   }
   ```
