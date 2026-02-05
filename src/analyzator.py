import re
import unicodedata
from scripts import config as cf

"""
    Výsledná analýza původního textu

    --- Metriky sekcí ---
    Sekce: ['Doporučení', 'subj', 'obj', 'dop', 'FW', 'USG GIT 19.8. 2014SONO GIT', 'RE']
    Počet sekcí: 7
    Průměrný počet znaků na sekci: 539.00
    Průměrný počet vět na sekci: 9.43

    --- Slovní metriky ---
    Anatomické názvy: ['antrum', 'bulbus']
    Počet anatomických slov: 2

    Diagnózy: ['anemie', 'infekty', 'antropometrie', 'neštovic']
    Počet diagnóz: 4

    Klíčová slova: ['kalprotectin', 'EEN', 'Stolice']
    Počet klíčových slov: 3

    Klinické příznaky a popisy stavů: ['afebrilní']
    Počet slov KPPS: 1

    Latinské názvy: ['atenuovanými', 'infiltrace', 'leukopenie']
    Počet latinských názvů: 3

    Léky: ['azathioprimem', 'Modulen']
    Počet léků: 2

    Mikrobiologie: ['antropometrie', 'kreatin', 'alb', 'CRP', 'ferit', 'trf', 'amylázy', 'Fe', 'kalprotectin', 'imunoglobulinů', 'FW']
    Počet názvů z mikrobiologie: 11

    Procedury a terapie: []
    Počet procedur a terapií: 0


    --- Větné metriky ---
    Počet vět: 66
    Průměrná délka věty: 72.52
    Počet znaků: 4945
    Počet vět mimo sekce: 66
    Počet znaků mimo sekce: 4945
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


def count_words(text: str, theme_root: str):
    with open(theme_root, 'r', encoding='utf-8') as fr:
        theme_words = {line.strip() for line in fr}

    words = re.findall(r'\w+', text)
    
    found = {w for w in words if w in theme_words}
    
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
    sections = []
    lines = text.split("\n")

    with open(cf.SECTION, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            sections.append(line)

    current_name = None
    current_content = []
    # Připravíme normalizované klíče
    normalized_keys = [normalize_section_name(k) for k in sections]

    def save_current():
        if current_name is not None:
            content = "\n".join(current_content).strip()
            sect_tuple.append((current_name, content))
    
    for line in lines:
        stripped = line.strip()
    
        # Normalizace řádku pro porovnání
        norm_line = normalize_section_name(stripped)
    
        # Zjištění, zda řádek začíná klíčem
        is_section = False
        for key in normalized_keys:
            if norm_line.startswith(key):
                is_section = key
                break
    
        if is_section:
            # Uložit předchozí sekci
            save_current()
    
            # Uložit jméno sekce ve formě jak je v textu
            current_name = stripped.split(":")[0]  # vezmeme jen název sekce
            current_content = []
    
            # Pokud řádek obsahuje i obsah (např. "FW: 2/")
            after_colon = stripped.split(":", 1)
            if len(after_colon) > 1 and after_colon[1].strip():
                current_content.append(after_colon[1].strip())
    
        else:
            # Obsah sekce
            if current_name is not None:
                current_content.append(stripped)
    
    # Uložit poslední sekci
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
    except Exception as e:
        print(f"Error while analyzing {output_file}: {e}.")
        return 0

    return 1
