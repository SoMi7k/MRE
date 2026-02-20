import re
import os

API_KEY = "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/5"

DATA_ROOT = "data"
CSV_DATA_ROOT = os.path.join(DATA_ROOT, "csv")
JSON_DATA_ROOT = os.path.join(DATA_ROOT, "json")
DOCCANO_DATA_ROOT = os.path.join(DATA_ROOT, "doccano")

PROMPT_ROOT = os.path.join(DATA_ROOT, "inputs")
REPORTS_ROOT = os.path.join(DATA_ROOT, "medical_reports")
TASKS_ROOT = os.path.join(DATA_ROOT, "task")

RESULT_ROOT = "results"
RESULT_JSON_ROOT = os.path.join(RESULT_ROOT, "json")
RESULT_MD_ROOT = os.path.join(RESULT_ROOT, "md")
RESULT_TXT = os.path.join(RESULT_ROOT, "txt")

REGEX = re.compile(r'\w|[ěščřžýáíéúůó]|[+-]')

ANATOMY = os.path.join(DOCCANO_DATA_ROOT, "Anatomicke_nazvy.txt")
DIAGNOSIS = os.path.join(DOCCANO_DATA_ROOT, "Diagnozy.txt")
KEY_WORDS = os.path.join(DOCCANO_DATA_ROOT, "Klicove_slova.txt")
KPPS = os.path.join(DOCCANO_DATA_ROOT, "KPPS.txt")
LATIN = os.path.join(DOCCANO_DATA_ROOT, "Latinske_nazvy.txt")
MEDICAMENTS = os.path.join(DOCCANO_DATA_ROOT, "Leky.txt")
MICROBIOLOGY = os.path.join(DOCCANO_DATA_ROOT, "Mikrobiologie.txt")
PROCEDURES = os.path.join(DOCCANO_DATA_ROOT, "Procedury_Terapie.txt")
SECTION = os.path.join(DOCCANO_DATA_ROOT, "Sekce.txt")

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

