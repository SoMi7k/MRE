import re
from typing import Any, Dict, Tuple
import scripts.config as cf

"""
    Výsledná analýza extrahovaného textu
    
    --- Metriky klíčů ---
    Počet klíčů: ?
    Počet podklíčů: ?
    Průměrný počet znaků na klíč: ?
    Průměrný počet vět na klíč: ?

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

def split_sentences(text: str) -> list[str]:
    if not text:
        return []
    return re.split(r'(?<=[.!?])\s+', text.strip())

def extract_words(text: str) -> int:
    words = text.split()
    return len(words)

def extract_text_stats(value: Any) -> Tuple[int, int, int]:
    """
    Vrací (počet_vět, počet_znaků) z libovolné hodnoty
    """
    if isinstance(value, str):
        sentences = split_sentences(value)
        words = extract_words(value)
        return len(sentences), words, len(value)

    if isinstance(value, (int, float, bool)):
        text = str(value)
        return len(split_sentences(text)), extract_words(text), len(text)

    return 0, 0, 0

def traverse_json(
    data: Any,
    depth: int = 0,
    stats: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    """
    Rekurzivní průchod JSONem.
    depth == 0 → hlavní klíče
    depth > 0 → zanořené klíče
    """
    if stats is None:
        stats = {
            "total_keys": 0,
            "main_keys": 0,
            "nested_keys": 0,

            "main_sentences": 0,
            "main_chars": 0,

            "main_words": 0,
            "nested_words": 0,

            "nested_sentences": 0,
            "nested_chars": 0,
        }

    if isinstance(data, dict):
        for _, value in data.items():
            stats["total_keys"] += 1

            sent, words, chars = extract_text_stats(value)

            if depth == 0:
                stats["main_keys"] += 1
                stats["main_sentences"] += sent
                stats["main_chars"] += chars
                stats["main_words"] += words
            else:
                stats["nested_keys"] += 1
                stats["nested_sentences"] += sent
                stats["nested_chars"] += chars
                stats["nested_words"] += words

            traverse_json(value, depth + 1, stats)

    elif isinstance(data, list):
        for item in data:
            traverse_json(item, depth, stats)

    return stats

def count_words(text: str, theme_root: str):
    with open(theme_root, 'r', encoding='utf-8') as fr:
        theme_words = {line.strip() for line in fr}

    words = re.findall(r'\w+', text)
    
    found = {w for w in words if w in theme_words}
    
    return list(found), len(found)


def analyzeJson(input: dict, outpath: str):
    try:
        # Spojení klíčů do jednoho řetězce odděleného mezerou
        str_keys = " ".join(map(str, input.keys()))
        
        # Spojení hodnot do jednoho řetězce odděleného mezerou
        str_values = " ".join(map(str, input.values()))
            
        # --- Klíče ---
        key_stats = traverse_json(input)

        main_keys = key_stats["main_keys"]
        nested_keys = key_stats["nested_keys"]

        avg_sent_main = (
            key_stats["main_sentences"] / main_keys
            if main_keys else 0
        )

        avg_sent_nested = (
            key_stats["nested_sentences"] / nested_keys
            if nested_keys else 0
        )
        
        avg_words_main = (
            key_stats["main_words"] / main_keys
            if main_keys else 0
        )
        
        avg_words_nested = (
            key_stats["nested_words"] / nested_keys
            if nested_keys else 0
        )
                
        avg_chars_main = (
            key_stats["main_chars"] / main_keys
            if main_keys else 0
        )

        avg_chars_nested = (
            key_stats["nested_chars"] / nested_keys
            if nested_keys else 0
        )
        
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

        # --- Zápis do TXT ---
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(f"""
                    Výsledná analýza původního textu

                    --- Metriky klíčů ---
                    Počet klíčů: {key_stats["total_keys"]}
                    Počet hlavních klíčů: {main_keys}
                    Počet podklíčů: {nested_keys}
                    
                    Průměrný počet vět na hlavní klíč: {avg_sent_main:.2f}
                    Průměrný počet vět na zanořený klíč: {avg_sent_nested:.2f}

                    Průměrný počet slov na hlavní klíč: {avg_words_main:.2f}
                    Průměrný počet slov na zanořený klíč: {avg_words_nested:.2f}

                    Průměrný počet znaků na hlavní klíč: {avg_chars_main:.2f}
                    Průměrný počet znaků na zanořený klíč: {avg_chars_nested:.2f}

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
                """)
            
    except Exception as e:
        print(f"Error while analyzing {outpath}: {e}.")
        return 0

    return 1

    