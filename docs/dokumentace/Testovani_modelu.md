### Konvence pojmenování výstupních souborů

**Formát:** `<llm>_<datum>_<report>_<task>.md`

**Komponenty:**
- `<llm>` - název použitého LLM modelu (např. `claude`, `gpt4`, `gemini`)
- `<datum>` - datum ve formátu `YYYY-MM-DD` nebo `DD-MM-YY`
- `<report>` - identifikátor lékařské zprávy (např. `r01`)
- `<task>` - identifikátor úlohy/instrukce (např. `t02`)

**Příklady:**
- `Claude_2024-10-26_r01_t02.md`
- `GPT_2024-10-26_r03_t01.md`

**Pravidla:**
- Datum předchází identifikátorům pro lepší chronologické řazení
- Používejte konzistentní formát data napříč všemi soubory
- Čísla reportů a tasků s vedoucími nulami pro správné řazení

### Poznámky k testování
Při anglické verzi zadání jsou výsledky v angličtině pouze u 2 LLM - Claude, Mistral


### Table of LLM
| Modely   | Počet slov | Přesnost | Smysluplnost entit |  |
|--------- |---|---|---|---|
| ChatGPT  |   |   |   |   |
| Claude   |   |   |   |   |
| Gemini   |   |   |   |   |
| Mistral  |   |   |   |   |
| Llama    |   |   |   |   | 
