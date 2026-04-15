#!/usr/bin/env python3
"""
Life Twin Insight Agent
A Level 3 Track A submission for the LifeAtlas LPI Developer Kit.

Purpose:
Transforms user questions about sleep, focus, energy, stress, and habit loops
into explainable SMILE-based optimization plans using LPI MCP tools.
"""

import json
import subprocess
import sys
import os

REPO_ROOT = os.path.expanduser("~/Desktop/lpi-developer-kit")
LPI_SERVER_CMD = ["node", os.path.join(REPO_ROOT, "dist", "src", "index.js")]


def call_mcp_tool(process, tool_name: str, arguments: dict) -> str:
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
    }
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()

    line = process.stdout.readline()
    if not line:
        return f"[ERROR] No response from {tool_name}"

    response = json.loads(line)
    if "result" in response and "content" in response["result"]:
        return response["result"]["content"][0].get("text", "")
    return "[ERROR] Unexpected MCP response"


def run_agent(question: str):
    proc = subprocess.Popen(
        LPI_SERVER_CMD,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=REPO_ROOT,
    )

    # MCP initialize
    init_req = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "life-twin-insight-agent", "version": "1.0"},
        },
    }
    proc.stdin.write(json.dumps(init_req) + "\n")
    proc.stdin.flush()
    proc.stdout.readline()

    notif = {"jsonrpc": "2.0", "method": "notifications/initialized"}
    proc.stdin.write(json.dumps(notif) + "\n")
    proc.stdin.flush()

    print("\n🔍 Gathering SMILE-based optimization insights...\n")

    smile_overview = call_mcp_tool(proc, "smile_overview", {})
    insights = call_mcp_tool(
        proc,
        "get_insights",
        {"scenario": "personal health digital twin", "tier": "free"},
    )
    knowledge = call_mcp_tool(
        proc,
        "query_knowledge",
        {"query": "human performance optimization and habit loops"},
    )

    proc.terminate()

    print("=" * 70)
    print("🧠 LIFE TWIN INSIGHT REPORT")
    print("=" * 70)
    print(f"\nQuestion: {question}\n")

    print("📌 SMILE FOUNDATION")
    print(smile_overview[:600])

    print("\n⚡ PERSONAL HEALTH DIGITAL TWIN INSIGHTS")
    print(insights[:800])

    print("\n📚 KNOWLEDGE BASE CONTEXT")
    print(knowledge[:800])

    print("\n" + "=" * 70)
    print("✅ SOURCES USED")
    print("=" * 70)
    print("[1] smile_overview")
    print("[2] get_insights(personal health digital twin)")
    print("[3] query_knowledge(human performance optimization)")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python agent.py "Why do I crash every afternoon?"')
        sys.exit(1)

    run_agent(sys.argv[1])