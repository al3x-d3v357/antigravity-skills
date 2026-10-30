"""
YouTube MCP Server (FastMCP)
Exposicao de ferramentas para automacao de uploads e capas no YouTube Studio.
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
from browser import upload_video, verify_session, USER_DATA_DIR

mcp = FastMCP("youtube")


@mcp.tool()
async def youtube_check_session() -> Dict[str, Any]:
    """
    Verifica se a sessao de login do YouTube Studio esta ativa e configurada.
    """
    is_valid = await verify_session()
    return {
        "logged_in": is_valid,
        "profile_path": str(USER_DATA_DIR),
        "instructions": "Execute 'python login.bat' na pasta do youtube-mcp se precisar logar." if not is_valid else "Pronto para enviar vídeos."
    }


@mcp.tool()
async def youtube_upload_video(
    video_path: str,
    thumbnail_path: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    visibility: str = "unlisted",
    made_for_kids: bool = False,
    headless: bool = False,
) -> Dict[str, Any]:
    """
    Envia um arquivo de video para o YouTube Studio com capa personalizada (thumbnail), titulo, descricao e tags.

    Args:
        video_path: Caminho absoluto para o arquivo de video (.mp4, .mkv, .mov).
        thumbnail_path: Caminho absoluto para a imagem da capa/thumbnail (.png, .jpg).
        title: Titulo do video (maximo 100 caracteres). Se vazio, usa o nome do arquivo.
        description: Descricao completa do video com links, capitulos e creditos.
        tags: Tags separadas por virgula (ex: 'unity, gamedev, devlog, 3d').
        visibility: Visibilidade do video: 'public', 'unlisted' (padrao) ou 'private'.
        made_for_kids: Definir se o video e infantil (padrao: False).
        headless: Executar o navegador em segundo plano (True) ou visivel (False).

    Returns:
        Dicionario contendo o status do upload e o link gerado do video.
    """
    return await upload_video(
        video_path=video_path,
        thumbnail_path=thumbnail_path,
        title=title,
        description=description,
        tags=tags,
        visibility=visibility,
        made_for_kids=made_for_kids,
        headless=headless,
    )


if __name__ == "__main__":
    mcp.run()
