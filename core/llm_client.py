import os
import json
import logging
import time
from typing import Dict, Any, Generator

from core.osint_dataset import classify_synthetic_message

try:
    from openai import OpenAI, APIConnectionError, APITimeoutError, RateLimitError
except ImportError:
    OpenAI = None
    APIConnectionError = Exception
    APITimeoutError = Exception
    RateLimitError = Exception

# Configure lightweight structured logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ShadowLLM")

class ShadowLLMClient:
    """
    Lightweight execution bridge between Shadow agents and AMD Developer Cloud (vLLM / Qwen).
    Built for resilience in hackathon/demo environments.
    """

    def __init__(self):
        self.api_base = os.getenv("SHADOW_API_BASE", "https://api.openai.com/v1")
        self.model = os.getenv("SHADOW_MODEL", "qwen-2.5-7b")
        self.api_key = os.getenv("SHADOW_API_KEY", "dummy-key-for-mock")
        self.timeout = float(os.getenv("SHADOW_TIMEOUT", "30.0"))
        self.mock_mode = os.getenv("SHADOW_MOCK_MODE", "true").lower() == "true"
        
        if OpenAI is None:
            logger.warning("openai package not found. Forcing MOCK MODE.")
            self.mock_mode = True

        if not self.mock_mode:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_base,
                timeout=self.timeout
            )
        else:
            self.client = None
            logger.info("ShadowLLMClient initialized in MOCK MODE.")

    def _clean_json(self, response_text: str) -> str:
        """Strip markdown code fences and clean output to raw JSON."""
        text = response_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
            
        if text.endswith("```"):
            text = text[:-3]
            
        return text.strip()

    def generate_response(self, system_prompt: str, user_input: str) -> Dict[str, Any]:
        """
        Generate a response with retry logic and JSON parsing.
        Returns a parsed dictionary, automatically falling back to mock mode on persistent failure.
        """
        if self.mock_mode:
            return self._get_mock_response(system_prompt, user_input)

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.0,
                    response_format={"type": "json_object"} if "qwen" not in self.model.lower() else None
                )
                
                raw_content = response.choices[0].message.content
                cleaned_content = self._clean_json(raw_content)
                return json.loads(cleaned_content)
                
            except (APIConnectionError, APITimeoutError, RateLimitError) as e:
                logger.warning(f"API Error on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt == max_retries - 1:
                    logger.error("Max retries reached. Falling back to mock response to prevent demo freeze.")
                    return self._get_mock_response(system_prompt, user_input)
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except json.JSONDecodeError as e:
                logger.warning(f"JSON Parse Error on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt == max_retries - 1:
                    logger.error("Max retries reached. Falling back to mock response.")
                    return self._get_mock_response(system_prompt, user_input)
                    
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                logger.error("Falling back to mock response instantly.")
                return self._get_mock_response(system_prompt, user_input)

    def stream_response(self, system_prompt: str, user_input: str) -> Generator[str, None, None]:
        """Stream the LLM response (useful for UI feedback)."""
        if self.mock_mode:
            mock_data = json.dumps(self._get_mock_response(system_prompt, user_input), indent=2)
            for chunk in mock_data.split(" "):
                yield chunk + " "
                time.sleep(0.02)
            return

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.0,
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            yield f"\n[Connection Error: {e}. Falling back to mock data...]\n\n"
            mock_data = json.dumps(self._get_mock_response(system_prompt, user_input), indent=2)
            yield mock_data

    def _get_mock_response(self, system_prompt: str, user_input: str) -> Dict[str, Any]:
        """
        Return deterministic mock responses based on input.
        Provides robust fallback for SAFE, SUSPICIOUS, HIGH RISK, and CRITICAL scenarios.
        """
        # If user_input is JSON from a pipeline step, extract just the original message
        try:
            parsed_input = json.loads(user_input)
            if isinstance(parsed_input, dict) and "message" in parsed_input:
                message_text = parsed_input["message"]
            else:
                message_text = user_input
        except json.JSONDecodeError:
            message_text = user_input

        # Determine simulated risk level using OSINT precheck
        precheck = classify_synthetic_message(message_text)
        category = precheck.get("probable_category", "unknown")

        if category == "legitimate_transaction":
            risk = "SAFE"
        elif category == "betting_scam":
            risk = "SUSPICIOUS"
        elif category == "mpesa_reversal":
            risk = "HIGH RISK"
        elif category in ["safaricom_impersonation", "fuliza_scam", "kra_penalty", "otp_sim_swap"]:
            risk = "CRITICAL"
        else:
            # Fallback mapping from OSINT risk level if unhandled
            osint_risk = precheck.get("risk_level", "HIGH")
            risk_mapping = {"LOW": "SAFE", "MEDIUM": "SUSPICIOUS", "HIGH": "HIGH RISK", "CRITICAL": "CRITICAL"}
            risk = risk_mapping.get(osint_risk, "HIGH RISK")

        # Route to appropriate mock based on the agent's system prompt signature
        if "You are the Language Intelligence Agent" in system_prompt:
            return self._mock_language_agent(risk)
        elif "You are the Threat Pattern Agent" in system_prompt:
            return self._mock_threat_pattern_agent(risk)
        elif "You are the Risk Scoring Agent" in system_prompt:
            return self._mock_risk_scoring_agent(risk)
        elif "You are the Action Agent" in system_prompt:
            return self._mock_action_agent(risk)
        else:
            # Generic fallback
            return {"status": "success", "mock": True, "risk": risk}

    def _mock_language_agent(self, risk: str) -> Dict[str, Any]:
        if risk == "SAFE":
            return {
                "primary_language": "english",
                "secondary_languages": [],
                "is_code_switched": False,
                "sheng_terms_detected": [],
                "swahili_urgency_phrases": [],
                "formality_level": "formal",
                "language_anomalies": [],
                "linguistic_fraud_signals": [],
                "confidence": 0.99,
                "reasoning_summary": "Standard formal English, no anomalies detected."
            }
        elif risk == "SUSPICIOUS":
            return {
                "primary_language": "swahili",
                "secondary_languages": ["english", "sheng"],
                "is_code_switched": True,
                "sheng_terms_detected": ["bet", "shinda"],
                "swahili_urgency_phrases": ["cheza sasa"],
                "formality_level": "informal",
                "language_anomalies": ["Overly enthusiastic tone"],
                "linguistic_fraud_signals": ["Enticing language for gambling"],
                "confidence": 0.88,
                "reasoning_summary": "Informal language mixing Swahili and Sheng, typical of betting promos."
            }
        elif risk == "HIGH RISK":
            return {
                "primary_language": "swahili",
                "secondary_languages": ["sheng"],
                "is_code_switched": True,
                "sheng_terms_detected": ["tuma", "rudisha", "haraka"],
                "swahili_urgency_phrases": ["rudisha pesa tafadhali", "tuma haraka"],
                "formality_level": "informal",
                "language_anomalies": ["Pleading tone mixed with demands"],
                "linguistic_fraud_signals": ["High urgency", "Emotional manipulation"],
                "confidence": 0.92,
                "reasoning_summary": "Urgent Swahili/Sheng mix requesting money reversal."
            }
        else: # CRITICAL
            return {
                "primary_language": "english",
                "secondary_languages": ["swahili"],
                "is_code_switched": True,
                "sheng_terms_detected": [],
                "swahili_urgency_phrases": ["akaunti yako itafungwa"],
                "formality_level": "impersonating-formal",
                "language_anomalies": ["Poor grammar for an official entity", "Inconsistent casing"],
                "linguistic_fraud_signals": ["Threatening tone", "Authority impersonation"],
                "confidence": 0.95,
                "reasoning_summary": "Highly anomalous language attempting to sound like an official entity."
            }

    def _mock_threat_pattern_agent(self, risk: str) -> Dict[str, Any]:
        if risk == "SAFE":
            return {
                "scam_categories_detected": [],
                "primary_category": "none",
                "threat_signals": {},
                "impersonated_entity": "None",
                "manipulation_hook": "none",
                "extracted_demands": [],
                "legitimacy_evidence_for": ["Standard transaction format"],
                "legitimacy_evidence_against": [],
                "is_likely_legitimate": True,
                "reasoning_summary": "No threat patterns detected."
            }
        elif risk == "SUSPICIOUS":
            return {
                "scam_categories_detected": [
                    {
                        "category_id": "betting_scam",
                        "category_label": "Fake Betting / Prize",
                        "confidence": 0.85,
                        "evidence": ["Mentions betting/prize companies"]
                    }
                ],
                "primary_category": "betting_scam",
                "threat_signals": {
                    "unrealistic_promises": True,
                    "requests_small_fee": False
                },
                "impersonated_entity": "SportPesa/Betika",
                "manipulation_hook": "greed",
                "extracted_demands": ["Click link", "Place bet"],
                "legitimacy_evidence_for": [],
                "legitimacy_evidence_against": ["Unsolicited betting promo"],
                "is_likely_legitimate": False,
                "reasoning_summary": "Suspicious betting or prize claim detected."
            }
        elif risk == "HIGH RISK":
            return {
                "scam_categories_detected": [
                    {
                        "category_id": "mpesa_reversal",
                        "category_label": "M-Pesa Reversal",
                        "confidence": 0.95,
                        "evidence": ["Asks for refund of falsely sent money"]
                    }
                ],
                "primary_category": "mpesa_reversal",
                "threat_signals": {
                    "urgency_language_detected": True,
                    "wrong_number_reversal": True,
                    "unknown_sender_number": True
                },
                "impersonated_entity": "None",
                "manipulation_hook": "urgency",
                "extracted_demands": ["Send money back"],
                "legitimacy_evidence_for": [],
                "legitimacy_evidence_against": ["Sent from personal number, not Safaricom shortcode"],
                "is_likely_legitimate": False,
                "reasoning_summary": "Classic M-Pesa reversal scam pattern matched."
            }
        else: # CRITICAL
            return {
                "scam_categories_detected": [
                    {
                        "category_id": "authority_impersonation",
                        "category_label": "Authority Impersonation",
                        "confidence": 0.98,
                        "evidence": ["Claims to be Safaricom/Fuliza/KRA", "Requests OTP"]
                    }
                ],
                "primary_category": "authority_impersonation",
                "threat_signals": {
                    "requests_otp_or_pin": True,
                    "impersonates_authority": True,
                    "account_suspension_threat": True
                },
                "impersonated_entity": "Safaricom/Fuliza/KRA",
                "manipulation_hook": "fear",
                "extracted_demands": ["Share OTP", "Click verification link"],
                "legitimacy_evidence_for": [],
                "legitimacy_evidence_against": ["Sent from personal number", "Official entities don't ask for OTP"],
                "is_likely_legitimate": False,
                "reasoning_summary": "Critical authority impersonation scam attempting account takeover."
            }

    def _mock_risk_scoring_agent(self, risk: str) -> Dict[str, Any]:
        risk_map = {
            "SAFE": ("LOW", 0),
            "SUSPICIOUS": ("MEDIUM", 4),
            "HIGH RISK": ("HIGH", 7),
            "CRITICAL": ("CRITICAL", 9)
        }
        level, score = risk_map[risk]
        
        if risk == "SAFE":
            return {
                "raw_score": score,
                "risk_level": level,
                "score_override_applied": False,
                "override_reason": None,
                "triggered_indicators": [],
                "top_risk_drivers": [],
                "confidence": 0.95,
                "reasoning_summary": "Score 0. Safe."
            }
        elif risk == "SUSPICIOUS":
            return {
                "raw_score": score,
                "risk_level": level,
                "score_override_applied": False,
                "override_reason": None,
                "triggered_indicators": [
                    {"indicator": "suspicious_keywords", "weight": 4, "evidence": "Betting/prize keywords"}
                ],
                "top_risk_drivers": ["suspicious_keywords"],
                "confidence": 0.85,
                "reasoning_summary": f"Risk scored as {level} due to suspicious betting patterns."
            }
        elif risk == "HIGH RISK":
            return {
                "raw_score": score,
                "risk_level": level,
                "score_override_applied": False,
                "override_reason": None,
                "triggered_indicators": [
                    {"indicator": "reversal_request", "weight": 7, "evidence": "Asking to return funds"}
                ],
                "top_risk_drivers": ["reversal_request"],
                "confidence": 0.90,
                "reasoning_summary": f"Risk scored as {level} based on M-Pesa reversal indicators."
            }
        else: # CRITICAL
            return {
                "raw_score": score,
                "risk_level": level,
                "score_override_applied": False,
                "override_reason": None,
                "triggered_indicators": [
                    {"indicator": "impersonates_authority", "weight": 5, "evidence": "Claims to be official entity"},
                    {"indicator": "requests_otp_or_pin", "weight": 4, "evidence": "Mentions OTP or verification"}
                ],
                "top_risk_drivers": ["impersonates_authority", "requests_otp_or_pin"],
                "confidence": 0.98,
                "reasoning_summary": f"Risk scored as {level} due to critical impersonation and credential theft attempts."
            }

    def _mock_action_agent(self, risk: str) -> Dict[str, Any]:
        if risk == "SAFE":
            return {
                "verdict": "SAFE",
                "risk_level": "LOW",
                "scam_type": "None detected",
                "dashboard_summary": "Message appears legitimate.",
                "explanation": {
                    "what_is_happening": "This looks like a standard communication.",
                    "how_the_scam_works": "N/A",
                    "red_flags_found": []
                },
                "recommended_actions": [
                    {"priority": 1, "action": "No action needed", "reason": "Message is safe"}
                ],
                "do_not_do": [],
                "reporting": {"should_report": False, "contacts": []},
                "safety_tip": {
                    "english": "Always verify unexpected messages.",
                    "swahili": "Daima thibitisha ujumbe usiotarajiwa.",
                    "sheng": "Kuwa mjanja na ma text za ufala."
                },
                "confidence": 0.99
            }
        elif risk == "SUSPICIOUS":
            return {
                "verdict": "SUSPICIOUS",
                "risk_level": "MEDIUM",
                "scam_type": "Possible Betting Scam",
                "dashboard_summary": "Suspicious betting or prize claim.",
                "explanation": {
                    "what_is_happening": "You received a message about a potential prize or bet.",
                    "how_the_scam_works": "Scammers promise large returns to steal small upfront fees.",
                    "red_flags_found": ["Unrealistic returns promised", "Unknown sender"]
                },
                "recommended_actions": [
                    {"priority": 1, "action": "Do not send any money", "reason": "High chance of loss"}
                ],
                "do_not_do": ["Do not click any links", "Do not reply"],
                "reporting": {
                    "should_report": True,
                    "contacts": [{"name": "Safaricom SMS", "value": "333", "reason": "Spam reporting"}]
                },
                "safety_tip": {
                    "english": "If it's too good to be true, it probably is.",
                    "swahili": "Kama ni nzuri sana kuwa kweli, labda ni uongo.",
                    "sheng": "Cheza chini, hizi form za quick money ni scam."
                },
                "confidence": 0.85
            }
        elif risk == "HIGH RISK":
            return {
                "verdict": "SCAM",
                "risk_level": "HIGH",
                "scam_type": "M-Pesa Reversal Fraud",
                "dashboard_summary": "High Risk: M-Pesa Reversal Scam Detected",
                "explanation": {
                    "what_is_happening": "Someone is pretending to have sent you money by mistake.",
                    "how_the_scam_works": "They send a fake SMS looking like M-Pesa, then call you urgently asking for a refund.",
                    "red_flags_found": ["Fake M-Pesa format", "High urgency", "Sent from personal number"]
                },
                "recommended_actions": [
                    {"priority": 1, "action": "Ignore the message completely", "reason": "It is a known scam tactic"},
                    {"priority": 2, "action": "Check your actual M-Pesa balance via USSD *334#", "reason": "To confirm no money actually arrived"}
                ],
                "do_not_do": ["Do NOT send money back", "Do NOT share your M-Pesa PIN"],
                "reporting": {
                    "should_report": True,
                    "contacts": [{"name": "Safaricom Fraud SMS", "value": "333", "reason": "Free official reporting line"}]
                },
                "safety_tip": {
                    "english": "Never refund money directly. Tell them to contact Safaricom to reverse it.",
                    "swahili": "Usirudishe pesa moja kwa moja. Waambie wapigie Safaricom kuirejesha.",
                    "sheng": "Zima huyo msee, mwambie apigie customer care. Usitume doo."
                },
                "confidence": 0.98
            }
        else: # CRITICAL
            return {
                "verdict": "SCAM",
                "risk_level": "CRITICAL",
                "scam_type": "Authority Impersonation",
                "dashboard_summary": "Critical: Account Takeover Attempt",
                "explanation": {
                    "what_is_happening": "A scammer is impersonating Safaricom, Fuliza, or KRA to steal your account.",
                    "how_the_scam_works": "They threaten you with account suspension or fake loans to trick you into sharing your OTP or PIN.",
                    "red_flags_found": ["Requests OTP", "Impersonates official entity", "Threatens account suspension"]
                },
                "recommended_actions": [
                    {"priority": 1, "action": "Do not share any OTP or PIN", "reason": "Official entities never ask for this."}
                ],
                "do_not_do": ["Do NOT share your OTP", "Do NOT click any links"],
                "reporting": {
                    "should_report": True,
                    "contacts": [{"name": "Safaricom Fraud SMS", "value": "333", "reason": "Free official reporting line"}]
                },
                "safety_tip": {
                    "english": "Never share your OTP or PIN with anyone, even if they claim to be from Safaricom.",
                    "swahili": "Usishiriki OTP au PIN yako na mtu yeyote, hata kama anadai kutoka Safaricom.",
                    "sheng": "Chunga sana, usiwahi peana OTP yako kwa mtu, hata kama anajiita Safaricom."
                },
                "confidence": 0.99
            }

# Hybrid Mode: OSINT Precheck Integrated
