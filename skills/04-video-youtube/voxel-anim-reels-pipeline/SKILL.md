---
name: voxel-anim-reels-pipeline
description: Pipeline profissional e de alta qualidade para renderização de animações 3D de personagens voxel no Blender e composição de Reels verticais (9:16, 1080x1920) prontos para redes sociais.
---

# Voxel Animation Reels Pipeline

Este pipeline automatiza a renderização direta em alta qualidade e alta fidelidade luminosa de animações de personagens 3D (Voxel Art / Low Poly) no Blender e a montagem de vídeos verticais (9:16) focados 100% nas animações puras do personagem.

## 🎯 Diretrizes Obrigatórias do Alex
1. **Calibração Luminosa de Estúdio (Anti-Subexposição):**
   - **Key Light:** 45.000W (Branco quente `1.0, 0.98, 0.94`, Size 20.0).
   - **Fill Light:** 22.000W (Ardósia frio suave `0.85, 0.92, 1.0`, Size 30.0).
   - **Rim Light:** 55.000W (Realce de contorno `1.0, 0.95, 0.88`, Size 18.0).
   - **Top Softbox:** 18.000W (Zenital difuso `0.95, 0.97, 1.0`, Size 35.0).
   - **World Shader:** Slate/Navy Studio (`Color: 0.12, 0.15, 0.22`, `Strength: 1.2`).
   - **Piso Ciclorama:** Matte ardósia refinado (`Base Color: 0.15, 0.18, 0.25`, `Roughness: 0.55`, `Specular: 0.40`).
   - **Exposição da Câmera:** `scene.view_settings.exposure = 0.65`, perfil `AgX` ou `Filmic` Medium High Contrast.
   - **Métrica Alvo de Brilho:** Média RGB da personagem entre 140 e 175 (sem estouro de brancos `blown < 0.01%`).

2. **Apenas as Animações:** Exibir exclusivamente as ações do personagem (Idle, Walk, Run, Jump, Attack), sem menus de software, wireframes ou viewport suja.
3. **Cortes e Ritmo:**
   - Cada animação é executada em ciclos completos (ex: 2 a 3 loops perfeitos de walk/run).
   - Transições limpas e badges sutis na paleta oficial (`#3852B4`, `#5E7AC4`, `#F3BE7A`, `#F08D39`).
4. **Áudio Calibrado:** Trilha sonora rítmica e masterizada conforme EBU R128 (-14 LUFS).
5. **Zero Emojis:** Nas legendas das postagens, cumprir estritamente a regra de zero emojis.
