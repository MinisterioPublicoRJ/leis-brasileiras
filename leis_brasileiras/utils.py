import re
from unidecode import unidecode
import pandas as pd
import numpy as np

def extract_projeto(s, law_type=None):
    clean_s = s.replace('.', '').replace("//", "/")
    clean_s = re.sub('\s', '', clean_s)
    if law_type == 'lei':
        m = re.search(
            '(ProjetodeLei|ProjLei)'
            '(nº)?(\d+)\-?\w?(/|,de|de)(\d+)',
            clean_s)
    elif law_type == 'lei_comp':
        m = re.search(
            '(ProjetodeLei|ProjLei)Complementar'
            '(nº)?(\d+)\-?\w?(/|,de|de|)(\d+)',
            clean_s)
    elif law_type == 'decreto':
        m = re.search(
            '(ProjetodeDecretoLegislativo|ProjDecretoLegislativo)'
            '(nº)?(\d+)\-?\w?(/|,de|de|)(\d+)',
            clean_s)
    elif law_type == 'emenda':
        m = re.search(
            '(ProjetodeEmendaàLeiOrgânica|PropostadeEmenda)'
            '(nº)?(\d+)\-?\w?(/|,de|de|)(\d+)',
            clean_s)
    else:
        m = None
    if m:
        nr = m.group(3).zfill(4)
        ano = m.group(5)
        return '{}/{}'.format(nr, ano)
    return ''

def get_from_depara(nm, depara, column='cpf'):
    is_name = depara['nome_camara'] == clean_author_name(nm)
    if np.any(is_name):
        return depara[is_name][column].iloc[0]

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