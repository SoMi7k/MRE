import re
import os
#from features import env

"""Project configuration constants for data paths, labels, and model lists."""

# API KEY
# API_KEY = env.API_keys("OPENROUTER_API_KEY").get_api_key()

# Data roots
DATA_ROOT = "data"
CSV_DATA_ROOT = os.path.join(DATA_ROOT, "csv")
JSON_DATA_ROOT = os.path.join(DATA_ROOT, "json")
DOCCANO_DATA_ROOT = os.path.join(DATA_ROOT, "doccano")
PROMPT_ROOT = os.path.join(DATA_ROOT, "inputs")
REPORTS_ROOT = os.path.join(DATA_ROOT, "medical_reports")
TASKS_ROOT = os.path.join(DATA_ROOT, "task")

# Result roots
RESULT_ROOT = "results"
RESULT_JSON_ROOT = os.path.join(RESULT_ROOT, "json")
RESULT_MD_ROOT = os.path.join(RESULT_ROOT, "md")
RESULT_TXT = os.path.join(RESULT_ROOT, "txt")

# Basic regex
REGEX = re.compile(r'\w|[ěščřžýáíéúůó]|[+-]')

# Anotated words roots
ANATOMY = os.path.join(DOCCANO_DATA_ROOT, "Anatomicke_nazvy.txt")
DIAGNOSIS = os.path.join(DOCCANO_DATA_ROOT, "Diagnozy.txt")
KEY_WORDS = os.path.join(DOCCANO_DATA_ROOT, "Klicove_slova.txt")
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
    "openai/gpt-5-chat",
    "google/gemini-3-pro-preview",
    "x-ai/grok-4",
    "mistralai/mixtral-8x7b-instruct",
    "openrouter/free"
]

# Table for output folders names
LLMS_REVERSED = {
    "OpenRouter": "openrouter/free",
    "Claude": "anthropic/claude-sonnet-4.5", 
    "GPT": "openai/gpt-5-chat", 
    "Mistral": "mistralai/mixtral-8x7b-instruct", 
    "Gemini": "google/gemini-3-pro-preview", 
    "Llama": "meta-llama/llama-3.2-3b-instruct", 
    "Grok": "x-ai/grok-4", 
    "DeepSeek": "deepseek/deepseek-v3.2"
}

LLMS = {'openrouter/free': 'OpenRouter', 
        'anthropic/claude-sonnet-4.5': 'Claude', 
        'openai/gpt-5-chat': 'GPT', 
        'mistralai/mixtral-8x7b-instruct': 'Mistral', 
        'google/gemini-3-pro-preview': 'Gemini', 
        'meta-llama/llama-3.2-3b-instruct': 'Llama', 
        'x-ai/grok-4': 'Grok', 
        'deepseek/deepseek-v3.2': 'DeepSeek'
}