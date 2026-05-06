import time
import json
from dataclasses import dataclass, field
from typing import Dict, Any, List

from core.llm_client import ShadowLLMClient
from core.osint_dataset import classify_synthetic_message
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
            state.execution_log.append("OSINT PreCheck: Known Kenyan threat pattern detected")
            threat_context = precheck_category
        elif precheck_risk == "LOW" or precheck_category == "legitimate_transaction":
            state.execution_log.append("OSINT PreCheck: Legitimate transaction pattern")

        # Step 1: Language Agent
        sys_lang = get_system_prompt("language_agent")
        user_lang = build_language_agent_input(message)
        state.language_data = self._safe_agent_run("LanguageAgent", sys_lang, user_lang, state, lang_fb)
        
        # Step 2: Threat Pattern Agent
        sys_threat = get_system_prompt("threat_pattern_agent")
        user_threat = build_threat_pattern_agent_input(message, state.language_data, threat_context)
        state.threat_data = self._safe_agent_run("ThreatPatternAgent", sys_threat, user_threat, state, threat_fb)
        
        # Step 3: Risk Scoring Agent
        sys_risk = get_system_prompt("risk_scoring_agent")
        user_risk = build_risk_scoring_agent_input(message, state.language_data, state.threat_data)
        state.risk_data = self._safe_agent_run("RiskScoringAgent", sys_risk, user_risk, state, risk_fb)
        
        # Step 4: Action Agent
        sys_action = get_system_prompt("action_agent")
        user_action = build_action_agent_input(message, state.language_data, state.threat_data, state.risk_data)
        state.action_data = self._safe_agent_run("ActionAgent", sys_action, user_action, state, action_fb)
        
        return state

# Hybrid Flow: OSINT -> LLM Fallback Evaluated
