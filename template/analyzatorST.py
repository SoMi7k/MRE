import os
import json
import streamlit as st
from scripts import config
import src.analyzator as analyzator
import src.analyzatorJson as analyzatorJson
import re

report_dir = config.REPORTS_ROOT
result_path_llm = config.RESULT_LMM
result_path_report = config.RESULT_REPORT
result_json_path = config.RESULT_JSON_ROOT
data = ""

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
        outpath = os.path.join(result_path_report, input_path)

        try:
            with open(report_path, "r", encoding="utf-8") as f:
                text = f.read()

            if analyzator.analyze_text(text, outpath):
                st.success(f"\nHotovo! Výsledek uložen do: {outpath}")
        except Exception as e:
            st.error(f"ERROR while analyzing file {report_path}: {e}")
        
        
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
                # Jiný formát
                else:
                    st.warning(f"Soubor `{selected_file}` má nepodporovaný formát.")
            except Exception as e:
                st.error(f"Chyba při čtení souboru: {e}")
                
        print(data)        
        if data:
            outpath = os.path.join(result_path_llm, selected_file).replace(".json", ".txt")
            try: 
                analyzatorJson.analyzeJson(data, outpath, find_report_path(path))
                st.success(f"\nHotovo! Výsledek uložen jako: {outpath}")
            except Exception as e:
                st.error(f"Error while analyzing {selected_file}: {e}")