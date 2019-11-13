import sys

import pandas as pd
from decouple import AutoConfig

from leis_brasileiras.utils import extract_projeto


USAGE_STRING = """
    usage: python integrate_data.py TYPE PROJETOS_FILES LEI_FILES OUTPUT_NAME

    TYPE needs to be 'lei', 'lei_comp', 'decreto' or 'emenda'

    PROJETOS_FILES and LEI_FILES may be comprised of several CSVs,
    separated by commas:

    python integrate_data.py lei projetos1.csv,projetos2.csv leis.csv output.csv
"""

if len(sys.argv) < 4:
    print(USAGE_STRING)
    sys.exit(1)

SUPPORTED_TYPES = ['lei', 'lei_comp', 'decreto', 'emenda']
TYPE_TO_TABLE = {
    'lei': 'projetos_lei_ordinaria',
    'lei_comp': 'projetos_lei_complementar',
    'decreto': 'projetos_decreto',
    'emenda': 'projetos_emenda_lei_organica'
}

START_YEAR = 2009
TYPE = sys.argv[1]
PROJETOS_FILES = sys.argv[2].split(',')
LEI_FILES = sys.argv[3].split(',')
OUTPUT_FILE = sys.argv[4]

if TYPE not in SUPPORTED_TYPES:
    raise RuntimeError('{} not supported! Supported types are:\n'
        '{}'.format(TYPE, SUPPORTED_TYPES))

# Get projetos de lei
projetos = []
for pf in PROJETOS_FILES:
    projetos.append(pd.read_csv(pf, ';'))
projetos = pd.concat(projetos)

projetos = projetos.rename({'lei': 'projeto'}, axis=1)

projetos.dropna(subset=['ementa', 'autor'], inplace=True)
projetos.drop_duplicates(subset=['projeto', 'data_publicacao'], inplace=True)

projetos['nr_projeto'] = projetos['projeto'].apply(lambda x: x.split('/')[0])
projetos['ano'] = projetos['projeto'].apply(lambda x: x.split('/')[1])

projetos[projetos['ano'].astype(int) >= START_YEAR]

projetos.sort_values(['ano', 'nr_projeto'], ascending=False, inplace=True)
projetos.drop(['nr_projeto', 'ano'], axis=1, inplace=True)

# Get leis
leis = []
for lf in LEI_FILES:
    leis.append(pd.read_csv(lf, ';'))
leis = pd.concat(leis)

leis['nr_projeto'] = leis['inteiro_teor'].apply(
    extract_projeto, law_type=TYPE)

# Merge leis with their respective projetos
dfm = projetos.merge(
    leis[['lei', 'ano', 'status', 'nr_projeto']].astype(str),
    how='left',
    left_on='projeto',
    right_on='nr_projeto')
dfm['status'] = dfm['status'].fillna('Não se aplica')
dfm['cod_municipio'] = 330455
dfm['nm_municipio'] = 'RIO DE JANEIRO'
dfm = dfm.drop(['nr_projeto'], axis=1)

dfm.to_csv(OUTPUT_FILE, ';', index=False)
