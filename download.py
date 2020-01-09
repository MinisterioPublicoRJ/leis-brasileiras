import contextlib
import os

from leis_brasileiras.leis import (
    DecretosCamaraMunicipalRJ,
    ProjetosDeDecretoCamaraMunicipalRJ1720,
    ProjetosDeDecretoCamaraMunicipalRJ1316,
    ProjetosDeDecretoCamaraMunicipalRJ0912,
    EmendasLeiOrganicaCamaraMunicipalRJ,
    ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ1720,
    ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ1316,
    ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ0912,
    LeisOrdinariasCamaraMunicipalRJ,
    ProjetosDeLeiCamaraMunicipalRJ0912,
    ProjetosDeLeiCamaraMunicipalRJ1316,
    ProjetosDeLeiCamaraMunicipalRJ1720,
    LeisComplementaresCamaraMunicipalRJ,
    ProjetosDeLeiComplementarCamaraMunicipalRJ1720,
    ProjetosDeLeiComplementarCamaraMunicipalRJ1316,
    ProjetosDeLeiComplementarCamaraMunicipalRJ0912

)


OUTPUT_FOLDER = 'output'
with contextlib.suppress(FileExistsError):
    os.mkdir(OUTPUT_FOLDER)

docs = [
    DecretosCamaraMunicipalRJ(
        f'{OUTPUT_FOLDER}/decretos.csv'),
    ProjetosDeDecretoCamaraMunicipalRJ1720(
        f'{OUTPUT_FOLDER}/projetos_decreto_1720.csv'),
    ProjetosDeDecretoCamaraMunicipalRJ1316(
        f'{OUTPUT_FOLDER}/projetos_decreto_1316.csv'),
    ProjetosDeDecretoCamaraMunicipalRJ0912(
        f'{OUTPUT_FOLDER}/projetos_decreto_0912.csv'),
    EmendasLeiOrganicaCamaraMunicipalRJ(
        f'{OUTPUT_FOLDER}/emendas_lei_organica.csv'),
    ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ1720(
        f'{OUTPUT_FOLDER}/projetos_emenda_lei_organica_1720.csv'),
    ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ1316(
        f'{OUTPUT_FOLDER}/projetos_emenda_lei_organica_1316.csv'),
    ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ0912(
        f'{OUTPUT_FOLDER}/projetos_emenda_lei_organica_0912.csv'),
    LeisOrdinariasCamaraMunicipalRJ(
        f'{OUTPUT_FOLDER}/leis_ordinarias.csv'),
    ProjetosDeLeiCamaraMunicipalRJ0912(
        f'{OUTPUT_FOLDER}/projetos_lei_0912.csv'),
    ProjetosDeLeiCamaraMunicipalRJ1316(
        f'{OUTPUT_FOLDER}/projetos_lei_1316.csv'),
    ProjetosDeLeiCamaraMunicipalRJ1720(
        f'{OUTPUT_FOLDER}/projetos_lei_1720.csv'),
    LeisComplementaresCamaraMunicipalRJ(
        f'{OUTPUT_FOLDER}/leis_complementares.csv'),
    ProjetosDeLeiComplementarCamaraMunicipalRJ1720(
        f'{OUTPUT_FOLDER}/projetos_lei_complementares_1720.csv'),
    ProjetosDeLeiComplementarCamaraMunicipalRJ1316(
        f'{OUTPUT_FOLDER}/projetos_lei_complementares_1316.csv'),
    ProjetosDeLeiComplementarCamaraMunicipalRJ0912(
        f'{OUTPUT_FOLDER}/projetos_lei_complementares_0912.csv'),
]

for doc in docs:
    doc.download()
