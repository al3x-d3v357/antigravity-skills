# 🎨 Canva MCP Server

Servidor oficial do Canva via Model Context Protocol (MCP) para automação de design, criação de posts, capas de canal e busca de assets.

## 🔗 Endpoint Oficial

- **URL:** `https://mcp.canva.com/mcp`
- **Protocolo:** Remote MCP / SSE via `mcp-remote`

## 🚀 Configuração no Antigravity IDE

Adicione ao `~/.gemini/config/mcp_config.json`:
```json
"canva": {
  "command": "npx",
  "args": [
    "-y",
    "mcp-remote",
    "https://mcp.canva.com/mcp"
  ]
}
```

## 🔑 Autenticação

Na primeira execução, o `mcp-remote` abrirá o navegador para login e autorização OAuth na sua conta do Canva.