import pandas as pd
import os
import streamlit as st
import src.API as API
import json
import features.env as ft
import src.data as dt

selected_LLM = None
API_key = ft.API_keys(None)

# Sidebar
with st.sidebar:
    LLM_list = ["Claude-Sonnet-3.7", "gpt-4.1", "Mistral-7B", "Gemini", "BioGPT", "ClinicalBERT", "Czert-B"]
    selected_LLM = st.selectbox("Choose a LLM model:", LLM_list)

if selected_LLM:
    API_key = ft.API_keys(dt.LLM_keys[selected_LLM])

# Mainpage
st.title("Welcome to MRE Project")

data_dir = "data/"
files = os.listdir(data_dir)

if files:
    selected_file = st.selectbox("Choose a file to view:", files)

if st.button("View data", type="primary"):
    if selected_file:
        path = os.path.join(data_dir, selected_file)
        if ".json" in selected_file:
            with open("data/structure.json", "r", encoding="utf-8") as f:
                df = json.load(f)
        else:
            df = pd.read_csv(path)
        st.write(f"### Showing: `{selected_file}`")
        st.dataframe(df)
    else:
        st.warning("No files found in the data folder.")

#prompt = st.text_input("")
#st.write("Prompt: ", prompt)

text = "data/text.txt"
prompt = """
        Jsi asistent, který extrahuje informace ze vstupního textu a převádí je do přesného JSON formátu. 
        Použij pouze informace uvedené ve vstupu. Pokud něco chybí, použij hodnotu null.
        Výstup vrať přesně jako validní JSON, bez komentářů nebo vysvětlení.
        """

json_root = "data/structure.json"
with open(json_root, "r", encoding="utf-8") as f:
    json_file = json.load(f)

with open(text, mode="r", encoding="utf-8") as fr:
    text = fr.read()
        

Idata = dt.InputData(text, prompt, json_file)

st.markdown("---")

if st.button("Call LLM", type="primary"):
    gen = API.Generator(None)
    match selected_LLM:
        case "gpt-4.1":
            gen.set_new_model(API.openAI(Idata, API_key))
        case "Claude-Sonnet-3.7":
            gen.set_new_model(API.Claude(Idata, API_key))
        case "Mistral-7B":
            gen.set_new_model(API.Mistral(Idata, API_key))
        case "Gemini":
            gen.set_new_model(API.Gemini(Idata, API_key))
        case "ClinicalBERT":
            gen.set_new_model(API.ClinicalBERT(Idata, API_key))
        case "BioGPT":
            gen.set_new_model(API.BioGPT(Idata, API_key))
            
    gen.get_model().generate()
    st.markdown("**:green-background[All done]**")
    #gen.get_model().printer()

st.markdown("---")

if st.button("Show results", type="primary"):
    full_prompt = f"{prompt}\n\n{json_file}"
    st.write(full_prompt)





