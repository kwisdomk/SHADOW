import os
import sys

# Ensure the core/agents modules are discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.pipeline import ShadowPipeline

def run_tests():
    print("="*60)
    print(" Shadow Pipeline - Smoke Test")
    print("="*60)
    
    # Force mock mode for testing without LLM API
    os.environ["SHADOW_MOCK_MODE"] = "true"
    
    pipeline = ShadowPipeline()
    
    test_cases = [
        ("Legit M-Pesa", "Confirmed. You have received KSh 500 from John."),
        ("SportPesa jackpot scam", "Hongera! Wewe ndio mshindi wa 500k SportPesa Weekly Jackpot. Tuma 2,500 ya registration fee kupokea pesa kwa MPESA yako leo."),
        ("M-Pesa reversal", "Maze nilikosea nikatuma thao, rudisha haraka."),
        ("Fuliza boost scam", "Safaricom promotion: Kuongeza Fuliza limit yako hadi 50,000, tuma KES 300 kwa Till 889XXX for system activation."),
        ("KRA penalty scam", "KRA ALERT: Uko na tax arrears ya KES 23,450 kwa iTax system yako. Lipa ndani ya masaa 48 au utashtakiwa. Call 0756XXXXXX sasa.")
    ]
    
    for name, message in test_cases:
        print(f"\n[Testing] {name}")
        print(f"Message: {message}")
        state = pipeline.run(message)
        
        precheck_risk = state.precheck_data.get('risk_level', 'UNKNOWN')
        precheck_category = state.precheck_data.get('probable_category', 'UNKNOWN')
        
        verdict = state.action_data.get('verdict', 'UNKNOWN')
        risk_level = state.risk_data.get('risk_level', 'UNKNOWN')
        if not risk_level or risk_level == 'UNKNOWN':
            # Fallback to action_data risk if risk_data doesn't have it
            risk_level = state.action_data.get('risk_level', 'UNKNOWN')
        
        print(f"PreCheck Result: [{precheck_risk}] {precheck_category}")
        print(f"Final Verdict: {verdict}")
        print(f"Risk Level: {risk_level}")
        print("\nExecution Timeline:")
        print(state.formatted_trace)
        print("\nExecution Log:")
        for log in state.execution_log:
            print(f"  - {log}")
        print("-" * 40)
        
    print("\nAll tests completed with zero crashes.")

if __name__ == "__main__":
    run_tests()
