import streamlit as st

from template import (
    pipeline,
    dataViewer,
    testInputMaker,
    resultMaker,
    llmOutputs,
    analyzatorST
)

def show():
    # Mainpage
    st.title("Welcome to MRE Project")
    
    st.markdown("""   
        ## Abstract
        
        ...
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## About project

    # MRE

    ## 👤 Author

    **David Wimmer**

    ## 🎓 Bachelor Thesis

    **Utilizing LLM for structured information extraction from medical reports**

    ### 📋 Assignment

    1. Familiarize yourself with the available MRE project data in the context of the task of structured information extraction from medical reports.
    2. Explore current Large Language Models (LLMs) and related natural language processing (NLP) tools.
    3. Propose a detailed methodology for structured information extraction utilizing the selected Large Language Models.
    4. Implement a prototype of the proposed structured information extraction solution.
    5. Evaluate the achieved results of the prototype implementation against the defined validation plan.

    ## 🏫 University

    **University of West Bohemia in Pilsen**  
    **Faculty of Applied Sciences**

    ## ⚙️ License

    No license
    """)

    
######################
#  CONFIGURATE PART  #
######################

st.set_page_config("MRE - Streamlit")

# Inicializace session state
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Home"

# Sidebar navigace
with st.sidebar:
    st.title("📑 Navigace")

    sections = {
        "Home": "home",
        "Data Viewer": "data_viewer",
        "LLM Pipeline": "output_maker",
        "Prompt Maker": "prompt_maker",
        "Result Maker": "result_maker",
        "Results Viewer": "results_viewer",
        "Analyzator": "analyzer"
    }
    
    for section_name in sections.keys():
        if st.button(section_name, use_container_width=True):
            st.session_state.current_section = section_name
            st.rerun()
            
# Zobrazení vybrané sekce
current = st.session_state.current_section   
            
match current:
    case "Home":
        show()
    case "Data Viewer":
        dataViewer.show()
    case "Prompt Maker":
        testInputMaker.show()
    case "Result Maker":
        resultMaker.show()
    case "Results Viewer":
        llmOutputs.show()
    case "LLM Pipeline":
        pipeline.show()
    case "Analyzator":
        analyzatorST.show()

st.markdown("---")

