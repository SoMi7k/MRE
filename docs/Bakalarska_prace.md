# Dokumentace

Tato dokumentace obsahuje kompletní technickou dokumentaci a doplňující materiály k projektu MRE.¨

# Abstrakt

# Motivace

Růst umělé inteligence v posledních letech nabírá značného tempa a její využití se postupně rozšiřuje do většiny oborů lidské činnosti. Jednou z klíčových oblastí umělé inteligence je zpracování přirozeného jazyka (NLP –  *Natural Language Processing*), jehož cílem je analýza, porozumění a generování textu či mluveného slova. Významným milníkem v této oblasti se staly velké jazykové modely (LLM –  *Large Language Models*), které vykazují schopnost pracovat s komplexními a nestrukturovanými daty.

Zdravotnictví představuje oblast s enormním množstvím textových dat, zejména ve formě lékařských zpráv, nálezů a klinických záznamů. Tyto dokumenty obsahují cenné informace o zdravotním stavu pacientů, průběhu onemocnění, provedených vyšetřeních a zvolené léčbě. Většina těchto dat je však uložena v nestrukturované podobě, což výrazně komplikuje jejich další zpracování, analýzu a využití pro výzkumné či klinické účely.

Automatická extrakce str ukturovaných informací z lékařských textů by mohla výrazně snížit časovou i administrativní zátěž zdravotnického personálu a zároveň umožnit efektivnější práci s daty. Přestože jsou velké jazykové modely slibným nástrojem pro tento účel, jejich použití na reálných lékařských zprávách zatím není dostatečně prozkoumáno, zejména z hlediska spolehlivosti, konzistence výstupů a etických aspektů.

Další výzvu představuje ochrana citlivých osobních údajů pacientů. Legislativní požadavky, jako je nařízení GDPR, kladou důraz na anonymizaci dat a bezpečné nakládání s informacemi, což omezuje přímé využití moderních jazykových modelů v klinickém prostředí.

Motivací této práce je proto přispět k lepšímu porozumění možnostem využití velkých jazykových modelů při extrakci strukturovaných informací z anonymizovaných lékařských zpráv a porovnat jejich chování napříč různými modely v kontextu reálných zdravotnických dat.

# Obsah

**1. Úvod**

**2. Umělá inteligence a její využití ve zdravotnictví**
	2.1 Umělé inteligence
	2.2 Zpracování přirozeného jazyka
	2.3 AI ve zdravotnictví

**3. Data projektu MRE**
	3.1 Téma lékařských zpráv
	3.2 Struktura a anonymizace
	3.3 Testovací data

**4. Návrh řešení**
	4.1 Celkový koncept
	4.2 Volba modelů

**5. Implementace prototypu**
	5.1 Prostředí a nástroje
	5.2 Projekt MRE
	5.3 Promtování

**6. Experimenty a vyhodnocení**
	6.1 Statistické vyhodnocení
	6.2 Výsledky: tabulky, grafy, příklady
	6.3 Chybná rozhodnutí a analýza chyb (error analysis), případné příčiny a návrhy na zlepšení

**7. Závěr**
	7.1 Shrnutí přínosu práce
   	7.2 Odpovědi na výzkumné otázky
	7.3 Doporučení pro budoucí práci

**Literatura (Zdroje)**
(Ukázky - např. ukázka z dat)
Seznam obrázků
Seznam výpisů
Tabulky

# 1. Úvod

České zdravotnictví se v současnosti potýká s výzvami spojenými s digitalizací nově vznikajících i historicky papírově archivovaných dat. Jejich objem v důsledku modernizace a rozvoje nových technologií rychle narůstá. Tento trend přináší významnou přidanou hodnotu jak pro současné, tak i budoucí pacienty. Rozmach metod umělé inteligence, zejména velkých jazykových modelů v oblasti zpracování přirozeného jazyka (NLP), poskytuje zdravotnickému personálu i vědcům nové nástroje, které mohou významně přispět k efektivnější práci a otevřít prostor pro nové příležitosti.

Data představují základní stavební kámen pro vývoj, zlepšování a udržování aktuálnosti velkých jazykových modelů. Lékařské zprávy však v porovnání s jinými typy dat narážejí na specifické překážky, a to zejména v oblasti zajištění anonymity a v souladu s evropským nařízením GDPR. V této práci jsou proto všechna použitá data plně anonymizována a jejich obsah je využíván pouze v nezbytném rozsahu.

Hlavním cílem práce je prověřit možnosti současných generativních AI nástrojů pro zpracování volného textu lékařských zpráv a ověřit jejich schopnost extrahovat významné informace do strukturované podoby. Zároveň je snahou posoudit, do jaké míry lze tyto nástroje využít v českém zdravotnickém prostředí, kde jazyková i doménová specifika představují významnou překážku.

Data využitá v této práci tvoří popisné zprávy k CT snímkům pacientů s diagnózou mrtvice a Crohnovy choroby. Zprávy pocházejí z Fakultní nemocnice Plzeň a jsou psány výhradně v českém jazyce. Texty přirozeně obsahují překlepy, odborný žargon, zkratky a další prvky, které mohou komplikovat jejich automatické zpracování.

Většina dosavadních výzkumů v oblasti zpracování lékařských zpráv se soustředí především na anglický jazyk. Čeština se však vyznačuje výraznou morfologickou složitostí a četným výskytem výjimek, zkratek a česko-anglických kombinací. Tato práce se proto zaměřuje na zjištění, zda jsou vybrané modely schopné tyto překážky překonat a nabídnout relevantní a prakticky využitelné výsledky.

# 2. Umělá inteligence a její využití ve zdravotnictví

## 2.1 Umělá inteligence

Umělá inteligence patří mezi nejrychleji se rozvíjející oblasti moderní informatiky. Její rozvoj je často přirovnáván k nástupu osobních počítačů na počátku 80. let, například uvedení počítače IBM PC společností IBM v roce 1981. Umělá inteligence je definována jako „věda a inženýrství zabývající se tvorbou inteligentních strojů“ [1]. Výrazný rozvoj AI je úzce spjat s postupující digitalizací společnosti a s výrazným zlepšením výpočetního výkonu hardwaru, který dnes umožňuje efektivní zpracování velmi rozsáhlých objemů dat.

Současné systémy umělé inteligence jsou schopny řešit úlohy v oblastech vizuálního vnímání, rozpoznávání řeči, plánování, rozhodování či strojového překladu mezi přirozenými jazyky [2].

### 2.1.1 Strojové učení

Jednou z klíčových součástí umělé inteligence je strojové učení (angl.  *Machine Learning,* ML). Strojové učení se zaměřuje na vývoj algoritmů, které umožňují modelům získávat znalosti z dat a zlepšovat své chování bez nutnosti explicitního programování. Zvolený způsob učení má zásadní vliv na výslednou kvalitu modelu.

Základními přístupy ke strojovému učení jsou:

* učení s učitelem (*supervised learning*),
* učení bez učitele (*unsupervised learning*),
* učení posilováním (*reinforcement learning*).

V rámci strojového učení existuje celá řada modelů založených na různých principech. V posledních letech však výrazně dominují modely založené na umělých neuronových sítích. Na tomto základě vznikl podobor strojového učení označovaný jako **hluboké učení** (angl.  *Deep Learning*, DL), který se zaměřuje na trénování neuronových sítí s větším počtem vrstev.

Hluboké učení umožňuje počítačovým systémům automaticky extrahovat hierarchické reprezentace dat a efektivně zpracovávat komplexní informace. Modely využívající hluboké učení jsou tvořeny více vrstvami neuronů, přičemž jednotlivé vrstvy postupně zachycují stále abstraktnější rysy vstupních dat. Z technického hlediska se hluboké učení zabývá algoritmy optimalizujícími proces učení neuronových sítí tak, aby byla minimalizována chyba modelu. Mezi klíčové prvky patří aktivační funkce, ztrátové funkce, algoritmus zpětného šíření chyby ( *backpropagation* ) a optimalizační algoritmy.

Metody hlubokého učení se uplatňují v celé řadě oblastí, například v automobilovém průmyslu, financích, zdravotnictví, výrobě či mediálním průmyslu.

S hlubokým učením jsou však spojeny i významné výzvy. Modely vyžadují velké množství kvalitních trénovacích dat a jejich trénování je často výpočetně náročné, což vede k vysoké spotřebě elektrické energie. Dalším problémem je omezená interpretovatelnost modelů, které jsou často označovány jako tzv. „černé skříňky“, jelikož vnitřní rozhodovací procesy nejsou snadno vysvětlitelné. V důsledku toho mohou v modelech vznikat systematické chyby nebo nežádoucí šum. Vytvoření kvalitního modelu hlubokého učení proto vyžaduje pečlivý návrh, odborné znalosti a dostatečné výpočetní zdroje [4].

### 2.1.2 Neuronové sítě

Umělé neuronové sítě (angl.  *Artificial Neural Networks* , ANN) představují matematické modely inspirované fungováním biologických neuronových sítí. Jejich cílem je simulovat základní principy přenosu a zpracování informací v lidském mozku [3]. Díky těmto vlastnostem nacházejí neuronové sítě uplatnění například v robotice, počítačovém vidění nebo zpracování přirozeného jazyka.

Existuje celá řada modelů neuronových sítí, od velmi jednoduchých struktur založených na perceptronech až po složité biologicky motivované modely, které detailně popisují chování jednotlivých neuronů. Příkladem takového modelu je Hindmarshův–Roseův model neuronu. Mezi historicky významné modely patří také neuronový model navržený McCullochem a Pittsem[5], který lze popsat vztahem

$$
y = f(\sum_{i=1}^{N}(w_ix_i) - v)
$$

kde

- **$x_i$** jsou vstupy neuronu,
- **$w_i$** jsou synaptické váhy,
- **$v$** označuje bias neboli práh neuronu,
- **$f$** je aktivační funkce,
- **$y$** je výstup neuronu

Jednotlivé neurony jsou v neuronové síti organizovány do vrstev, které společně tvoří celkovou architekturu modelu. Typická neuronová síť se skládá ze vstupní vrstvy, jedné nebo více skrytých vrstev a výstupní vrstvy. Vstupní vrstva přijímá data, skryté vrstvy zajišťují jejich postupné zpracování a výstupní vrstva poskytuje výslednou predikci modelu. Počet vrstev a neuronů v jednotlivých vrstvách má zásadní vliv na schopnost sítě modelovat složité vztahy v datech.[6]

Zdroje:

1. McCarthy, [2007](https://asistdl.onlinelibrary.wiley.com/doi/full/10.1002/pra2.487?casa_token=KE9z5oyV4o4AAAAA%3ABR-7D6IyD68FLHLj1bftCxdEYxVKqpLFDg75KOj3aiE7-vlXuXTXtfWXkt3PfvYH6apmDQcft6Gjias#pra2487-bib-0022), p.2
2. SAP. *What is Artificial Intelligence? AI in Business* [online]. [cit. 2025-01-24]. Dostupné z: [https://www.sap.com/uk/products/artificial-intelligence/what-is-artificial-intelligence.html](https://www.sap.com/uk/products/artificial-intelligence/what-is-artificial-intelligence.html)
3. FORMÁNEK, Ivo; FARANA, Radim. ARTIFICIAL INTELLIGENCE–ARTIFICIAL NEURAL NETWORKS UMĚLÁ INTELIGENCE–UMĚLÉ NEURONOVÉ SÍTĚ.  *VŠPP Enterpreneurship studies* , 24.
4. SAP. What is Deep Learning? *AI in Business *[online]. [cit. 2025-6-11]. Dostupné z: [https://www.sap.com/resources/what-is-deep-learning]()
5. MCCULLOCH, Warren S.; PITTS, Walter. A logical calculus of the ideas immanent in nervous activity.  *The bulletin of mathematical biophysics* , 1943, 5.4: 115-133
6. HORKÝ, Ladislav; BŘINDA, Karel. Neuronové sítě. 2009

## 2. Zpracování přirozeného jazyka

Přirozený jazyk (dále jen PJ) představuje základní prostředek lidské komunikace a přenosu znalostí. Umožňuje předávání informací napříč generacemi a propojuje historický vývoj lidstva se současností. Jazyk slouží nejen ke komunikaci, ale také k uchovávání a strukturování lidského poznání.

Zpracování přirozeného jazyka (*Natural Language Processing*, NLP) je oblast umělé inteligence, která se zabývá vývojem metod a algoritmů umožňujících počítačům porozumět, analyzovat a generovat lidský jazyk. Cílem NLP je vytvořit systémy schopné pracovat s jazykem podobným způsobem, jakým jej používá člověk.

Aby byl stroj schopen efektivně zpracovávat přirozený jazyk, musí řešit řadu základních otázek, mezi které patří zejména:

* co jsou slova, jejich tvary a vnitřní struktura (např. morfémy),
* jak se slova a větné složky kombinují do vět,
* jaké významy slova nesou a co označují,
* jak se význam celé věty skládá z významů jednotlivých slov a slovních spojení.

Kromě toho musí být systém zpracovávající přirozený jazyk schopen orientovat se v různých jazykových rovinách, jako jsou rovina fonetická, morfologická, syntaktická a sémantická, případně i pragmatická. Schopnost porozumět přirozenému jazyku tak zahrnuje práci s jeho komplexní strukturou a kontextem, který význam jednotlivých jazykových prvků ovlivňuje.

Vývoj metod pro zpracování přirozeného jazyka představoval dlouhodobý a náročný proces. První přístupy byly založeny na ručně definovaných pravidlech a lingvistických znalostech, zatímco moderní NLP systémy využívají především metody strojového učení a hlubokého učení. Tyto přístupy umožňují automatické získávání jazykových vzorů z velkého množství textových dat a vedly k výraznému zlepšení výsledků v řadě praktických úloh, jako je strojový překlad, analýza textu nebo extrakce informací. [1]

### 2.1 Funkce NLP

Aby byly stroje schopny porozumět lidské konverzaci a pracovat s přirozeným jazykem, byly vyvinuty algoritmy zpracování přirozeného jazyka. Proces zpracování textu lze rozdělit do několika základních částí, které na sebe navazují:

* předzpracování textu,
* reprezentace textu,
* analýza textu,
* syntaktická analýza.

Předzpracování textu zahrnuje základní operace, jako je tokenizace a *lowercasing*. Tokenizace rozděluje vstupní text na jednotlivé tokeny, nejčastěji slova, zatímco *lowercasing* převádí všechna písmena na malá, čímž se snižuje variabilita textu. Dále se používají techniky jako lemmatizace, která převádí slova na jejich základní tvar (lemma), nebo stemming, jehož cílem je nalezení kmene slova. Tyto kroky napomáhají sjednocení různých tvarů slov a zjednodušují další zpracování.

Ve fázi reprezentace textu dochází k převodu textových dat do numerické podoby, se kterou je možné dále pracovat. Jedním ze základních přístupů je výpočet četnosti výskytu jednotlivých slov v dokumentu. Pomocí vzorce *TF-IDF* (*Term Frequency–Inverse Document Frequency*) je každému slovu přiřazena váha, která zohledňuje jeho důležitost v rámci dokumentu i celého korpusu. Například v anglickém jazyce mají velmi častá slova, jako jsou **and** nebo **the**, nižší váhu než méně frekventovaná slova, která nesou vyšší informační hodnotu.

Analýza textu se zaměřuje na práci s významem a kontextem. V přirozeném jazyce se často vyskytují mnohoznačná slova nebo homonyma, jejichž význam závisí na konkrétním kontextu. U věty „Vlak jel po kolejích.“ je zřejmé, že slovo *kolejích* označuje dopravní infrastrukturu, nikoli vysokoškolské koleje. Pro zachycení tohoto kontextu se využívají metody, jako je rozpoznávání pojmenovaných entit (*Named Entity Recognition*, NER), které přiřazují slovům nebo jejich skupinám významové kategorie. Výstupem může být například označení *{kolejích: doprava}*. Součástí analýzy textu může být také určování sentimentu, tedy rozpoznání, zda je význam věty kladný, neutrální nebo záporný, což se odvozuje od použitých slov a jejich kontextu.

Syntaktická analýza se zaměřuje na vztahy mezi jednotlivými slovy ve větě a jejich gramatickou funkci. Jejím cílem je rozdělení slov podle slovních druhů a určení jejich role ve větě, například zda se jedná o podmět, přísudek nebo předmět. Syntaktická analýza umožňuje lépe pochopit strukturu věty a vztahy mezi jejími částmi, což je důležité zejména při složitějších jazykových konstrukcích. Tyto informace se dále využívají například při strojovém překladu, extrakci informací nebo porozumění významu celých vět. [2]

### 2.2 Velké datové modely

Významný pokrok v oblasti zpracování přirozeného jazyka zaznamenal podobor označovaný jako velké jazykové modely (*Large Language Models* , LLM). Tyto modely jsou založeny na rozsáhlých neuronových sítích s velkým počtem parametrů, které jsou trénovány na rozsáhlých textových datech. Jejich cílem je naučit se statistické a sémantické vztahy mezi slovy a větami a na jejich základě generovat smysluplný textový výstup.

Architektura velkých jazykových modelů je založena především na dopředných neuronových sítích (*Feed-Forward Networks*) a mechanismech pozornosti (*attention*), které umožňují modelu pracovat s kontextem celého vstupu. Na rozdíl od starších přístupů nejsou moderní velké jazykové modely založeny na rekurentních neuronových sítích, ale využívají paralelní zpracování vstupních sekvencí, což výrazně zvyšuje jejich efektivitu a škálovatelnost.

Velké jazykové modely lze dále rozdělit podle způsobu jejich ladění a zaměření na konkrétní úlohy na **základní (generické)**, **instrukčně laděné** a **dialogově laděné** modely. Základní modely jsou trénovány především na predikci následujícího tokenu v textu a slouží jako výchozí bod pro další úpravy. Instrukčně laděné modely jsou následně přizpůsobeny k plnění konkrétních úloh na základě zadaných instrukcí. Dialogově laděné modely jsou optimalizovány pro vedení interaktivní komunikace s uživatelem a jsou často využívány ve formě chatbotů nebo konverzačních systémů umělé inteligence. V rámci této práce jsou využívány právě dialogově laděné modely.

V souvislosti s velkými jazykovými modely se často používá pojem *generativní umělá inteligence* (*Generative AI*, zkr. GenAI). Tento pojem označuje modely schopné generovat nový obsah na základě vzorů získaných z trénovacích dat. Do generativní AI spadají nejen velké jazykové modely, ale také modely generující obraz, zvuk či video. Velké jazykové a multimodální modely tak tvoří základ současné generativní umělé inteligence, která umožňuje tvorbu textu, programového kódu, obrazového i zvukového obsahu. [3]

#### 2.2.1 Transformátor

Architektura transformátoru byla poprvé představena v roce 2017 ve vědeckém článku „Attention Is All You Need“ autory Vaswanim a kol. a je považována za zásadní milník v oblasti hlubokého učení [4]. Transformátor představuje neuronovou architekturu založenou na mechanismu pozornosti, který umožňuje modelu při zpracování textu zohledňovat vztahy mezi všemi slovy ve vstupní sekvenci současně.

Základními stavebními prvky transformátoru jsou vrstvy vícenásobné pozornosti (*multi-head attention*) a dopředné neuronové sítě. Díky této architektuře je možné efektivně zachytit dlouhodobé závislosti v textu bez nutnosti rekurentního zpracování. Transformátor se stal základem většiny moderních velkých jazykových modelů a významně přispěl k jejich vysoké výkonnosti v úlohách zpracování přirozeného jazyka. [5]

#### 2.2.2 Schopnosti

Velké jazykové modely jsou trénovány na široké spektrum úloh a disponují řadou schopností v závislosti na typu vstupních dat. Textově zaměřené modely dokáží provádět generování textu, strojový překlad, sumarizaci dokumentů nebo odpovídání na otázky. Multimodální modely rozšiřují tyto schopnosti o práci s obrazovými daty, například rozpoznávání obsahu obrázků nebo extrakci textu z obrazových vstupů.

Další skupinu tvoří modely zaměřené na zpracování zvuku, které umožňují převod řeči na text a naopak. Kombinací těchto schopností vznikají komplexní systémy schopné pracovat s různými typy vstupních dat a poskytovat uživateli přirozené rozhraní pro komunikaci s umělou inteligencí. [5] [6]

**ZDROJE**

1. PALA, Karel. Počítačové zpracování přirozeného jazyka. *NLP FI MU*, 2000.
2. https://www.sap.com/uk/resources/what-is-natural-language-processing
3. HENDL, Jan. Jazykové modely a umělá inteligence. In: *Sborník konference Medsoft 2023*. 2023. p. 1-9.
4. https://www.ibm.com/think/topics/transformer-model
5. https://huggingface.co/learn/llm-course/chapter1
6. https://www.sap.com/uk/resources/what-is-large-language-model

## 2.3 AI ve zdravotnictví - bude doplněno

### 2.3.1 Historie

### 2.3.2 Oblasti využití



# 3. Data projektu MRE

## 3.1 Téma lékařských zpráv

Nedílnou součástí bakalářské práce bylo zpracování vstupních dat. Data pocházela z Fakultní nemocnice Plzeň a obsahovala anonymizované lékařské zprávy pacientů s Crohnovou chorobou a cévní mozkovou příhodou (mrtvicí). Jednalo se o reálná klinická data, která se výrazně lišila jak délkou jednotlivých záznamů, tak i jejich obsahem a zaměřením. Zprávy zahrnovaly různé typy lékařských vyšetření a záznamů, například vyšetření CT, MR, SONO, perfuzní vyšetření, ambulantní zprávy či hospitalizační záznamy.

## 3.2 Struktura a Anonymizace

Z jazykového hlediska jsou lékařské zprávy charakteristické vysokou mírou odborné terminologie, častým výskytem zkratek, latinských názvů, nejednoznačných formulací a stylistických i pravopisných nekonzistencí. Texty rovněž obsahují neúplné věty, telegrafický styl zápisu a kombinaci strukturovaných i nestrukturovaných částí, což výrazně zvyšuje náročnost automatické extrakce informací.

Zprávy byly zadávajícím učitelem poskytnuty ve formátu CSV. Jednotlivá data byla zptacována tak, aby každý csv soubor měl tyto entity: *url* - odkaz na webový server projektu MRE s danou zprávou, *datetime* - čas vyšetření, title - název vyšetření a *text* - text lékařské zprávy. U lékařských zpráv zabývajícími se mrtvicí nebyly poskytnuty url adresy.

Lékařské zprávy byly předem anonymizovány v rámci projektu MRE Fakulty aplikovaných věd a z osobních údajů byl ve zprávách uveden jen věk. Ve několika zprávách je uvedeno, že pacient souhlasil se zprocováním dat. Proto je vše v souladu s evropským nařízením GDPR.

## 3.3 Testovací data

Při hodnocení správnosti extrakce nebyly k dispozici předem připravené testovací ani referenční (ground truth) soubory. Z tohoto důvodu nebylo možné provést klasické vyhodnocení pomocí přesnosti a úplnosti vůči zlatému standardu. Místo toho byly navrženy vlastní metriky umožňující relativní porovnání výsledků extrakce napříč vybranými velkými jazykovými modely (LLM). Tyto metriky se zaměřovaly především na konzistenci výstupů, úplnost extrahovaných informací a jejich shodu s obsahem původního textu.



# 4. Návrh řešení

## 4.1 Celkový koncept

Projekt byl rozdělen do tří hlavních částí:  **předzpracování dat** , **vytvoření metrik** a  **evaluace výsledků** . Jednotlivé části byly dále členěny na dílčí podúkoly, které na sebe logicky navazovaly. Celkový koncept řešení je schematicky znázorněn na obrázku # a v následujících podkapitolách je podrobně rozebrán.

Před samotnou extrakcí bylo nutné provést základní úpravy dat, zéjmena sjednotit strukturu csv souborů. Jelikož nebyly poskytnuty testovací data, bylo potřeba vybrat zprávy s nějvětším obsahem informací. U pacientů s Crohnovou chorobou bylo upřednostňováno téma návštěvy lékaře (ambulantní zprávy), jelikož tento typ dokumentů obsahoval největší množství textových informací a zároveň nejširší spektrum strukturovaných údajů, jako jsou diagnózy, medikace, laboratorní výsledky a doporučení. Naopak u zpráv týkajících se cévní mozkové příhody nebylo žádné konkrétní téma preferováno, neboť jednotlivé záznamy byly tematicky homogennější a často se vztahovaly k zobrazovacím metodám mozku.

### 4.1.1 Předzpracování dat

Před samotnou extrakcí informací bylo nezbytné provést základní předzpracování vstupních dat. Hlavním cílem této fáze bylo sjednocení struktury poskytnutých CSV souborů a příprava dat tak, aby byla vhodná pro další automatické zpracování.

Vzhledem k tomu, že nebyla k dispozici samsostatná testovací ani validační data, bylo nutné provést výběr reprezentativních lékařských zpráv s co nejvyšším informačním obsahem. Kritériem výběru byl zejména rozsah textu a množství klinicky relevantních informací.

U pacientů s Crohnovou chorobou bylo upřednostněno téma návštěvy lékaře, konkrétně ambulantní zprávy. Tyto dokumenty se ukázaly jako nejvhodnější, neboť obsahovaly největší množství textových informací a zároveň široké spektrum strukturovaných údajů, jako jsou diagnózy, medikace, laboratorní výsledky a doporučení pro další léčbu.

Naopak u zpráv týkajících se cévní mozkové příhody nebylo žádné konkrétní téma preferováno. Jednotlivé záznamy byly obsahově homogennější a převážně se vztahovaly k výsledkům zobrazovacích metod mozku, zejména CT a MR vyšetřením, což umožňovalo jejich použití bez další tematické filtrace.

### 4.1.2 Metriky

#### 4.1.2.1 Vytvoření metriky

Vytvoření vhodných metrik pro hodnocení kvality extrakce informací představovalo jeden z nejnáročnějších aspektů této práce. Standardně používané metriky, jako je přesnost ( *precision* ), úplnost ( *recall* ), F1 skóre nebo regresní metody, nejsou v kontextu této práce snadno aplikovatelné. Důvodem je absence referenčních anotovaných dat (tzv.  *ground truth* ), stejně jako vysoká variabilita a nestrukturovanost vstupních lékařských textů.

Z těchto důvodů byly navrženy vlastní, převážně kvalitativní a kvantitativně–deskriptivní metriky, jejichž cílem není absolutní hodnocení správnosti, ale **relativní porovnání chování jednotlivých velkých jazykových modelů (LLM)** napříč různými aspekty extrakce. Navržené metriky rozdělují hodnocení do několika vzájemně se doplňujících dimenzí, které umožňují identifikovat silné a slabé stránky jednotlivých modelů.

*Výsledky prezentované v této kapitole se v současné fázi vztahují výhradně k datům pacientů s Crohnovou nemocí. Rozšíření metrik a jejich aplikace na další diagnózy, zejména cévní mozkovou příhodu, je plánováno jako součást další práce.*

#### 4.1.2.2 Anotace

Klíčovým předpokladem pro konstrukci metrik bylo vytvoření anotovaného slovníku pojmů, na jejichž výskyt se hodnocení extrakce zaměřuje. Anotace slouží jako referenční rámec, nikoliv jako úplný zlatý standard, a umožňuje sledovat, zda model dokáže identifikovat a zachovat významově důležité informace.

Anotovány byly zejména následující typy výrazů:

* **strukturální prvky textu** , jako jsou názvy sekcí (např.  *subj* ,  *obj* ,  *doporučení* ),
* **klíčová slova specifická pro Crohnovu nemoc** (např.  *CRP, kalprotectin, ileum* ),
* **lékařské a latinské termíny**, včetně názvů diagnóz, léčiv a anatomických struktur,
* **klinické příznaky a popisy zdravotního stavu** .

Tato anotace umožnila následně kvantifikovat, jakým způsobem jednotlivé modely s těmito pojmy pracují, zda je zachovávají, modifikují, či zcela opomíjejí.

#### 4.1.2.3 Dimenze hodnocení extrakce

Navržené metriky jsou rozděleny do několika základních dimenzí, které reflektují různé aspekty kvality výstupů:

* porovnání výsledků mezi jednotlivými modely,
* konzistence výstupů při opakovaném zpracování,
* vliv použití cizího jazyka v promptu,
* vliv různých typů promptování.

### 4.1.3 Evaluace výsledků

Metriky vytvořené v tomto projektu sice slouží k nalezení silných a slabých stránek modelů, ale ne všechny metriky jsou schopné být automatizovány. Některé z těchto metrik musejí být ručně vyhodnocovány soubor po souboru, což mohlo vést k různým odchylkám. Porovnání modelů na základě výsledků z testování bude vedeno ručním vyhodnocením a většina závěru bude záviset na slovním popisu výhod a nevýhod vybraných LLM.

## 4.2 Volba modelů

Výběr jazykových modelů byl v úvodní fázi rozdělen do tří základních kategorií:  **obecné modely**, **lékařsky orientované modely** a  **modely zaměřené na český jazyk**. Cílem tohoto rozdělení bylo pokrýt jak široce používané velké jazykové modely bez doménového zaměření, tak i specializované modely optimalizované pro zdravotnickou oblast nebo český jazyk.

Obecné modely byly chápány jako rozsáhlé korporátní jazykové modely využívané celosvětově, které nejsou explicitně zaměřeny na konkrétní doménu. Naopak lékařské a české modely měly představovat doménově specifická řešení, potenciálně lépe přizpůsobená zpracování odborných textů nebo textů v českém jazyce.

Při podrobnějším průzkumu dostupných modelů však bylo zjištěno, že většina lékařsky orientovaných jazykových modelů je buď  **komerčně placená**, nebo  **přístupná pouze na základě zvláštního povolení ze strany vydavatele**. Dalším významným omezením bylo, že tyto modely často nebyly primárně navrženy pro úlohy strukturované extrakce informací, ale spíše pro generování nebo doplňování textu, případně konverzační využití.

Podobná situace nastala také u modelů zaměřených výhradně na český jazyk. Počet dostupných a veřejně přístupných modelů trénovaných specificky na českých datech je velmi omezený a žádný z nich nenabízel dostatečnou podporu pro úlohy extrakce strukturovaných informací z textu. Z tohoto důvodu nebylo možné tyto modely efektivně zahrnout do experimentální části práce.

Na základě uvedených omezení byly proto do dalšího zkoumání vybrány pouze  **obecné velké jazykové modely**, které v současnosti patří mezi nejrozšířenější a nejvýkonnější dostupná řešení. Výběr konkrétních modelů byl proveden na základě průzkumu odborných a technologických zdrojů, dostupnosti modelů a jejich schopností práce s delšími texty a strukturovanými výstupy.

Vybrány proto byly jen obecné a to nejrozšířenější modely součastnosti. Po průzkůmu několika webových stránek bylo vybrány následující modely:

| Brand      | Name of LLM | Model                                   |
| ---------- | ----------- | --------------------------------------- |
| Anthropic  | Claude.ai   | Sonnet 4.5                              |
| OpenAI     | ChatGPT     | GPT-5                                   |
| Mistral AI | Le Chat     | Mistral Large / Pixtral Large / Mixtral |
| Google     | Gemini      | 2.5. Flash / 3.0 Pro                   |
| xAi        | Grok        | Grok 4                                  |
| Deepseek   | Deepseek    | DeepSeek-V3.2                           |
| Meta       | Llama       | Llama-3.2-3B                            |


# 5. Implementace prototypu

## 5.1 Metodika a použité nástroje

Tato kapitola popisuje softwarové vybavení, vývojové prostředí a využité programové knihovny, které tvořily technologický základ pro realizaci praktické části práce.

### 5.1.1 Vývojové prostředí

Pro implementaci veškerých algoritmů a uživatelského rozhraní bylo využito integrované vývojové prostředí (IDE)  **Microsoft Visual Studio Code (VS Code)**. Volba tohoto prostředí byla podložena jeho vysokou modularitou a širokou podporou pro jazyk  **Python**, který byl zvolen jako primární programovací jazyk. Python v současnosti představuje standard v oblastech strojového učení, analýzy dat a integrace modelů umělé inteligence, a to především díky rozsáhlému ekosystému knihoven a podpoře rozhraní API.

### 5.1.2 Softwarové nástroje a platformy

#### 5.1.2.1 Jupyter Notebook

Pro fázi analýzy dat a prototypování funkcí určených k předzpracování (preprocessing) byl využit nástroj  **Jupyter Notebook**. Tento nástroj umožňuje interaktivní spouštění bloků kódu, což usnadňuje ladění a vizualizaci dat v reálném čase. V rámci práce byl využíván jak ve formě webového rozhraní *JupyterLab*, tak prostřednictvím integrace přímo v prostředí VS Code.

#### 5.1.2.2 Doccano

Pro účely vytvoření evaluačních metrik a trénovacích dat bylo nezbytné provést manuální anotaci lékařských zpráv. K tomuto účelu byl zvolen open-source nástroj **Doccano**. Z důvodu izolace závislostí a snadné replikovatelnosti prostředí byl tento anotační nástroj provozován v rámci kontejnerizační platformy **Docker** .

#### 5.1.2.3 Knihovny jazyka Python a správa závislostí

Kromě standardních knihoven jazyka Python byly využity specializované balíčky třetích stran. Správa těchto knihoven byla realizována prostřednictvím správce balíčků **pip**. Kompletní seznam všech využitých knihoven včetně jejich specifických verzí je pro účely reprodukovatelnosti uveden v souboru `requirements.txt`, který je součástí přílohové části práce.

## 5.2 Projekt MRE

### 5.2.1 Struktura projektu

Pojekt MRE je rozdělen do následujících adresářů:

- **data** - v adresáři jsou uloženy vybrané texty z csv souborů, popisy pro modely, poskytnuté csv soubory, anotované slova a texty určené k promtování (prompty)
- **docs** - zde se uchovává dokumentace a všechny doplňující informace k provozu projektu
- **results** - adresář s výsledkami modelů
- **scripts** - využívá konfigurační soubory a soubor pro uchování adres a konstant
- **scr** - obsahuje většinu použitých kódů a programů využitých při práci na projektu MRE
- **st_src** - obsahuje kódy pro webovou aplikaci

#### 5.2.1.1 Data

Adresář data uchovává všechny potřebná data k vypracování projektu MRE. Adresář obsahuje 5 podadresářů.

- **csv** - obsahuje strukturované lékařské zprávy poskytnuté vedoucím ve formátu csv
- **doccano** - extrahovaná slova z doccana rozřezená do textových souborů
- **prompts** - soubory ve fromátu json určené na komunikaci s modely (promting)
- **tasks** - texty s instrukcemi pro LLM
- **medical_reports** - vybrané lékařské zprávy ze souborů csv

### 5.2.2 Webová aplikace

Webová aplikace byla navržena jako podpůrný nástroj pro poloautomatickou generaci promptů, zpracování výstupů a analýzu lékařských zpráv. Vzhledem k absenci přímého napojení na API velkých jazykových modelů (LLM) nebylo možné proces plně automatizovat. Aplikace tak slouží primárně k optimalizaci pracovního toku (workflow) a usnadnění manuálních úkonů spojených s experimentální částí projektu.

#### 5.2.2.1 Použité technologie

Pro vývoj webového rozhraní byl zvolen jazyk Python, který nabízí řadu frameworků pro tvorbu webových aplikací (např. Flask, Django). Pro účely této práce byla vybrána knihovna **Streamlit**. Tento framework je optimalizován pro rychlý vývoj datově orientovaných aplikací a prototypování, což plně odpovídalo požadavkům na jednoduché, ale funkční uživatelské rozhraní bez nutnosti složité implementace backendové logiky.

#### 5.2.2.2 Funkcionalita aplikace

Aplikace je členěna do pěti samostatných modulů (stránek), které pokrývají jednotlivé fáze zpracování dat:

- **Data Viewer** – Modul pro vizualizaci a prohlížení zdrojových dat uložených v adresáři `data`. Pro tabulkové zobrazení datových sad je využita knihovna **Pandas**.
- **Prompt Maker** – Nástroj pro systematickou tvorbu a správu promptů, které jsou následně manuálně vkládány do testovaných LLM modelů.
- **Result Maker** – Slouží ke strukturovanému ukládání výstupů získaných z modelů do souborového systému.
- **Results Viewer** – Rozhraní pro prohlížení a kontrolu uložených výsledků experimentů.
- **Analyzator** – Modul provádějící analýzu lékařských zpráv, jehož výstupem jsou vypočtené evaluační metriky.

#### 5.2.2.3 Architektura aplikace

Vstupním bodem aplikace je soubor **`main.py`**, který zajišťuje inicializaci prostředí a navigaci. Jednotlivé funkční moduly (stránky) jsou implementovány v samostatných souborech umístěných v adresáři `st_src`. Komplexní logika a výpočetní operace, které přesahují rámec prezentační vrstvy, jsou vyčleněny do pomocných modulů v adresáři `src`, čímž je zajištěna přehlednost a udržitelnost kódu.

## 5.3 Metoda interakce s modely (prompting)

Při využívání vybraných jazykových modelů byla zvažována integrace pomocí aplikačního rozhraní **API**.  Ačkoliv poskytovatelé těchto modelů standardně nabízejí knihovny pro přímou komunikaci v rámci vývojového prostředí, přístup k těmto rozhraním je v mnoha případech podmíněn zpoplatněním nebo komerční licencí.

Z tohoto důvodu byl zvolen proces manuálního zpracování dat:

1. V lokálním prostředí (VS Code) byly připraveny vstupní soubory obsahující testovací data a definované prompty.
2. Tato data byla následně vkládána do webových rozhraní příslušných modelů.
3. Získané odpovědi byly exportovány a následně zpracovány pomocí vlastní **webové aplikace v knihovně Streamlit**, která sloužila k unifikaci výsledků a jejich transfor\\\\\\\\\\\\\\maci do finálních datových formátů pro další analýzu.
