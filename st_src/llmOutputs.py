import pandas as pd
import os
import streamlit as st
import json
from scripts import config

def show():
    st.title("📊 Results Viewer")

    result_path = config.RESULT_JSON_ROOT
    res_dirs = os.listdir(result_path)
    dir_paths = [os.path.join(result_path, name) for name in res_dirs]

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
        st.warning(f"Ve složce `{selected_dir}` nebyly nalezeny žádné soubory (obsahující \"{filter_text}\")")
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