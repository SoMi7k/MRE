from typing import Any, Dict, Tuple
import scripts.config as cf
import src.halucation_finder as halFinder

def extract_words(text: str) -> int:
    words = text.split()
    return len(words)

def extract_text_stats(value: Any) -> Tuple[int, int]:
    """Vrací (počet_slov, počet_znaků) z libovolné hodnoty."""
    if isinstance(value, str):
        return extract_words(value), len(value)
    return 0, 0

def collect_text_stats(value: Any) -> Tuple[int, int]:
    """
    Rekurzivně projde hodnotu a agreguje slova + znaky ze všech
    string listů a zanořených dict hodnot.
    Používá se pro výpočet stats hlavního klíče.
    """
    if isinstance(value, str):
        return extract_words(value), len(value)
    
    total_words, total_chars = 0, 0
    
    if isinstance(value, dict):
        for v in value.values():
            w, c = collect_text_stats(v)
            total_words += w
            total_chars += c
    elif isinstance(value, list):
        for item in value:
            w, c = collect_text_stats(item)
            total_words += w
            total_chars += c
    
    return total_words, total_chars

def traverse_json(
    data: Any,
    depth: int = 0,
    stats: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    """
    Rekurzivní průchod JSONem.
    depth == 0 → hlavní klíče (kontrola, subjektivně, ...)
    depth > 0 → zanořené klíče
    """
    if stats is None:
        stats = {
            "total_keys": 0,
            "main_keys": 0,
            "nested_keys": 0,

            "key_chars": 0,       # délka všech klíčů
            "value_chars": 0,     # délka všech hodnot (jen stringy)
            "value_words": 0,     # počet slov ve všech hodnotách (jen stringy)
        }

    if isinstance(data, dict):
        for key, value in data.items():
            stats["total_keys"] += 1
            stats["key_chars"] += len(key)

            if depth == 0:
                stats["main_keys"] += 1
                # Agregujeme veškerý text z celé větve
                words, chars = collect_text_stats(value)
                stats["value_chars"] += chars
                stats["value_words"] += words
            else:
                stats["nested_keys"] += 1
                # Jen přímá string hodnota
                words, chars = extract_text_stats(value)
                stats["value_chars"] += chars
                stats["value_words"] += words

            traverse_json(value, depth + 1, stats)

    elif isinstance(data, list):
        for item in data:
            traverse_json(item, depth, stats)

    return stats

def count_words(text: str, theme_root: str):
    with open(theme_root, 'r', encoding='utf-8') as fr:
        # Očistíme každý řádek od mezer, čárek a dalších nežádoucích znaků
        theme_phrases = {
            line.strip().strip(',').lower()
            for line in fr
            if line.strip()
        }

    text_lower = text.lower()

    # Hledáme každou frázi přímo jako podřetězec v textu
    found = {phrase for phrase in theme_phrases if phrase in text_lower}

    return list(found), len(found)


def analyzeJson(input: dict, outpath: str, report_path: str):
    try:
        # Spojení klíčů do jednoho řetězce odděleného mezerou
        str_keys = " ".join(map(str, input.keys()))
        
        # Spojení hodnot do jednoho řetězce odděleného mezerou
        str_values = " ".join(map(str, input.values()))
            
        # --- Klíče ---
        key_stats = traverse_json(input)

        main_keys = key_stats["main_keys"]
        nested_keys = key_stats["nested_keys"]
        
        # --- Anotace slov ---
        section_found, section_count = count_words(str_keys, cf.SECTION)
        anatomy_found, anatomy_count = count_words(str_values, cf.ANATOMY)
        diagnosis_found, diagnosis_count = count_words(str_values, cf.DIAGNOSIS)
        keywords_found, keywords_count = count_words(str_values, cf.KEY_WORDS)
        kpps_found, kpps_count = count_words(str_values, cf.KPPS)
        latin_found, latin_count = count_words(str_values, cf.LATIN)
        medicaments_found, medicaments_count = count_words(str_values, cf.MEDICAMENTS)
        microbiology_found, microbiology_count = count_words(str_values, cf.MICROBIOLOGY)
        procedures_found, procedures_count = count_words(str_values, cf.PROCEDURES)
        
        # --- Halucinace ----
        extra_key_words, extra_value_words = halFinder.compare(input, report_path)

        # --- Zápis do TXT ---
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(f"""\
Výsledná analýza extrahovaného textu:

--- Metriky klíčů ---
Počet klíčů: {key_stats["total_keys"]}
Počet hlavních klíčů: {main_keys}
Počet zanořených klíčů: {nested_keys}

Počet znaků všech klíčů: {key_stats["key_chars"]}
Počet znaků všech slov v hodnotách: {key_stats["value_chars"]}
Počet všech slov v hodnotách: {key_stats["value_words"]}

--- Slovní metriky ---
Sekce: {section_found}
Počet sekcí: {section_count}

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

--- Halucinace ---
Počet vymyšlených klíčových slov: {len(extra_key_words)}
Vymyšlená klíčová slova: {extra_key_words}
Počet vymyšlených slov ve values: {len(extra_value_words)}
Vymyšlená slova ve values: {extra_value_words}
            """)
            
    except Exception as e:
        raise e