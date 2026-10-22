---
name: architect-agent-bridge
description: Orquestra um fluxo em duas fases (Extração de Contexto e Execução Estrita) entre um agente local menor e um modelo arquiteto avançado (como o Gemini), ideal para projetos na Godot Engine, Blender ou desenvolvimento geral. Use quando o usuário pedir para escanear/mapear o projeto atual para enviar a outra IA, gerar um pacote de contexto detalhado, ou aplicar estritamente um passo a passo/código gerado pelo Gemini sem desvios de roteiro.
---
# Architect Agent Bridge

Esta skill estabelece uma ponte de trabalho eficiente entre um agente local de menor capacidade de raciocínio e um modelo arquiteto de alta potência (como o Gemini). Ela divide o trabalho em dois modos distintos: **Modo 1 (Extração de Contexto)**, onde o agente local coleta e estrutura todos os dados técnicos do projeto sem tentar adivinhar soluções complexas, e **Modo 2 (Execução Estrita)**, onde o agente aplica cirurgicamente o código e o passo a passo fornecidos pelo arquiteto sem alterar a lógica ou improvisar.

## When to Use

- Quando o usuário pedir para analisar, mapear ou exportar o estado atual do projeto (cenas, nós, scripts, estrutura de pastas) para enviar ao Gemini ou outra IA mais potente.
- Quando uma mecânica ou arquitetura for complexa demais para o agente local resolver sozinho (ex: física realista de veículos na Godot, shaders avançados, arquitetura de sistemas).
- Quando o usuário retornar com uma resposta, plano passo a passo ou código pronto gerado pelo Gemini e exigir que o agente local implemente tudo fielmente sem fugir do roteiro.
- Quando o usuário quiser que o Gemini gere um prompt de extração ou um plano de implementação blindado para colar no agente local do computador.

## Steps

### Fase 1: Extração Profunda de Contexto (Scanner Mode)

Quando acionado para preparar os dados do projeto para o modelo arquiteto, execute a coleta exaustiva seguindo esta estrutura:

1. **Identifique o Escopo e o Problema:** Pergunte ou extraia qual é o objetivo final (ex: "Fazer o carro andar com física realista na Godot") e qual entidade ou pasta é o foco.
2. **Mapeie a Árvore de Arquivosrelevantes:** Liste os diretórios e arquivos principais do projeto (`res://` na Godot, pacotes ou módulos), ignorando pastas de cache ou binários pesados (`.godot/`, `node_modules/`, `.git/`).
3. **Inspecione a Hierarquia de Cenas e Nós (Especial para Godot/3D):**
   - Abra os arquivos de cena relevantes (`.tscn`).
   -Extraia a árvore exata de nós com seus nomes e tipos (ex: `VehicleBody3D > VehicleWheel3D`, `CharacterBody3D > CollisionShape3D`, `Camera3D`), além de propriedades modificadas no Inspector (massa, fricção, grupos, layers de colisão e sinais conectados).
4. **Extraia os Scripts e Configurações Atuais:**
   - Leia o conteúdo integral dos scripts vinculados (`.gd`, `.cs`, `.py`) e configurações críticas do projeto (como `Input Map` e `Physics` no `project.godot`).
5. **Gere o "Dossiê de Contexto para o Arquiteto":**
   - Entregue um bloco único em Markdown formatado e pronto para copiar e colar no Gemini, contendo:
     - **Contexto do Ambiente:** Versão da Engine/Linguagem e sistema operacional.
     - **Árvore de Nós/Arquivos:** Representação visual exata da estrutura.
     - **Código Atual Completo:** Scripts anexados na íntegra.
     - **Pedido ao Arquiteto:** Uma instrução final pedindo ao Gemini que devolva a solução em formato de **Plano de Execução Estrita** (código completo sem omissões + instruções exatas de nós/propriedades).

---

### Fase 2: Execução Estrita de Roteiro (Strict Executor Mode)

Quando o usuário fornecer o passo a passo e o código gerados pelo Gemini para aplicação no projeto:

1. **Ative o Bloqueio Criativo (Zero Improviso):**
   - Não refatore, não "otimize", não troque nomes de variáveis, não resuma funções e não altere a matemática/física enviada pelo arquiteto.
   - Trate a instrução recebida como uma especificação imutável.
2. **Valide os Pré-requisitos Antes de Escrever:**
   - Verifique se os arquivos, caminhos (`res://...`) e nós citados no roteiro do Gemini existem no projeto.
   - Se um nó ou arquivo precisar ser criado conforme o passo a passo, crie-o exatamente com o mesmo nome, tipo e hierarquia especificados.
3. **Aplique Passo a Passo Sequencialmente:**
   - **Substituição de Código:** Escreva o código completo nos arquivos indicados. Nunca use placeholders como `# resto do código aqui` ou `// ...`.
   - **Ajuste de Propriedades e Cenas:** Se o roteiro exigir mudanças em cenas (`.tscn`) ou configurações (`project.godot`), aplique os valores numéricos exatos (ex: valores de `engine_force`, `steering`, `stiffness`, `damping` ou `Input Map`).
4. **Verifique a Integridade e Reporte:**
   - Após cada alteração, confirme se o arquivo foi salvo corretamente e se não há erros de sintaxe ou referências quebradas.
   - Entregue um **Checklist de Execução** listando cada item do roteiro do Gemini como `[Concluído]` e informe apenas o que o usuário precisa testar manualmente na interface (se houver).

---

### Como Atuar Quando Esta Skill Rodar no Próprio Gemini (Papel de Arquiteto)

Se o usuário estiver conversando diretamente com o Gemini e acionar este fluxo:

1. **Se o usuário ainda não trouxe os dados do projeto:** Gere um comando direto de **Fase 1** para ele copiar e colar no agente local dele, instruindo o agente local a varrer o projeto e cuspir o Dossiê de Contexto.
2. **Se o usuário trouxe o Dossiê de Contexto do agente local:** Analise profundamente a arquitetura, crie a solução completa (ex: física avançada, rotação, suspensão, câmera) e entregue a resposta já envelopada como um **Prompt de Fase 2 (Execução Estrita)** pronto para o usuário copiar e colar de volta no agente local.

## Gotchas

- **Nunca omita código na Fase 2:** Agentes locais menores se perdem facilmente com trechos parciais (`...`). Sempre exija e escreva arquivos inteiros do início ao fim.
- **Cuidado com referências de nós na Godot:** Um erro comum é o script tentar acessar `$WheelFL` quando o nó na cena se chama `FrontLeftWheel`. Na Fase 1, sempre extraia os nomes reais dos nós; na Fase 2, respeite estritamente os caminhos `NodePath` definidos.
- **Parar ao encontrar conflito:** Na Fase 2, se um arquivo ou estrutura do projeto for incompatível com o roteiro do Gemini, o agente local deve **parar imediatamente** e relatar a divergência exata ao usuário em vez de tentar "consertar por conta própria".
