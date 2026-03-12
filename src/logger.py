import csv
import os
from datetime import datetime
from scripts import config

# Pricing tabulka zůstává stejná
pricing = {
    "anthropic/claude-sonnet-4.5": {"input": 3.00, "output": 15.00},
    "deepseek/deepseek-v3.2": {"input": 0.25, "output": 0.40},
    "openai/gpt-5.2": {"input": 1.75, "output": 14.00},
    "google/gemini-3.1-pro-preview": {"input": 2.00, "output": 12.00},
    "x-ai/grok-4": {"input": 3.00, "output": 15.00},
    "mistralai/mixtral-8x22b-instruct": {"input": 2.00, "output": 6.00},
    "meta-llama/llama-4-maverick": {"input": 0.15, "output": 0.60}
}

class Logger():
    def __init__(self, path=None) -> None:
        # Pokud cesta není zadána, vezme se z configu a změní se na .csv
        self.path = path or os.path.join(config.RESULT_ROOT, "logger.csv")
        self.pricing = pricing
       
    def write_cost(self, model: str, scenario: str, input_tok: int, output_tok: int, cost: float, input_name: str) -> None:
        result = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model": model,
            "scenario": scenario,
            "input_name": input_name.replace(".json", ""),
            "input_tokens": input_tok,
            "output_tokens": output_tok,
            "total_cost_usd": cost,
        }
        
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        file_exists = os.path.exists(self.path)

        # Rychlejší zápis bez nutnosti nahrávat Pandas
        with open(self.path, mode="a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=result.keys())
            if not file_exists or os.path.getsize(self.path) == 0:
                writer.writeheader()
            writer.writerow(result)

        print(f"[{result['timestamp']}] - [Scenario - filename] {scenario} {input_name} - [COST] {result['model']} | Total: {result['total_cost_usd']:.6f} USD")