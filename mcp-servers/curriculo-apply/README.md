# 📄 Currículo Auto-Apply MCP Server

Automação completa para busca de vagas e envio silencioso de currículos em segundo plano ("por trás dos panos") via Playwright e FastMCP.

## 🚀 Instalação e Configuração Rápida

1. **Instale as dependências Python (se ainda não possuir)**:
   ```bash
   pip install "mcp[cli]" playwright
   playwright install chromium
   ```

2. **Login Inicial Interativo (One-Time Setup)**:
   Abra a pasta `D:\GitHub\antigravity-skills\skills\curriculo-auto-apply\scripts` e execute:
   ```cmd
   login.bat
   ```
   Ou via terminal:
   ```bash
   python browser_engine.py --login linkedin
   ```
   Faça login na sua conta no navegador Chromium que abrir e pressione ENTER no terminal.
   A sessão será salva de forma segura em `~/.job_sessions/session_linkedin.json`.

3. **Configuração no Antigravity**:
   Adicione ao seu `%USERPROFILE%\.gemini\config\mcp_config.json`:
   ```json
   "curriculo-apply": {
     "command": "python",
     "args": ["D:\\GitHub\\antigravity-skills\\skills\\curriculo-auto-apply\\scripts\\server.py"],
     "env": {
       "PYTHONIOENCODING": "utf-8"
     }
   }
   ```
