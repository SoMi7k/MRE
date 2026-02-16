#from src import find_texts
import pandas as pd
from scripts import config
import os
import re
import matplotlib.pyplot as plt

base_root = config.CSV_DATA_ROOT
files = os.listdir(base_root)
crohn = os.path.join(base_root, files[0])
crohn_2 = os.path.join(base_root, files[1])
stroke = os.path.join(base_root, files[2])

ids = [53, 65, 73, 78, 123, 152, 164, 175, 220, 229]

if __name__ == "__main__":
    df = pd.read_csv(crohn_2)
    texts: list[str] = []
    out_texts: list[tuple] = []
    for _, row in df.iterrows():
        if config.TITLES_CROHN[2] in str(row['title']):  # přístup ke sloupci 'title'
            texts.append(str(row['text']))  # přístup ke sloupci 'text'
    
    for i, text in enumerate(texts):
        array = re.findall(r'\s', text)
        if (len(array) < 500 and len(array) > 0):
        #if (len(array) > 3000):
            out_texts.append((text, i))
            print(f"Soubor {i} - match chars: {len(array)}")
        
    start = 1
    path = f"{os.path.join(config.REPORTS_ROOT, "try")}\\0{start + i}_crohn.txt"
    with open(path, 'w', encoding='utf-8') as fr:
        for text, id in out_texts:
            fr.write(f"ID: {id}\n")
            fr.write(text)
            fr.write("\n\n" + "="*80 + "\n\n") 
    """
    word_counts = []

    for text in texts:
        words = re.findall(r'\s', text)
        word_counts.append(len(words))
    
    plt.figure()
    plt.hist(word_counts, bins=30)
    plt.xlabel("Počet slov")
    plt.ylabel("Počet dokumentů")
    plt.title("Rozvrstvení dokumentů podle počtu slov")
    plt.show()
    """

# Lowest crohn   - 5, 8, 9     
# Highest crohn  - 175, 73, 229
# Lowest stroke  - 2, 0, 1
# Highest stroke - 9, 5, 8

# Crohn > 3000 znaků
