import pandas as pd
import os
import streamlit as st
# import src.API as API
import json
import features.env as ft
import src.data as dt
from scripts import config
from datetime import datetime

selected_LLM = None
API_key = ft.API_keys(None)

# Sidebar
with st.sidebar:
    LLM_list = ["Claude-Sonnet-3.7", "GPT-4.1", "Mistral-7B", "Gemini", "BioGPT", "ClinicalBERT", "Czert-B"]
    selected_LLM = st.selectbox("Choose a LLM model:", LLM_list)

if selected_LLM:
    API_key = ft.API_keys(dt.LLM_keys[selected_LLM])

# Mainpage
st.title("Welcome to MRE Project")

csv_dir = config.CSV_DATA_ROOT
json_dir = config.JSON_DATA_ROOT
report_dir = config.REPORTS_ROOT
tasks_dir = config.TASKS_ROOT
prompt_dir = config.PROMPT_ROOT

dirs = [csv_dir, json_dir, report_dir, tasks_dir, prompt_dir]

st.title("📂 Data Viewer")

# Vyber složku
selected_dir = st.selectbox("Vyber složku:", dirs)

# Získej seznam souborů v dané složce
if os.path.exists(selected_dir):
    files = [
        f for f in os.listdir(selected_dir)
        if os.path.isfile(os.path.join(selected_dir, f))
    ]
else:
    files = []

if not files:
    st.warning(f"Ve složce `{selected_dir}` nebyly nalezeny žádné soubory.")
else:
    # Vyber konkrétní soubor
    selected_file = st.selectbox("Vyber soubor k prohlédnutí:", files)

    if st.button("Show data", type="primary"):
        path = os.path.join(selected_dir, selected_file)
        try:
            # CSV
            if selected_file.endswith(".csv"):
                df = pd.read_csv(path)
                st.write(f"### 🧾 Náhled souboru `{selected_file}`")
                st.dataframe(df)

            # JSON
            elif selected_file.endswith(".json"):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list) and all(isinstance(x, dict) for x in data):
                    df = pd.DataFrame(data)
                    st.write(f"### 🧾 Náhled souboru `{selected_file}`")
                    st.dataframe(df)
                else:
                    st.json(data)

            # TXT
            elif selected_file.endswith(".txt"):
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                st.write(f"### 📄 Obsah souboru `{selected_file}`")
                st.text(text)

            # Jiný formát
            else:
                st.warning(f"Soubor `{selected_file}` má nepodporovaný formát.")

        except Exception as e:
            st.error(f"Chyba při čtení souboru: {e}")

Idata = dt.InputData("","","")

st.markdown("---")

st.title("📝 Test Input Maker")

st.markdown("Instrukce")
t_number = st.text_input("Číslo tasku:")
task = st.text_area(
    "Zadej instrukce pro LLM:",
    placeholder="Sem napiš instrukce...",
    height=150
)

st.markdown("Lékařská zpráva")
r_number = st.text_input("Číslo lékařské zprávy:")
report = st.text_area(
    "Zadej text lékařské zprávy:",
    placeholder="Sem vlož text...",
    height=250
)

if st.button("Vytvoř prompt", type="primary"):
    try:

        # Vytvoř JSON se strukturou
        data = {
            "task": task.strip(),
            "report": report.strip()
        }

        outpath = os.path.join(prompt_dir, f"r{r_number}_t{t_number}.json")
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        st.success("✅ Soubory úspěšně vytvořeny!")
    except Exception as e:
        st.error(f"Chyba při ukládání: {e}")

st.markdown("---")

st.title("📝 Result Maker")
st.markdown("LLM")

LLMs = ["Claude", "GPT", "Mistral", "Gemini", "Llama", "Grok"]
sel_LLM = st.selectbox("Choose a LLM model:", LLMs)
report_number = st.text_input("Č. lékařské zprávy:")
task_number = st.text_input("Č. tasku:")
result_text = st.text_area("Zadej výseldek LLM:", placeholder="Sem vlož výsledný json", height=250)

if st.button("Create result", type="primary"):
    try:
        dirname = config.RESULT_JSON_ROOT
        filename = f"{sel_LLM}_{datetime.now().strftime("%d%m%y")}_r{report_number}_t{task_number}.json"
        if (int(report_number) < 10):
            report_theme = "crohn"
        else:
            report_theme = "stroke"
        outfile = os.path.join(dirname, report_theme, filename)

        # Uložení souboru
        with open(outfile, "w", encoding="utf-8") as fr:
            fr.write(result_text)
            fr.write("\n")

        st.success("✅ Soubory úspěšně vytvořeny!")

    except Exception as e:
        st.error(f"Chyba při ukládání: {e}")
    
st.markdown("---")

result_path = config.RESULT_JSON_ROOT
res_dirs = os.listdir(result_path)
dir_paths = [os.path.join(result_path, name) for name in res_dirs]

st.title("LLM outputs")

# Vyber složku
selected_dir = st.selectbox("Vyber složku:", dir_paths)

# Input pro filtrování souborů
filter_text = st.text_input("Filtrovat soubory podle názvu (např. 'r03'):", "")

# Získej seznam souborů v dané složce
if os.path.exists(selected_dir):
    files = [
        f for f in os.listdir(selected_dir)
        if os.path.isfile(os.path.join(selected_dir, f))
    ]
    # Filtrování souborů podle zadaného textu
    if filter_text:
        files = [f for f in files if filter_text.lower() in f.lower()]
else:
    files = []

if not files:
    st.warning(f"Ve složce `{selected_dir}` nebyly nalezeny žádné soubory {f'(obsahující "{filter_text}") if filter_text else ""'}.")
else:
    # Vyber konkrétní soubor
    selected_file = st.selectbox("Vyber soubor k prohlédnutí:", files)
    if st.button("Show result", type="primary"):
        path = os.path.join(selected_dir, selected_file)
        try:
            # JSON
            if selected_file.endswith(".json"):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list) and all(isinstance(x, dict) for x in data):
                    df = pd.DataFrame(data)
                    st.write(f"### 📄 Obsah souboru `{selected_file}`")
                    st.dataframe(df)
                else:
                    st.json(data)
            # Jiný formát
            else:
                st.warning(f"Soubor `{selected_file}` má nepodporovaný formát.")
        except Exception as e:
            st.error(f"Chyba při čtení souboru: {e}")




