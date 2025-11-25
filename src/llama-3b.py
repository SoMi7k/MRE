from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_name = "meta-llama/Llama-3.2-3B"

tokenizer = AutoTokenizer.from_pretrained(model_name, token="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")
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto", token="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")

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# === Spojený prompt ===
full_prompt = ""

result = pipe(full_prompt, max_new_tokens=1200, temperature=0.2)

# === Výsledek ===
with open("llama.md", 'w', encoding='utf-8') as wr:
    wr.write(result[0]["generated_text"] + "\n")