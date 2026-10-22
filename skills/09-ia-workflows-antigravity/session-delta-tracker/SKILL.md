---
name: session-delta-tracker
description: Registra um resumo operacional de 5 linhas ao final de cada execução para manter contexto persistente entre sessões.
---

# Session Delta Tracker

Ao finalizar qualquer entrega ou quando solicitado encerramento de sessão, gere ou atualize o arquivo `docs/session_delta.md`:

```markdown
### Snapshot de Contexto Operacional
- **Última Ação:** [Resumo de 1 frase do que foi implementado]
- **Arquivos Alterados:** [Lista de caminhos separados por vírgula]
- **Status do Compilador:** [SUCCESS ou FAILED + erro isolado]
- **Próximo Passo Imediato:** [Ação seguinte prioritária]
- **Assets Pendentes:** [Modelos/áudios faltantes ou None]
```

Na sessão seguinte, o agente precisa ler apenas este arquivo para retomar o projeto consumindo menos de 150 tokens.
