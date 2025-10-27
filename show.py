import pandas as pd
from scripts import config
import os
#import re

base_root = config.CSV_DATA_ROOT
files = os.listdir(base_root)
crohn = os.path.join(base_root, files[0])
crohn_2 = os.path.join(base_root, files[1])
stroke = os.path.join(base_root, files[2])
