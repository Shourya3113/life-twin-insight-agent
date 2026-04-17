#!/usr/bin/env python3
"""
Life Twin Insight Agent
Track A — Level 3 submission for the LifeAtlas LPI Developer Kit.

Purpose:
Transforms user questions about sleep, focus, energy, stress, and habit loops
into explainable SMILE-based optimization plans using LPI MCP tools + local LLM.
"""

import json
import subprocess
import sys
import os
import urllib.request
import urllib.error

# Auto-detect repo root relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(SCRIPT_DIR, "..", "lpi-developer-kit")
REPO_ROOT = os.path.abspath(REPO_ROOT)
LPI_SERVER_CMD = ["node", os.path.join(REPO_ROOT, "dist", "src", "index.js")]
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:1.5b"


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


def call_ollama(prompt: str) -> str:
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "[ERROR] No response from Ollama")
    except urllib.error.URLError:
        return "[ERROR] Ollama not running. Start it with: ollama serve"


def run_agent(question: str):
    # Check sandbox exists
    index_path = os.path.join(REPO_ROOT, "dist", "src", "index.js")
    if not os.path.exists(index_path):
        print(f"[ERROR] LPI sandbox not found at {REPO_ROOT}. Run npm install && npm run build first.")
        sys.exit(1)

    proc = subprocess.Popen(
        LPI_SERVER_CMD,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=REPO_ROOT,
    )

    # MCP initialize handshake
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

    print("\n🔍 Querying LPI tools...\n")

    # Tool 1: SMILE overview — methodology foundation
    print("[1/3] smile_overview — loading SMILE methodology...")
    smile_overview = call_mcp_tool(proc, "smile_overview", {})

    # Tool 2: get_insights — personal health digital twin context
    print("[2/3] get_insights — fetching personal health digital twin guidance...")
    insights = call_mcp_tool(
        proc, "get_insights",
        {"scenario": "personal health digital twin", "tier": "free"}
    )

    # Tool 3: query_knowledge — search using the ACTUAL user question
    print("[3/3] query_knowledge — searching knowledge base for your question...")
    knowledge = call_mcp_tool(
        proc, "query_knowledge",
        {"query": question}
    )

    proc.terminate()

    # Build prompt for LLM with full provenance context
    prompt = f"""You are a personal life optimization AI agent built on the SMILE methodology (Sustainable Methodology for Impact Lifecycle Enablement).

A user has asked: "{question}"

You have gathered the following knowledge from three LPI tools:

--- [Tool 1: smile_overview] ---
{smile_overview[:1200]}

--- [Tool 2: get_insights (personal health digital twin)] ---
{insights[:1000]}

--- [Tool 3: query_knowledge("{question}")] ---
{knowledge[:1000]}

Based ONLY on the above tool outputs, answer the user's question with:
1. A direct answer grounded in SMILE methodology
2. Specific actionable recommendations
3. Which SMILE phase(s) are most relevant to their situation
4. One insight that surprised you from the knowledge base

Be specific, practical, and cite which tool provided each key insight. Format clearly."""

    print("\n🤖 Synthesizing with local LLM (qwen2.5:1.5b)...\n")
    answer = call_ollama(prompt)

    print("=" * 70)
    print("🧠 LIFE TWIN INSIGHT REPORT")
    print("=" * 70)
    print(f"\nQuestion: {question}\n")
    print(answer)
    print("\n" + "=" * 70)
    print("✅ PROVENANCE — Tools Used")
    print("=" * 70)
    print("[1] smile_overview({}) — SMILE methodology foundation")
    print("[2] get_insights({scenario: 'personal health digital twin'}) — health guidance")
    print(f'[3] query_knowledge({{query: "{question}"}}) — knowledge base search')
    print("=" * 70)


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print('Usage: python3 agent.py "Why do I crash every afternoon?"')
            sys.exit(1)

        question = sys.argv[1].strip()

        if len(question) < 5:
            print("[ERROR] Please provide a more descriptive question.")
            sys.exit(1)

        run_agent(question)

    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}. Check your setup.")
    except Exception as e:
        print(f"[ERROR] Agent failed: {e}")
