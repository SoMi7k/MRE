import re

DATA_ROOT = "data"
CSV_DATA_ROOT = "data\\csv"
JSON_DATA_ROOT = "data\\json"

PROMPT_ROOT = "data\\prompts"
REPORTS_ROOT = "data\\medical_reports"
TASKS_ROOT = "data\\tasks"

RESULT_ROOT = "results"
RESULT_JSON_ROOT = "results\\json"
RESULT_MD_ROOT = "results\\md"

REGEX = re.compile(r'\w|[ěščřžýáíéúůó]|[+-]')

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

