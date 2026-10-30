#!/usr/bin/env node
/**
 * Goxel Voxel Art MCP Server
 * Conecta o Antigravity ao Goxel para geração e manipulação automatizada de Voxel Art 3D.
 */

const fs = require('fs');
const path = require('path');
const { spawn, execSync } = require('child_process');
const readline = require('readline');

const GOXEL_BIN = process.env.GOXEL_BIN || (
  fs.existsSync('/media/alex/alex/softwares/goxel-0.15.1-extracted/AppRun')
    ? '/media/alex/alex/softwares/goxel-0.15.1-extracted/AppRun'
    : (fs.existsSync('/media/alex/alex/softwares/goxel-0.15.1.AppImage')
      ? '/media/alex/alex/softwares/goxel-0.15.1.AppImage'
      : 'goxel')
);

const DEFAULT_OUTPUT_DIR = process.env.GOXEL_OUTPUT_DIR || (
  fs.existsSync('/media/alex/alex/pro_unity/block_tactics/blocktactics/Assets/BlockTactics/VoxelCharacters')
    ? '/media/alex/alex/pro_unity/block_tactics/blocktactics/Assets/BlockTactics/VoxelCharacters'
    : path.join(process.cwd(), 'output_voxels')
);

if (!fs.existsSync(DEFAULT_OUTPUT_DIR)) {
  try { fs.mkdirSync(DEFAULT_OUTPUT_DIR, { recursive: true }); } catch (e) {}
}

const TOOLS = [
  {
    name: 'goxel_create_character',
    description: 'Constrói um personagem em Voxel Art 3D (Arqueiro, Tanque, Mago, Suporte ou customizado) utilizando o Goxel e exporta para .vox e .obj.',
    inputSchema: {
      type: 'object',
      properties: {
        character_class: {
          type: 'string',
          enum: ['archer', 'tank', 'mage', 'support', 'elf_healer', 'cyberpunk_archer', 'ogre', 'peasant_rider'],
          description: 'Classe do herói a ser gerado'
        },
        output_dir: {
          type: 'string',
          description: 'Diretório onde salvar os arquivos gerados (opcional)'
        },
        export_obj: {
          type: 'boolean',
          description: 'Se verdadeiro, também converte e exporta o modelo para .obj 3D'
        },
        open_in_gui: {
          type: 'boolean',
          description: 'Se verdadeiro, abre a interface gráfica do Goxel com o personagem na tela'
        }
      },
      required: ['character_class']
    }
  },
  {
    name: 'goxel_create_object',
    description: 'Constrói um objeto, arma ou item de cenário em Voxel Art 3D (espada, escudo, cajado, arco, baú, poção, tocha, pilar).',
    inputSchema: {
      type: 'object',
      properties: {
        object_type: {
          type: 'string',
          enum: ['sword', 'shield', 'staff', 'bow', 'chest', 'potion', 'torch', 'pillar'],
          description: 'Tipo de objeto a ser modelado'
        },
        output_path: {
          type: 'string',
          description: 'Caminho completo do arquivo de saída .vox'
        },
        export_obj: {
          type: 'boolean',
          description: 'Se verdadeiro, também exporta para .obj'
        },
        open_in_gui: {
          type: 'boolean',
          description: 'Se verdadeiro, abre no Goxel GUI'
        }
      },
      required: ['object_type', 'output_path']
    }
  },
  {
    name: 'goxel_run_custom_script',
    description: 'Executa um script procedural JavaScript arbitrário dentro do motor QuickJS do Goxel para esculturas voxel complexas.',
    inputSchema: {
      type: 'object',
      properties: {
        script_code: {
          type: 'string',
          description: 'Código JavaScript a ser executado dentro do Goxel (acessa goxel.image.activeLayer.volume)'
        },
        output_vox_path: {
          type: 'string',
          description: 'Caminho para salvar o volume final em .vox'
        }
      },
      required: ['script_code', 'output_vox_path']
    }
  },
  {
    name: 'goxel_export_model',
    description: 'Converte um arquivo de voxels (.vox ou .gox) para .obj, .gltf ou render .png.',
    inputSchema: {
      type: 'object',
      properties: {
        input_file: {
          type: 'string',
          description: 'Arquivo de origem (.vox ou .gox)'
        },
        output_file: {
          type: 'string',
          description: 'Arquivo de destino (.obj, .gltf ou .png)'
        }
      },
      required: ['input_file', 'output_file']
    }
  },
  {
    name: 'goxel_open_gui',
    description: 'Abre a janela gráfica do Goxel com um modelo de voxels carregado na tela.',
    inputSchema: {
      type: 'object',
      properties: {
        file_path: {
          type: 'string',
          description: 'Caminho do arquivo .vox ou .gox para visualizar no Goxel'
        }
      },
      required: ['file_path']
    }
  }
];

function getVoxelHelpers() {
  return `
function setBox(vol, x1, y1, z1, x2, y2, z2, color) {
  let minX = Math.min(x1, x2), maxX = Math.max(x1, x2);
  let minY = Math.min(y1, y2), maxY = Math.max(y1, y2);
  let minZ = Math.min(z1, z2), maxZ = Math.max(z1, z2);
  for (let x = minX; x <= maxX; x++) {
    for (let y = minY; y <= maxY; y++) {
      for (let z = minZ; z <= maxZ; z++) {
        vol.setAt([x, y, z], color);
      }
    }
  }
}
`;
}

function handleCreateCharacter(args) {
  const charClass = args.character_class;
  const outDir = args.output_dir || DEFAULT_OUTPUT_DIR;
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const voxPath = path.join(outDir, `${charClass}.vox`);
  const objPath = path.join(outDir, `${charClass}.obj`);

  let buildCode = '';
  if (charClass === 'archer') {
    buildCode = `
      const C_SKIN = [235, 195, 160, 255];
      const C_TUNIC = [45, 135, 55, 255];
      const C_TUNIC_DARK = [32, 100, 40, 255];
      const C_LEATHER = [105, 60, 30, 255];
      const C_LEATHER_DARK = [70, 40, 20, 255];
      const C_GOLD = [255, 205, 40, 255];
      const C_HAIR = [140, 75, 30, 255];
      const C_FEATHER = [255, 60, 60, 255];
      const C_BOW = [90, 50, 25, 255];
      const C_STRING = [230, 230, 230, 255];

      // Botas e Pernas
      setBox(vol, -3, -2, 0, -1, 2, 2, C_LEATHER_DARK);
      setBox(vol, 1, -2, 0, 3, 2, 2, C_LEATHER_DARK);
      setBox(vol, -3, -2, 3, -1, 1, 9, C_TUNIC_DARK);
      setBox(vol, 1, -2, 3, 3, 1, 9, C_TUNIC_DARK);

      // Túnica e Cinto
      setBox(vol, -4, -2, 10, 4, 2, 17, C_TUNIC);
      setBox(vol, -4, -3, 10, 4, 3, 11, C_LEATHER);
      setBox(vol, -1, 3, 10, 1, 3, 11, C_GOLD);

      // Cabeça, Cabelo e Rosto
      setBox(vol, -3, -3, 18, 3, 3, 24, C_SKIN);
      setBox(vol, -4, -4, 20, 4, -3, 25, C_HAIR);
      vol.setAt([-1, 3, 21], [30, 110, 180, 255]);
      vol.setAt([1, 3, 21], [30, 110, 180, 255]);

      // Chapéu e Pena
      setBox(vol, -4, -4, 25, 4, 4, 25, C_TUNIC_DARK);
      setBox(vol, -3, -4, 26, 3, 2, 26, C_TUNIC);
      setBox(vol, -2, -3, 27, 2, 0, 27, C_TUNIC);
      setBox(vol, -4, 0, 26, -4, 1, 29, C_FEATHER);

      // Braços e Arco
      setBox(vol, 4, -1, 14, 6, 1, 17, C_TUNIC);
      setBox(vol, 5, -1, 10, 6, 1, 13, C_SKIN);
      setBox(vol, -6, -1, 14, -4, 1, 17, C_TUNIC);
      setBox(vol, -6, 0, 12, -5, 3, 14, C_SKIN);

      for (let z = 5; z <= 22; z++) vol.setAt([-6, 4, z], C_BOW);
      vol.setAt([-6, 3, 23], C_BOW);
      vol.setAt([-6, 3, 4], C_BOW);
      for (let z = 4; z <= 23; z++) vol.setAt([-6, 2, z], C_STRING);
    `;
  } else if (charClass === 'tank') {
    buildCode = `
      const C_STEEL = [65, 85, 115, 255];
      const C_STEEL_DARK = [40, 55, 75, 255];
      const C_GOLD = [225, 185, 45, 255];
      const C_CYAN = [45, 220, 255, 255];
      const C_DARK = [30, 35, 45, 255];

      // Botas e Pernas
      setBox(vol, -4, -3, 0, -1, 3, 3, C_STEEL_DARK);
      setBox(vol, 1, -3, 0, 4, 3, 3, C_STEEL_DARK);
      setBox(vol, -4, -2, 4, -1, 2, 9, C_STEEL);
      setBox(vol, 1, -2, 4, 4, 2, 9, C_STEEL);

      // Peitoral Maciço e Ombreiras
      setBox(vol, -5, -3, 10, 5, 3, 18, C_STEEL);
      setBox(vol, -4, 4, 12, 4, 4, 17, C_STEEL_DARK);
      setBox(vol, -1, 4, 14, 1, 4, 16, C_GOLD);
      setBox(vol, -7, -3, 15, -4, 3, 20, C_GOLD);
      setBox(vol, 4, -3, 15, 7, 3, 20, C_GOLD);

      // Elmo Fechado com Visor Luminoso
      setBox(vol, -4, -4, 18, 4, 4, 25, C_STEEL);
      setBox(vol, -3, -4, 26, 3, 4, 27, C_STEEL_DARK);
      setBox(vol, -3, 4, 21, 3, 4, 22, C_CYAN);

      // Escudo Torre
      setBox(vol, -8, -1, 4, -8, 7, 21, C_STEEL_DARK);
      setBox(vol, -9, -1, 4, -9, 7, 5, C_GOLD);
      setBox(vol, -9, -1, 20, -9, 7, 21, C_GOLD);
      setBox(vol, -9, 2, 9, -9, 4, 17, C_GOLD);

      // Espada
      setBox(vol, 6, 3, 8, 6, 4, 11, C_DARK);
      setBox(vol, 5, 3, 12, 7, 4, 12, C_GOLD);
      setBox(vol, 6, 3, 13, 6, 4, 24, [200, 215, 230, 255]);
    `;
  } else if (charClass === 'mage') {
    buildCode = `
      const C_ROBE = [85, 35, 140, 255];
      const C_ROBE_DARK = [55, 20, 95, 255];
      const C_GOLD = [250, 195, 45, 255];
      const C_CRYSTAL = [215, 55, 255, 255];
      const C_SKIN = [235, 195, 160, 255];
      const C_BEARD = [220, 220, 230, 255];

      // Túnica Longa
      setBox(vol, -4, -3, 0, 4, 3, 2, C_GOLD);
      setBox(vol, -4, -3, 3, 4, 3, 9, C_ROBE_DARK);
      setBox(vol, -4, -3, 10, 4, 3, 17, C_ROBE);
      setBox(vol, -1, 3, 3, 1, 3, 17, C_GOLD);

      // Cabeça, Barba e Chapéu
      setBox(vol, -3, -3, 18, 3, 3, 24, C_SKIN);
      setBox(vol, -3, 3, 17, 3, 4, 21, C_BEARD);
      vol.setAt([-1, 3, 22], C_CRYSTAL);
      vol.setAt([1, 3, 22], C_CRYSTAL);

      setBox(vol, -5, -5, 25, 5, 5, 25, C_ROBE_DARK);
      setBox(vol, -3, -3, 26, 3, 3, 27, C_ROBE);
      setBox(vol, -2, -2, 28, 2, 2, 29, C_ROBE);
      setBox(vol, -1, -2, 30, 1, 0, 31, C_ROBE);
      vol.setAt([0, -2, 32], C_GOLD);

      // Cajado com Cristal
      for (let z = 0; z <= 24; z++) vol.setAt([6, 2, z], [75, 45, 25, 255]);
      setBox(vol, 5, 1, 24, 7, 3, 25, C_GOLD);
      setBox(vol, 5, 1, 26, 7, 3, 28, C_CRYSTAL);
    `;
  } else if (charClass === 'support') {
    buildCode = `
      const C_WHITE = [240, 240, 245, 255];
      const C_GOLD = [255, 215, 50, 255];
      const C_CYAN = [75, 225, 235, 255];
      const C_SKIN = [235, 195, 160, 255];

      // Vestes Sagradas
      setBox(vol, -4, -3, 0, 4, 3, 2, C_GOLD);
      setBox(vol, -4, -3, 3, 4, 3, 17, C_WHITE);
      setBox(vol, -2, 3, 5, -1, 3, 17, C_GOLD);
      setBox(vol, 1, 3, 5, 2, 3, 17, C_GOLD);

      // Cabeça e Auréola
      setBox(vol, -3, -3, 18, 3, 3, 24, C_SKIN);
      vol.setAt([-1, 3, 21], C_CYAN);
      vol.setAt([1, 3, 21], C_CYAN);

      for (let x = -3; x <= 3; x++) {
        vol.setAt([x, -3, 28], C_GOLD);
        vol.setAt([x, 3, 28], C_GOLD);
      }
      for (let y = -2; y <= 2; y++) {
        vol.setAt([-3, y, 28], C_GOLD);
        vol.setAt([3, y, 28], C_GOLD);
      }

      // Cetro de Luz Divina
      for (let z = 4; z <= 20; z++) vol.setAt([6, 2, z], C_GOLD);
      setBox(vol, 5, 1, 22, 7, 3, 24, C_CYAN);
    `;
  } else if (charClass === 'elf_healer') {
    buildCode = `
      const C_SKIN = [245, 215, 185, 255];
      const C_HAIR = [225, 230, 240, 255];
      const C_EYE_GREEN = [40, 215, 140, 255];
      const C_EYE_WHITE = [250, 250, 255, 255];
      const C_ROBE_WHITE = [245, 248, 250, 255];
      const C_ROBE_EMERALD = [35, 155, 95, 255];
      const C_ROBE_MINT = [95, 215, 160, 255];
      const C_SILVER = [190, 205, 215, 255];
      const C_GOLD_LEAF = [245, 210, 60, 255];
      const C_WOOD_LIVING = [105, 65, 35, 255];
      const C_HEAL_GLOW = [60, 255, 160, 255];
      const C_HEAL_SPARKLE = [180, 255, 220, 255];

      // Botas Élficas com pontas curvadas
      setBox(vol, -3, -2, 0, -1, 2, 2, [80, 50, 30, 255]);
      setBox(vol, 1, -2, 0, 3, 2, 2, [80, 50, 30, 255]);
      vol.setAt([-2, 4, 1], C_ROBE_MINT);
      vol.setAt([2, 4, 1], C_ROBE_MINT);

      // Túnica e Corpete
      setBox(vol, -4, -3, 1, 4, 3, 2, C_SILVER);
      setBox(vol, -4, -3, 3, 4, 3, 9, C_ROBE_WHITE);
      setBox(vol, -2, 3, 2, 2, 3, 9, C_ROBE_EMERALD);
      setBox(vol, -4, -2, 10, 4, 2, 17, C_ROBE_WHITE);
      setBox(vol, -4, -3, 10, 4, 3, 11, C_SILVER);
      setBox(vol, -1, 3, 10, 1, 3, 11, C_GOLD_LEAF);
      vol.setAt([0, 3, 10], C_HEAL_GLOW);
      setBox(vol, -3, 2, 12, 3, 2, 16, C_ROBE_EMERALD);

      // Cabeça e Orelhas Élficas Longas
      setBox(vol, -3, -3, 18, 3, 3, 24, C_SKIN);
      // Orelha Esquerda
      setBox(vol, -4, -1, 21, -4, 1, 23, C_SKIN);
      setBox(vol, -5, -2, 22, -5, 0, 24, C_SKIN);
      setBox(vol, -6, -3, 23, -6, -1, 25, C_SKIN);
      vol.setAt([-7, -4, 25], C_SKIN);
      vol.setAt([-7, -4, 26], C_ROBE_MINT);
      // Orelha Direita
      setBox(vol, 4, -1, 21, 4, 1, 23, C_SKIN);
      setBox(vol, 5, -2, 22, 5, 0, 24, C_SKIN);
      setBox(vol, 6, -3, 23, 6, -1, 25, C_SKIN);
      vol.setAt([7, -4, 25], C_SKIN);
      vol.setAt([7, -4, 26], C_ROBE_MINT);

      // Cabelo Prateado Longo e Diadema
      setBox(vol, -4, -4, 12, 4, -3, 25, C_HAIR);
      setBox(vol, -3, -3, 25, 3, 2, 26, C_HAIR);
      for (let x = -3; x <= 3; x++) vol.setAt([x, 3, 24], C_SILVER);
      vol.setAt([0, 4, 24], C_HEAL_GLOW);

      // Olhos Verde Esmeralda
      vol.setAt([-2, 3, 21], C_EYE_WHITE);
      vol.setAt([-1, 3, 21], C_EYE_GREEN);
      vol.setAt([2, 3, 21], C_EYE_WHITE);
      vol.setAt([1, 3, 21], C_EYE_GREEN);

      // Asas de Espírito da Floresta
      setBox(vol, -6, -4, 16, -4, -4, 21, C_HEAL_SPARKLE);
      setBox(vol, -7, -5, 18, -5, -4, 22, C_HEAL_GLOW);
      setBox(vol, 4, -4, 16, 6, -4, 21, C_HEAL_SPARKLE);
      setBox(vol, 5, -5, 18, 7, -4, 22, C_HEAL_GLOW);

      // Cajado da Árvore da Vida com Flor de Cura
      setBox(vol, 4, -1, 14, 5, 2, 17, C_ROBE_WHITE);
      for (let z = 0; z <= 22; z++) vol.setAt([6, 2, z], C_WOOD_LIVING);
      vol.setAt([6, 3, 6], C_ROBE_EMERALD);
      vol.setAt([5, 2, 10], C_ROBE_MINT);
      setBox(vol, 5, 1, 24, 7, 3, 26, C_HEAL_GLOW);
      vol.setAt([6, 2, 27], C_HEAL_SPARKLE);
      vol.setAt([6, 2, 28], C_HEAL_GLOW);

      // Orbe de Cura na Mão Esquerda
      setBox(vol, -5, -1, 14, -4, 2, 17, C_ROBE_WHITE);
      setBox(vol, -6, 2, 13, -5, 4, 15, C_SKIN);
      setBox(vol, -7, 3, 16, -5, 5, 18, C_HEAL_GLOW);
      vol.setAt([-6, 4, 19], C_HEAL_SPARKLE);
    `;
  } else if (charClass === 'cyberpunk_archer') {
    buildCode = `
      const C_CARBON = [24, 27, 36, 255];
      const C_CARBON_LIGHT = [45, 50, 65, 255];
      const C_ORANGE = [255, 115, 0, 255];
      const C_ORANGE_GLOW = [255, 160, 40, 255];
      const C_CYBER_BLUE = [20, 60, 160, 255];
      const C_CYAN = [0, 225, 255, 255];
      const C_CYAN_GLOW = [120, 245, 255, 255];
      const C_SKIN = [235, 195, 160, 255];
      const C_HAIR = [30, 32, 42, 255];
      const C_STEEL = [110, 120, 135, 255];

      // Botas Taticas com Solado Neon Laranja
      setBox(vol, -3, -2, 0, -1, 2, 0, C_ORANGE);
      setBox(vol, 1, -2, 0, 3, 2, 0, C_ORANGE);
      setBox(vol, -3, -2, 1, -1, 2, 3, C_CARBON);
      setBox(vol, 1, -2, 1, 3, 2, 3, C_CARBON);

      // Pernas / Calcas de Combate Azul Cibernetico com Joelheiras Ciano
      setBox(vol, -3, -2, 4, -1, 1, 9, C_CYBER_BLUE);
      setBox(vol, 1, -2, 4, 3, 1, 9, C_CYBER_BLUE);
      vol.setAt([-2, 2, 6], C_CYAN);
      vol.setAt([2, 2, 6], C_CYAN);

      // Colete / Jaqueta Cibernetica Carbono com Faixas Laranja e Nucleo Ciano
      setBox(vol, -4, -2, 10, 4, 2, 17, C_CARBON);
      setBox(vol, -4, -3, 10, 4, -3, 11, C_ORANGE);
      setBox(vol, -4, 3, 10, 4, 3, 11, C_ORANGE);
      vol.setAt([-4, -2, 15], C_ORANGE);
      vol.setAt([4, -2, 15], C_ORANGE);
      // Reator / Nucleo Peitoral
      setBox(vol, -1, 3, 13, 1, 3, 15, C_CYAN);
      vol.setAt([0, 3, 14], C_CYAN_GLOW);

      // Mochila de Bateria / Quiver Tatico nas Costas
      setBox(vol, -3, -4, 11, 3, -3, 17, C_CARBON_LIGHT);
      vol.setAt([-2, -4, 13], C_ORANGE);
      vol.setAt([0, -4, 13], C_ORANGE);
      vol.setAt([2, -4, 13], C_ORANGE);
      vol.setAt([-2, -4, 16], C_CYAN);
      vol.setAt([2, -4, 16], C_CYAN);

      // Cabeca, Rosto e Cyber Visor
      setBox(vol, -3, -3, 18, 3, 3, 24, C_SKIN);
      // Visor Holografico Neon Azul/Ciano nos Olhos
      setBox(vol, -3, 4, 21, 3, 4, 22, C_CYAN);
      vol.setAt([2, 4, 22], C_ORANGE);

      // Cabelo Cyberpunk com Pontas Spiky Laranja
      setBox(vol, -4, -4, 20, 4, -3, 25, C_HAIR);
      setBox(vol, -3, -3, 25, 3, 3, 26, C_HAIR);
      vol.setAt([-2, 1, 27], C_ORANGE);
      vol.setAt([0, 2, 27], C_ORANGE_GLOW);
      vol.setAt([2, 1, 27], C_ORANGE);
      vol.setAt([-1, -1, 27], C_ORANGE);
      vol.setAt([1, -1, 27], C_ORANGE);

      // Braco Direito (Humano com Manopla de Tiro)
      setBox(vol, 4, -1, 14, 6, 1, 17, C_CYBER_BLUE);
      setBox(vol, 5, -1, 11, 6, 1, 13, C_SKIN);
      setBox(vol, 5, 0, 9, 6, 2, 11, C_CARBON);
      vol.setAt([6, 1, 10], C_ORANGE);

      // Braco Esquerdo (Protese Cibernetica Total em Aco/Ciano segurando o Arco)
      setBox(vol, -6, -1, 14, -4, 1, 17, C_STEEL);
      setBox(vol, -6, -1, 11, -5, 1, 13, C_CARBON_LIGHT);
      vol.setAt([-6, 0, 12], C_CYAN);
      setBox(vol, -6, 0, 9, -5, 3, 11, C_STEEL);

      // Arco Composto Cyberpunk (Frame Carbono + Acentos Laranja + Laser Cord Ciano)
      for (let z = 3; z <= 24; z++) vol.setAt([-6, 4, z], C_CARBON);
      setBox(vol, -6, 4, 22, -6, 5, 24, C_ORANGE);
      setBox(vol, -6, 4, 3, -6, 5, 5, C_ORANGE);
      vol.setAt([-6, 6, 23], C_CYAN);
      vol.setAt([-6, 6, 4], C_CYAN);
      vol.setAt([-6, 3, 14], C_ORANGE);
      vol.setAt([-6, 2, 14], C_CYAN);
      for (let z = 5; z <= 22; z++) vol.setAt([-6, 2, z], C_CYAN);
    `;
  } else if (charClass === 'ogre') {
    buildCode = `
      // 4 Tons de Verde para a Pele e Anatomia do Ogro
      const C_GREEN_DARK  = [34, 68, 28, 255];   // 1. Verde Escuro / Sombra Muscular e Contornos
      const C_GREEN_MID   = [55, 110, 42, 255];  // 2. Verde Médio / Pele Base do Ogro
      const C_GREEN_LIGHT = [82, 158, 58, 255];  // 3. Verde Claro / Musculatura em Destaque
      const C_GREEN_PALE  = [122, 188, 82, 255]; // 4. Verde Pálido / Peito, Barriga e Iluminação

      // Acessórios e Elementos Rústicos
      const C_LEATHER      = [95, 52, 25, 255];
      const C_LEATHER_DARK = [60, 32, 15, 255];
      const C_BONE         = [225, 215, 185, 255];
      const C_TUSK         = [240, 235, 205, 255];
      const C_EYE_YELLOW   = [250, 190, 20, 255];
      const C_PUPIL        = [30, 20, 10, 255];
      const C_HAIR         = [42, 36, 30, 255];
      const C_WOOD         = [75, 42, 22, 255];
      const C_WOOD_DARK    = [58, 30, 14, 255];
      const C_IRON         = [145, 150, 160, 255];

      // 1. Pernas e Pés Maciços
      // Perna Esquerda
      setBox(vol, -6, -3, 0, -2, 3, 2, C_GREEN_DARK);
      setBox(vol, -6, 3, 0, -2, 4, 1, C_GREEN_LIGHT);
      vol.setAt([-5, 4, 0], C_BONE);
      vol.setAt([-3, 4, 0], C_BONE);
      setBox(vol, -6, -2, 3, -2, 2, 8, C_GREEN_MID);
      setBox(vol, -5, 2, 3, -3, 2, 8, C_GREEN_LIGHT);
      setBox(vol, -6, -3, 4, -2, 3, 5, C_LEATHER);

      // Perna Direita
      setBox(vol, 2, -3, 0, 6, 3, 2, C_GREEN_DARK);
      setBox(vol, 2, 3, 0, 6, 4, 1, C_GREEN_LIGHT);
      vol.setAt([3, 4, 0], C_BONE);
      vol.setAt([5, 4, 0], C_BONE);
      setBox(vol, 2, -2, 3, 6, 2, 8, C_GREEN_MID);
      setBox(vol, 3, 2, 3, 5, 2, 8, C_GREEN_LIGHT);
      setBox(vol, 2, -3, 4, 6, 3, 5, C_LEATHER);

      // 2. Cintura, Tanga de Couro e Fivela de Crânio/Osso
      setBox(vol, -6, -3, 9, 6, 3, 11, C_LEATHER_DARK);
      setBox(vol, -3, 3, 7, 3, 4, 10, C_LEATHER);
      setBox(vol, -3, -4, 8, 3, -3, 10, C_LEATHER_DARK);
      setBox(vol, -6, -4, 11, 6, 4, 12, C_LEATHER);
      setBox(vol, -2, 4, 10, 2, 5, 13, C_BONE);
      vol.setAt([-1, 5, 11], C_PUPIL);
      vol.setAt([1, 5, 11], C_PUPIL);

      // 3. Tronco Gigantesco, Corcunda e Barriga Imponente
      setBox(vol, -7, -4, 12, 7, 3, 21, C_GREEN_MID);
      setBox(vol, -6, -5, 16, 6, -3, 23, C_GREEN_DARK); // Corcunda dorsal
      setBox(vol, -5, 2, 12, 5, 5, 17, C_GREEN_PALE);   // Barriga volumosa em verde claro
      setBox(vol, -6, 2, 18, 6, 5, 21, C_GREEN_LIGHT);  // Peitorais
      setBox(vol, -1, 3, 18, 1, 5, 20, C_GREEN_MID);    // Divisão do peitoral
      setBox(vol, -7, -1, 13, -7, 2, 17, C_GREEN_DARK);  // Flancos sombreados
      setBox(vol, 7, -1, 13, 7, 2, 17, C_GREEN_DARK);

      // Bandoleira de couro diagonal no peito
      for (let i = -5; i <= 5; i++) {
        let zL = Math.floor(13 + (i + 5) * 0.9);
        vol.setAt([i, 4, zL], C_LEATHER);
        vol.setAt([i, -4, zL], C_LEATHER);
      }

      // 4. Pescoço Maciço e Ombros
      setBox(vol, -4, -2, 21, 4, 3, 23, C_GREEN_MID);
      // Ombro Esquerdo
      setBox(vol, -10, -3, 17, -7, 3, 22, C_GREEN_MID);
      setBox(vol, -10, -2, 19, -8, 2, 22, C_GREEN_LIGHT);
      setBox(vol, -11, -3, 20, -8, 3, 22, C_LEATHER); // Ombreira de couro
      vol.setAt([-10, 0, 23], C_BONE); // Espinho de osso na ombreira
      // Ombro Direito
      setBox(vol, 7, -3, 17, 10, 3, 22, C_GREEN_MID);
      setBox(vol, 8, -2, 19, 10, 2, 22, C_GREEN_LIGHT);

      // 5. Cabeça de Ogro, Presas, Mandíbula e Olhos
      setBox(vol, -4, -2, 22, 4, 3, 28, C_GREEN_MID);
      setBox(vol, -4, 2, 21, 4, 5, 24, C_GREEN_LIGHT); // Mandíbula inferior protuberante
      setBox(vol, -3, 4, 21, 3, 5, 22, C_GREEN_PALE);  // Queixo
      // Presas inferiores voltadas para cima
      vol.setAt([-3, 5, 23], C_TUSK);
      vol.setAt([-3, 5, 24], C_TUSK);
      vol.setAt([-3, 5, 25], C_TUSK);
      vol.setAt([3, 5, 23], C_TUSK);
      vol.setAt([3, 5, 24], C_TUSK);
      vol.setAt([3, 5, 25], C_TUSK);

      // Nariz achatado largo
      setBox(vol, -2, 4, 24, 2, 5, 25, C_GREEN_DARK);
      vol.setAt([-1, 5, 24], [20, 40, 16, 255]); // Narina
      vol.setAt([1, 5, 24], [20, 40, 16, 255]);

      // Sobrancelhas pesadas e olhos ferozes
      setBox(vol, -4, 4, 27, 4, 5, 27, C_GREEN_DARK);
      vol.setAt([-2, 4, 26], C_EYE_YELLOW);
      vol.setAt([-1, 4, 26], C_PUPIL);
      vol.setAt([2, 4, 26], C_EYE_YELLOW);
      vol.setAt([1, 4, 26], C_PUPIL);

      // Orelhas pontudas
      setBox(vol, -6, 0, 24, -5, 1, 26, C_GREEN_LIGHT);
      vol.setAt([-7, 0, 26], C_GREEN_PALE);
      setBox(vol, 5, 0, 24, 6, 1, 26, C_GREEN_LIGHT);
      vol.setAt([7, 0, 26], C_GREEN_PALE);

      // Crista / Moicano rústico
      setBox(vol, -1, -3, 28, 1, 1, 30, C_HAIR);
      setBox(vol, -1, -4, 25, 1, -3, 28, C_HAIR);

      // 6. Braço Esquerdo (Punho Fechado Ameaçador)
      setBox(vol, -10, -2, 13, -7, 2, 17, C_GREEN_MID);
      setBox(vol, -10, -2, 10, -7, 2, 12, C_LEATHER); // Braçadeira
      vol.setAt([-10, 2, 11], C_IRON);
      setBox(vol, -10, -1, 6, -6, 3, 9, C_GREEN_LIGHT); // Mão e Punho
      setBox(vol, -10, 2, 6, -6, 3, 8, C_GREEN_DARK);

      // 7. Braço Direito e Clava Gigante com Pregos
      setBox(vol, 7, -2, 13, 10, 2, 17, C_GREEN_MID);
      setBox(vol, 7, -2, 11, 10, 2, 12, C_LEATHER);
      vol.setAt([10, 2, 11], C_IRON);
      setBox(vol, 7, 0, 8, 10, 3, 10, C_GREEN_LIGHT); // Mão segurando a clava

      // Porrete / Clava de Madeira Maciça
      setBox(vol, 8, 1, 3, 9, 2, 15, C_WOOD); // Empunhadura
      setBox(vol, 7, 0, 15, 11, 4, 25, C_WOOD); // Bloco principal
      setBox(vol, 6, -1, 18, 12, 5, 23, C_WOOD_DARK); // Reforço central
      // Cravos e espinhos de ferro
      setBox(vol, 8, 1, 26, 9, 2, 27, C_IRON); // Espinho superior
      setBox(vol, 5, 1, 19, 6, 2, 20, C_IRON); // Espinho lateral esquerdo
      setBox(vol, 12, 1, 19, 13, 2, 20, C_IRON); // Espinho lateral direito
      setBox(vol, 8, -2, 20, 9, -1, 21, C_IRON); // Espinho traseiro
      setBox(vol, 8, 5, 20, 9, 6, 21, C_IRON);  // Espinho frontal
    `;
  } else if (charClass === 'peasant_rider') {
    buildCode = `
      // --- PALETA DE CORES ---
      // Cavalo (Castanho Alazão)
      const C_HORSE_BASE     = [135, 75, 40, 255];
      const C_HORSE_DARK     = [95, 50, 25, 255];
      const C_HORSE_LIGHT    = [165, 95, 55, 255];
      const C_HORSE_MUZZLE   = [215, 190, 175, 255];
      const C_HORSE_NOSE     = [60, 35, 25, 255];
      const C_HORSE_EYE      = [25, 20, 15, 255];
      const C_HORSE_MANE     = [45, 28, 18, 255];
      const C_HOOF           = [40, 38, 35, 255];
      const C_STAR_WHITE     = [240, 240, 245, 255];

      // Arreios, Manta e Sela
      const C_BLANKET        = [175, 55, 45, 255];
      const C_SADDLE         = [85, 48, 26, 255];
      const C_REINS          = [65, 38, 20, 255];
      const C_STIRRUP        = [150, 155, 165, 255];
      const C_SACK           = [195, 170, 125, 255];

      // Camponês
      const C_SKIN           = [225, 175, 135, 255];
      const C_PANTS          = [80, 85, 95, 255];
      const C_BOOTS          = [65, 40, 22, 255];
      const C_TUNIC          = [210, 195, 165, 255];
      const C_VEST           = [110, 70, 40, 255];
      const C_BELT           = [55, 32, 18, 255];
      const C_HAIR           = [85, 52, 28, 255];
      const C_EYE            = [35, 75, 120, 255];
      const C_STRAW_HAT      = [225, 195, 105, 255];
      const C_STRAW_DARK     = [190, 160, 80, 255];

      // Forcado / Pitchfork
      const C_WOOD_POLE      = [115, 75, 45, 255];
      const C_IRON_PRONGS    = [160, 165, 175, 255];

      // 1. O CAVALO: PATAS E CASCOS
      setBox(vol, -4, -10, 0, -2, -8, 2, C_HOOF);
      setBox(vol, -4, -10, 3, -2, -8, 8, C_HORSE_DARK);
      setBox(vol, -4, -10, 9, -2, -7, 13, C_HORSE_BASE);

      setBox(vol, 2, -10, 0, 4, -8, 2, C_HOOF);
      setBox(vol, 2, -10, 3, 4, -8, 8, C_HORSE_DARK);
      setBox(vol, 2, -10, 9, 4, -7, 13, C_HORSE_BASE);

      setBox(vol, -4, 7, 0, -2, 9, 2, C_HOOF);
      setBox(vol, -4, 7, 3, -2, 9, 8, C_HORSE_DARK);
      setBox(vol, -4, 6, 9, -2, 9, 13, C_HORSE_BASE);

      setBox(vol, 2, 7, 0, 4, 9, 2, C_HOOF);
      setBox(vol, 2, 7, 3, 4, 9, 8, C_HORSE_DARK);
      setBox(vol, 2, 6, 9, 4, 9, 13, C_HORSE_BASE);

      // 2. O CAVALO: CORPO, ANCA E DORSO
      setBox(vol, -4, -10, 12, 4, 8, 17, C_HORSE_BASE);
      setBox(vol, -3, -11, 13, 3, 9, 18, C_HORSE_LIGHT);
      setBox(vol, -4, -11, 14, 4, -6, 18, C_HORSE_BASE);
      setBox(vol, -4, 4, 14, 4, 9, 18, C_HORSE_BASE);

      setBox(vol, -1, -12, 10, 1, -11, 17, C_HORSE_MANE);
      setBox(vol, -1, -13, 5, 1, -12, 12, C_HORSE_MANE);
      vol.setAt([0, -13, 4], C_HORSE_MANE);

      // 3. O CAVALO: PESCOÇO, CABEÇA E CRINA
      setBox(vol, -2, 7, 18, 2, 10, 21, C_HORSE_BASE);
      setBox(vol, -2, 9, 20, 2, 12, 24, C_HORSE_BASE);
      setBox(vol, -2, 11, 23, 2, 14, 27, C_HORSE_BASE);

      setBox(vol, -1, 6, 19, 1, 7, 22, C_HORSE_MANE);
      setBox(vol, -1, 8, 22, 1, 9, 25, C_HORSE_MANE);
      setBox(vol, -1, 10, 25, 1, 11, 28, C_HORSE_MANE);

      setBox(vol, -2, 13, 23, 2, 17, 27, C_HORSE_BASE);
      setBox(vol, -2, 18, 22, 2, 20, 25, C_HORSE_MUZZLE);
      vol.setAt([-1, 21, 23], C_HORSE_NOSE);
      vol.setAt([1, 21, 23], C_HORSE_NOSE);
      setBox(vol, -1, 15, 26, 1, 16, 27, C_STAR_WHITE);
      vol.setAt([-3, 15, 25], C_HORSE_EYE);
      vol.setAt([3, 15, 25], C_HORSE_EYE);
      vol.setAt([-2, 13, 28], C_HORSE_DARK);
      vol.setAt([-2, 13, 29], C_HORSE_BASE);
      vol.setAt([2, 13, 28], C_HORSE_DARK);
      vol.setAt([2, 13, 29], C_HORSE_BASE);

      // 4. ARREIOS, SELA E SACO DE PROVISÕES
      setBox(vol, -4, -3, 18, 4, 3, 18, C_BLANKET);
      vol.setAt([-4, -3, 17], C_BLANKET);
      vol.setAt([4, -3, 17], C_BLANKET);
      vol.setAt([-4, 3, 17], C_BLANKET);
      vol.setAt([4, 3, 17], C_BLANKET);

      setBox(vol, -3, -2, 19, 3, 2, 19, C_SADDLE);
      setBox(vol, -3, -3, 20, 3, -2, 20, C_SADDLE);
      setBox(vol, -2, 2, 20, 2, 3, 20, C_SADDLE);

      vol.setAt([-5, 0, 18], C_REINS);
      vol.setAt([-5, 0, 17], C_REINS);
      vol.setAt([-5, 0, 16], C_REINS);
      vol.setAt([-5, 0, 15], C_STIRRUP);
      vol.setAt([5, 0, 18], C_REINS);
      vol.setAt([5, 0, 17], C_REINS);
      vol.setAt([5, 0, 16], C_REINS);
      vol.setAt([5, 0, 15], C_STIRRUP);

      setBox(vol, -3, 17, 23, 3, 18, 23, C_REINS);
      for (let y = 5; y <= 17; y++) {
        let zR = Math.floor(21 + (y - 5) * 0.16);
        vol.setAt([-3, y, zR], C_REINS);
        vol.setAt([3, y, zR], C_REINS);
      }

      setBox(vol, -3, -8, 18, 3, -5, 21, C_SACK);
      setBox(vol, -4, -7, 19, -3, -6, 20, C_SACK);
      setBox(vol, 3, -7, 19, 4, -6, 20, C_SACK);
      for (let x = -3; x <= 3; x++) {
        vol.setAt([x, -6, 21], C_BELT);
      }

      // 5. O CAMPONÊS: PERNAS E BOTAS MONTADAS
      setBox(vol, -4, -1, 19, -3, 1, 20, C_PANTS);
      setBox(vol, -5, -1, 16, -4, 1, 18, C_PANTS);
      setBox(vol, -5, 0, 13, -4, 2, 15, C_BOOTS);

      setBox(vol, 3, -1, 19, 4, 1, 20, C_PANTS);
      setBox(vol, 4, -1, 16, 5, 1, 18, C_PANTS);
      setBox(vol, 4, 0, 13, 5, 2, 15, C_BOOTS);

      // 6. O CAMPONÊS: TRONCO, TÚNICA E COLETE
      setBox(vol, -2, -1, 20, 2, 1, 21, C_BELT);
      vol.setAt([0, 2, 21], [220, 180, 50, 255]);

      setBox(vol, -3, -1, 22, 3, 1, 27, C_TUNIC);
      setBox(vol, -3, -2, 22, 3, -1, 27, C_VEST);
      setBox(vol, -3, 0, 22, -2, 2, 27, C_VEST);
      setBox(vol, 2, 0, 22, 3, 2, 27, C_VEST);

      setBox(vol, -1, -1, 28, 1, 1, 28, C_SKIN);

      // 7. CABEÇA, ROSTO E CHAPÉU DE PALHA
      setBox(vol, -2, -1, 29, 2, 2, 32, C_SKIN);
      setBox(vol, -3, -2, 29, 3, -1, 33, C_HAIR);
      setBox(vol, -3, 0, 29, -3, 2, 32, C_HAIR);
      setBox(vol, 3, 0, 29, 3, 2, 32, C_HAIR);

      vol.setAt([-1, 3, 31], C_EYE);
      vol.setAt([1, 3, 31], C_EYE);
      vol.setAt([0, 3, 30], [210, 155, 115, 255]);
      vol.setAt([-1, 3, 29], C_HAIR);
      vol.setAt([0, 3, 29], [190, 130, 100, 255]);
      vol.setAt([1, 3, 29], C_HAIR);

      setBox(vol, -5, -4, 33, 5, 4, 33, C_STRAW_DARK);
      setBox(vol, -3, -2, 34, 3, 2, 35, C_STRAW_HAT);
      setBox(vol, -2, -1, 36, 2, 1, 36, C_STRAW_HAT);
      for (let x = -3; x <= 3; x++) {
        vol.setAt([x, -3, 34], C_BELT);
        vol.setAt([x, 3, 34], C_BELT);
      }

      // 8. BRAÇOS, RÉDEAS E FORCADO DE FENO
      setBox(vol, -4, 0, 25, -3, 1, 27, C_TUNIC);
      setBox(vol, -4, 1, 23, -3, 3, 25, C_SKIN);
      setBox(vol, -3, 3, 22, -2, 4, 23, C_SKIN);

      setBox(vol, 3, 0, 25, 4, 1, 27, C_TUNIC);
      setBox(vol, 4, 1, 24, 5, 2, 26, C_SKIN);
      setBox(vol, 4, 2, 23, 5, 3, 24, C_SKIN);

      for (let z = 10; z <= 38; z++) {
        vol.setAt([5, 3, z], C_WOOD_POLE);
      }
      setBox(vol, 3, 3, 39, 7, 3, 39, C_IRON_PRONGS);
      setBox(vol, 3, 3, 40, 3, 3, 45, C_IRON_PRONGS);
      setBox(vol, 5, 3, 40, 5, 3, 46, C_IRON_PRONGS);
      setBox(vol, 7, 3, 40, 7, 3, 45, C_IRON_PRONGS);
    `;
  }

  const scriptContent = `
    ${getVoxelHelpers()}
    let vol = goxel.image.activeLayer.volume;
    ${buildCode}
    vol.save("${voxPath}");
  `;

  const tmpScript = path.join('/tmp', `goxel_gen_${Date.now()}.js`);
  fs.writeFileSync(tmpScript, scriptContent, 'utf-8');

  try {
    execSync(`${GOXEL_BIN} --script=${tmpScript}`, { stdio: 'pipe' });
  } finally {
    try { fs.unlinkSync(tmpScript); } catch (e) {}
  }

  let exportedObj = false;
  if (args.export_obj !== false) {
    try {
      execSync(`${GOXEL_BIN} "${voxPath}" -e "${objPath}"`, { stdio: 'pipe' });
      exportedObj = true;
    } catch (e) {}
  }

  if (args.open_in_gui) {
    spawn(GOXEL_BIN, [voxPath], {
      detached: true,
      stdio: 'ignore',
      env: { ...process.env, DISPLAY: process.env.DISPLAY || ':0' }
    }).unref();
  }

  return {
    success: true,
    character_class: charClass,
    vox_path: voxPath,
    obj_path: exportedObj ? objPath : null,
    opened_in_gui: !!args.open_in_gui
  };
}

function handleCreateObject(args) {
  const type = args.object_type;
  const outPath = args.output_path;
  const outDir = path.dirname(outPath);
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  let buildCode = '';
  if (type === 'sword') {
    buildCode = `
      setBox(vol, -1, -1, 0, 1, 1, 4, [60, 40, 20, 255]);
      setBox(vol, -4, -1, 5, 4, 1, 6, [240, 190, 40, 255]);
      setBox(vol, -2, -1, 7, 2, 1, 22, [210, 225, 240, 255]);
      vol.setAt([0, 0, 23], [210, 225, 240, 255]);
    `;
  } else if (type === 'chest') {
    buildCode = `
      setBox(vol, -6, -4, 0, 6, 4, 8, [110, 65, 30, 255]);
      setBox(vol, -6, -4, 0, 6, -4, 8, [60, 60, 65, 255]);
      setBox(vol, -6, 4, 0, 6, 4, 8, [60, 60, 65, 255]);
      setBox(vol, -1, 4, 4, 1, 5, 6, [255, 215, 50, 255]);
    `;
  } else if (type === 'potion') {
    buildCode = `
      setBox(vol, -3, -3, 0, 3, 3, 6, [255, 40, 80, 255]);
      setBox(vol, -1, -1, 7, 1, 1, 9, [230, 240, 255, 180]);
      setBox(vol, -2, -2, 10, 2, 2, 11, [140, 85, 45, 255]);
    `;
  } else {
    buildCode = `
      setBox(vol, -4, -4, 0, 4, 4, 16, [140, 140, 150, 255]);
    `;
  }

  const scriptContent = `
    ${getVoxelHelpers()}
    let vol = goxel.image.activeLayer.volume;
    ${buildCode}
    vol.save("${outPath}");
  `;

  const tmpScript = path.join('/tmp', `goxel_obj_${Date.now()}.js`);
  fs.writeFileSync(tmpScript, scriptContent, 'utf-8');

  try {
    execSync(`${GOXEL_BIN} --script=${tmpScript}`, { stdio: 'pipe' });
  } finally {
    try { fs.unlinkSync(tmpScript); } catch (e) {}
  }

  let objPath = null;
  if (args.export_obj) {
    objPath = outPath.replace(/\\.vox$/i, '.obj');
    try {
      execSync(`${GOXEL_BIN} "${outPath}" -e "${objPath}"`, { stdio: 'pipe' });
    } catch (e) {}
  }

  if (args.open_in_gui) {
    spawn(GOXEL_BIN, [outPath], {
      detached: true,
      stdio: 'ignore',
      env: { ...process.env, DISPLAY: process.env.DISPLAY || ':0' }
    }).unref();
  }

  return { success: true, vox_path: outPath, obj_path: objPath };
}

function handleExport(args) {
  execSync(`${GOXEL_BIN} "${args.input_file}" -e "${args.output_file}"`, { stdio: 'pipe' });
  return { success: true, output_file: args.output_file };
}

function handleOpenGui(args) {
  const child = spawn(GOXEL_BIN, [args.file_path], {
    detached: true,
    stdio: 'ignore',
    env: { ...process.env, DISPLAY: process.env.DISPLAY || ':0' }
  });
  child.unref();
  return { success: true, pid: child.pid, file_path: args.file_path };
}

// JSON-RPC 2.0 Loop
const rl = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: false });

rl.on('line', (line) => {
  if (!line.trim()) return;
  try {
    const req = JSON.parse(line);
    const id = req.id;
    const method = req.method;

    if (method === 'initialize') {
      const response = {
        jsonrpc: '2.0',
        id: id,
        result: {
          protocolVersion: '2024-11-05',
          capabilities: { tools: {} },
          serverInfo: { name: 'goxel-mcp-server', version: '1.0.0' }
        }
      };
      process.stdout.write(JSON.stringify(response) + '\n');
    } else if (method === 'notifications/initialized') {
      // Acknowledgement
    } else if (method === 'ping') {
      process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id: id, result: {} }) + '\n');
    } else if (method === 'tools/list') {
      const response = {
        jsonrpc: '2.0',
        id: id,
        result: { tools: TOOLS }
      };
      process.stdout.write(JSON.stringify(response) + '\n');
    } else if (method === 'tools/call') {
      const toolName = req.params.name;
      const args = req.params.arguments || {};
      let result;

      try {
        if (toolName === 'goxel_create_character') {
          result = handleCreateCharacter(args);
        } else if (toolName === 'goxel_create_object') {
          result = handleCreateObject(args);
        } else if (toolName === 'goxel_export_model') {
          result = handleExport(args);
        } else if (toolName === 'goxel_open_gui') {
          result = handleOpenGui(args);
        } else if (toolName === 'goxel_run_custom_script') {
          const scriptContent = `
            ${getVoxelHelpers()}
            let vol = goxel.image.activeLayer.volume;
            ${args.script_code}
            vol.save("${args.output_vox_path}");
          `;
          const tmpScript = path.join('/tmp', `goxel_custom_${Date.now()}.js`);
          fs.writeFileSync(tmpScript, scriptContent, 'utf-8');
          try {
            execSync(`${GOXEL_BIN} --script=${tmpScript}`, { stdio: 'pipe' });
            result = { success: true, output_path: args.output_vox_path };
          } finally {
            try { fs.unlinkSync(tmpScript); } catch (e) {}
          }
        } else {
          throw new Error(`Tool not found: ${toolName}`);
        }

        const response = {
          jsonrpc: '2.0',
          id: id,
          result: {
            content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
          }
        };
        process.stdout.write(JSON.stringify(response) + '\n');
      } catch (err) {
        const response = {
          jsonrpc: '2.0',
          id: id,
          error: { code: -32000, message: err.message }
        };
        process.stdout.write(JSON.stringify(response) + '\n');
      }
    }
  } catch (err) {}
});
