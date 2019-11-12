import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from decouple import AutoConfig


config = AutoConfig(search_path='.')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_HOST = config('POSTGRES_HOST')
POSTGRES_PORT = config('POSTGRES_PORT')
POSTGRES_DB = config('POSTGRES_DB')

engine = create_engine(
    f'postgresql://{POSTGRES_USER}@{POSTGRES_HOST}'
    f':{POSTGRES_PORT}/{POSTGRES_DB}')

depara = pd.read_sql(
    'SELECT * FROM eleitoral.depara_vereadores_camara_tse_lupa',
    engine)
vereadores = pd.read_sql(
    'SELECT * FROM lupa.vereadores_rj',
    engine)

vereadores['cpf'] = vereadores.apply(
    lambda row:
        depara[depara['nome_lupa'] == row['nome_vereador']].iloc[0]['cpf']
        if row['nm_municipio'] == 'RIO DE JANEIRO'
        else np.nan,
    axis=1)
vereadores['chave_vereador'] = vereadores.index

vereadores.to_sql(
    'vereadores_rj',
    engine,
    schema='lupa',
    index=False,
    if_exists='replace'
)
