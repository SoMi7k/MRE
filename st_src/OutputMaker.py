import streamlit as st
import pandas as pd
from datetime import datetime 
import os
import json
import scripts.config as config
import requests
from typing import Any

prompt_dir = config.PROMPT_ROOT
prompts = os.listdir(prompt_dir)

def POST(model: str, prompt: dict) -> Any:
    headers = {
        "Authorization": f"Bearer {config.API_KEY}",
        "Content-Type": "application/json"
    }
    
    full_prompt = f"""
        {prompt["task"]}
        
        TEXT:
        {prompt["report"]}
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
        print(response.json())
        return {"error": response.json()}

    result = response.json()

    return result

def show():
    st.title("📝 Output Maker")
    
    selected_model = st.selectbox("Vyber model:", config.MODELS)
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
            if output["error"]:
                st.error(f"Error generating ouput from LLM: {output["error"]}")
            else:
                content = output["choices"][0]["message"]["content"]
            st.subheader("Výstup modelu")

            try:
                parsed = json.loads(content)
                st.dataframe(pd.DataFrame([parsed]))
            except Exception as e:
                st.error(f"Chyba při načítání JSON výstupu: {e}")

            st.success("✅ Hotovo")

        except Exception as e:
            st.error(f"Chyba při POST: {e}")

    st.markdown("---")
    
    st.title("📋 Result Maker")
    st.markdown("LLM")
    
    result_text = st.text_area("Zadej výseldek LLM:", placeholder="Sem vlož výsledný json", height=250)

    if st.button("Create result", type="primary"):
        try:
            filename = f"{config.LLMS[selected_model]}_{datetime.now().strftime("%d%m%y")}_{selected_prompt}"
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