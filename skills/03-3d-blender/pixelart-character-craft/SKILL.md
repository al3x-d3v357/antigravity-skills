---
name: pixelart-character-craft
description: Pipeline profissional e de alta fidelidade para criação, customização anatômica, animação e montagem de Spritesheets de personagens Pixel Art (16x16 e 32x32) utilizando o LibreSprite via MCP e CLI.
---

# Pixel Art Character Crafting (LibreSprite & Antigravity)

Esta skill orienta os agentes a criar e animar personagens em Pixel Art com controle anatômico estrito, utilizando o servidor MCP `pixelart` e o motor **LibreSprite v1.3**.

## 1. Diretrizes Visuais & Paleta do Alex

- **Paleta Corporativa do Alex** (`alex_corporate`):
  - **Azul Royal Profundo**: `#3852B4` (placas de armadura, túnicas principais)
  - **Azul Médio / Ardósia**: `#5E7AC4` (bordas secundárias, iluminação)
  - **Dourado / Âmbar Quente**: `#F3BE7A` (cabelos, fivelas, guarnições, empunhaduras)
  - **Laranja Tangerina Neon**: `#F08D39` (detalhes mágicos, zíperes sci-fi, plumas de elmo)
  - **Verde Institucional (OBO)**: `#43BDB0` (gemas mágicas, visores, orbes e itens de cura)
  - **Branco Puro**: `#FFFFFF` (brilho especular, esclera dos olhos)
  - **Preto Profundo / Azulado**: `#0E1224` (outlines externos)

## 2. Anatomia & Camadas do Personagem (Grade 32x32)

Ao gerar ou desenhar personagens, estruturar em camadas de baixo para cima:
1. **Sombra no chão** (elipse semi-transparente nos pixels inferiores)
2. **Capa / Vestimenta traseira** (quando aplicável)
3. **Pernas e Botas** (calças, joelheiras, sapatos de couro com destaque de luz)
4. **Tronco / Peitoral** (armadura ou vestimenta com divisão de volume e luz)
5. **Pescoço e Cabeça** (tom de pele base com sombra abaixo do queixo)
6. **Rosto e Olhos** (olhos de alto contraste de 2 a 3 pixels com íris colorida)
7. **Cabelo / Elmo / Capuz** (volume capilar ou elmo com viseira)
8. **Braços, Mãos e Armas** (espada longa, cajado com gema mística, adagas duplas, escudo)
9. **Outline Seletivo** (contorno escuro apenas onde encontra o ar/transparência)

## 3. Ferramentas do MCP `pixelart`

- `pixelart_create_character`: Cria personagens completos (`warrior`, `mage`, `rogue`, `paladin`, `cyberpunk_runner`, `healer`). Gera `.png`, `.aseprite` e preview 4x.
- `pixelart_animate_character`: Produz sequências de animação (`idle`, `walk`, `attack`, `jump`, `hurt`) e compila o Spritesheet consolidado (PNG + JSON) e `.aseprite` animado.
- `pixelart_draw_matrix`: Desenha cirurgicamente pixel por pixel via matriz ASCII e dicionário de cores hex.
- `pixelart_build_spritesheet`: Empacota múltiplos frames avulsos em folha de sprites.
- `pixelart_open_in_gui`: Abre o arquivo diretamente na interface gráfica do LibreSprite.
