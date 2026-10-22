---
name: blender-affinity-texturing
description: Workflow profissional para exportar mapas UV de faces selecionadas no Blender (Edit Mode), enviar e pintar no Serif Affinity (Designer/Photo) com alto contraste, e aplicar automaticamente as texturas no Base Color de slots de materiais dedicados no Blender.
---

# Blender <-> Affinity Texturing Workflow

Este guia e skill automatizam o pipeline de pintura e texturização de modelos 3D combinando a modelagem do **Blender** com a precisão vetorial e artística da suíte **Serif Affinity**.

---

## 🚀 Fluxo de Trabalho (Pipeline 3 Passos)

### Passo 1: Selecionar e Exportar a Face no Blender
1. No Blender, entre no **Modo Edit** (`Tab`).
2. Selecione a face (ou faces) que deseja pintar.
3. Certifique-se de que a malha possui uma camada UV válida (`UVMap`).
4. Execute o script de extração automática:
   ```python
   exec(open(r"D:\GitHub\export_uv_to_affinity.py").read())
   ```
   *O script gera um arquivo SVG/PNG de alta resolução com fundo preto de contraste e contorno ciano fluorescente, abrindo-o diretamente no Affinity.*

### Passo 2: Pintura e Texturização no Affinity
1. No Affinity Designer ou Photo, utilize a camada superior para pintar ou desenhar sua arte/textura.
2. A camada da UV serve como máscara e guia de proporções.
3. Quando concluir a arte, oculte as linhas guias da UV (deixando apenas sua textura e o fundo desejado).
4. Salve o documento ou exporte como PNG em:
   - `D:\GitHub\arts3d\personagens\<nome_do_projeto>\textura_<nome>.png`

### Passo 3: Aplicação Restrita à Face no Blender
Para evitar que a textura se repita nas outras faces da malha:
1. A malha deve possuir **2 slots de material**:
   - **Slot 0 (`Material_Base`):** Material padrão liso sem imagem para as outras faces.
   - **Slot 1 (`Material_Face`):** Material exclusivo com nó `ShaderNodeTexImage` ligado ao `Base Color`.
2. Apenas a face selecionada recebe `material_index = 1`.
3. Na Viewport 3D do Blender, ative o modo **Material Preview** (`Z` -> *Material Preview*).

---

## 🛠️ Orientação Correta das Coordenadas UV

Para faces frontais de personagens e blocos:
- Vértice Inferior Esquerdo (Bottom-Left: -X, -Z) ➡️ UV `(0.0, 0.0)`
- Vértice Inferior Direito (Bottom-Right: +X, -Z) ➡️ UV `(1.0, 0.0)`
- Vértice Superior Direito (Top-Right: +X, +Z) ➡️ UV `(1.0, 1.0)`
- Vértice Superior Esquerdo (Top-Left: -X, +Z) ➡️ UV `(0.0, 1.0)`

Isso garante que a orientação vertical (+Z no Blender) corresponda exatamente ao topo da imagem no Affinity.
