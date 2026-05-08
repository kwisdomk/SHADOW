import streamlit as st
import sys
import os
import time

# ── Page Config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="SHADOW — Kenyan Fraud Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Styling ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0f;
    color: #e2e8f0;
}

.stApp {
    background-color: #0a0a0f;
}

/* Header */
.shadow-header {
    text-align: center;
    padding: 2rem 0 1rem 0;
    border-bottom: 1px solid #1e293b;
    margin-bottom: 2rem;
}

.shadow-title {
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    color: #f8fafc;
    font-family: 'JetBrains Mono', monospace;
}

.shadow-subtitle {
    color: #64748b;
    font-size: 0.9rem;
    letter-spacing: 0.15em;
    margin-top: 0.3rem;
}

.amd-badge {
    display: inline-block;
    background: linear-gradient(135deg, #ED1C24, #FF6B35);
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 3px 10px;
    border-radius: 3px;
    margin-top: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
}

/* Verdict Cards */
.verdict-scam {
    background: linear-gradient(135deg, #1a0505, #2d0808);
    border: 2px solid #ef4444;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
}

.verdict-suspicious {
    background: linear-gradient(135deg, #1a1205, #2d1f08);
    border: 2px solid #f59e0b;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
}

.verdict-safe {
    background: linear-gradient(135deg, #051a0a, #082d12);
    border: 2px solid #22c55e;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
}

.verdict-label {
    font-size: 2rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.2em;
}

.verdict-scam .verdict-label { color: #ef4444; }
.verdict-suspicious .verdict-label { color: #f59e0b; }
.verdict-safe .verdict-label { color: #22c55e; }

.verdict-summary {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 0.5rem;
}

/* Risk Score */
.risk-bar-container {
    background: #1e293b;
    border-radius: 6px;
    height: 10px;
    width: 100%;
    margin: 0.5rem 0;
    overflow: hidden;
}

.risk-bar-fill {
    height: 10px;
    border-radius: 6px;
    transition: width 0.5s ease;
}

/* Trace Timeline */
.trace-container {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 1.2rem;
    margin-top: 1rem;
}

.trace-step {
    display: flex;
    align-items: flex-start;
    margin-bottom: 0.8rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #1e293b;
}

.trace-step:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}

.trace-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-top: 4px;
    margin-right: 12px;
    flex-shrink: 0;
}

.trace-agent {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #64748b;
    min-width: 160px;
}

.trace-summary {
    font-size: 0.82rem;
    color: #cbd5e1;
}

/* Info panels */
.info-panel {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}

.info-panel h4 {
    color: #64748b;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
}

.red-flag {
    background: #1a0505;
    border-left: 3px solid #ef4444;
    padding: 0.4rem 0.8rem;
    border-radius: 0 4px 4px 0;
    font-size: 0.82rem;
    color: #fca5a5;
    margin-bottom: 0.4rem;
}

.action-item {
    background: #0a1628;
    border-left: 3px solid #3b82f6;
    padding: 0.4rem 0.8rem;
    border-radius: 0 4px 4px 0;
    font-size: 0.82rem;
    color: #93c5fd;
    margin-bottom: 0.4rem;
}

.safety-tip {
    background: #0a1628;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 0.5rem;
}

.safety-tip-lang {
    font-size: 0.7rem;
    font-weight: 700;
    color: #3b82f6;
    letter-spacing: 0.1em;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.2rem;
}

.safety-tip-text {
    font-size: 0.82rem;
    color: #cbd5e1;
    margin-bottom: 0.6rem;
}

/* Preset pills */
.preset-label {
    font-size: 0.72rem;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}

/* Input area */
.stTextArea textarea {
    background-color: #0f172a !important;
    border: 1px solid #1e293b !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    border-radius: 8px !important;
}

.stTextArea textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.2) !important;
}

.stButton button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    color: white !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    font-size: 0.9rem !important;
}

.stButton button:hover {
    background: linear-gradient(135deg, #1e40af, #1d4ed8) !important;
}

/* Divider */
hr { border-color: #1e293b !important; }

/* Spinner */
.stSpinner > div { border-top-color: #3b82f6 !important; }
</style>
""", unsafe_allow_html=True)

# ── Pipeline Import ───────────────────────────────────────────────
# Add parent directory to path so imports work from app/ or root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from agents.pipeline import ShadowPipeline
    PIPELINE_AVAILABLE = True
except ImportError:
    PIPELINE_AVAILABLE = False

# ── Preset Messages ───────────────────────────────────────────────
PRESETS = {
    "— Select a demo scenario —": "",
    "🔴 Safaricom Impersonation": "Habari kutoka Safaricom. Laini yako inatumika na mtu mwingine (double registration). Piga *33*0000* kuzuia hii haraka au akaunti yako itafungwa ndani ya masaa 2.",
    "🔴 KRA Penalty Threat": "KRA ALERT: Uko na tax arrears ya KES 23,450 kwa iTax system yako. Lipa ndani ya masaa 48 au utashtakiwa. Piga simu 0756XXXXXX sasa.",
    "🟠 M-Pesa Reversal Scam": "Aki naomba urudishe ile pesa nimekutumia by mistake saa hii. Ni ya fees ya mtoto tafadhali. Tuma haraka 0712XXXXXX.",
    "🟠 Fuliza Boost Scam": "KAMA ULIPATA FULIZA SEMA THANKS. Inbox nikuboostie fuliza from 0 to 100k in 2 minutes hii January hakuna stress.",
    "🟡 Betting Jackpot Scam": "Hongera! Wewe ndio mshindi wa 500k SportPesa Weekly Jackpot. Tuma 2,500 ya registration fee kupokea pesa kwa MPESA yako leo.",
    "🟡 WhatsApp OTP Theft": "Boss nisamehe, nilituma code ya WhatsApp kwa namba yako by mistake. Naomba unitumie hiyo code 6-digits haraka niingie kwa group ya kazi.",
    "✅ Legitimate M-Pesa": "MPESA Confirmed. You have received Ksh 3,500.00 from JOHN KAMAU 0722XXXXXX on 8/5/26 at 10:23 AM. New M-PESA balance is Ksh 4,120.00.",
}

# ── Risk Color Helper ─────────────────────────────────────────────
def get_risk_color(level: str) -> str:
    return {
        "CRITICAL": "#ef4444",
        "HIGH": "#f97316",
        "MEDIUM": "#f59e0b",
        "LOW": "#22c55e"
    }.get(level, "#64748b")

def get_verdict_class(verdict: str) -> str:
    if verdict == "SCAM":
        return "verdict-scam"
    elif verdict == "SUSPICIOUS":
        return "verdict-suspicious"
    return "verdict-safe"

def get_verdict_emoji(verdict: str) -> str:
    return {"SCAM": "🚨", "SUSPICIOUS": "⚠️", "SAFE": "✅"}.get(verdict, "❓")

def get_trace_dot_color(agent: str, risk_hint: str) -> str:
    if risk_hint in ["CRITICAL", "HIGH"]:
        return "#ef4444"
    elif risk_hint in ["MEDIUM"]:
        return "#f59e0b"
    elif agent == "OSINT PRECHECK":
        return "#8b5cf6"
    elif agent == "LANGUAGE AGENT":
        return "#3b82f6"
    elif agent == "THREAT AGENT":
        return "#f97316"
    elif agent == "RISK AGENT":
        return "#ef4444"
    elif agent == "ACTION AGENT":
        return "#22c55e"
    return "#64748b"

# ── Header ────────────────────────────────────────────────────────
st.markdown("""
<div class="shadow-header">
    <div class="shadow-title">◈ SHADOW</div>
    <div class="shadow-subtitle">KENYAN FRAUD INTELLIGENCE SYSTEM</div>
    <div class="amd-badge">⚡ POWERED BY AMD INSTINCT MI300X + ROCm</div>
</div>
""", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1.3], gap="large")

with left_col:
    st.markdown("#### 📥 Analyze a Message")

    # Preset selector
    preset_choice = st.selectbox(
        "Load a demo scenario",
        options=list(PRESETS.keys()),
        label_visibility="collapsed"
    )

    # Pre-fill text area from preset
    default_text = PRESETS.get(preset_choice, "")

    message = st.text_area(
        "Message",
        value=default_text,
        height=160,
        placeholder="Paste a suspicious SMS, WhatsApp message, or notification here...",
        label_visibility="collapsed"
    )

    analyze_clicked = st.button("🔍 ANALYZE WITH SHADOW", use_container_width=True)

    # Stats strip
    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    s1.metric("Scam Categories", "11")
    s2.metric("Languages", "EN / SW / Sheng")
    s3.metric("Pipeline Agents", "4")

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#475569; font-family: JetBrains Mono, monospace;'>
    SHADOW uses a hybrid OSINT + 4-agent LLM pipeline to detect<br>
    Kenyan mobile fraud in real time. Qwen3 inference runs on<br>
    AMD Instinct MI300X via vLLM + ROCm.
    </div>
    """, unsafe_allow_html=True)

# ── Analysis Logic ─────────────────────────────────────────────────
with right_col:
    if analyze_clicked:
        if not message.strip():
            st.warning("Please paste a message to analyze.")
        else:
            with st.spinner("Shadow is analyzing..."):
                start = time.time()

                if PIPELINE_AVAILABLE:
                    try:
                        pipeline = ShadowPipeline()
                        state = pipeline.run(message)
                        action = state.action_data or {}
                        risk = state.risk_data or {}
                        trace = state.execution_trace or []
                        elapsed = round(time.time() - start, 2)
                    except Exception as e:
                        st.error(f"Pipeline error: {str(e)}")
                        # Safe fallback
                        action = {
                            "verdict": "INCONCLUSIVE",
                            "risk_level": "UNKNOWN",
                            "scam_type": "Error",
                            "dashboard_summary": "An error occurred during analysis.",
                            "confidence": 0.0,
                            "explanation": {"red_flags_found": ["System error"]},
                            "recommended_actions": [],
                            "do_not_do": [],
                            "safety_tip": {},
                            "reporting": {}
                        }
                        risk = {"raw_score": 0}
                        trace = [{"agent": "SYSTEM", "step": 1, "summary": "Error running pipeline", "risk_hint": "UNKNOWN"}]
                        elapsed = round(time.time() - start, 2)
                else:
                    # Fallback demo state if imports fail
                    action = {
                        "verdict": "SUSPICIOUS",
                        "risk_level": "MEDIUM",
                        "scam_type": "Pipeline Offline (Mock)",
                        "dashboard_summary": "This is a fallback response because the pipeline failed to load.",
                        "confidence": 0.50,
                        "explanation": {"red_flags_found": ["Mock execution"]},
                        "recommended_actions": [{"action": "Check system paths and imports"}],
                        "do_not_do": ["Trust this mock verdict"],
                        "safety_tip": {"english": "System is offline.", "swahili": "Mfumo haupatikani.", "sheng": "System iko chini."},
                        "reporting": {"should_report": False, "contacts": []}
                    }
                    risk = {"raw_score": 5}
                    trace = [{"agent": "MOCK AGENT", "step": 1, "summary": "Pipeline import failed", "risk_hint": "MEDIUM"}]
                    elapsed = 0.0

            # Safe gets with empty defaults to prevent NoneType crashes
            verdict = action.get("verdict") or "INCONCLUSIVE"
            risk_level = action.get("risk_level") or "UNKNOWN"
            scam_type = action.get("scam_type") or "Unknown"
            summary = action.get("dashboard_summary") or ""
            confidence = action.get("confidence")
            if confidence is None:
                confidence = 0.0
            
            raw_score = risk.get("raw_score")
            if raw_score is None:
                raw_score = 0
                
            explanation = action.get("explanation") or {}
            red_flags = explanation.get("red_flags_found") or []
            
            recommended = action.get("recommended_actions") or []
            do_not = action.get("do_not_do") or []
            
            safety_tip = action.get("safety_tip") or {}
            reporting = action.get("reporting") or {}

            # ── Verdict Card ──────────────────────────────────────
            verdict_class = get_verdict_class(verdict)
            verdict_emoji = get_verdict_emoji(verdict)
            risk_color = get_risk_color(risk_level)
            score_pct = min(int((raw_score / 10) * 100), 100)

            st.markdown(f"""
            <div class="{verdict_class}">
                <div class="verdict-label">{verdict_emoji} {verdict}</div>
                <div class="verdict-summary">{summary}</div>
                <div style="margin-top:0.8rem; font-size:0.78rem; color:#64748b;">
                    {scam_type} &nbsp;|&nbsp; Confidence: {int(confidence*100)}% &nbsp;|&nbsp; {elapsed}s
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Risk Score Bar ────────────────────────────────────
            st.markdown(f"""
            <div class="info-panel">
                <h4>⚡ Risk Score</h4>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="font-size:0.8rem; color:#94a3b8;">Score: {raw_score}/10</span>
                    <span style="font-size:0.8rem; font-weight:700; color:{risk_color};">{risk_level}</span>
                </div>
                <div class="risk-bar-container">
                    <div class="risk-bar-fill" style="width:{score_pct}%; background:{risk_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Two columns: Red Flags + Actions ──────────────────
            c1, c2 = st.columns(2)

            with c1:
                flags_html = "".join([f'<div class="red-flag">⚠ {f}</div>' for f in red_flags]) or '<div style="color:#64748b; font-size:0.8rem;">None detected</div>'
                st.markdown(f"""
                <div class="info-panel">
                    <h4>🚩 Red Flags</h4>
                    {flags_html}
                </div>
                """, unsafe_allow_html=True)

            with c2:
                # Need to handle dictionary vs string in recommended actions list just in case
                actions_html = ""
                for a in recommended:
                    if isinstance(a, dict):
                        action_text = a.get("action", "")
                        if action_text:
                            actions_html += f'<div class="action-item">→ {action_text}</div>'
                    elif isinstance(a, str):
                        actions_html += f'<div class="action-item">→ {a}</div>'
                
                donot_html = "".join([f'<div class="red-flag">✗ {d}</div>' for d in do_not if isinstance(d, str)])
                
                st.markdown(f"""
                <div class="info-panel">
                    <h4>✅ What To Do</h4>
                    {actions_html}
                    {donot_html}
                </div>
                """, unsafe_allow_html=True)

            # ── Execution Trace ───────────────────────────────────
            trace_html = """
            <div class="info-panel" style="margin-top:0;">
                <h4>🧠 Agent Reasoning Timeline</h4>
                <div class="trace-container">
            """
            
            if not trace:
                trace_html += '<div style="color:#64748b; font-size:0.8rem;">No trace available.</div>'
            for step in trace:
                if not isinstance(step, dict):
                    continue
                agent = step.get("agent") or "SYSTEM"
                summary_text = step.get("summary") or ""
                risk_hint = step.get("risk_hint") or ""
                dot_color = get_trace_dot_color(agent, risk_hint)
                trace_html += f"""
                <div class="trace-step">
                    <div class="trace-dot" style="background:{dot_color};"></div>
                    <div>
                        <div class="trace-agent">[{step.get('step', 0)}] {agent}</div>
                        <div class="trace-summary">{summary_text}</div>
                    </div>
                </div>
                """
            trace_html += "</div></div>"
            st.markdown(trace_html, unsafe_allow_html=True)

            # ── Safety Tip ────────────────────────────────────────
            if safety_tip:
                st.markdown(f"""
                <div class="safety-tip">
                    <div class="safety-tip-lang">EN</div>
                    <div class="safety-tip-text">{safety_tip.get('english', 'Not available')}</div>
                    <div class="safety-tip-lang">SW</div>
                    <div class="safety-tip-text">{safety_tip.get('swahili', 'Haipatikani')}</div>
                    <div class="safety-tip-lang">SHENG</div>
                    <div class="safety-tip-text">{safety_tip.get('sheng', 'Haiwezekani')}</div>
                </div>
                """, unsafe_allow_html=True)

            # ── Reporting ─────────────────────────────────────────
            if reporting.get("should_report") and reporting.get("contacts"):
                contacts = reporting.get("contacts", [])
                contact_parts = []
                for c in contacts:
                    if isinstance(c, dict) and 'name' in c and 'value' in c:
                        contact_parts.append(f"{c['name']}: <strong>{c['value']}</strong>")
                
                if contact_parts:
                    contact_str = " &nbsp;|&nbsp; ".join(contact_parts)
                    st.markdown(f"""
                    <div style="margin-top:0.8rem; padding:0.8rem; background:#0a1628;
                         border:1px solid #1e3a5f; border-radius:8px;
                         font-size:0.8rem; color:#93c5fd;">
                        📢 Report this: {contact_str}
                    </div>
                    """, unsafe_allow_html=True)

    else:
        # Empty state
        st.markdown("""
        <div style="
            height: 400px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #334155;
            border: 1px dashed #1e293b;
            border-radius: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            text-align: center;
            padding: 2rem;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">◈</div>
            <div style="font-size: 1rem; color: #475569; margin-bottom: 0.5rem;">SHADOW IS WATCHING</div>
            <div style="color: #334155;">Paste a message or select a demo scenario<br>to begin fraud analysis.</div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem 0; color:#334155;
     font-size:0.72rem; font-family:'JetBrains Mono', monospace;
     border-top: 1px solid #1e293b; margin-top: 2rem;">
    SHADOW — AMD Developer Hackathon 2026 &nbsp;|&nbsp;
    Qwen3 on MI300X via vLLM + ROCm &nbsp;|&nbsp;
    Built for Kenya's 54M mobile users &nbsp;|&nbsp;
    <a href="https://github.com/kwisdomk/SHADOW" style="color:#3b82f6;">GitHub</a>
</div>
""", unsafe_allow_html=True)
