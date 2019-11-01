import sys

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Integer
from decouple import AutoConfig

from leis_brasileiras.utils import (
    expand_results,
    extract_projeto,
    get_from_depara
)


USAGE_STRING = """
    usage: python integrate_data.py TYPE PROJETOS_FILES LEI_FILES

    TYPE needs to be 'lei', 'lei_comp', 'decreto' or 'emenda'

    PROJETOS_FILES and LEI_FILES may be comprised of several CSVs,
    separated by commas:

    python integrate_data.py projetos1.csv,projetos2.csv leis.csv
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

if TYPE not in SUPPORTED_TYPES:
    print('{} not supported! Supported types:\n'
          '{}'.format(TYPE, SUPPORTED_TYPES))
    sys.exit(1)

config = AutoConfig(search_path='.')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_HOST = config('POSTGRES_HOST')
POSTGRES_PORT = config('POSTGRES_PORT')
POSTGRES_DB = config('POSTGRES_DB')

engine = create_engine(
    f'postgresql://{POSTGRES_USER}@{POSTGRES_HOST}'
    f':{POSTGRES_PORT}/{POSTGRES_DB}')

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

# Get CPF from vereadores using depara
depara = pd.read_sql(
    'SELECT * FROM eleitoral.depara_vereadores_camara_tse_lupa',
    engine)

dfm['cpfs'] = dfm['autor'].apply(
    lambda x: ",".join(list(
        filter(
            lambda cpf: cpf is not None,
            [get_from_depara(nm, depara, 'cpf') for nm in x.split(',')]
        )
    ))
)
dfm = expand_results(dfm, target_columns=['cpfs'])

# Get key from vereador table
vereadores = pd.read_sql(
    'SELECT cpf, chave_vereador FROM lupa.vereadores_rj',
    engine)

dfm = dfm.merge(vereadores, how='left', left_on='cpfs', right_on='cpf')
dfm = dfm.drop(['cpfs'], axis=1)

# Reorganize columns
column_order = [
    'cod_municipio', 'nm_municipio',
    'projeto', 'autor', 'data_publicacao', 'ementa', 'inteiro_teor',
    'lei', 'ano', 'status', 'cpf', 'chave_vereador'
]
dfm = dfm[column_order]

# Save integrated data to postgres
table_name = TYPE_TO_TABLE[TYPE]
dfm.to_sql(
    table_name,
    engine,
    schema='eleitoral',
    index=False,
    if_exists='replace',
    dtype={"chave_vereador": Integer()})
