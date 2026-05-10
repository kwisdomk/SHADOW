---
title: SHADOW Kenyan Fraud Intelligence
emoji: 🛡️
colorFrom: red
colorTo: gray
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
---

# SHADOW — Kenyan Fraud Intelligence System

> AMD Developer Hackathon 2026 · Agentic AI Track

## Project Overview

Shadow is an advanced OSINT + LLM Hybrid Agentic Pipeline designed specifically to detect, analyze, and neutralize Kenyan-specific mobile fraud vectors. The system mitigates the impact of localized scams such as M-Pesa reversal fraud, Fuliza exploitation, KRA impersonation, and betting-related phishing.

Shadow solves the "Data Cold Start" problem by employing a hybrid architecture: it merges deterministic Open Source Intelligence (OSINT) with an explainable, multi-agent Large Language Model (LLM) pipeline. This ensures highly accurate classification, context-aware reasoning, and actionable mitigation strategies tailored to the Kenyan demographic, including support for English, Swahili, and Sheng dialects.

## Architecture Diagram

```text
[ Incoming SMS / Message ]
           │
           ▼
┌──────────────────────────┐
│  OSINT Intelligence Layer│
│  (core/osint_dataset.py) │
│  - Deterministic Check   │
│  - Keyword Matching      │
│  - Scam Taxonomy Mapping │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Agent Pipeline Engine   │
│  (agents/pipeline.py)    │
│                          │
│  1. Language Agent       │
│  2. Threat Agent         │
│  3. Risk Agent           │
│  4. Action Agent         │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  AMD vLLM / Qwen Bridge  │
│  (core/llm_client.py)    │
│  - Context Injection     │
│  - Reasoning Engine      │
└──────────┬───────────────┘
           │
           ▼
[ Explainable JSON Output & Execution Log ]
           │
           ▼
┌──────────────────────────┐
│  Streamlit Live Dashboard│
│  (app/main.py)           │
│  - Real-time Analysis UI │
│  - Execution Timeline    │
│  - Risk Scoring Display  │
└──────────────────────────┘
```

## Agent Pipeline Flow

1. **OSINT Pre-Analysis (Hybrid Intelligence Mode)**: Messages are instantly matched against known Kenyan scam topologies to provide a deterministic baseline.
2. **Language Agent**: Detects the dialect (English, Swahili, Sheng) and standardizes the context for subsequent analysis.
3. **Threat Agent**: Analyzes the intent of the message based on localized threat vectors.
4. **Risk Agent**: Computes a continuous risk score (0-100) and categorizes severity.
5. **Action Agent**: Determines the recommended user action (e.g., Block, Report to Safaricom, Ignore).

## Features

- **Kenyan Fraud Detection**: Specialized in detecting hyper-local scams (e.g., M-Pesa, Fuliza, KRA, Hustler Fund).
- **Sheng + Swahili Language Detection**: Seamlessly processes colloquialisms and mixed-language SMS typical in East Africa.
- **OSINT-Driven Classification**: Fuses known deterministic scam indicators with probabilistic AI reasoning.
- **Explainable AI Logs (`execution_log`)**: Glass-box observability that documents the exact reasoning step-by-step for full transparency.
- **Streamlit Live Dashboard**: Interactive real-time web UI for threat analysis and execution timeline visualization.
- **AMD Hardware Optimized**: Built to run on the AMD Developer Cloud utilizing vLLM and Qwen models, with a robust fallback mock mode for deterministic demos.

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate      # Windows
# source venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app.py
```

## How to Run

### 1. Create a Virtual Environment

It is strongly recommended to isolate project dependencies in a virtual environment.

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` prepended to your terminal prompt, confirming the environment is active.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file and add your AMD Cloud API key (optional — mock mode works without it)
# Windows:
copy .env.example .env

# macOS/Linux:
# cp .env.example .env
```

### 4. Launch the Streamlit Dashboard (Primary Interface)

```bash
streamlit run app.py
```

The dashboard runs at `http://localhost:8501` and provides a full interactive UI for submitting messages, viewing risk scores, agent reasoning, and the step-by-step execution timeline.

### 5. Run Pipeline Smoke Tests (CLI)

```bash
python scripts/test_pipeline.py
```

## Future Work

- **AMD MI300X Deployment**: Fully scale the vLLM integration on AMD MI300X infrastructure for enterprise-grade throughput.
- **WhatsApp Bot Integration**: Directly parse user-forwarded messages for instant fraud scoring.
