import os
import streamlit as st
from scripts import config
from datetime import datetime

def show():
    st.title("📋 Result Maker")
    st.markdown("LLM")

    LLMs = ["Claude", "GPT", "Mistral", "Gemini", "Llama", "Grok", "DeepSeek"]
    sel_LLM = st.selectbox("Choose a LLM model:", LLMs)
    report_number = st.text_input("Č. lékařské zprávy:")
    task_number = st.text_input("Č. tasku:")
    result_text = st.text_area("Zadej výseldek LLM:", placeholder="Sem vlož výsledný json", height=250)

    if st.button("Create result", type="primary"):
        try:
            dirname = config.RESULT_JSON_ROOT
            filename = f"{sel_LLM}_{datetime.now().strftime("%d%m%y")}_r{report_number}_t{task_number}.json"
            report_theme = "crohn"
            outfile = os.path.join(dirname, report_theme, filename)

            # Uložení souboru
            with open(outfile, "w", encoding="utf-8") as fr:
                fr.write(result_text)
                fr.write("\n")

            st.success("✅ Soubory úspěšně vytvořeny!")

        except Exception as e:
            st.error(f"Chyba při ukládání: {e}")