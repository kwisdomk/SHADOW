import time
import json
from dataclasses import dataclass, field
from typing import Dict, Any, List

from core.llm_client import ShadowLLMClient
from core.osint_dataset import classify_synthetic_message
from core.execution_trace import ExecutionTrace, format_execution_trace
from core.prompts import (
    get_system_prompt,
    build_language_agent_input,
    build_threat_pattern_agent_input,
    build_risk_scoring_agent_input,
    build_action_agent_input
)

@dataclass
class ShadowState:
    """Central state object for the Shadow Pipeline."""
    raw_message: str
    precheck_data: Dict[str, Any] = field(default_factory=dict)
    language_data: Dict[str, Any] = field(default_factory=dict)
    threat_data: Dict[str, Any] = field(default_factory=dict)
    risk_data: Dict[str, Any] = field(default_factory=dict)
    action_data: Dict[str, Any] = field(default_factory=dict)
    execution_log: List[str] = field(default_factory=list)
    execution_trace: List[Dict[str, Any]] = field(default_factory=list)
    formatted_trace: str = ""

class ShadowPipeline:
    """
    Sequential orchestration engine that processes suspicious SMS
    through all 4 Shadow agents.
    """
    def __init__(self):
        self.client = ShadowLLMClient()

    def _safe_agent_run(self, agent_name: str, system_prompt: str, user_input: str, state: ShadowState, fallback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Runs an agent safely, capturing timing and exceptions, applying fallback if needed."""
        start_time = time.time()
        try:
            result = self.client.generate_response(system_prompt, user_input)
            duration = round(time.time() - start_time, 2)
            
            reasoning = result.get("reasoning_summary")
            if not reasoning and agent_name == "ActionAgent":
                reasoning = result.get("dashboard_summary", "Action agent completed.")
            if not reasoning:
                reasoning = "Analysis completed."
                 
            state.execution_log.append(f"{agent_name} ({duration}s): SUCCESS - {reasoning}")
            return result
        except Exception as e:
            duration = round(time.time() - start_time, 2)
            state.execution_log.append(f"{agent_name} ({duration}s): ERROR - {str(e)}")
            return fallback_data

    def run(self, message: str) -> ShadowState:
        """Executes the pipeline sequentially."""
        state = ShadowState(raw_message=message)
        trace = ExecutionTrace()
        
        # Defined fallbacks for reliability
        lang_fb = {"primary_language": "unknown", "confidence": 0.0}
        threat_fb = {"scam_categories_detected": [], "primary_category": "none", "threat_signals": {}}
        risk_fb = {"raw_score": 3, "risk_level": "MEDIUM"}
        action_fb = {
            "verdict": "INCONCLUSIVE",
            "risk_level": "MEDIUM",
            "scam_type": "Unknown",
            "dashboard_summary": "Analysis failed, manual review required.",
            "recommended_actions": [{"priority": 1, "action": "Manual Review", "reason": "Pipeline failure"}]
        }

        # Step 0: OSINT Pre-Analysis Stage
        state.precheck_data = classify_synthetic_message(message)
        precheck_risk = state.precheck_data.get("risk_level", "UNKNOWN")
        precheck_category = state.precheck_data.get("probable_category", "unknown")
        
        threat_context = None
        if precheck_risk in ["HIGH", "CRITICAL"]:
            osint_summary = f"Matched {precheck_category} pattern from deterministic dataset"
            state.execution_log.append("OSINT PreCheck: Known Kenyan threat pattern detected")
            threat_context = precheck_category
        elif precheck_risk == "LOW" or precheck_category == "legitimate_transaction":
            osint_summary = "No known OSINT match - escalating to LLM reasoning layer"
            state.execution_log.append("OSINT PreCheck: Legitimate transaction pattern")
        else:
            osint_summary = "No known OSINT match - escalating to LLM reasoning layer"
            
        trace.add_step(
            agent="OSINT PRECHECK",
            input_str=message,
            output=state.precheck_data,
            summary=osint_summary,
            risk_hint=precheck_risk
        )

        # Step 1: Language Agent
        sys_lang = get_system_prompt("language_agent")
        user_lang = build_language_agent_input(message)
        state.language_data = self._safe_agent_run("LanguageAgent", sys_lang, user_lang, state, lang_fb)
        
        primary_lang = state.language_data.get("primary_language", "Unknown")
        trace.add_step(
            agent="LANGUAGE AGENT",
            input_str=user_lang,
            output=state.language_data,
            summary=f"{primary_lang} detected"
        )
        
        # Step 2: Threat Pattern Agent
        sys_threat = get_system_prompt("threat_pattern_agent")
        user_threat = build_threat_pattern_agent_input(message, state.language_data, threat_context)
        state.threat_data = self._safe_agent_run("ThreatPatternAgent", sys_threat, user_threat, state, threat_fb)
        
        threat_summary = state.threat_data.get("reasoning_summary", "Threat analysis completed")
        if state.threat_data.get("primary_category") and state.threat_data.get("primary_category") != "none":
            threat_summary = f"{state.threat_data.get('primary_category')} intent confirmed"
            
        trace.add_step(
            agent="THREAT AGENT",
            input_str=user_threat,
            output=state.threat_data,
            summary=threat_summary
        )
        
        # Step 3: Risk Scoring Agent
        sys_risk = get_system_prompt("risk_scoring_agent")
        user_risk = build_risk_scoring_agent_input(message, state.language_data, state.threat_data)
        state.risk_data = self._safe_agent_run("RiskScoringAgent", sys_risk, user_risk, state, risk_fb)
        
        risk_level = state.risk_data.get("risk_level", "UNKNOWN")
        raw_score = state.risk_data.get("raw_score", 0)
        trace.add_step(
            agent="RISK AGENT",
            input_str=user_risk,
            output=state.risk_data,
            summary=f"{risk_level} ({raw_score})",
            risk_hint=risk_level
        )
        
        # Step 4: Action Agent
        sys_action = get_system_prompt("action_agent")
        user_action = build_action_agent_input(message, state.language_data, state.threat_data, state.risk_data)
        state.action_data = self._safe_agent_run("ActionAgent", sys_action, user_action, state, action_fb)
        
        verdict = state.action_data.get("verdict", "INCONCLUSIVE")
        actions = state.action_data.get("recommended_actions", [])
        action_names = " + ".join([a.get("action", "") for a in actions if a.get("action")]) if actions else verdict
        if action_names == verdict:
             action_summary = verdict
        else:
             action_summary = f"{verdict} -> {action_names}"
             
        trace.add_step(
            agent="ACTION AGENT",
            input_str=user_action,
            output=state.action_data,
            summary=action_summary
        )
        
        state.execution_trace = trace.get_trace()
        state.formatted_trace = format_execution_trace(state.execution_trace)
        
        return state

# Hybrid Flow: OSINT -> LLM Fallback Evaluated
