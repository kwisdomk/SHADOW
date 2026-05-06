"""
core/synthetic_threat_intel.py
Shadow — AI Fraud Detection System
AMD Hackathon 2026

Generates synthetic Kenyan fraud datasets (Sheng/Swahili/English) to overcome
the "Data Cold Start" problem. Uses the Shadow LLM Client to generate high-quality,
localized scam variations for training and evaluation.
"""

import json
import time
import os
import sys
from typing import List, Dict, Any

# Ensure the core module is discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.llm_client import ShadowLLMClient
from core.kenyan_context import SCAM_CATEGORIES, SHENG_SCAM_GLOSSARY

SYNTHETIC_GENERATOR_PROMPT = """
You are a Kenyan cybersecurity data engineer. Your task is to generate realistic,
synthetic fraud SMS messages to train our AI models.
We are focusing on the Kenyan context, specifically using code-switching (English, Swahili, Sheng).

Target Scam Category: {category_label}
Description: {category_description}
Keywords: {keywords}
Example Patterns: {example_patterns}

Glossary of Sheng terms to optionally incorporate:
{sheng_glossary}

Generate {count} unique, realistic SMS variations of this scam.
Ensure they vary in tone (urgent, threatening, pleading, formal-impersonation).
Include authentic Kenyan names (e.g., Kamau, Omondi, Wanjiku), typical amounts (e.g., KES 500, Ksh 30,000),
and standard shortcodes/numbers where applicable.

Return ONLY a valid JSON object matching this schema. NO MARKDOWN FENCES, no preamble.
{{
  "synthetic_messages": [
    {{
      "message": "<the raw sms text>",
      "language_mix": "<english|swahili|sheng|mixed>",
      "tone": "<urgent|threatening|pleading|impersonation>",
      "key_signals": ["<signal 1>", "<signal 2>"]
    }}
  ]
}}
"""

class SyntheticDataGenerator:
    """Generates synthetic threat intelligence data using the AMD Cloud / Qwen model."""
    
    def __init__(self):
        self.llm_client = ShadowLLMClient()
        
    def generate_category_dataset(self, category_id: str, count: int = 5) -> Dict[str, Any]:
        """Generate synthetic examples for a specific scam category."""
        if category_id not in SCAM_CATEGORIES:
            raise ValueError(f"Unknown category_id: {category_id}")
            
        category = SCAM_CATEGORIES[category_id]
        
        system_prompt = SYNTHETIC_GENERATOR_PROMPT.format(
            category_label=category["label"],
            category_description=category["description"],
            keywords=", ".join(category.get("keywords", [])),
            example_patterns=" | ".join(category.get("example_patterns", [])),
            sheng_glossary=json.dumps(SHENG_SCAM_GLOSSARY, indent=2),
            count=count
        )
        
        user_input = f"Generate {count} synthetic examples for the {category['label']} category."
        
        print(f"Generating {count} synthetic examples for '{category_id}'...")
        start_time = time.time()
        
        try:
            result = self.llm_client.generate_response(system_prompt, user_input)
            duration = round(time.time() - start_time, 2)
            print(f"Generation complete in {duration}s.")
            return result
        except Exception as e:
            print(f"Error generating synthetic data: {e}")
            return {"synthetic_messages": []}

    def generate_full_benchmark(self, count_per_category: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        """Generates a full benchmark dataset across all known scam categories."""
        benchmark_dataset = {}
        for cat_id in SCAM_CATEGORIES.keys():
            result = self.generate_category_dataset(cat_id, count=count_per_category)
            benchmark_dataset[cat_id] = result.get("synthetic_messages", [])
            # Brief pause to avoid rate limits
            time.sleep(1)
            
        return benchmark_dataset

if __name__ == "__main__":
    import os
    os.environ["SHADOW_MOCK_MODE"] = "true"
    generator = SyntheticDataGenerator()
    # Test generation for a single category
    print("Testing Synthetic Data Generation (M-Pesa Reversal)")
    data = generator.generate_category_dataset("mpesa_reversal", count=2)
    print(json.dumps(data, indent=2))
