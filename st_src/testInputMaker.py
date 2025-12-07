import streamlit as st
import os
import json
import scripts.config as config

prompt_dir = config.PROMPT_ROOT

def show():
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