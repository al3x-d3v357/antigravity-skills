---
name: fsm-logic-decoupler
description: Modela lógica de movimentação, bots e regras de jogo em C# puro desconectado de MonoBehaviour para economia de tokens.
---

# FSM Logic Decoupler

Isole regras de negócio e máquinas de estado de classes derivadas de `MonoBehaviour`.

## Padrão Obrigatório
1. **Estado Puro:** Crie interfaces simples `IState<T>` sem métodos da Unity (`Update`, `Start`, `GetComponent`).
2. **Atualização Explícita:** Apenas receba deltas de tempo (`float deltaTime`) e vetores de entrada (`Vector2 input`).
3. **Controlador Leve:** O `MonoBehaviour` deve apenas repassar inputs físicos e delegar a decisão lógica para a FSM.

Isso permite testar e alterar comportamentos de gameplay via scripts minúsculos de menos de 40 linhas.
