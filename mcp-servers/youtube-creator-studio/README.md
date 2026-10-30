# 🎬 YouTube Studio MCP Server

Servidor de automação do **YouTube Studio** via Playwright e Model Context Protocol (MCP) para o **Google Antigravity IDE**.

Permite o envio automático de vídeos completos com **títulos, descrições, tags, capas personalizadas (thumbnails)** e visibilidade (*Público, Não-listado ou Privado*), sem restrições de cota ou necessidade de configurar projetos complexos no Google Cloud.

---

## 🚀 Instalação e Autenticação (1 Clique)

1. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Login Único**:
   Dê um duplo clique no arquivo [`login.bat`](./login.bat) (ou execute no terminal):
   ```bash
   python browser.py login
   ```
   *Faça login com a conta do seu canal do YouTube na janela que abrir e aperte ENTER no terminal. O perfil de sessão persistente será salvo em `~/.youtube_studio_profile`.*

---

## 🛠️ Ferramentas Disponíveis no MCP

### `youtube_upload_video`
- **`video_path`**: Caminho do arquivo de vídeo (`.mp4`, `.mkv`, etc.).
- **`thumbnail_path`**: Caminho da imagem da capa gerada/editada (`.png`, `.jpg`).
- **`title`**: Título do vídeo (até 100 caracteres).
- **`description`**: Descrição do vídeo com links, timestamps, etc.
- **`tags`**: Tags separadas por vírgula.
- **`visibility`**: `public`, `unlisted` (padrão) ou `private`.

### `youtube_check_session`
- Verifica se a sessão do YouTube Studio está ativa e pronta para uso.

---

## 📄 Licença
Distribuído sob a licença MIT. Desenvolvido por **Alex Sandro (@al3x-d3v357)**.
