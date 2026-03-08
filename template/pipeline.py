import streamlit as st
import pandas as pd
from datetime import datetime 
import os
import json
import scripts.config as config
import requests
from typing import Any
from src.logger import Logger
from src.analyzatorJson import analyzeJson
import re

logger = Logger()

def find_report_path(json_path: str):
    match = re.search(r"rc(\d+)", json_path)
    pattern = ""

    if match:
        pattern = "c" + match.group(1)            
        print(f"Nalezeno: {pattern}")
        report_path = ""
        
        for dir in os.listdir(config.REPORTS_ROOT):
            if re.findall(pattern, dir):
                report_path = os.path.join(config.REPORTS_ROOT, dir)
                break
    else:
        raise Exception(f"Original medical report was not found from path: {json_path}") 
    
    print(report_path)
    return report_path

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
        return None
    
    result = response.json()

    return result

def extract_json_from_content(content: str) -> str:
    """Extract JSON from content that might be wrapped in markdown code blocks."""
    # Try direct parsing first
    try:
        json.loads(content)
        return content
    except json.JSONDecodeError:
        pass
    
    # Try to extract from markdown code blocks (```json ... ```)
    match = re.search(r'```(?:json)?\s*\n(.*?)\n```', content, re.DOTALL)
    if match:
        json_str = match.group(1).strip()
        try:
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            pass
    
    # If all else fails, return the original content
    return content


def save_output(model: str, filepath: str, model_output: str) -> None:
    try:
        filename = f"{os.path.basename(filepath)}_{datetime.now().strftime('%d%m%y')}"
        outpath = os.path.join(config.RESULT_JSON_ROOT, "crohn", config.LLMS[model],filename)
        
        # Uložení souboru
        with open(outpath, "w", encoding="utf-8") as fr:
            fr.write(model_output)
            fr.write("\n")

        st.success("✅ Soubory úspěšně vytvořeny!")
        
    except Exception as e:
        st.error(f"Chyba při ukládání: {e}")

def show():
    st.title("📝 My LLM Pipeline")
    # Model choice
    selected_model = st.selectbox("Vyber model:", config.MODELS)
    
    # Scenario paths
    scenarios = os.listdir(config.PROMPT_ROOT)
    scenario_dirs = [os.path.join(config.PROMPT_ROOT, scenario) for scenario in scenarios if os.path.isdir(os.path.join(config.PROMPT_ROOT, scenario))]
    selected_scenario = st.selectbox("Vyber scénář pro testování:", scenario_dirs)
    
    # Input choice
    input_names = os.listdir(selected_scenario)
    selected_prompt = None
    if input_names:
        inputs = [os.path.join(selected_scenario, prompt) for prompt in input_names if os.path.isfile(os.path.join(selected_scenario, prompt))]
        selected_prompt = st.selectbox("Vyber prompt:", inputs)

        # inicializace session state
        if "preview" not in st.session_state:
            st.session_state.preview = None

        # načtení promptu
        try:
            with open(selected_prompt, "r", encoding="utf-8") as f:
                st.session_state.preview = json.load(f)
        except Exception as e:
            st.error(f"Error while reading {selected_prompt}: {e}")
            return
    else:
        st.info("V scénáři nejsou žádné soubory, zvol jiný.")

    # Tlačítko pro náhled
    if selected_prompt:
        if st.button("View prompt", type="secondary"):
            st.write(f"### 🧾 Náhled souboru `{selected_prompt}`")

            preview = st.session_state.preview

            if isinstance(preview, list):
                st.dataframe(pd.DataFrame(preview))
            elif isinstance(preview, dict):
                st.json(preview)
            else:
                st.write(preview)

        # Pipeline Start 
        if st.button("Start workflow", type="primary"):
            progress = st.progress(0)
            with st.status("Running workflow...", expanded=True) as status:

                # 1️⃣ LLM CALL
                try:
                    status.write("📡 Calling LLM model...")
                    progress.progress(10)

                    preview = st.session_state.preview

                    with st.spinner("Waiting for LLM response..."):
                        output = POST(selected_model, preview)

                    if not output:
                        status.update(label="❌ LLM call failed", state="error")
                        st.error("Error while generating output from LLM!")
                        return

                    content = output["choices"][0]["message"]["content"]

                    progress.progress(40)

                    status.write("✅ LLM response received")

                    usage = output["usage"]
                    logger.write_cost(
                        model=selected_model,
                        input_tok=usage["prompt_tokens"],
                        output_tok=usage["completion_tokens"],
                        input_name=selected_prompt
                    )

                except Exception as e:
                    status.update(label="❌ LLM processing failed", state="error")
                    st.error(f"Chyba při vytváření výsledku z LLM: {e}")
                    return

                # 2️⃣ SAVE OUTPUT
                try:
                    status.write("💾 Saving output...")
                    progress.progress(60)

                    # Extract JSON from content (handles markdown code blocks, etc.)
                    clean_content = extract_json_from_content(content)
                    
                    try:
                        parsed = json.loads(clean_content)
                        text = json.dumps(parsed, indent=4, ensure_ascii=False)
                    except json.JSONDecodeError as json_err:
                        # If content is not valid JSON, save as-is and warn user
                        st.warning(f"⚠️ LLM output is not valid JSON: {json_err}")
                        return

                    save_output(selected_model, selected_prompt, text)

                    progress.progress(75)
                    status.write("✅ Output saved")

                except Exception as e:
                    status.update(label="❌ Saving failed", state="error")
                    st.error(f"Chyba při ukládání výstupu z LLM: {e}")
                    return

                # 3️⃣ ANALYZE OUTPUT
                try:
                    status.write("🔎 Running JSON analysis...")
                    progress.progress(85)
                    
                    filename = f"{os.path.basename(selected_prompt)}_{datetime.now().strftime('%d%m%y')}"
                    outpath = os.path.join(
                        config.RESULT_LMM,
                        config.LLMS[selected_model],
                        filename
                    ).replace(".json", ".txt")

                    analyzeJson(parsed, outpath, find_report_path(selected_prompt))

                    progress.progress(100)

                    status.write("✅ Analysis finished")

                except Exception as e:
                    status.update(label="❌ Analysis failed", state="error")
                    st.error(f"Chyba při analýze výstupu: {e}")
                    return

                status.update(label="🎉 Workflow completed", state="complete")

            # OUTPUT SECTIONS

            st.subheader("Výstup modelu")

            with st.expander("📄 Model Output", expanded=True):
                st.write(content)

            with st.expander("📊 JSON Output"):
                st.json(parsed)

            st.success(f"Výsledek uložen jako: {outpath}")
    