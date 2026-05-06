# SHADOW — Kenyan Fraud Intelligence System

## Project Overview

Shadow is an advanced OSINT + LLM Hybrid Agentic Pipeline designed specifically to detect, analyze, and neutralize Kenyan-specific mobile fraud vectors. Built as a proof-of-concept for the AMD Developer Hackathon, the system mitigates the impact of localized scams such as M-Pesa reversal fraud, Fuliza exploitation, KRA impersonation, and betting-related phishing.

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
- **AMD Hardware Optimized**: Built to run on the AMD Developer Cloud utilizing vLLM and Qwen models, with a robust fallback mock mode for deterministic demos.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure Environment:
   ```bash
   # Copy the example environment file and add your AMD Cloud API key if not using Mock Mode
   cp .env.example .env
   ```

3. Run the Pipeline Smoke Tests:
   ```bash
   python scripts/test_pipeline.py
   ```

## Future Work

- **Streamlit Live Dashboard**: Develop a real-time web interface for interactive threat analysis.
- **AMD MI300X Deployment**: Fully scale the vLLM integration on AMD MI300X infrastructure for enterprise-grade throughput.
- **WhatsApp Bot Integration**: Directly parse user-forwarded messages for instant fraud scoring.
