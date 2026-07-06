# 🧭 Disha AI

## *The life companion every Indian student deserves at every crossroads*

> \\\*\\\*Kaggle / Google — AI Agents Intensive Vibe Coding Capstone 2026\\\*\\\*
> \\\*\\\*Track: Agents for Good\\\*\\\* | Freestyle sub-track

[!\[ADK 2.0](https://img.shields.io/badge/Google%20ADK-2.0-green)](https://adk.dev)
[!\[Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-purple)](https://aistudio.google.com)
[!\[MCP](https://img.shields.io/badge/MCP-Filesystem-orange)](https://modelcontextprotocol.io)
[!\[Cost](https://img.shields.io/badge/Cost-₹0%20Free-brightgreen)](https://aistudio.google.com/apikey)
[!\[Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)

\---

## The Problem — Backed by the United Nations

> \\\*"The Bharat Career Aspirations Report 2025 (UNICEF) reveals that only 1 in 10 Indian students in Classes 9–12 have access to professional career guidance. The remaining 9 in 10 navigate their futures based on family advice, peer pressure, or outdated notions of safe careers."\\\*

**250 million students** are currently enrolled in Indian schools and colleges.

**225 million of them** are making the biggest decisions of their lives — which stream after 10th, which college, JEE or NEET, GATE or job, India or abroad — completely alone.

Not because they're lazy. Not because they're incapable.

Because **no tool exists that understands their complete situation** — their SC/ST category advantage they don't know about, their family's financial constraints, their desire to stay near their parents, their confusion about scholarships they qualify for, their stress about disappointing people who love them.

Disha AI was built because **we are this student.** We built the tool we needed and never had.

\---

## What Disha AI Does

Disha AI is a **multi-agent life navigation system** that walks with Indian students at every major crossroads of their educational journey:

```
SECONDARY TRANSITION (Class 10 Completion)
   │
   ▼ Stream Stratification Mapping (Science, Commerce, Humanities, or Applied Vocational Tracks)
   │
SENIOR SECONDARY PIVOT (Class 12 Completion)
   │
   ▼ Multi-Channel Alignment (National Entrances, Professional Foundations, Creative Design, or Direct Degree Formats)
   │
TERTIARY GRADUATION LOOP (Undergraduate Completion)
   │
   ▼ Strategic Career Routing (Corporate Placement, Post-Graduate Research, Specialized Diplomas, or International Specialization)
   │
ACUTE STAGNATION STATE (Lost / Unsure Target Alignment)
   ▼ Behavioral Trajectory Calibration (Decompression, Latent Focus Mapping, and Immediate Action Deployment)
```

Unlike existing tools that give a one-time psychometric test and disappear, **Disha remembers you.** Every session is saved locally. When you return, Disha knows your name, your family situation, what you decided last time, and how your life has changed.

\---

## Architecture — ADK 2.0 Graph Workflow

╔═══════════════════════════════════════════════════════════════════════════╗
║                     DISHA AI — SYSTEM ARCHITECTURE                        ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   Student opens Streamlit UI Interface                                    ║
║           │                                                               ║
║           ▼                                                               ║
║   ┌───────────────────────────────────────────────────────────────────┐   ║
║   │              ADK 2.0 GRAPH WORKFLOW (root_agent)                  │   ║
║   │   Workflow(name="disha_ai", edges=[...])                          │   ║
║   │                                                                   │   ║
║   │  START                                                            │   ║
║   │    │                                                              │   ║
║   │    ▼                                                              │   ║
║   │  [NODE 1] stage_router (gemini-2.5-flash)                         │   ║
║   │    • Multi-turn synchronous task profiling execution              │   ║
║   │    • Extracts: Life Stage, Category, Income, Spatial, Stress      │   ║
║   │    • Output: Sanitized LifeContext JSON Payload                   │   ║
║   │    │                                                              │   ║
║   │    ▼                                                              │   ║
║   │  [NODE 2] interest_discovery (gemini-2.5-flash)                   │   ║
║   │    • Behavioral Elicitation (Bypasses stated preference bias)     │   ║
║   │    • Probes: Absorption, Social Competency, Revealed Consumption  │   ║
║   │    • Classification: Maps input into 11 Cognitive Token Clusters  │   ║
║   │    • Output: InterestProfile JSON Appended State                  │   ║
║   │    │                                                              │   ║
║   │    ▼                                                              │   ║
║   │  [NODE 3] india_opportunity_finder (gemini-2.5-flash + Search UI) │   ║
║   │    • Target Runtime Context Expansion (Live API Ingestion)        │   ║
║   │    • Dynamically resolves localized statutory aid & scholarships  │   ║
║   │    • Pulls active domain entrance rules, cutoffs & job metrics    │   ║
║   │    • Output: Localized OpportunityMap JSON Data Structure         │   ║
║   │    │                                                              │   ║
║   │    ▼                                                              │   ║
║   │  [NODE 4] path_architect (gemini-2.5-flash)                       │   ║
║   │    • Multi-variable optimization pass across all disciplines      │   ║ 
║   │    • Generates: Path A (Risk-Mitigated) & Path B (High Upside)    │   ║
║   │    • Includes hard realities: logistics, resource cost, timelines │   ║
║   │    • Enforces deterministic, singular optimization advice         │   ║
║   │    │                                                              │   ║
║   │    ▼                                                              │   ║
║   │  [NODE 5] first_step_coach (gemini-2.5-flash + MCP FILESYSTEM)    │   ║
║   │    │                                                              │   ║
║   │    │  ┌─────────────────────────────────────────────────────┐     │   ║
║   │    │  │   MCP LOCAL FILESYSTEM SERVER INTERFACE             │     │   ║ 
║   │    │  │   npx @modelcontextprotocol/server-filesystem       │     │   ║
║   │    │  │   Sandboxed to: ./disha_agent/memory_store/         │     │   ║
║   │    │  │                                                     │     │   ║
║   │    │  │   read_file("student_journal.json")  → Past Session │     │   ║
║   │    │  │   write_file("student_journal.json") → State Sync   │     │   ║
║   │    │  └─────────────────────────────────────────────────────┘     │   ║
║   │    │                                                              │   ║
║   │    │  ANTIGRAVITY HARNESS GOVERNOR (Embedded):                    │   ║
║   │    │  IF psychometric_stress >= 7 -> ENGAGE MICRO-STEP MODE       │   ║
║   │    │    → Suppresses roadmap complexity down to <5min bounds      │   ║
║   │    │    → IF stress >= 9 -> Intercept, Freeze Pipeline Advisory   │   ║
║   │    │      → Reroute to multilingual human crisis network (iCall)  │   ║
║   │    │                                                              │   ║
║   │    • Computes granular operational execution target               │   ║
║   │    • Commits session summary transaction via sandboxed MCP        │   ║
║   │    │                                                              │   ║
║   │    ▼                                                              │   ║
║   │   END                                                             │   ║
║   └───────────────────────────────────────────────────────────────────┘   ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

\---

## Course Rubric — All 6 Concepts Demonstrated

###  1. ADK Multi-Agent System (Graph Workflow)

```python
from google.adk import Agent, Workflow

root\\\_agent = Workflow(
    name="disha\\\_ai",
    edges=\\\[
        ("START",             life\\\_stage\\\_detector),
        (life\\\_stage\\\_detector, interest\\\_discovery),
        (interest\\\_discovery,  india\\\_navigator),
        (india\\\_navigator,     path\\\_architect),
        (path\\\_architect,      first\\\_step\\\_coach),
        (first\\\_step\\\_coach,    "END"),
    ],
)
```

Five distinct agents. Five distinct jobs. A directed graph where each edge is architecturally necessary. This is not a chatbot — it's a deterministic multi-agent pipeline.

###  2. MCP Server Integration

```python
from google.adk.tools.mcp\\\_tool.mcp\\\_toolset import MCPToolset
from google.adk.tools.mcp\\\_tool.mcp\\\_session\\\_manager import StdioConnectionParams
from mcp import StdioServerParameters

mcp\\\_memory\\\_toolset = MCPToolset(
    connection\\\_params=StdioConnectionParams(
        server\\\_params=StdioServerParameters(
            command="npx",
            args=\\\["-y", "@modelcontextprotocol/server-filesystem", MEMORY\\\_STORE\\\_PATH],
        ),
    ),
)
```

The MCP filesystem server gives `first\\\_step\\\_coach` the ability to read and write the student's life journal — creating genuine long-term memory that persists across sessions, months, and life stages.

###  3. Antigravity Harness

Embedded in `first\\\_step\\\_coach`. Detects three signals: confusion, overwhelm, and paralysis. On detection, re-routes to Micro-Step Mode — giving the smallest possible action instead of a full plan. Re-tests for clarity. If student remains paralysed after maximum attempts, recommends human support.

###  4. Security

* All student data stays on their local machine — never uploaded anywhere
* MCP server is sandboxed to `./memory\\\_store/` directory only
* No API keys in code — environment variables only via `.env`
* No third-party data collection

###  5. Long-term Memory (Sessions)

* `InMemorySessionService` for current conversation state
* MCP filesystem for cross-session persistent memory
* `student\\\_journal.json` accumulates every session — Disha remembers you across months

###  6. Agent Skills with Web Search

`india\\\_navigator` uses `google\\\_search` tool to fetch real-time data — actual scholarship deadlines, live GATE cutoffs, current salary ranges. Not hardcoded knowledge. Real data at query time.

\---

## The Interest Discovery Innovation

The single most important feature of Disha AI — and the one no other tool has.

**Every existing career tool asks: "What are you interested in?"**

This question is useless for the majority of confused Indian students. 80% say they don't know.

Disha AI asks instead:

* *"When did you last forget to eat — what were you doing?"*
* *"When friends have a problem, what help do they ask YOU for?"*
* *"What makes you most angry about the world?"*
* *"If you open YouTube randomly, what do you end up watching?"*

These reveal **latent interests through behaviour and emotion** — not self-declaration. This is the feature that makes Disha genuinely useful for the student who has "no idea what they like."

\---

## Setup — 100% Free, Runs Locally

### Requirements

* Python 3.10+
* Node.js 18+ (for MCP server)
* Free Google AI Studio API key

### Step 1: Get Free API Key

Visit [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey) — free, no billing required.

### Step 2: Install Node.js

```bash
# macOS
brew install node

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup\\\_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Windows: download from https://nodejs.org
```

### Step 3: Clone and Install

```bash
git clone https://github.com/YOUR\\\_USERNAME/disha-ai.git
cd disha-ai

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\\\Scripts\\\\activate

pip install -r requirements.txt
```

### Step 4: Configure

```bash
cp .env.example .env
# Edit .env and add your GOOGLE\\\_API\\\_KEY
```

### Step 5: Run with Streamlit UI (Recommended)

```bash
streamlit run app.py
# Opens at http://localhost:8501
```

### Step 6: Or Run with ADK Web UI

```bash
adk web .
# Opens ADK's built-in chat interface
```

### Step 7: Or Run in Terminal

```bash
adk run disha\\\_agent
```

\---

## Who This Helps

|Student|Situation|What Disha Does|
|-|-|-|
|Rahul, 16, Class 10|Confused between Science and Commerce|Discovers his interest in systems and money → recommends Commerce with CS → finds scholarship|
|Priya, 18, Class 12|JEE rank not good enough for IIT|Uncovers interest in biology → maps NEET options + AIIMS → finds state government scholarship|
|Rudra, 22, BE Final|GATE vs Job vs Germany — completely paralysed|SC category advantage revealed → GATE dual-track recommended → Rajiv Gandhi Fellowship identified|
|Ananya, 24, Graduated|No direction, lost, stressed|Interest in helping people discovered through questioning → social work + MBA in HR → first step given|
|Karan, 15, Class 10|"I have zero interests"|Behavioural questions reveal he fixes everything that breaks → Mechanical/Electronics path|

\---

## Impact

* **250 million** students currently enrolled in Indian education
* **225 million** without professional guidance
* **₹0** cost to use Disha AI
* **100%** local — student data never leaves their machine
* Works for **every stage** — Class 10 through career, not just one moment

\---

## Why We Built This

We are engineering students in Mumbai. We made the most important decisions of our lives — GATE or job, India or Germany, which stream, which college — completely alone, at 2am, stressed, overthinking, with nobody who understood our actual situation.

We built the tool we needed and never had.

And we built it for the 225 million students who are in the same place right now.

\---

## Tech Stack

|Component|Technology|
|-|-|
|Agent Framework|Google ADK 2.0|
|AI Model|Gemini 2.5 Flash|
|MCP Server|@modelcontextprotocol/server-filesystem|
|Web Search|ADK built-in google\_search tool|
|Frontend|Streamlit|
|Memory|MCP filesystem + JSON|
|Security|Local-only, .env, sandboxed MCP|

\---

*Disha AI — Built for Kaggle/Google AI Agents Intensive Capstone 2026
"We built the tool we needed and never had."*

