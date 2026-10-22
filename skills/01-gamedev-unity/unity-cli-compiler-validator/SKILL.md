---
name: unity-cli-compiler-validator
description: Valida a compilação do projeto Unity via CLI e retorna apenas status booleano e a linha de falha.
---

# Unity CLI Compiler Validator

Evite suposições sobre a integridade do código.

## Execução
Execute:
`python skills/01-gamedev-unity/unity-cli-compiler-validator/validate_compile.py "<UNITY_PATH>" "<PROJECT_PATH>"`

## Diretrizes de Resposta
- Se retornar `COMPILE_STATUS: SUCCESS`, avance para a próxima tarefa sem emitir considerações sobre integridade.
- Se retornar `COMPILE_STATUS: FAILED`, use imediatamente a habilidade `code-patch-diff-engine` para corrigir os erros identificados.
