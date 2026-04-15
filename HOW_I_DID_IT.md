# HOW I BUILT THE LIFE TWIN INSIGHT AGENT

## 1) What I built
I built a **human performance digital twin agent** that helps translate questions around sleep quality, energy crashes, focus depth, stress, and workout consistency into structured SMILE-based optimization insights.

The goal was to make the agent feel like the first layer of a personal life operating system that can help users understand why their performance fluctuates and what recovery or optimization actions they should take.

---

## 2) Step-by-step workflow
### Step 1 — LPI sandbox setup
I first completed the full LPI sandbox setup:
- installed Node.js
- resolved npm compatibility and cache issues
- ran `npm run build`
- successfully passed all **8/8 LPI tool tests**

This gave me confidence that the MCP tool layer was stable.

### Step 2 — studied the example agent
I studied the provided `examples/agent.py` to understand:
- subprocess-based MCP communication
- JSON-RPC tool calling
- initialization handshake
- provenance tracking

### Step 3 — customized for human optimization
Instead of building a generic methodology agent, I focused on a **personal health and performance digital twin use case**, because this aligns strongly with my research interests in AI, human optimization, and adaptive systems.

I selected these tools:
- `smile_overview`
- `get_insights`
- `query_knowledge`

to combine methodology, personal health guidance, and performance optimization context.

### Step 4 — explainability layer
I made sure the final report clearly lists:
- which tools were used
- why each tool contributed
- how the output maps to the user’s question

This was important because explainable AI is one of the strongest evaluation criteria in the program.

---

## 3) Problems I hit and how I solved them
The biggest challenge was **environment setup on macOS over campus Wi-Fi**.

I faced:
- DNS failures with GitHub
- npm version instability
- cache permission issues
- Ollama registry DNS issues

I solved these by:
- switching DNS servers
- moving Git to SSH authentication
- downgrading npm to a stable version
- fixing cache ownership issues
- validating the full sandbox before building the agent

This taught me the importance of solving infrastructure friction early before building product logic.

---

## 4) What I learned
The biggest thing I learned was how **MCP turns tools into modular reasoning building blocks**.

Rather than making the LLM “know everything,” the agent becomes much more reliable when it:
1. queries specialized tools
2. grounds answers in methodology
3. exposes clear provenance

This project changed how I think about building AI systems:
the strongest systems are not just smart, they are **structured, explainable, and deeply connected to real-world feedback loops**.