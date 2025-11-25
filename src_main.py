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


if __name__ == "__main__":
    df = pd.read_csv(crohn)

    texts: list[str] = []
    for _, row in df.iterrows():
        if config.TITLES_CROHN[2] in str(row['title']):  # přístup ke sloupci 'title'
            texts.append(str(row['text']))  # přístup ke sloupci 'text'
            
    for i, text in enumerate(texts):
        array = re.findall(r'\S', text)
        # if (len(array) < 800 and len(array) > 200):
        # if (len(array) > 1000):
        print(f"Soubor {i} - match chars: {len(array)}")

# Lowest crohn   - 5, 8, 9     
# Highest crohn  - 175, 73, 229
# Lowest stroke  - 2, 0, 1
# Highest stroke - 9, 5, 8