# Zaznamenané výsledky

**Prompt**
- obecný / stručný
- krátký / dlouhý

**Lékařská zpráva**
- Zaměření - Crohn / Mrtvice
- Téma - Návštěva lékaře, s. kl., ...
- dlouhý / krátký

## Popis testovacích scénářů
1) Základní měření
    Prompt - obecný, krátký, český, stejný
    Texty - různě dlouhé (5), Crohn - Návštěva lékaře

### Claude

Klíčové slova anglicky. (1/1)
Nepatrná změna (361/375 - 2)

### Gemini

Klíčové slova česky. (0/1)
Změna nepatrná. (291/310 - 2)

### GPT

Klíčové slova česky. (0/1)
Kratší prompt má daleko více tokenů. (328/269 - 2)

### Grok

Klíčové slova česky. (0/1)
Patrná změna (175/207 - 2)

### Mistral

Klíčové slova anglicky. (1/1)
Beze změny. (290/288 - 2)

### Obecné poznámky

Při delším promptu se více zachovávají celé věty. Při kratších se dělení vět více viditelné.
Rozdíl (Např. Mistral r02.t03/t06):
    "objektivni_nalez": {
        "popis": [
        "zavedena sonda do pravé nostrily",
        "celkový stav dobrý, růžový, přibyl +2 kg",
        "břicho měkké",
        "pigmentované névy na břiše",
        "játra, slezina nezvětšené",
        "zatím bez sekundárních pohlavních znaků",
        "kůže čistá"
        ]
    },

    "objektivni_nalez": {
        "datum": "19.08.2014",
        "popis": [
        "Zavedena sonda do pravé nostrily, celkový stav dobrý, růžový, přibyl +2 kg.",
        "Břicho měkké, pigmentované névy na břiše, játra a slezina nezvětšené, zatím bez sekundárních pohlavních znaků, kůže čistá."
        ]
    },
