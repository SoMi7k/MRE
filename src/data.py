class InputData:
    """"""
    def __init__(self, text_to_extract: str, prompt: str, json_structure: str):
        """Inits Extractor parametrs"""
        self.text = text_to_extract
        self.prompt = prompt
        self.json = json_structure


LLM_keys = {
    "Claude-Sonnet-3.7": "ANTHROPIC_API_KEY",
    "gpt-4.1": "OPENAI_API_KEY",
    "Mistral-7B": "MISTRAL_API_KEY",
    "BioGPT": "HF_API_KEY", 
    "ClinicalBERT": "HF_API_KEY", 
    "Czert-B": "HF_API_KEY",
    "Gemini": "GEMINI_API_KEY"
}
