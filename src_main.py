#from src import find_texts
import pandas as pd
from scripts import config
import os
import re

base_root = config.CSV_DATA_ROOT
files = os.listdir(base_root)
crohn = os.path.join(base_root, files[0])
crohn_2 = os.path.join(base_root, files[1])
stroke = os.path.join(base_root, files[2])

ids = [53, 65, 73, 78, 123, 152, 164, 175, 220, 229]

if __name__ == "__main__":
    df = pd.read_csv(crohn_2)

    texts: list[str] = []
    out_texts = []
    for _, row in df.iterrows():
        if config.TITLES_CROHN[2] in str(row['title']):  # přístup ke sloupci 'title'
            texts.append(str(row['text']))  # přístup ke sloupci 'text'
            
    for i, text in enumerate(texts):
        if i in ids:
            out_texts.append(text)
        #array = re.findall(r'\S', text)
        # if (len(array) < 800 and len(array) > 200):
        # if (len(array) > 3000):
        #    print(f"Soubor {i} - match chars: {len(array)}")
    
for i in range(len(out_texts)):
    start = 4
    path = f"{config.REPORTS_ROOT}\\0{start + i}_crohn.txt"
    with open(path, 'w', encoding='utf-8') as fr:
        fr.write(out_texts[i])        


# Lowest crohn   - 5, 8, 9     
# Highest crohn  - 175, 73, 229
# Lowest stroke  - 2, 0, 1
# Highest stroke - 9, 5, 8

# Crohn > 3000 znaků
