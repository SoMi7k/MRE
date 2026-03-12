import re
import os
from features import env

"""Project configuration constants for data paths, labels, and model lists."""

# API KEY
API_KEY = env.API_keys("OPENROUTER_API_KEY").get_api_key()

# Data roots
DATA_ROOT = "data"
CSV_DATA_ROOT = os.path.join(DATA_ROOT, "csv")
JSON_DATA_ROOT = os.path.join(DATA_ROOT, "json")
DOCCANO_DATA_ROOT = os.path.join(DATA_ROOT, "doccano")
PROMPT_ROOT = os.path.join(DATA_ROOT, "inputs")
REPORTS_ROOT = os.path.join(DATA_ROOT, "medical_reports")
TASKS_ROOT = os.path.join(DATA_ROOT, "task")

# Result roots
RESULT_ROOT = "output"
RESULT_JSON_ROOT = os.path.join(RESULT_ROOT, "json")
RESULT_MD_ROOT = os.path.join(RESULT_ROOT, "md")
RESULT_REPORT = os.path.join(RESULT_ROOT, "analyze_reports")
RESULT_LMM = os.path.join(RESULT_ROOT, "analyze_llm")

# Basic regex
REGEX = re.compile(r'\w|[ěščřžýáíéúůó]|[+-]')

# Anotated words roots
ANATOMY = os.path.join(DOCCANO_DATA_ROOT, "Anatomicke_nazvy.txt")
DIAGNOSIS = os.path.join(DOCCANO_DATA_ROOT, "Diagnozy.txt")
KEY_WORDS = os.path.join(DOCCANO_DATA_ROOT, "Casto_vyskytujici_se_slova.txt")
KPPS = os.path.join(DOCCANO_DATA_ROOT, "KPPS.txt")
LATIN = os.path.join(DOCCANO_DATA_ROOT, "Latinske_nazvy.txt")
MEDICAMENTS = os.path.join(DOCCANO_DATA_ROOT, "Leky.txt")
MICROBIOLOGY = os.path.join(DOCCANO_DATA_ROOT, "Mikrobiologie.txt")
PROCEDURES = os.path.join(DOCCANO_DATA_ROOT, "Procedury_Terapie.txt")
SECTION = os.path.join(DOCCANO_DATA_ROOT, "Sekce.txt")

# Titles in report with crohn disease
TITLES_CROHN = [
    "Sono GIT",
    "Sono břicha",
    "Návštěva ambulance / ordinace",
    "Sono břicha, GIT",
    'MR kolene', 'MR enterografie', 
    'Dynamická scinti ledvin 99mTc MAG3', 
    'Esofagogastroduodenoskopické vyš.', 
    'Koloskopické vyš.', 
    'Kapslová enteroskopie', 
    'MR mozku', 
    'MR LS páteře', 
    'MR břicha', 
    'MR pánve', 
    'PET/MR s apl. 18F'
]

# Titles in report with stroke
TITLES_STROKE = [
    'CT mozku: s k.l. iv.', 
    'CT mozku: bez k.l.', 
    'CT vyšetření', 
    'CT AG'
]

# Models use in this project
MODELS = [
    "openrouter/free",
    "anthropic/claude-sonnet-4.5",
    "deepseek/deepseek-v3.2",
    "openai/gpt-5.2",
    "google/gemini-3-flash-preview",
    "x-ai/grok-4",
    "mistralai/mixtral-8x22b-instruct",
    "meta-llama/llama-4-maverick"
]

# Table for output folders names
LLMS = {
    MODELS[0]: 'OpenRouter', 
    MODELS[1]: 'Claude', 
    MODELS[3]: 'GPT', 
    MODELS[6]: 'Mistral', 
    MODELS[4]: 'Gemini', 
    MODELS[7]: 'Llama', 
    MODELS[5]: 'Grok', 
    MODELS[2]: 'DeepSeek'
}