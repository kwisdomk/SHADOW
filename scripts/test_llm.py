import os
import sys

# Ensure the core module is discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.llm_client import ShadowLLMClient
from core.prompts import get_system_prompt

def run_smoke_test():
    print("="*60)
    print(" Shadow LLM Client - Smoke Test")
    print("="*60)
    
    # Force mock mode for the smoke test to avoid needing an API key
    os.environ["SHADOW_MOCK_MODE"] = "true"
    
    client = ShadowLLMClient()
    
    print("\n[1] Testing generate_response (SAFE message)")
    system_prompt_action = get_system_prompt("action_agent")
    user_input_safe = "Hello, your M-Pesa balance is 500 Ksh."
    response = client.generate_response(system_prompt_action, user_input_safe)
    print(f"Verdict: {response.get('verdict')}")
    print(f"Risk Level: {response.get('risk_level')}")
    print(f"Confidence: {response.get('confidence')}")

    print("\n[2] Testing generate_response (HIGH RISK message)")
    user_input_risk = "Tuma hiyo pesa kwa hii namba haraka sana ndio nifungue account yako ya KRA."
    response = client.generate_response(system_prompt_action, user_input_risk)
    print(f"Verdict: {response.get('verdict')}")
    print(f"Risk Level: {response.get('risk_level')}")
    print(f"Confidence: {response.get('confidence')}")
    
    print("\n[3] Testing stream_response (SUSPICIOUS message)")
    user_input_suspicious = "You have won a betting prize. Send 500 to register."
    print("Streaming output:")
    stream = client.stream_response(system_prompt_action, user_input_suspicious)
    for chunk in stream:
        print(chunk, end="", flush=True)
    print("\n\n" + "="*60)
    print(" Smoke Test Complete!")
    print("="*60)

if __name__ == "__main__":
    run_smoke_test()
