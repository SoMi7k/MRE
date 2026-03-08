import re
import unicodedata
from scripts import config as cf

# --- Pomocné funkce ---
def split_into_sentences(text):
    """
    Segmentace vět vhodná pro klinické texty:
    - tečka + mezera + velké písmeno
    - tečka na konci řádku
    - nový řádek
    - oddělovače typu '- ' nebo '* '
    """
    # Nahrazení nových řádků za tečku, pokud na nich věta končí
    line_splits = re.split(r'\n+', text)

    sentences = []
    for part in line_splits:
        part = part.strip()
        if not part:
            continue
        
        # segmentace podle "tečka + velké písmeno"
        segs = re.split(r'(?<=[0-9a-zA-Z])\.(?=\s+[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ])', part)
        for s in segs:
            s = s.strip()
            if s:
                sentences.append(s)
    return sentences


def count_words(text: str, theme_root: str):
    with open(theme_root, 'r', encoding='utf-8') as fr:
        # Očistíme každý řádek od mezer, čárek a dalších nežádoucích znaků
        theme_phrases = {
            line.strip().strip(',').lower()
            for line in fr
            if line.strip()
        }

    print(theme_phrases)

    text_lower = text.lower()

    # Hledáme každou frázi přímo jako podřetězec v textu
    found = {phrase for phrase in theme_phrases if phrase in text_lower}

    return list(found), len(found)


def normalize_section_name(name: str) -> str:
    """Očistí název sekce – lowercase, bez diakritiky, bez dvojtečky."""
    name = name.strip().rstrip(":")
    name = "".join(
        c for c in unicodedata.normalize("NFD", name)
        if unicodedata.category(c) != "Mn"
    )
    return name.lower()


def detect_sections(text):
    sect_tuple = []
    lines = text.splitlines()

    # načtení sekcí
    with open(cf.SECTION, "r", encoding="utf-8") as f:
        sections = [s.strip() for s in f if s.strip()]

    current_name = None
    current_content = []

    def save_current():
        nonlocal current_name, current_content
        if current_name is not None:
            sect_tuple.append(
                (current_name, "\n".join(current_content).strip())
            )

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        found_section = None

        for section in sections:
            # hledáme sekci jen na začátku řádku
            pattern = r'^' + re.escape(section)
            if re.match(pattern, stripped, re.IGNORECASE):
                found_section = section
                break
            
        if found_section:
            # uložíme předchozí sekci
            save_current()

            current_name = found_section
            current_content = []

            # odebereme název sekce z řádku
            rest = re.sub(r'^' + re.escape(found_section) + r'[:\s]*', '', stripped, flags=re.IGNORECASE)
            if rest:
                current_content.append(rest)

        else:
            if current_name is not None:
                current_content.append(stripped)

    save_current()

    return sect_tuple


# --- Hlavní funkce ---
def analyze_text(input_text: str, output_file: str) -> int:
    try: 
        # --- Věty ---
        sentences = split_into_sentences(input_text)
        num_sentences = len(sentences)
        avg_sentence_len = sum(len(s) for s in sentences) / num_sentences if num_sentences else 0
        char_count = len(input_text)

        # --- Sekce ---
        sections = detect_sections(input_text)
        num_sections = len(sections)
        avg_chars_per_section = sum(len(s[1]) for s in sections) / num_sections if num_sections else 0
        avg_sent_per_section = num_sentences / num_sections if num_sections else 0

        # --- Anotace slov ---
        anatomy_found, anatomy_count = count_words(input_text, cf.ANATOMY)
        diagnosis_found, diagnosis_count = count_words(input_text, cf.DIAGNOSIS)
        keywords_found, keywords_count = count_words(input_text, cf.KEY_WORDS)
        kpps_found, kpps_count = count_words(input_text, cf.KPPS)
        latin_found, latin_count = count_words(input_text, cf.LATIN)
        medicaments_found, medicaments_count = count_words(input_text, cf.MEDICAMENTS)
        microbiology_found, microbiology_count = count_words(input_text, cf.MICROBIOLOGY)
        procedures_found, procedures_count = count_words(input_text, cf.PROCEDURES)

        # --- Zápis do TXT ---
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"""\
Výsledná analýza původního textu:

--- Metriky sekcí ---
Sekce: {[name for name, _ in sections]}
Počet sekcí: {num_sections}
Průměrný počet znaků na sekci: {avg_chars_per_section:.2f}
Průměrný počet vět na sekci: {avg_sent_per_section:.2f}

--- Větné metriky ---
Počet vět: {num_sentences}
Průměrná délka věty: {avg_sentence_len:.2f}
Počet znaků: {char_count}

--- Slovní metriky ---
Anatomické názvy: {anatomy_found}
Počet anatomických slov: {anatomy_count}

Diagnózy: {diagnosis_found}
Počet diagnóz: {diagnosis_count}

Často vyskytující se slova: {keywords_found}
Počet často vyskytujích se slov: {keywords_count}

Klinické příznaky a popisy stavů: {kpps_found}
Počet slov KPPS: {kpps_count}

Latinské názvy: {latin_found}
Počet latinských názvů: {latin_count}

Léky: {medicaments_found}
Počet léků: {medicaments_count}

Mikrobiologie: {microbiology_found}
Počet názvů z mikrobiologie: {microbiology_count}

Procedury a terapie: {procedures_found}
Počet procedur a terapií: {procedures_count}

        """)
    except Exception as e:
        print(f"Error while analyzing {output_file}: {e}.")
        return 0

    return 1
