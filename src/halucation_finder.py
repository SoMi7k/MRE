from scripts import config
import os
import json
import re

def normalize_word(word: str) -> str:
    """Normalizace slova."""
    return word.lower().strip(",.()[]{};:!?\"'`")


def extract_words_from_text(text: str) -> set[str]:
    """Extrahuje slova z libovolného textu."""
    words = re.findall(r"\b\w+\b", text.lower())
    return set(normalize_word(w) for w in words if w.strip())


def load_report_words(filepath: str) -> set[str]:
    """Načte slova z TXT reportu."""
    with open(filepath, "r", encoding="utf-8") as fr:
        content = fr.read()

    valid_words = extract_words_from_text(content)

    print(f"✅ Načteno {len(valid_words)} unikátních slov z TXT reportu")
    return valid_words


def load_extracted_words(extractpath: str) -> set[str]:
    """Načte slova z JSON extractu."""
    try:
        with open(extractpath, "r", encoding="utf-8") as f:
            loaded = json.load(f)

        # převede celý JSON na string
        json_text = json.dumps(loaded, ensure_ascii=False)

        valid_words = extract_words_from_text(json_text)

        print(f"✅ Načteno {len(valid_words)} unikátních slov z JSON extractu")
        return valid_words

    except Exception as e:
        print(f"❌ Chyba při čtení JSON: {e}")
        return set()


# =========================
# MAIN
# =========================
def compare(): 
    text_path = config.REPORTS_ROOT
    result_path = config.RESULT_JSON_ROOT

    report_id = 78
    filepath = os.path.join(text_path, f"c{report_id}.txt")
    extractpath = os.path.join(result_path, "crohn", "GPT_200226_r78_t4.json")
    
    report_words = load_report_words(filepath)
    extracted_words = load_extracted_words(extractpath)

    # slova navíc v JSON oproti TXT
    extra_words = extracted_words - report_words

    print("\n==============================================")
    print(f"🔍 Nalezeno {len(extra_words)} slov navíc v JSON oproti TXT")
    print("==============================================\n")

    for word in sorted(extra_words):
        print(word)

    # uložit do souboru
    output_path = os.path.join(result_path, f"extra_words_c{report_id}.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        for word in sorted(extra_words):
            f.write(word + "\n")

    print(f"\n💾 Výsledek uložen do: {output_path}")
    
compare()