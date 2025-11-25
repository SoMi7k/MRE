### Konvence pojmenování výstupních souborů

**Formát:** `<llm>_<datum>_<report>_<task>.md`

**Komponenty:**

- `<llm>` - název použitého LLM modelu (např. `claude`, `gpt4`, `gemini`)
- `<datum>` - datum ve formátu `DD-MM-YY`
- `<report>` - identifikátor lékařské zprávy (např. `r01`)
- `<task>` - identifikátor úlohy/instrukce (např. `t02`)

**Příklady:**

- `Claude_261024_r01_t02.json`
- `GPT_261024_r03_t01.json`

**Pravidla:**

- Datum předchází identifikátorům pro lepší chronologické řazení
- Používejte konzistentní formát data napříč všemi soubory
- Čísla reportů a tasků s vedoucími nulami pro správné řazení
