import os
import json
import streamlit as st
from scripts import config
import src.analyzator as analyzator
import src.analyzatorJson as analyzatorJson

report_dir = config.REPORTS_ROOT
result_dir = config.RESULT_TXT
result_json_path = config.RESULT_JSON_ROOT
data = ""

def show():
    st.title("🔍 Anylazator")

    st.markdown("### Analýza lékařské zprávy")
    st.markdown("Zadejte cestu k textovému souboru se vstupem:")

    if os.path.exists(report_dir):
        an_files = [
            f for f in os.listdir(report_dir)
            if os.path.isfile(os.path.join(report_dir, f))
        ]

    input_path = st.selectbox("Medical report input", an_files, index=None,
        placeholder="Choose a report file:",)

    if st.button("Validate1", type="primary") and input_path:
        report_path = os.path.join(report_dir, input_path)
        outpath = os.path.join(result_dir, input_path)

        with open(report_path, "r", encoding="utf-8") as f:
            text = f.read()

        if analyzator.analyze_text(text, outpath):
            st.success(f"\nHotovo! Výsledek uložen do: {outpath}")
        
    st.markdown("---")
    
    st.markdown("### Analýza JSON výstupu z LLM")
    st.markdown("Zadejte cestu k textovému souboru se vstupem:")
    
    result_path = config.RESULT_JSON_ROOT
    res_dirs = os.listdir(result_path)
    dir_paths = [os.path.join(result_path, name) for name in res_dirs]

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
        data = ""
        if st.button("Validate2", type="primary"):
            path = os.path.join(selected_dir, selected_file)
            try:
                # JSON
                if selected_file.endswith(".json"):
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        #data = json.dumps(loaded, ensure_ascii=False)
                        st.write(data)
                # Jiný formát
                else:
                    st.warning(f"Soubor `{selected_file}` má nepodporovaný formát.")
            except Exception as e:
                st.error(f"Chyba při čtení souboru: {e}")
                
        if data:
            outpath = os.path.join(result_dir, selected_file).replace(".json", ".txt")
            if analyzatorJson.analyzeJson(data, outpath):
                st.success(f"\nHotovo! Výsledek uložen jako: {outpath}")
            else:
                st.error(f"Error while analyzing {outpath}")