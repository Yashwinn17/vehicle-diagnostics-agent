# 🔧 Vehicle Diagnostics Agent

**An AI-powered automotive diagnostician that runs 100% FREE — locally with Ollama or on Google Gemini.**

Analyzes OBD-II trouble codes, identifies root causes across multiple codes, and generates prioritized repair plans with cost estimates.

> Day 1 of 84 — Agentic AI Engineer Roadmap

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-green)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-purple)
![Gemini](https://img.shields.io/badge/Gemini-Free_Tier-orange)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)

---

## Why This Exists

Most AI agent tutorials require an OpenAI API key and $20/month. This agent runs **completely free** — either locally on your machine with Ollama, or on Google Gemini with a supported model on your API key.

It also solves a real problem: automotive diagnostic tools cost $10K+ and still require a technician to interpret results. This agent analyzes multiple codes simultaneously, identifies root causes vs. symptoms, and saves unnecessary repairs.

---

## Architecture

```
┌──────────────────────────────────────────────────┐
│                  User Input                       │
│          (codes + vehicle info)                   │
└───────────────────┬──────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│            LLM Provider Factory                   │
│    ┌─────────────┐    ┌──────────────────┐       │
│    │   Ollama     │    │  Google Gemini    │       │
│    │  (local)     │ OR │  (free tier)      │       │
│    │ llama3.1:8b  │    │ gemini-2.5-flash-lite │    │
│    └─────────────┘    └──────────────────┘       │
└───────────────────┬──────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│          LangGraph ReAct Agent                    │
│       (Autonomous tool selection)                 │
│                                                   │
│  ┌──────────┐ ┌──────────────┐ ┌──────────────┐  │
│  │ Lookup   │ │ Relationship │ │   Repair     │  │
│  │ Codes    │ │  Analyzer    │ │  Estimator   │  │
│  └──────────┘ └──────────────┘ └──────────────┘  │
│                                                   │
│         ┌──────────────────┐                      │
│         │  OBD-II Knowledge │                     │
│         │   Base (30+ codes │                     │
│         │  + relationships) │                     │
│         └──────────────────┘                      │
└───────────────────┬──────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────┐
│             Diagnostic Report                     │
│  - Root cause identification                     │
│  - Prioritized repair sequence                   │
│  - Cost estimates (age-adjusted)                 │
│  - Safety/urgency classification                 │
│  - Plain English explanation                     │
└──────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| LLM (Primary) | Ollama + llama3.1:8b | **$0** (local) |
| LLM (Fallback) | Google Gemini 2.5 Flash-Lite | Depends on your API access |
| Agent Framework | LangChain + LangGraph | Free |
| Knowledge Base | Python dataclasses | Free |
| Data Models | Pydantic v2 | Free |
| UI | Streamlit | Free |

**Total cost: $0**

---

## Quick Start

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.ai) installed and running

### 1. Pull the model
```bash
ollama pull llama3.1:8b
```

### 2. Clone and install
```bash
git clone https://github.com/YOUR_USERNAME/vehicle-diagnostics-agent.git
cd vehicle-diagnostics-agent
pip install -r requirements.txt
```

### 3. Configure
```bash
cp .env.example .env
# Optional: Add GOOGLE_API_KEY for Gemini fallback
# Default Gemini model: gemini-2.5-flash-lite
```

### 4. Run
```bash
# Streamlit UI
streamlit run app.py

# CLI mode
python -m src.agent P0300 P0171 P0420
```

### 5. Switch providers anytime
In the Streamlit sidebar, toggle between Ollama (local) and Gemini (cloud).

---

## Example: Multi-Code Root Cause Analysis

**Input:** `P0300 P0171 P0174`

**What a basic lookup gives you:** 3 separate problems, 3 separate repairs, $750+ total.

**What this agent gives you:** The lean condition (P0171 + P0174) is the ROOT CAUSE. The misfire (P0300) is a SYMPTOM. Fix one vacuum leak → all three codes clear. Actual cost: $100-$300.

**That's $450+ saved** by understanding code relationships.

---

## Key Engineering Decisions

1. **LLM Provider Factory pattern** — `get_llm()` abstracts Ollama vs Gemini so agent code never cares which model is running. This pattern will be reused in every project for the next 83 days.

2. **More explicit prompting for local models** — GPT-4 can infer tool order from context. Llama 3.1 8B benefits from explicit step-by-step instructions. The prompts are tuned for local model reliability.

3. **Graceful degradation** — If Ollama tool calling fails, the error message tells you exactly how to switch to Gemini or try a different model. No cryptic crashes.

---

## License

MIT
