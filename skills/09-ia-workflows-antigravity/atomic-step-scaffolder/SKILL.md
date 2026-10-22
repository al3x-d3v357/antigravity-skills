---
name: atomic-step-scaffolder
description: Fraciona planos complexos de jogos em microetapas sequenciais estritas, impedindo a geração de respostas gigantescas.
---

# Atomic Step Scaffolder

Quando uma tarefa envolver a criação ou refatoração de um subsistema de jogo:

## Regras de Execução
1. **Uma Entidade por Vez:** Proibido gerar mecânica de jogador, IA de bot e HUD em uma única resposta.
2. **Ciclo Fechado:** 
   - Etapa A: Gerar ou patchear o script.
   - Etapa B: Validar compilação (`unity-cli-compiler-validator`).
   - Etapa C: Parar e reportar em 2 linhas antes de passar para o próximo subsistema.
3. Se o usuário pedir "implemente o jogo todo", gere um checklist numerado curto e implemente imediatamente apenas o passo 1.
