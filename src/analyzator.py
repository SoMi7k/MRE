import re
from scripts import config as cf

"""
    Výsledná analýza původního textu
    
    --- Metriky sekcí ---
    Sekce: []
    Počet sekcí: ?
    Průměrný počet znaků na sekci: ?
    Průměrný počet vět na sekci: ?

    --- Slovní metriky ---
    Latinské slova: []
    Počet latinských slov: ?
    # Klíčová slova: []
    # Počet klíčových slov: ?

    --- Větné metriky ---
    Počet vět: ?
    Průměrná délka věty: ?
    Počet znaků: ?
    Počet vět mimo sekce: ?
    Počet znaků mimo sekce: ?
"""


"""
    Porovnávací soubor

    --- Sémantické metriky ---
    Sémantická úplnost (semantic recall): ?
    Sémantická přesnost (semantic precision): ?
    Počet sémantických halucinací: ?
    Podíl sémantických halucinací (%): ?

    --- Struktura významu ---
    Sémantická věrnost struktury: správná / částečně / špatná
    Sémantická modifikace (semantic shift): ?
"""

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


def count_words(text: str, arr: list[str]):
    words = re.findall(r'\w+', text)
    found = [w for w in words if w in arr]
    return found, len(found)


def detect_sections(text):
    """
    Detekuje sekce na základě seznamu klíčových názvů sekcí (section_keywords).

    - section_keywords = cf.SECTION (list řetězců)
    - Sekce začíná, pokud řádek (bez mezer) obsahuje některý z názvů.
    - Sekce pokračuje, dokud nenarazíme na další klíč sekce.
    """

    lines = text.split("\n")
    sections = []

    current_name = None
    current_content = []

    def save_current():
        if current_name is not None:
            # Očistit obsah od prázdných řádků na okrajích
            content = "\n".join(current_content).strip()
            sections.append((current_name, content))

    normalized_keys = [k for k in cf.SECTION]

    for line in lines:
        stripped = line.strip(" ")

        # Je toto nový začátek sekce?
        if stripped in normalized_keys:
            # Uložit předchozí sekci
            save_current()

            # Začít novou sekci
            current_name = stripped  # původní text názvu sekce
            current_content = []
        else:
            # Obsah sekce
            if current_name is not None:
                current_content.append(stripped)

    # poslední sekce
    save_current()

    return sections


def count_chars(text):
    return len(text)


# --- Hlavní funkce ---

def analyze_text(input_text, output_file):
    # Věty
    sentences = split_into_sentences(input_text)
    num_sentences = len(sentences)
    avg_sentence_len = sum(len(s) for s in sentences) / num_sentences if num_sentences else 0
    char_count = count_chars(input_text)

    # Sekce
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

    # --- Věty a znaky mimo sekce ---
    text_in_sections = "\n\n".join(s[1] for s in sections)
    text_outside_sections = input_text.replace(text_in_sections, "")
    out_sentences = split_into_sentences(text_outside_sections)
    out_chars = len(text_outside_sections)

    # --- Zápis do TXT ---
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"""
    Výsledná analýza původního textu

    --- Metriky sekcí ---
    Sekce: {[name for name, _ in sections]}
    Počet sekcí: {num_sections}
    Průměrný počet znaků na sekci: {avg_chars_per_section:.2f}
    Průměrný počet vět na sekci: {avg_sent_per_section:.2f}

    --- Slovní metriky ---
    Anatomické názvy: {anatomy_found}
    Počet anatomických slov: {anatomy_count}

    Diagnózy: {diagnosis_found}
    Počet diagnóz: {diagnosis_count}

    Klíčová slova: {keywords_found}
    Počet klíčových slov: {keywords_count}

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


    --- Větné metriky ---
    Počet vět: {num_sentences}
    Průměrná délka věty: {avg_sentence_len:.2f}
    Počet znaků: {char_count}
    Počet vět mimo sekce: {len(out_sentences)}
    Počet znaků mimo sekce: {out_chars}
    """)

    return output_file
