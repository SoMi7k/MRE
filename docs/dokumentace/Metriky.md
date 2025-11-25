# **Metriky pro hodnocení extrakce LLM**

---

## Dimenze testování

* Porovnání metrik mezi modely
* Konzistence
* Cizí jazyk
* Různé typy promtování

---

### Metriky pro rozdělení kvality výstupů

* Úplnost extrakce
* Přesnost extrakce

### Úplnost extrakce

Počet skutečných položek v textu vs. počet model extrahoval.

* Kolik slov daný model extrahuje?
* Odpovídá počet sekcí?

Metriky:

* počet sekcí / počet extrahovaných sekcí
* počet původních znaků / počet výsledných znaků

#### Míra komprese informací

* Pokud je daná extrakce dlouhá, obsahuje více informací, nebo je pouze rozdělená na více slov?

Metriky:

* průměrná délka extrahované věty
* počet vět na jednu položku
* počet sloučených / rozdělených vět

Měřitelné pomocí počtu teček.

### Přesnost extrakce

* Je extrahovaný chybně interpretovaný? Např. („břicho měkké“ → „mäkké bolesti“)
* Dolšo ke zkreslení významu? („břicho měkké“ → „...“)
* Vyskytují se změny formulace?

#### Halucinace

* Přidává model informace, které v textu nejsou?

Metriky:

* počet halucinací / počtem celkových slov

#### Citlivost na lékařské termíny

* Jsou v extrakci důležité slova? (Potřeba anotace důležitých slov)
* Přejmenovává latinské/lékařské pojmy na české a opačně? (např. „slezina nezvětšená“ → extrahováno jako „splenomegalie“)

Příklad entit pro CrN:
(CRP, kolon, ileum, recidiva, kortikoidy, azathioprin...)

#### Zabarvení textu

* „Změkčuje“ či „dramatizuje“ model popis?
* Přidávání emočních hodnotících výrazů („celkově špatný stav“)

Metriky:

* správné / lehce zkreslené / nesprávné

### Shoda se strukturou / formátem

* Je dodržena struktura pokud zadám/nezadám výslovně JSON formát?
* Je struktura chybná, potřebuje opravy?
* Jakou kvalitu bude mít extrakce pči vstupu s předem definovanou strukturou?
* Při zadaném formátu je změněna dabá struktura?

Metriky:

* Slovní hodnocení

---

## **Různé směry testování**

* Prompting v jiném jazyce
* Konzistence
* Různé typy promtování

### Prompting v jiném jazyce

* Změní se výsledek v ostatních metrikách při zvolení jiného jazyku na promptování?

Měřené části textu:

* jazyk klíčů (CZ/EN)
* jazyk hodnot (CZ/EN)
* míra míchání jazyků (počet výskytů EN v CZ textu)

Metriky:

* učinnější / stejné / neúčinné
* závisí / nezávisí na jazyku

### Konzistence

* Bude při opakování stejných dat jiný výsledek?

Metriky:

* rozdíl v počtu tokenů
* změny ve slovních spojeních

### Různé typy promtování

* Jaký vliv má délka promptu na výsledek?
* Jak se změní výstup při různých typech promptů?

Typy promptů:

* krátký prompt
* dlouhý prompt
* obfuskovaný prompt („udělej to stručně“)
* reverzní instrukce („neshrnuj, pouze extrahuj“)

Metriky:

* Slovní popis
* změna v počtu položek / změna struktury
