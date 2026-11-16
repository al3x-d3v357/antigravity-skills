#!/usr/bin/env python3
"""MCP Server for inspecting, creating, editing, and opening DragonBones Pro projects."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

DRAGONBONES_DIR = Path(r"D:\Programas\Egret\DragonBonesPro")
DRAGONBONES_EXE = DRAGONBONES_DIR / "DragonBonesPro.exe"
EXAMPLES_DIR = DRAGONBONES_DIR / "examples"
PROJECTS_2D_DIR = Path(r"D:\Projetos\2D")
SEARCH_ROOTS = (PROJECTS_2D_DIR, Path(r"D:\Projetos\Unity"), EXAMPLES_DIR)

TOOLS: list[dict[str, Any]] = [
    {
        "name": "get_dragonbones_info",
        "description": "Return DragonBones Pro installation details, executable status, and default directories on D:.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "list_dragonbones_projects",
        "description": "List DragonBones projects and exports (.dbproj, *_ske.json, *.ExportJson, examples) on D:.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Optional directory on D: to scan instead of default project folders.",
                }
            },
        },
    },
    {
        "name": "inspect_dragonbones_data",
        "description": "Inspect a DragonBones .dbproj or skeleton JSON file (armatures, bones, slots, skins, animations).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the .dbproj or skeleton .json file."}
            },
            "required": ["path"],
        },
    },
    {
        "name": "create_dragonbones_project",
        "description": "Create a new DragonBones skeleton JSON (*_ske.json) and texture atlas JSON (*_tex.json) on D:\\Projetos\\2D.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Project / armature name."},
                "output_dir": {
                    "type": "string",
                    "description": "Optional target directory on D:. Defaults to D:\\Projetos\\2D\\<name>.",
                },
                "frame_rate": {"type": "integer", "description": "Animation frame rate (default 24)."},
                "bones": {
                    "type": "array",
                    "description": "Optional list of bones: {name, parent?, x?, y?, length?}.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "parent": {"type": "string"},
                            "x": {"type": "number"},
                            "y": {"type": "number"},
                            "length": {"type": "number"},
                        },
                        "required": ["name"],
                    },
                },
                "slots": {
                    "type": "array",
                    "description": "Optional list of slots: {name, parent}.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "parent": {"type": "string"},
                        },
                        "required": ["name", "parent"],
                    },
                },
            },
            "required": ["name"],
        },
    },
    {
        "name": "add_dragonbones_animation",
        "description": "Add or update an animation in an existing DragonBones skeleton JSON file.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to *_ske.json or DragonBones .json file."},
                "armature_name": {
                    "type": "string",
                    "description": "Target armature name (defaults to the first armature).",
                },
                "animation_name": {"type": "string", "description": "Name of the animation to add or update."},
                "duration": {"type": "integer", "description": "Duration in frames (default 24)."},
                "play_times": {"type": "integer", "description": "Loop count (0 = infinite loop, default 0)."},
                "bones": {
                    "type": "array",
                    "description": "Optional DragonBones bone timeline entries.",
                    "items": {"type": "object"},
                },
            },
            "required": ["path", "animation_name"],
        },
    },
    {
        "name": "open_in_dragonbones",
        "description": "Launch DragonBonesPro.exe, optionally opening a specific .dbproj or project file.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Optional path to a .dbproj or DragonBones file to open.",
                }
            },
        },
    },
]


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def inspect_dragonbones(path: Path) -> dict[str, Any]:
    data = _read_json(path)
    armatures = data.get("armature") or data.get("armatures") or []
    summary: list[dict[str, Any]] = []
    for arm in armatures:
        if not isinstance(arm, dict):
            continue
        bones = arm.get("bone") or []
        slots = arm.get("slot") or []
        skins = arm.get("skin") or []
        animations = arm.get("animation") or []
        summary.append(
            {
                "name": arm.get("name"),
                "type": arm.get("type"),
                "frameRate": arm.get("frameRate"),
                "bone_count": len(bones),
                "bones": [b.get("name") for b in bones if isinstance(b, dict)],
                "slot_count": len(slots),
                "skin_count": len(skins),
                "animations": [
                    {
                        "name": a.get("name"),
                        "duration": a.get("duration"),
                        "playTimes": a.get("playTimes"),
                    }
                    for a in animations
                    if isinstance(a, dict)
                ],
            }
        )
    return {
        "path": str(path),
        "name": data.get("name"),
        "version": data.get("version"),
        "frameRate": data.get("frameRate"),
        "armature_count": len(summary),
        "armatures": summary,
    }


def create_project(args: dict[str, Any]) -> dict[str, Any]:
    name = args["name"].strip()
    if not name:
        raise ValueError("Project name cannot be empty.")
    out_dir = Path(args["output_dir"]) if args.get("output_dir") else (PROJECTS_2D_DIR / name)
    out_dir.mkdir(parents=True, exist_ok=True)

    frame_rate = int(args.get("frame_rate", 24))
    bones: list[dict[str, Any]] = [{"name": "root"}]
    for b in args.get("bones") or []:
        if b["name"] == "root":
            continue
        entry: dict[str, Any] = {"name": b["name"], "parent": b.get("parent", "root")}
        if "length" in b:
            entry["length"] = b["length"]
        if "x" in b or "y" in b:
            entry["transform"] = {"x": b.get("x", 0), "y": b.get("y", 0)}
        bones.append(entry)

    slots = [{"name": s["name"], "parent": s["parent"]} for s in (args.get("slots") or [])]

    ske_data = {
        "frameRate": frame_rate,
        "name": name,
        "version": "5.5",
        "compatibleVersion": "5.5",
        "armature": [
            {
                "type": "Armature",
                "frameRate": frame_rate,
                "name": name,
                "bone": bones,
                "slot": slots,
                "skin": [{"slot": []}],
                "animation": [{"duration": 0, "playTimes": 0, "name": "idle"}],
                "defaultActions": [{"gotoAndPlay": "idle"}],
            }
        ],
    }

    tex_data = {
        "width": 512,
        "height": 512,
        "name": name,
        "imagePath": f"{name}_tex.png",
        "SubTexture": [],
    }

    ske_path = out_dir / f"{name}_ske.json"
    tex_path = out_dir / f"{name}_tex.json"
    ske_path.write_text(json.dumps(ske_data, indent=2), encoding="utf-8")
    tex_path.write_text(json.dumps(tex_data, indent=2), encoding="utf-8")

    return {
        "created": True,
        "project_dir": str(out_dir),
        "skeleton_file": str(ske_path),
        "texture_atlas_file": str(tex_path),
    }


def add_animation(args: dict[str, Any]) -> dict[str, Any]:
    path = Path(args["path"])
    data = _read_json(path)
    armatures = data.get("armature")
    if not isinstance(armatures, list) or not armatures:
        raise ValueError(f"No armatures found in {path}")

    target_name = args.get("armature_name")
    armature = next(
        (a for a in armatures if isinstance(a, dict) and (not target_name or a.get("name") == target_name)),
        None,
    )
    if armature is None:
        raise ValueError(f"Armature '{target_name}' not found in {path}")

    anim_name = args["animation_name"]
    new_anim: dict[str, Any] = {
        "name": anim_name,
        "duration": int(args.get("duration", 24)),
        "playTimes": int(args.get("play_times", 0)),
    }
    if args.get("bones"):
        new_anim["bone"] = args["bones"]

    animations = armature.setdefault("animation", [])
    idx = next((i for i, a in enumerate(animations) if isinstance(a, dict) and a.get("name") == anim_name), None)
    if idx is None:
        animations.append(new_anim)
        action = "added"
    else:
        animations[idx] = new_anim
        action = "updated"

    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return {"path": str(path), "armature": armature.get("name"), "animation": anim_name, "action": action}


def list_projects(directory: str | None = None) -> dict[str, Any]:
    roots = (Path(directory),) if directory else SEARCH_ROOTS
    skip_dirs = {"Library", "Temp", "Logs", "obj", "Build", ".git", "node_modules", "__pycache__"}
    suffixes = (".dbproj", ".exportjson", ".zip")
    found: list[str] = []

    def _walk(folder: Path) -> None:
        try:
            for entry in folder.iterdir():
                if entry.is_dir():
                    if entry.name not in skip_dirs:
                        _walk(entry)
                elif entry.name.lower().endswith(suffixes) or entry.name.lower().endswith("_ske.json"):
                    found.append(str(entry))
        except OSError:
            pass

    for root in roots:
        if root.exists():
            _walk(root)
    return {"projects": sorted(set(found))}


def handle_tool_call(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "get_dragonbones_info":
        res = {
            "install_dir": str(DRAGONBONES_DIR),
            "executable": str(DRAGONBONES_EXE),
            "executable_exists": DRAGONBONES_EXE.exists(),
            "examples_dir": str(EXAMPLES_DIR),
            "projects_2d_dir": str(PROJECTS_2D_DIR),
        }
    elif name == "list_dragonbones_projects":
        res = list_projects(args.get("directory"))
    elif name == "inspect_dragonbones_data":
        res = inspect_dragonbones(Path(args["path"]))
    elif name == "create_dragonbones_project":
        res = create_project(args)
    elif name == "add_dragonbones_animation":
        res = add_animation(args)
    elif name == "open_in_dragonbones":
        if not DRAGONBONES_EXE.exists():
            raise FileNotFoundError(f"DragonBonesPro.exe not found at {DRAGONBONES_EXE}")
        cmd = [str(DRAGONBONES_EXE)]
        if args.get("path"):
            cmd.append(str(Path(args["path"])))
        subprocess.Popen(cmd, cwd=str(DRAGONBONES_DIR), start_new_session=True)
        res = {"launched": True, "command": cmd}
    else:
        raise ValueError(f"Unknown tool: {name}")

    return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}


def main() -> None:
    """Run MCP stdio JSON-RPC 2.0 loop."""
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params") or {}
        if req_id is None:
            continue

        try:
            if method == "initialize":
                result: dict[str, Any] = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "dragonbones-mcp", "version": "1.0.0"},
                }
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": TOOLS}
            elif method == "tools/call":
                result = handle_tool_call(params["name"], params.get("arguments") or {})
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"},
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
                continue
            resp = {"jsonrpc": "2.0", "id": req_id, "result": result}
        except Exception as exc:
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32000, "message": str(exc)},
            }

        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
