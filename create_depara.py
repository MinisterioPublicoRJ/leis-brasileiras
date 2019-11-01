import re

import pandas as pd
import numpy as np
import psycopg2
from unidecode import unidecode
from sqlalchemy import create_engine
from decouple import AutoConfig

from leis_brasileiras.utils import (
    clean_author_name,
    extract_projeto
)


def create_depara(df_camara, df_vereadores):
    depara = {}
    for row in df_camara.iterrows():
        ano = row[1]['projeto'].split('/')[1]
        
        autores = row[1]['autor'].split(',')
        autores = [clean_author_name(autor) for autor in autores]

        df_valid = df_vereadores[df_vereadores['ano_eleicao'] > int(ano) - 4]
        df_valid = df_valid[['nome_urna', 'nome', 'cpf']]

        for autor in autores:
            if autor in depara:
                continue
            
            # Alguns nomes estão exatamente iguais nos dados do TSE
            viable_names = df_valid[df_valid['nome_urna'] == autor]
            if not viable_names.empty and len(viable_names['cpf'].unique()) == 1:
                depara[autor] = (
                    viable_names['nome_urna'].iloc[0], 
                    viable_names['cpf'].iloc[0],
                    viable_names['nome'].iloc[0])
                continue

            # Caso não encontre nos dados do TSE, procura por partes do nome
            viable_names = df_valid.copy()
            for part in autor.split():
                part = part.replace('.', '')
                viable1 = df_valid['nome_urna'].apply(lambda nm_dep: part in nm_dep)
                viable2 = df_valid['nome'].apply(lambda nm_dep: part in nm_dep)
                if np.any(viable1) or np.any(viable2):
                    viable_names = viable_names[viable1 | viable2]

            if not viable_names.empty and len(viable_names['cpf'].unique()) == 1:
                depara[autor] = (
                    viable_names['nome_urna'].iloc[0], 
                    viable_names['cpf'].iloc[0],
                    viable_names['nome'].iloc[0])
    return depara

def get_names_not_in_depara(df_camara, depara):
    not_in_depara = set()
    for row in df_camara.iterrows():
        autores = clean_author_name(row[1]['autor'])
        autores = autores.split(',')
        autores = [autor.strip() for autor in autores]
        
        for autor in autores:
            if autor not in depara:
                not_in_depara.add(autor)
    return not_in_depara

def correct_depara(depara):
    # Adicionar nomes faltantes
    depara['DR. FERNANDO MORAES'] = ('FERNANDO MORAES', '78594200749', 'JOSE FERNANDO MORAES ALVES')
    depara['PROFESSOR ROGERIO ROCAL'] = ('ROGERIO ROCAL', '04555478746', 'ROGERIO DE CASTRO LOPES')
    depara['VAL CEASA'] = ('VAL', '02867827744', 'ROOSEVELT BARRETO BARCELOS')
    
    # Tirar nomes errados
    depara['MARCIO GARCIA'] = ('MARCIO GARCIA', '07668281746', 'MARCIO BARRETO DOS SANTOS GARCIA')
    depara['ALOISIO FREITAS'] = ('ALOISIO FREITAS', '23568380749', 'MANOEL ALOISIO FREITAS')
    
    del depara['COMISSAO DE CIENCIA TECNOLOGIA COMUNICACAO E INFORMATICA']


config = AutoConfig(search_path='.')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_HOST = config('POSTGRES_HOST')
POSTGRES_PORT = config('POSTGRES_PORT')
POSTGRES_DB = config('POSTGRES_DB')

engine = create_engine(
    f'postgresql://{POSTGRES_USER}@{POSTGRES_HOST}'
    f':{POSTGRES_PORT}/{POSTGRES_DB}')


df_projetos1720 = pd.read_csv('output/projetos_lei_1720.csv', ';')
df_projetos1316 = pd.read_csv('output/projetos_lei_1316.csv', ';')
df_projetos0912 = pd.read_csv('output/projetos_lei_0912.csv', ';')
projetos = pd.concat([df_projetos1720, df_projetos1316, df_projetos0912])

projetos.dropna(subset=['ementa', 'autor'], inplace=True)
projetos.drop_duplicates(subset=['lei', 'data_publicacao'], inplace=True)

projetos['nr_lei'] = projetos['lei'].apply(lambda x: x.split('/')[0])
projetos['ano'] = projetos['lei'].apply(lambda x: x.split('/')[1])
projetos.sort_values(['ano', 'nr_lei'], ascending=False, inplace=True)
projetos.drop(['nr_lei', 'ano'], axis=1, inplace=True)

projetos = projetos.rename({'lei': 'projeto'}, axis=1)

projetos = projetos[projetos['projeto'].apply(
    lambda x: int(x.split('/')[1]) >= 2009)]

df_leis = pd.read_csv('output/leis_ordinarias.csv', ';')

df_leis['nr_projeto'] = df_leis['inteiro_teor'].apply(
    extract_projeto, law_type='lei')

dfm = projetos.merge(
    df_leis[['lei', 'ano', 'status', 'nr_projeto']].astype(str), 
    how='left', 
    left_on='projeto', 
    right_on='nr_projeto')

dfm['status'] = dfm['status'].fillna('Não se aplica')
dfm = dfm.drop(['nr_projeto'], axis=1)


query = """
    select ano_eleicao, nome, nome_urna, cpf, sigla_partido, 
    descricao_cargo, descricao_ue, descricao_totalizacao_turno
    from eleitoral.candidatos
    where descricao_cargo = 'VEREADOR'
    and descricao_ue = 'RIO DE JANEIRO'
    and descricao_totalizacao_turno in (
        '2O TURNO', 'ELEITO POR MEDIA', 'ELEITO POR QP', 
        '2.O TURNO', 'MEDIA', 'ELEITO', 'SUPLENTE');
"""
df_tse = pd.read_sql(query, engine)


depara = create_depara(dfm, df_tse)
correct_depara(depara)
df_depara = pd.DataFrame(
    [[x[0], x[1][0], x[1][2], x[1][1]] for x in depara.items()], 
    columns=['nome_camara', 'nome_urna_tse', 'nome_tse', 'cpf'])


# Depara Vereadores Lupa
query = """
    select *
    from lupa.vereadores_rj
    where nm_municipio = 'RIO DE JANEIRO';
"""
df_lupa = pd.read_sql(query, engine)


# Adicionar nomes presentes no Lupa (e corrigir nomes faltantes) no depara
tse_to_lupa = {}
for row in df_lupa.iterrows():
    nome_vereador_lupa = row[1]['nome_vereador']
    nome_urna_lupa = row[1]['nome_vereador_urna']
    
    nm_formatted = unidecode(nome_vereador_lupa).upper()
    
    eq = df_depara[df_depara.nome_tse == nm_formatted]
    if not eq.empty:
        tse_to_lupa[eq.nome_tse.iloc[0]] = (nome_vereador_lupa, nome_urna_lupa)
        
tse_to_lupa['REIMONT LUIZ OTONI SANTA BARBARA'] = (
    'Reimont Luiz Otoni Santa Bárbar', 'Reimont')
tse_to_lupa['LEONEL BRIZOLA'] = (
    'Leonel Brizola Neto', 'Leonel Brizola')
tse_to_lupa['JOAO BATISTA OLIVEIRA DE ARAUJO'] = (
    'João Batista Oliveira de Araújo ', 'Babá')
tse_to_lupa['VERONICA CHAVES DE CARVALHO COSTA'] = (
    'Veronica Chaves de Carvalho Cost', 'Veronica Costa')

df_depara['nome_lupa'] = df_depara['nome_tse'].apply(
    lambda x: tse_to_lupa[x][0] if x in tse_to_lupa else None)
df_depara['nome_urna_lupa'] = df_depara['nome_tse'].apply(
    lambda x: tse_to_lupa[x][1] if x in tse_to_lupa else None)

# Salva Depara no Postgres
df_depara.to_sql(
    'depara_vereadores_camara_tse_lupa',
    engine,
    schema='eleitoral',
    index=False,
    if_exists='replace')