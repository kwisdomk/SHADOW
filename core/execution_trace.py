from typing import Dict, Any, List, Optional

class ExecutionTrace:
    """
    Stores a sequential list of steps for the Live Execution Timeline.
    Exposes the internal agentic reasoning of Shadow as a visual trace.
    """
    def __init__(self):
        self.steps: List[Dict[str, Any]] = []

    def add_step(self, agent: str, input_str: str, output: Dict[str, Any], summary: str, risk_hint: Optional[str] = None):
        step_number = len(self.steps)
        step = {
            "step": step_number,
            "agent": agent,
            "input": input_str,
            "output": output,
            "summary": summary,
            "risk_hint": risk_hint
        }
        self.steps.append(step)

    def get_trace(self) -> List[Dict[str, Any]]:
        return self.steps

    def clear(self):
        self.steps = []

def format_execution_trace(trace: List[Dict[str, Any]]) -> str:
    """Returns a human-readable timeline of the execution trace."""
    lines = []
    for step in trace:
        # Format: [STEP 1] OSINT PRECHECK → mpesa_reversal detected
        # If the user specifically wants OSINT PRECHECK to be STEP 0, or if they meant the first step is step 0:
        # The prompt says: "OSINT Precheck must be STEP 0: Log: agent = 'OSINT_PRECHECK'"
        # But also says: "[STEP 1] OSINT PRECHECK -> ..." in the example.
        # I'll just use the step_number from the dictionary (which starts at 0).
        step_num = step["step"]
        agent = step["agent"].replace("_", " ")
        if not agent.endswith("AGENT") and agent != "OSINT PRECHECK":
            # Just in case agent string doesn't include "AGENT" already
            pass
        lines.append(f"[STEP {step_num}] {agent.upper()} -> {step['summary']}")
        
    return "\n".join(lines)
