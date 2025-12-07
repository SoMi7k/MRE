import streamlit as st
import scripts.config as config
import os
import json
import pandas as pd

csv_dir = config.CSV_DATA_ROOT
json_dir = config.JSON_DATA_ROOT
report_dir = config.REPORTS_ROOT
tasks_dir = config.TASKS_ROOT
prompt_dir = config.PROMPT_ROOT

dirs = [csv_dir, json_dir, report_dir, tasks_dir, prompt_dir]

def show():
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