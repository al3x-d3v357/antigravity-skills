---
name: project-changelog-tracker
description: Documenta automaticamente todas as solicitacoes, entregas e alteracoes do projeto em uma pasta dedicada (ex: docs/), controlando versoes incrementais (v1, v1.1, v2) para garantir contexto e persistencia entre novas sessoes de chat.
---

# Project Changelog & Context Tracker

Esta skill garante que toda tarefa, pedido do usuario e solucao implementada sejam registrados em arquivos de documentacao locais com controle estrito de versoes. Isso permite apagar o chat, abrir uma nova conversa e recuperar imediatamente o contexto do projeto.

---

## 1. Estrutura de Diretorios Obrigatoria

Todo projeto deve manter uma pasta exclusiva para documentacao e contexto:

```text
meu-projeto/
├── docs/
│   ├── CONTEXT.md        # Resumo executivo do estado atual do projeto
│   └── CHANGELOG.md      # Historico de versoes e tarefas documentadas
```

---

## 2. Regra de Versionamento

Ao registrar o que foi pedido e o que foi feito, determine a versao de acordo com o impacto da alteracao:

1. **Primeira documentacao (inicio do projeto ou modulo):**
* Definir como **`v1.0`** (ou `v1`).

2. **Alteracao pontual / minima (Minor/Patch):**
* Incremento decimal: `v1.1`, `v1.2`, `v1.3`...
* *Exemplos:* ajustes de variaveis, correcao de bug simples, pequenas mudancas visuais, refatoracao de um unico metodo.

3. **Alteracao estrutural / grande (Major):**
* Incremento inteiro: `v2.0`, `v3.0`...
* *Exemplos:* mudanca de arquitetura, adicao de um sistema completo, reestruturacao do projeto, substituicao de bibliotecas centrais.

---

## 3. Protocolo de Documentacao

Sempre que concluir uma solicitacao do usuario:

### Passo A: Atualizar ou criar `docs/CHANGELOG.md`

Adicione uma nova entrada no topo do historico:

```markdown
## [vX.Y] - Data / Registro
- **Pedido:** O que o usuario solicitou textualmente ou a intencao principal.
- **O que foi feito:** Acoes executadas, arquivos criados ou modificados.
- **Decisoes tecnicas:** Parametros importantes, bibliotecas ou escolhas tomadas.
```

### Passo B: Atualizar `docs/CONTEXT.md`

Mantenha este arquivo sempre enxuto (maximo 30-40 linhas) para servir de carga rapida para novas conversas:

* **Estado Atual:** Em que ponto o projeto esta e qual a versao vigente.
* **Modulos / Arquivos Chave:** Onde as coisas principais estao implementadas.
* **Proximos Passos:** O que ficou pendente ou foi planejado para a proxima iteracao.

---

## 4. Recuperacao de Contexto em Novo Chat

Ao iniciar uma nova conversa:

1. Verifique imediatamente a pasta `docs/`.
2. Leia `docs/CONTEXT.md` e a ultima entrada de `docs/CHANGELOG.md`.
3. Assuma o contexto a partir da ultima versao registrada antes de iniciar novas tarefas.
