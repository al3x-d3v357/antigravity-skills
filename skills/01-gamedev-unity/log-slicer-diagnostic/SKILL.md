---
name: log-slicer-diagnostic
description: Filtra logs brutos da Unity e do compilador, isolando apenas a linha exata do erro e economizando contexto.
---

# Log Slicer Diagnostic

Nunca leia arquivos de log brutos (`Editor.log`, `compile.log`, logs de terminal).

## Protocolo
1. Execute: `python skills/01-gamedev-unity/log-slicer-diagnostic/slice_log.py <caminho_do_log>`
2. Analise exclusivamente as linhas retornadas pelo script.
3. Se o script retornar `LOG_STATUS: NENHUM_ERRO_CRITICO_ENCONTRADO`, assuma compilação limpa sem solicitar o log completo.
