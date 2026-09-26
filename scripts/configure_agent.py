"""Print a TrueForge agent payload or register it with --apply."""
import argparse
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
READS = ["get_file_contents", "list_commits", "get_commit", "list_branches"]
WRITES = ["create_branch", "push_files", "create_pull_request"]

def build(model, connector):
    if not model.strip() or not connector.strip():
        raise ValueError("Model and connector names required")
    return {
        "name": "patchpilot",
        "description": "Reproduce and validate a Python repair; approve before GitHub writes.",
        "manifest": {
            "model": {"name": model},
            "instructions": (ROOT / "agent/instructions.md").read_text(encoding="utf-8-sig"),
            "mcp_servers": [{"name": connector, "enable_tools": READS + WRITES,
                             "require_approval_for_tools": WRITES, "preload": True}],
            "config": {
                "sandbox": {"enabled": True},
                "dynamic_sub_agents": {"enabled": False},
                "ask_user_questions": {"enabled": True},
                "generative_ui": {"enabled": False},
                "iteration_limit": 60,
            },
        },
    }

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model", required=True)
    p.add_argument("--connector", default="github")
    p.add_argument("--base-url", default="http://localhost:8790")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    payload = build(args.model, args.connector)
    if not args.apply:
        print(json.dumps(payload, indent=2))
        return
    parsed = urlparse(args.base_url)
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        p.error("Use a base URL without credentials, query or fragment")
    if parsed.scheme != "https" and not (parsed.scheme == "http" and parsed.hostname in ("localhost", "127.0.0.1", "::1")):
        p.error("Remote connections require HTTPS or a localhost SSH tunnel")
    headers = {"Content-Type": "application/json"}
    if os.getenv("TRUEFORGE_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["TRUEFORGE_TOKEN"]
    request = Request(args.base_url.rstrip("/") + "/api/v1/agents",
                      data=json.dumps(payload).encode(), headers=headers, method="POST")
    try:
        with urlopen(request, timeout=30) as response:
            json.load(response)
        print("Created PatchPilot. Verify three write-tool approval shields in TrueForge.")
    except HTTPError as exc:
        message = "Agent exists; edit it in TrueForge. Nothing overwritten." if exc.code == 409 else "Check server auth, model and connector names."
        raise SystemExit(f"HTTP {exc.code}: {message}") from None
    except (URLError, TimeoutError):
        raise SystemExit("Could not reach TrueForge; check the server and base URL.") from None

if __name__ == "__main__":
    main()

