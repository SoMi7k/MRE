import os
import streamlit as st
from scripts import config
import src.analyzator as analyzator

report_dir = config.REPORTS_ROOT
result_dir = config.RESULT_TXT

def show():
    st.title("🔍 Anylazator")

    st.markdown("Zadejte cestu k textovému souboru se vstupem:")

    if os.path.exists(report_dir):
        an_files = [
            f for f in os.listdir(report_dir)
            if os.path.isfile(os.path.join(report_dir, f))
        ]

    input_path = st.selectbox("Medical report input", an_files, index=None,
        placeholder="Choose a report file:",)

    if input_path:
        report_path = os.path.join(report_dir, input_path)
        outpath = os.path.join(result_dir, input_path)

        with open(report_path, "r", encoding="utf-8") as f:
            text = f.read()

        output = analyzator.analyze_text(text, outpath)
        st.success(f"\nHotovo! Výsledek uložen do: {output}")