import pandas as pd
from scripts import config
import os
#import re

def find():
    base_root = config.CSV_DATA_ROOT
    files = os.listdir(base_root)
    #crohn = os.path.join(base_root, files[0])
    #crohn_2 = os.path.join(base_root, files[1])
    stroke = os.path.join(base_root, files[2])

    df = pd.read_csv(stroke)

    texts = []

    for _, row in df.iterrows():
        print(str(row['title']))# každá řádka = Series s hodnotami
        if config.TITLES_STROKE[2] in str(row['title']):  # přístup ke sloupci 'title'
            texts.append(str(row['text']))  # přístup ke sloupci 'text'
            
    with open("output.txt", 'w', encoding='utf-8') as f:
        for text in texts:
            f.write(text)
            f.write("\n")
            f.write("---------------------------------------------------------------------")
            f.write("\n")
    """
    REGEX APPROACH
    only_chars = re.compile(r'[A-Z|a-z|ěščřžýáíé]+')

    for title in titles:
        clean_title = only_chars.findall(title)
        res = ' '.join(clean_title)   
        print(res)
    """
    """
    SPLIT APPROACH
    res = []
    for title in df.title:
        tokens = title.split("-")
        clean_title = tokens[1].strip()
        if clean_title not in res:
            res.append(clean_title)
        
    print(res)
    """