import re
import os

DATA_ROOT = "data"
CSV_DATA_ROOT = os.path.join(DATA_ROOT, "csv")
JSON_DATA_ROOT = os.path.join(DATA_ROOT, "json")
TXT_DATA_ROOT = os.path.join(DATA_ROOT, "txt")

PROMPT_ROOT = os.path.join(DATA_ROOT, "prompts")
REPORTS_ROOT = os.path.join(DATA_ROOT, "medical_reports")
TASKS_ROOT = os.path.join(DATA_ROOT, "tasks")

RESULT_ROOT = "results"
RESULT_JSON_ROOT = os.path.join(RESULT_ROOT, "json")
RESULT_MD_ROOT = os.path.join(RESULT_ROOT, "md")
RESULT_TXT = os.path.join(RESULT_ROOT, "txt")

REGEX = re.compile(r'\w|[ěščřžýáíéúůó]|[+-]')

ANATOMY = "data/txt/Anatomicke_nazvy.txt"
DIAGNOSIS = "data/txt/Diagnozy.txt"
KEY_WORDS = "data/txt/Klicove_slova.txt"
KPPS = "data/txt/KPPS.txt"
LATIN = "data/txt/Latinske_nazvy.txt"
MEDICAMENTS = "data/txt/Leky.txt"
MICROBIOLOGY = "data/txt/Mikrobiologie.txt"
PROCEDURES = "data/txt/Procedury_Terapie.txt"
SECTION = "data/txt/Sekce.txt"

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

TITLES_STROKE = [
    'CT mozku: s k.l. iv.', 
    'CT mozku: bez k.l.', 
    'CT vyšetření', 
    'CT AG'
]

