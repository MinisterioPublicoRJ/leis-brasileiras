import re
from unidecode import unidecode
import pandas as pd

def clean_author_name(x):
    x = unidecode(x)
    x = x.upper()
    x = re.sub(r'VEREADORA?', '', x)
    x = x.replace('.', '. ')
    x = re.sub('\s+', ' ', x)
    return x.strip()

def expand_results(df, target_columns=['nome_lupa', 'nome_urna_lupa']):
    def splitListToRows(row, row_accumulator, target_columns):
        splitted = []
        for column in target_columns:
            splitted.append(row[column].split(','))
        ln_nm = len(splitted[0])
        nm_cols = len(splitted)
        for i in range(ln_nm):
            new_row = row.to_dict()
            for j in range(nm_cols):
                new_row[target_columns[j]] = splitted[j][i]
            row_accumulator.append(new_row)
    new_rows = []
    df.apply(splitListToRows, axis=1, args=(new_rows, target_columns))
    new_df = pd.DataFrame(new_rows)
    return new_df