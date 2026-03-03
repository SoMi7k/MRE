import csv
import os
from datetime import datetime
from scripts import config

# Pricing tabulka zůstává stejná
pricing = {
    "anthropic/claude-sonnet-4.5": {"input": 3.00, "output": 15.00},
    "deepseek/deepseek-v3.2": {"input": 0.20, "output": 0.80},
    "openai/gpt-5-chat": {"input": 1.25, "output": 10.00},
    "google/gemini-3-pro-preview": {"input": 2.00, "output": 12.00},
    "x-ai/grok-4": {"input": 3.00, "output": 15.00},
    "mistralai/mixtral-8x7b-instruct": {"input": 0.24, "output": 0.24},
}

class CostLogger():
    def __init__(self, path=None):
        # Pokud cesta není zadána, vezme se z configu a změní se na .csv
        self.path = path or os.path.join(config.RESULT_ROOT, "costs_logger.csv")
        self.pricing = pricing
       
    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int):
        if model not in self.pricing:
            raise ValueError(f"Model {model} není v pricing tabulce.")

        p = self.pricing[model]
        input_cost = (input_tokens / 1_000_000) * p["input"]
        output_cost = (output_tokens / 1_000_000) * p["output"]
        total_cost = input_cost + output_cost

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_cost_usd": round(total_cost, 6),
        }
       
    def write_cost(self, model: str, input_tok: int, output_tok: int):
        result = self.calculate_cost(model, input_tok, output_tok)
        
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        file_exists = os.path.exists(self.path)

        # Rychlejší zápis bez nutnosti nahrávat Pandas
        with open(self.path, mode="a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=result.keys())
            if not file_exists or os.path.getsize(self.path) == 0:
                writer.writeheader()
            writer.writerow(result)

        print(f"[{result['timestamp']}] [COST] {result['model']} | Total: {result['total_cost_usd']:.6f} USD")
        return result