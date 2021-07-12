import re

from unidecode import unidecode
import pandas as pd


def extract_projeto(s, law_type=None):
    clean_s = s.replace('.', '').replace("//", "/")
    clean_s = re.sub(r'\s', '', clean_s)
    if law_type == 'lei':
        m = re.search(
            r'(ProjetodeLei|ProjLei)'
            r'(nº?)?(\d+)\-?\w?(/|,de|de)?(\d+)',
            clean_s)
    elif law_type == 'lei_comp':
        m = re.search(
            r'(ProjetodeLei|ProjLei)Complementar'
            r'(nº?)?(\d+)\-?\w?(/|,de|de|)(\d+)',
            clean_s)
    elif law_type == 'decreto':
        m = re.search(
            r'(ProjetodeDecretoLegislativo|ProjDecretoLegislativo)'
            r'(nº?)?(\d+)\-?\w?(/|,de|de|)(\d+)',
            clean_s)
    elif law_type == 'emenda':
        m = re.search(
            r'(ProjetodeEmendaàLeiOrgânica|PropostadeEmenda)'
            r'(nº?)?(\d+)\-?\w?(/|,de|de|)(\d+)',
            clean_s)
    elif law_type == 'resolucao':
        clean_s = unidecode(clean_s).upper()
        m = re.search(
            r'(PROJETORESOLUCAOOUREQUERIMENTO)'
            r'(NO?)?[A-Z]*(\d+)\-?[A-Z]?(/|,DE|DE)?(\d+)',
            clean_s)
    else:
        m = None
    if m:
        nr = m.group(3).zfill(4)
        ano = m.group(5)
        return '{}/{}'.format(nr, ano)
    return None


def expand_rows(df, target_column, separator=','):
    def splitListToRows(row, row_accumulator, target_column, separator):
        splitted = row[target_column].split(separator)
        for i in range(len(splitted)):
            new_row = row.to_dict()
            new_row[target_column] = splitted[i]
            row_accumulator.append(new_row)

    new_rows = []
    df.apply(splitListToRows, axis=1, args=(new_rows, target_column, separator))
    new_df = pd.DataFrame(new_rows)
    return new_df


def clean_name(x):
    return re.sub('\s+', ' ', unidecode(x).upper().strip())
