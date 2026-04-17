# HOW I BUILT THE LIFE TWIN INSIGHT AGENT

## What I built
A personal human optimization agent that takes a user's question about sleep,
energy crashes, focus, or habits and returns a SMILE-grounded answer synthesized
by a local LLM — with full tool provenance.

## Step-by-step

1. Set up the LPI sandbox — resolved npm and macOS pip issues, passed 8/8 tool tests
2. Studied examples/agent.py to understand MCP subprocess communication and JSON-RPC
3. Built the agent with direct MCP calls (no LangChain/CrewAI)
4. Added Ollama integration using stdlib urllib — no external dependencies
5. Made query_knowledge use the actual user question dynamically, not a hardcoded string
6. Added auto path detection so the repo root resolves relative to the script

## Problems I hit
- macOS blocked pip system-wide — fixed with venv
- Campus WiFi blocked PyPI — dropped requests entirely, used urllib from stdlib
- Initial agent didn't call an LLM at all — rewrote to pass tool outputs to qwen2.5:1.5b
- Hardcoded desktop path wouldn't work on other machines — switched to relative path detection

## Choices I made that weren't in the instructions
I skipped LangChain and CrewAI even though they were suggested. I wanted to
understand the MCP protocol directly — the JSON-RPC handshake, initialize sequence,
tool call structure — before abstracting it away. If I can't explain what a library
does underneath, I don't trust it.

I also focused the agent on personal health optimization rather than building a
generic SMILE explainer. My Level 1 my_twin answer was about tracking afternoon
energy crashes — so I built the agent to actually answer that question.

## What I'd do differently
I'd make tool selection dynamic — right now it always calls the same 3 tools
regardless of the question. A smarter agent would route to different tools based
on what the question is actually about. I'd also add streaming output so the
response appears token by token instead of making the user wait.

## What I learned
MCP turns tools into modular reasoning building blocks. The agent doesn't need
to know everything — it queries specialized tools, grounds answers in methodology,
and exposes provenance. The strongest AI systems are not just smart, they are
structured, explainable, and connected to real feedback loops.
