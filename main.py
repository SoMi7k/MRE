import pandas as pd
import os
import streamlit as st
import src.API as API
import json
import features.env as ft
import src.data as dt
from scripts import config

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
prompt_dir = config.PROMPT_ROOT
text_dir = config.TEXTS_ROOT
input_files_dir = config.TEST_INPUTS_ROOT

dirs = [csv_dir, json_dir, prompt_dir, text_dir, input_files_dir]

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

st.markdown("Prompt")
prompt = st.text_area(
    "Zadej prompt:",
    placeholder="Sem napiš prompt...",
    height=150
)

st.markdown("Text")

text_header = st.text_area(
    "Zadej text:",
    placeholder="# csv_filename | id_of_text (eg. id of mre, datetime)",
    height=30
)
text = st.text_area(
    "Zadej text:",
    placeholder="Sem vlož text...",
    height=250
)
"""
Nejlépe přidat do samostatných btns

# Ulož prompt a text do .txt souborů
with open(os.path.join(prompt_dir, "0x_prompt.txt"), "w", encoding="utf-8") as f:
    f.write(prompt.strip() + "\n")

with open(os.path.join(text_dir, "0x_text.txt"), "w", encoding="utf-8") as f:
    f.write(text_header.strip() + "\n")
    f.write(text.strip() + "\n")
"""
if st.button("Create prompt", type="primary"):
    try:

        # Vytvoř JSON se strukturou
        data = {
            # "_comment": "doplníš si sám",
            "prompt": prompt.strip(),
            "text": text.strip()
        }

        with open(os.path.join(input_files_dir, "0x_test_input.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        st.success("✅ Soubory úspěšně vytvořeny!")
    except Exception as e:
        st.error(f"Chyba při ukládání: {e}")
    
st.markdown("---")

result_path = config.RESULT_ROOT

res_dirs = os.listdir(result_path)
dir_paths = [os.path.join(result_path, name) for name in res_dirs]

st.title("LLM outputs")

# Vyber složku
selected_dir = st.selectbox("Vyber složku:", dir_paths)

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

    if st.button("Show result", type="primary"):
        path = os.path.join(selected_dir, selected_file)
        try:
            # TXT
            if selected_file.endswith(".txt"):
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                st.write(f"### 📄 Obsah souboru `{selected_file}`")
                st.text(text)

            # Jiný formát
            else:
                st.warning(f"Soubor `{selected_file}` má nepodporovaný formát.")

        except Exception as e:
            st.error(f"Chyba při čtení souboru: {e}")




