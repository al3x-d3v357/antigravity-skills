---
name: csharp-ast-indexer
description: Fornece assinaturas e métodos de scripts C# existentes sem carregar o código-fonte completo no prompt.
---

# C# AST Indexer

Antes de implementar novas classes ou modificar métodos existentes:
1. Consulte `docs/scripts_api_index.json` para validar nomes de métodos e propriedades públicas já declaradas.
2. Não solicite o arquivo `.cs` inteiro se apenas a assinatura do método for necessária para criar integração.
3. Atualize o índice executando `python skills/01-gamedev-unity/csharp-ast-indexer/index_scripts.py` após refatorações.
