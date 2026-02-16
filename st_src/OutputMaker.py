import streamlit as st
import pandas as pd
from datetime import datetime 
import os
import json
import scripts.config as config
import requests
from typing import Any

MODELS = [
    "meta-llama/llama-3.2-3b-instruct",
    "anthropic/claude-sonnet-4.5",
    "deepseek/deepseek-v3.2",
    "openai/gpt-5-chat",
    "google/gemini-3-pro-preview",
    "x-ai/grok-4",
    "mistralai/mixtral-8x7b-instruct"
]

prompt_dir = config.PROMPT_ROOT
prompts = os.listdir(prompt_dir)

def POST(model: str, prompt: dict) -> Any:
    headers = {
        "Authorization": f"Bearer {config.API_KEY}",
        "Content-Type": "application/json"
    }
    
    full_prompt = f"""
        {prompt["prompt"]}
        
        TEXT:
        {prompt["text"]}
    """

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0,
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        return {"error": response.text}

    result = response.json()

    return result

def show():
    st.title("📝 Output Maker")
    
    selected_model = st.selectbox("Vyber model:", MODELS)
    selected_prompt = st.selectbox("Vyber prompt:", prompts)

    # inicializace session state
    if "preview" not in st.session_state:
        st.session_state.preview = None

    # načtení promptu
    try:
        with open(os.path.join(prompt_dir, selected_prompt), "r", encoding="utf-8") as f:
            st.session_state.preview = json.load(f)
    except Exception as e:
        st.error(f"Error while reading {selected_prompt}: {e}")
        return

    # tlačítko pro náhled
    if st.button("View prompt", type="secondary"):
        st.write(f"### 🧾 Náhled souboru `{os.path.join(prompt_dir, selected_prompt)}`")

        preview = st.session_state.preview

        if isinstance(preview, list):
            st.dataframe(pd.DataFrame(preview))
        elif isinstance(preview, dict):
            st.json(preview)
        else:
            st.write(preview)

    # tlačítko POST
    if st.button("POST", type="primary"):
        try:
            preview = st.session_state.preview

            output = POST(selected_model, preview)

            content = output["choices"][0]["message"]["content"]

            st.subheader("Výstup modelu")
            st.write(content)

            try:
                parsed = json.loads(content)
                st.dataframe(pd.DataFrame([parsed]))
            except:
                pass

            st.success("✅ Hotovo")

        except Exception as e:
            st.error(f"Chyba při POST: {e}")

    st.markdown("---")
    
    st.title("📋 Result Maker")
    st.markdown("LLM")

    LLMs = {
        "Claude": "anthropic/claude-sonnet-4.5", 
        "GPT": "openai/gpt-5-chat", 
        "Mistral": "mistralai/mixtral-8x7b-instruct", 
        "Gemini": "google/gemini-3-pro-preview", 
        "Llama": "meta-llama/llama-3.2-3b-instruct", 
        "Grok": "x-ai/grok-4", 
        "DeepSeek": "deepseek/deepseek-v3.2"
    }
    
    result_text = st.text_area("Zadej výseldek LLM:", placeholder="Sem vlož výsledný json", height=250)

    if st.button("Create result", type="primary"):
        try:
            filename = f"{LLMs[selected_model]}_{datetime.now().strftime("%d%m%y")}"
            outpath = os.path.join(config.RESULT_JSON_ROOT, "crohn", filename)
            """
            if (int(report_number) < 10):
                report_theme = "crohn"
            else:
                report_theme = "stroke"
            """

            # Uložení souboru
            with open(outpath, "w", encoding="utf-8") as fr:
                fr.write(result_text)
                fr.write("\n")

            st.success("✅ Soubory úspěšně vytvořeny!")

        except Exception as e:
            st.error(f"Chyba při ukládání: {e}")