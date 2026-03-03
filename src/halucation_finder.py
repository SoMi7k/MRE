import re

def stem_czech_word(word: str) -> str:
    """Velmi jednoduchý český stemmer."""
    
    word = word.lower()

    suffixes = [
        "ami", "emi", "ovi", "ými", "ách", "ata", "aty",
        "ého", "ěmi", "emi", "imu", "ách", "ích",
        "ého", "ému", "ové", "ovi", "ými",
        "ého", "ě", "y", "a", "u", "o", "i", "í"
    ]

    for suffix in sorted(suffixes, key=len, reverse=True):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]

    return word

def normalize_word(word: str) -> str:
    """Normalizace slova."""
    word = word.lower().strip(",.()[]{};:!?\"'`")
    word = stem_czech_word(word)
    return word

def extract_words_from_json(data, key_words: set, value_words: set):
    """Rekurzivně extrahuje slova z JSON keys a values odděleně."""

    if isinstance(data, dict):

        for key, value in data.items():

            # extract words from key
            key_words.update(extract_words_from_text(str(key)))

            # recurse into value
            extract_words_from_json(value, key_words, value_words)

    elif isinstance(data, list):

        for item in data:
            extract_words_from_json(item, key_words, value_words)

    else:
        # primitive type → value
        value_words.update(extract_words_from_text(str(data)))

def extract_words_from_text(text: str) -> set[str]:
    """Extrahuje slova z libovolného textu."""
    words = re.findall(r"\b\w+\b", text.lower().replace("_", " "))
    return set(normalize_word(w) for w in words if w.strip())


def load_report_words(filepath: str) -> set[str]:
    """Načte slova z TXT reportu."""
    with open(filepath, "r", encoding="utf-8") as fr:
        content = fr.read()

    valid_words = extract_words_from_text(content)

    print(f"✅ Načteno {len(valid_words)} unikátních slov z TXT reportu")
    return valid_words

def load_extracted_words(loaded_json: dict) -> tuple[set[str], set[str]]:
    """Načte slova z JSON extractu a rozdělí na keys a values."""

    try:
        key_words: set = set()
        value_words: set = set()

        extract_words_from_json(loaded_json, key_words, value_words)

        print(f"✅ Načteno {len(key_words)} unikátních slov z JSON KEYS")
        print(f"✅ Načteno {len(value_words)} unikátních slov z JSON VALUES")

        return key_words, value_words

    except Exception as e:
        print(f"❌ Chyba při čtení JSON: {e}")
        return set(), set()

# =========================
# MAIN
# =========================
def compare(json_output: dict, report_path: str) -> tuple[list, list]:
    report_words = load_report_words(report_path)
    json_key_words, json_value_words = load_extracted_words(json_output)

    extra_key_words = json_key_words - report_words
    extra_value_words = json_value_words - report_words

    return sorted(extra_key_words), sorted(extra_value_words)

