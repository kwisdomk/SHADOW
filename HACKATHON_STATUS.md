# SHADOW - Hackathon Status Report

## 📍 Where We Are
We have successfully built the core foundation of **SHADOW**, the AI Fraud Detection System tailored for the Kenyan market. The application leverages a 4-agent pipeline (Language, Threat Pattern, Risk Scoring, and Action) to evaluate suspicious messages using a local/mock-capable LLM backend.

**Recently Fixed:**
- Resolved a critical bug where the `Risk Scoring Agent` was misrouting mock responses and returning `UNKNOWN (0)`. It now accurately computes and surfaces Risk Levels (LOW, MEDIUM, HIGH, CRITICAL) along with proper execution timelines.

## ✅ What's Done
1. **Core Pipeline Orchestration**: `ShadowPipeline` in `agents/pipeline.py` successfully chains 4 LLM agents sequentially, preserving state across the run.
2. **OSINT Pre-Check Layer**: `core/osint_dataset.py` contains deterministic rules for the most common Kenyan fraud variants (M-Pesa reversal, Safaricom impersonation, Fuliza boost, etc.).
3. **Execution Tracing**: Comprehensive logging and tracking of agent execution time, success/failure, and reasoning.
4. **Resilience / Fallback Mechanics**: `core/llm_client.py` includes a robust MOCK MODE that seamlessly takes over if API connections fail, guaranteeing a zero-crash demonstration.
5. **Streamlit UI Integration**: The `app/app.py` wrapper exists to expose the pipeline visually.
6. **Testing Suite**: `scripts/test_pipeline.py` effectively runs a smoke test across different threat vectors.

## 🚧 What's Not Done (Shortcomings)
1. **Live LLM Integration**: We are currently defaulting to MOCK MODE because the `openai` API/vLLM endpoints haven't been fully connected with live keys.
2. **Dynamic Agent Routing (LangGraph)**: The pipeline is strictly sequential. If we want true agentic conditional routing (e.g., skip Threat Pattern if OSINT is 100% certain), we need to implement `langgraph`.
3. **Dashboard Polish**: The Streamlit interface (`app.py`) might need aesthetic touch-ups to ensure a "WOW" factor for the judges (e.g., better visual indicators for CRITICAL vs LOW risk).
4. **AMD Hardware Proof**: We still need to gather the actual logs/proof showing `qwen-2.5-7b` running on AMD MI300X/ROCm for the submission requirements.

## ⚠️ Challenges & Roadblocks
- **LLM Latency & Reliability**: We implemented MOCK MODE precisely because relying on remote LLM endpoints during a live demo can be risky.
- **Context Parsing Errors**: We experienced issues parsing multi-agent inputs where previous agent JSON outputs were combined with text. 
- **Time Constraints**: The AMD Hackathon requires a video demo and a "Build-in-Public" post. This marketing and documentation overhead limits pure coding time.

## 🤝 How Teammates Can Help
- **UI/UX (Frontend)**: Run `app.py` and improve the Streamlit UI. Add warning colors, pulsing animations for CRITICAL alerts, and format the Execution Timeline beautifully.
- **Hardware/Backend**: Set up the live vLLM inference server on AMD hardware, capture the execution logs, and update `SHADOW_API_BASE` in `.env` so we can test with real inference.
- **Documentation/Submission**: Help draft the final devpost submission, record the video walkthrough, and write the required social media post detailing our use of AMD infrastructure.
