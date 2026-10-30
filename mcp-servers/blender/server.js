#!/usr/bin/env node
/**
 * Blender MCP Server
 * Conecta o Antigravity ao Blender 5.2 para manipulação 3D, rigging, animação e exportação.
 */

const fs = require('fs');
const path = require('path');
const { spawn, execSync } = require('child_process');
const readline = require('readline');

const BLENDER_BIN = process.env.BLENDER_BIN || (
  fs.existsSync('/media/alex/alex/softwares/blender-5.2.2-linux-x64/blender')
    ? '/media/alex/alex/softwares/blender-5.2.2-linux-x64/blender'
    : 'blender'
);

const TOOLS = [
  {
    name: 'blender_execute_code',
    description: 'Executa código Python (bpy) diretamente dentro do Blender em segundo plano.',
    inputSchema: {
      type: 'object',
      properties: {
        code: {
          type: 'string',
          description: 'Código Python contendo comandos bpy a serem executados'
        },
        blend_file: {
          type: 'string',
          description: 'Caminho opcional do arquivo .blend base'
        }
      },
      required: ['code']
    }
  },
  {
    name: 'blender_open_gui',
    description: 'Abre a interface gráfica completa do Blender na tela com o arquivo .blend ou projeto carregado.',
    inputSchema: {
      type: 'object',
      properties: {
        file_path: {
          type: 'string',
          description: 'Caminho do arquivo .blend ou modelo 3D para abrir no Blender'
        },
        play_animation: {
          type: 'boolean',
          description: 'Se verdadeiro, inicia a reprodução contínua da timeline/animação ao abrir'
        }
      },
      required: ['file_path']
    }
  },
  {
    name: 'blender_export_model',
    description: 'Exporta a cena atual do Blender para GLB, FBX ou OBJ otimizado para jogos.',
    inputSchema: {
      type: 'object',
      properties: {
        blend_file: {
          type: 'string',
          description: 'Arquivo .blend de origem'
        },
        output_file: {
          type: 'string',
          description: 'Arquivo de destino (.glb, .fbx ou .obj)'
        },
        format: {
          type: 'string',
          enum: ['glb', 'fbx', 'obj'],
          description: 'Formato de exportação'
        }
      },
      required: ['blend_file', 'output_file', 'format']
    }
  }
];

function handleExecuteCode(args) {
  const tmpScript = path.join('/tmp', `blender_exec_${Date.now()}.py`);
  fs.writeFileSync(tmpScript, args.code, 'utf-8');

  let cmd = `"${BLENDER_BIN}" --background`;
  if (args.blend_file && fs.existsSync(args.blend_file)) {
    cmd += ` "${args.blend_file}"`;
  }
  cmd += ` --python "${tmpScript}"`;

  try {
    const stdout = execSync(cmd, { stdio: 'pipe', encoding: 'utf-8' });
    return { success: true, output: stdout };
  } catch (err) {
    return { success: false, error: err.message, stderr: err.stderr ? err.stderr.toString() : '' };
  } finally {
    try { fs.unlinkSync(tmpScript); } catch (e) {}
  }
}

function handleOpenGui(args) {
  const filePath = args.file_path;
  const env = {
    ...process.env,
    DISPLAY: process.env.DISPLAY || ':1',
    XDG_RUNTIME_DIR: process.env.XDG_RUNTIME_DIR || '/run/user/1000'
  };

  const spawnArgs = [filePath];
  if (args.play_animation) {
    const tmpAnimScript = path.join('/tmp', `blender_autoplay_${Date.now()}.py`);
    fs.writeFileSync(tmpAnimScript, `
import bpy
def play_anim():
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'MATERIAL'
    bpy.ops.screen.animation_play()
bpy.app.timers.register(play_anim, first_interval=0.5)
`, 'utf-8');
    spawnArgs.push('--python', tmpAnimScript);
  }

  const child = spawn(BLENDER_BIN, spawnArgs, {
    detached: true,
    stdio: 'ignore',
    env
  });
  child.unref();

  return { success: true, pid: child.pid, file_path: filePath };
}

function handleExport(args) {
  const script = `
import bpy
fmt = "${args.format}".lower()
out_path = "${args.output_file}"
if fmt == 'glb':
    bpy.ops.export_scene.gltf(filepath=out_path, export_format='GLB', export_animations=True)
elif fmt == 'fbx':
    bpy.ops.export_scene.fbx(filepath=out_path, apply_unit_scale=True, bake_anim=True)
elif fmt == 'obj':
    bpy.ops.wm.obj_export(filepath=out_path)
`;
  return handleExecuteCode({ code: script, blend_file: args.blend_file });
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
      process.stdout.write(JSON.stringify({
        jsonrpc: '2.0',
        id,
        result: {
          protocolVersion: '2024-11-05',
          capabilities: { tools: {} },
          serverInfo: { name: 'blender-mcp-server', version: '1.0.0' }
        }
      }) + '\n');
    } else if (method === 'ping') {
      process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id, result: {} }) + '\n');
    } else if (method === 'tools/list') {
      process.stdout.write(JSON.stringify({
        jsonrpc: '2.0',
        id,
        result: { tools: TOOLS }
      }) + '\n');
    } else if (method === 'tools/call') {
      const toolName = req.params.name;
      const toolArgs = req.params.arguments || {};
      let result;

      if (toolName === 'blender_execute_code') {
        result = handleExecuteCode(toolArgs);
      } else if (toolName === 'blender_open_gui') {
        result = handleOpenGui(toolArgs);
      } else if (toolName === 'blender_export_model') {
        result = handleExport(toolArgs);
      } else {
        throw new Error(`Tool not found: ${toolName}`);
      }

      process.stdout.write(JSON.stringify({
        jsonrpc: '2.0',
        id,
        result: {
          content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
        }
      }) + '\n');
    }
  } catch (err) {
    // Handle error gracefully
  }
});
