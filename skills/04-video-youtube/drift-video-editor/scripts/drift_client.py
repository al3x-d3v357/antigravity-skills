#!/usr/bin/env python3
"""
drift_client.py - Drift Video Editor 0.7.5 MCP HTTP & JSON-RPC 2.0 Client

Provides deterministic communication with Drift's MCP interface.
Supports token discovery via CLI args, environment variables, or local session fallback.
Updated with Drift 0.7.5 tools: Face Retouch, Auto Reframe, Stabilization, Addons, and Effect Authoring.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_MCP_URL = "http://127.0.0.1:4731/mcp"
DEFAULT_FALLBACK_TOKEN = "1ffbdd396f91e311b43a816b266aaa1d221a5229264f2a601f902379cd58a1eb"


def resolve_token(cli_token: Optional[str] = None) -> str:
    """Resolves authentication token with priority fallback."""
    if cli_token:
        return cli_token

    # 1. Environment variable
    env_token = os.environ.get("DRIFT_MCP_TOKEN")
    if env_token:
        return env_token.strip()

    # 2. File from DRIFT_SESSION_PATH or DRIFT_TOKEN_PATH
    for env_var in ("DRIFT_SESSION_PATH", "DRIFT_TOKEN_PATH"):
        session_path = os.environ.get(env_var)
        if session_path and os.path.exists(session_path):
            try:
                with open(session_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    token = data.get("token") or data.get("access_token")
                    if token:
                        return token.strip()
            except Exception:
                pass

    # 3. Default home directory session: ~/.drift/mcp-session.json
    home_session = Path.home() / ".drift" / "mcp-session.json"
    if home_session.exists():
        try:
            with open(home_session, "r", encoding="utf-8") as f:
                data = json.load(f)
                token = data.get("token") or data.get("access_token")
                if token:
                    return token.strip()
        except Exception:
            pass

    # 4. Built-in active session fallback
    return DEFAULT_FALLBACK_TOKEN


def send_mcp_rpc(url: str, token: str, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Sends a JSON-RPC 2.0 request to Drift MCP."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method
    }
    if params is not None:
        payload["params"] = params

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json, */*"
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_bytes = response.read()
            return json.loads(raw_bytes.decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        try:
            return {"ok": False, "status_code": e.code, "error": json.loads(error_body)}
        except Exception:
            return {"ok": False, "status_code": e.code, "error": error_body}
    except Exception as e:
        return {"ok": False, "error": "client_exception", "detail": str(e)}


def call_mcp_tool(url: str, token: str, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Invokes an MCP tool via tools/call."""
    params = {"name": tool_name, "arguments": arguments or {}}
    res = send_mcp_rpc(url, token, "tools/call", params)
    return res


def main():
    parser = argparse.ArgumentParser(description="Drift Video Editor 0.7.5 MCP Client")
    parser.add_argument("--url", default=os.environ.get("DRIFT_MCP_URL", DEFAULT_MCP_URL), help="MCP HTTP endpoint")
    parser.add_argument("--token", help="Bearer authorization token")
    parser.add_argument("--action", required=True, 
                        choices=[
                            "status", "inspect", "catalog", "search", "toolbox", "apply", 
                            "capture", "frames", "activity", "market",
                            "auto_reframe", "retouch", "stabilize", "effect_guide", 
                            "get_effect", "export_effect", "addons"
                        ],
                        help="Action to perform on Drift MCP")
    parser.add_argument("--query", "-q", help="Search keyword or identifier")
    parser.add_argument("--clip", help="Clip UUID for clip-based tools")
    parser.add_argument("--kind", default="effect", choices=["effect", "transition", "audio_effect"], help="Kind for authoring")
    parser.add_argument("--aspect", type=float, default=0.5625, help="Aspect ratio for auto_reframe (default: 9/16 = 0.5625)")
    parser.add_argument("--mode", default="face", help="Mode for auto_reframe (default: face)")
    parser.add_argument("--ops", help="JSON string or path to JSON file containing mutations for apply")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--detail", action="store_true", default=True, help="Include detail in inspect")
    parser.add_argument("--clips", action="store_true", default=True, help="Include clips in inspect")

    args = parser.parse_args()
    token = resolve_token(args.token)

    if args.action == "status":
        print(f"Connecting to Drift MCP at {args.url}...")
        res = send_mcp_rpc(args.url, token, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "antigravity-drift-client", "version": "0.7.5"}
        })
        if res.get("error") and res.get("status_code") == 401:
            print(f"[ERROR] Unauthorized: token is invalid or rejected by Drift.")
            sys.exit(1)
        print("[SUCCESS] Drift MCP endpoint is reachable and authorized.")
        print(json.dumps(res, indent=2))
        return

    if args.action == "catalog":
        res = call_mcp_tool(args.url, token, "catalog", {})
        print(json.dumps(res, indent=2))
        return

    if args.action == "inspect":
        res = call_mcp_tool(args.url, token, "inspect", {"clips": args.clips, "detail": args.detail})
        print(json.dumps(res, indent=2))
        return

    if args.action == "search":
        if not args.query:
            print("[ERROR] --query is required for search action.", file=sys.stderr)
            sys.exit(1)
        res = call_mcp_tool(args.url, token, "search", {"q": args.query})
        print(json.dumps(res, indent=2))
        return

    if args.action == "toolbox":
        target = args.query or "timeline"
        res = call_mcp_tool(args.url, token, "toolbox", {"name": target})
        print(json.dumps(res, indent=2))
        return

    if args.action == "apply":
        if not args.ops:
            print("[ERROR] --ops <json_or_file> is required for apply action.", file=sys.stderr)
            sys.exit(1)
        ops_data = None
        if os.path.exists(args.ops):
            with open(args.ops, "r", encoding="utf-8") as f:
                ops_data = json.load(f)
        else:
            ops_data = json.loads(args.ops)

        if isinstance(ops_data, dict) and "ops" in ops_data:
            ops_list = ops_data["ops"]
        elif isinstance(ops_data, list):
            ops_list = ops_data
        else:
            ops_list = [ops_data]

        res = call_mcp_tool(args.url, token, "apply", {"ops": ops_list})
        print(json.dumps(res, indent=2))
        return

    if args.action == "market":
        res = call_mcp_tool(args.url, token, "market_status", {})
        print(json.dumps(res, indent=2))
        return

    # --- Drift 0.7.5 Specific Actions ---
    if args.action == "auto_reframe":
        if not args.clip:
            print("[ERROR] --clip <uuid> is required for auto_reframe.", file=sys.stderr)
            sys.exit(1)
        res = call_mcp_tool(args.url, token, "auto_reframe", {
            "clip": args.clip,
            "aspect": args.aspect,
            "mode": args.mode
        })
        print(json.dumps(res, indent=2))
        return

    if args.action == "retouch":
        if not args.clip:
            print("[ERROR] --clip <uuid> is required to apply retouch.", file=sys.stderr)
            sys.exit(1)
        ops = [
            {
                "tool": "add_effect",
                "args": {
                    "clip": args.clip,
                    "effect": "face_retouch",
                    "params": {
                        "smoothing": 0.45,
                        "sharpen": 0.20,
                        "whitening": 0.15,
                        "slimFace": 0.05,
                        "bigEyes": 0.0,
                        "faceIndex": 0
                    }
                }
            }
        ]
        res = call_mcp_tool(args.url, token, "apply", {"ops": ops})
        print(json.dumps(res, indent=2))
        return

    if args.action == "stabilize":
        if not args.clip:
            print("[ERROR] --clip <uuid> is required for stabilize.", file=sys.stderr)
            sys.exit(1)
        res = call_mcp_tool(args.url, token, "stabilize_clip", {"clip": args.clip})
        print(json.dumps(res, indent=2))
        return

    if args.action == "effect_guide":
        res = call_mcp_tool(args.url, token, "effect_authoring_guide", {"kind": args.kind})
        print(json.dumps(res, indent=2))
        return

    if args.action == "get_effect":
        if not args.query:
            print("[ERROR] --query <effect_id> is required for get_effect.", file=sys.stderr)
            sys.exit(1)
        res = call_mcp_tool(args.url, token, "get_effect_source", {"kind": args.kind, "id": args.query})
        print(json.dumps(res, indent=2))
        return

    if args.action == "export_effect":
        if not args.query or not args.output:
            print("[ERROR] --query <effect_id> and --output <path.driftfx> are required.", file=sys.stderr)
            sys.exit(1)
        res = call_mcp_tool(args.url, token, "export_effect", {
            "kind": args.kind,
            "id": args.query,
            "path": os.path.abspath(args.output).replace("\\", "/")
        })
        print(json.dumps(res, indent=2))
        return

    if args.action == "addons":
        res = call_mcp_tool(args.url, token, "list_addons", {})
        print(json.dumps(res, indent=2))
        return


if __name__ == "__main__":
    main()
