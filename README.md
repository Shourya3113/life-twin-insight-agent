# Life Twin Insight Agent

A Track A — Level 3 submission for the **LifeAtlas LPI Developer Kit**.

## What it does
The **Life Twin Insight Agent** is a personal human optimization AI agent that converts user questions about:

- sleep quality
- daily energy crashes
- focus depth
- stress patterns
- workout consistency
- productivity habit loops

into **SMILE-based digital twin optimization insights**.

It connects directly to the **LPI MCP Sandbox** and uses 3 explainable tools:
- `smile_overview`
- `get_insights`
- `query_knowledge`

The output provides:
1. SMILE methodology foundation
2. personal health digital twin recommendations
3. knowledge-base context for human performance optimization
4. explicit provenance of all sources used

---

## Why I built this
My goal was to create an agent that reflects how a personal digital twin could help predict low-energy periods, connect them to sleep, nutrition, stress, and habits, and proactively recommend recovery actions before performance drops.

This directly connects to my broader interest in:
- AI agents
- health intelligence
- human optimization
- digital twins
- quantum-inspired adaptive systems

---

## Usage
```bash
python agent.py "Why do I crash every afternoon?"


## Setup Instructions
### Requirements
- Python 3.10+
- Node.js
- Built `lpi-developer-kit` sandbox (`npm install && npm run build`)

### Install dependencies
```bash
pip install -r requirements.txt

Run the agent
python3 agent.py "Why do I crash every afternoon?"

How bad input is handled
- If no question is provided → usage help is shown
- If the question is too short → a descriptive error is returned
- If the sandbox build is missing → a safe setup error is shown
- Unexpected runtime errors are caught gracefully

open -a "Visual Studio Code" agent.py
