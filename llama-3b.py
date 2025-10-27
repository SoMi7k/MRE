from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_name = "meta-llama/Llama-3.2-3B"

tokenizer = AutoTokenizer.from_pretrained(model_name, token="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")
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto", token="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")

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

prompt = (
    "Pod tímto textem se nachází anonymizovaná lékařská zpráva. "
    "Tvůj úkol je extrahovat daný text a navrátit ho zpět ve formátu markdown. "
    "Snaž se zachovat co nejvíce informací z daného textu. "
    "Nesnaž si domýšlet, přidávat písmena, nebo slova. "
    "Pokud si nejsi jist co dané slovo znamená vynech ho.\n\n"
)

text = """Kontrola, poslední 10.3.2015, t.č. 18 a 1/4 roku - trvaly zánětlivé změny terminálního ilea.
Subjektivně zcela bez potíží.
Břicho nebolí.
Stolice 1-2x denně, formovaná či kašovitá, bez patologické příměsi.
Stravu toleruje.
Nemocný nebyl.
Chodí do školy.
- Léky:
* Imuran 2-0-0 tbl á 50 mg (od 30.9.2014, 1,4 mg/kg) - redukovaná dávka - heterozygot TPMT
- strava: bezezbytková

Obj.: hmotnost 66 (-0,5) kg, výška 178,5 (+0) cm
eutrofický, břicho v úrovni, měkké, nebolestivé, rezistenci spolehlivě nehmatám, v pravé jámě hmatná trvá mírná palpační citlivost, J+S nezvětšeny, exantém 0, otoky 0

Lab.: FW, KO+dif, CRP, alb, kalprotectin
10.6.2015 09:56 - 14:59
Sedimentace: B-FW1: 13
Krevní obraz: B-Le: 6,60 B-Ery: 4,62 B-Trombo: 259 B-Hb: 137 B-HTK: 0,413 B-Obj ery.: 90 B-Hb ery: 29,8 B-Hb konc: 333 B-Seg: 0,742 B-Ly: 0,160 B-Eo: 0,020 B-Ba: 0,009 B-Mo: 0,069 B-Seg - abs: 4,90 B-Ly - abs: 1,10 B-Eo - abs: 0,10 B-Ba - abs: 0,10 B-Mo - abs.: 0,50 B-Erytr.křivka: 16,9
Biochemie: S-CRP: 2 S-Albumin: 51,3
Stolice: K-Kalprotektin: 497

Dg.:
K508 Jiná Crohnova nemoc - terminální ileum, kolon, dg 9/2014 TNF-a neg. (G/G), TPMT heterozygot
I450 Blokáda pravého raménka

Re.: klinicky remise, hmotnostně mírně ubyl, laboratorně nízké zánětlivé parametry, kalprotektin středně zvýšený, PCDAI 0b dle USG (3/2015) přetrvávají zánětlivé změny terminálního ilea

Dop.:
- strava bezezbytková
- Léky:
* navýšit Imuran 2,5-0-0 tbl á 50 mg (1,9 mg/kg, od 30.9.2014)
- kontrola v gastroenterologické poradně DK 21.9.2015 v 11 hod + USG GIT 21.9.2015 v 10:45 hod. (vchod F, 6. patro, tel. 37 710 4679 - Po, St) s sebou vzorek stolice na kalprotektin
- při zhoršení stavu kontrola dříve
- domluva o předání gastroenterologovi pro dospělé

Kopii této zprávy odevzdejte svému dětskému lékaři.

Vystavené recepty:
IMURAN 50 MG por tbl flm 100x50mg, počet balení: 2

Informace o zdravotním stavu a provedených vyšetřeních byly pacientovi poskytnuty a bylo umožněno klást dotazy.
Údaje uvedené ve formuláři Souhlas s poskytováním informací o zdravotním stavu zůstávají beze změny."""

# === Spojený prompt ===
full_prompt = f"{prompt}{text}\n\nOdpověď ve formátu markdown:\n"

result = pipe(full_prompt, max_new_tokens=800, temperature=0.2)

# === Výsledek ===
with open("llama.md", 'w', encoding='utf-8') as wr:
    wr.write(result[0]["generated_text"] + "\n")