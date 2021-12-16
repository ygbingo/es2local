# -*- coding: utf-8 -*-
"""
Save data to local csv.
"""
from pandas import DataFrame
import numpy as np

def save_local_csv(rows, titles, filename):
    df = DataFrame(rows)
    df.to_csv(filename, header=titles,
                  index=False, encoding="utf-8-sig")
    print(f"Save data to file: {filename}")
