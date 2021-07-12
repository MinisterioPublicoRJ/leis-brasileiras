from leis_brasileiras.leis import (
    EmendasLeiOrganicaCamaraMunicipalRJ as emendas,
    DecretosCamaraMunicipalRJ as decretos,
    LeisOrdinariasCamaraMunicipalRJ as leis,
    LeisComplementaresCamaraMunicipalRJ as comp,
    ResolucoesPlenariasCamaraMunicipalRJ as res,
    # 21-24
    ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ2124 as proj_emendas_2124,
    ProjetosDeLeiCamaraMunicipalRJ2124 as proj_leis_2124,
    ProjetosDeLeiComplementarCamaraMunicipalRJ2124 as proj_comp_2124,
    ProjetosDeDecretoCamaraMunicipalRJ2124 as proj_decretos_2124,
    ProjetosResolucaoCamaraMunicipalRJ2124 as proj_res_2124,
    IndicacoesCamaraMunicipalRJ2124 as ind_2124,
    MocoesCamaraMunicipalRJ2124 as mocoes_2124,
    RequerimentoInformacaoCamaraMunicipalRJ2124 as reqinf_2124,
    RequerimentoCamaraMunicipalRJ2124 as req_2124,
    OficioCamaraMunicipalRJ2124 as oficio_2124,
    OficioDenunciaCamaraMunicipalRJ2124 as oficio_denuncia_2124,
    OficioOutrosCamaraMunicipalRJ2124 as oficio_outros_2124,
    OficioEditalCamaraMunicipalRJ2124 as oficio_edital_2124,
    OficioQuestaoOrdemCamaraMunicipalRJ2124 as oficio_ordem_2124,
    OficioParecerNormativoCJRCamaraMunicipalRJ2124 as oficio_cjr_2124,
    OficioRecursoCamaraMunicipalRJ2124 as oficio_recurso_2124,
    OficioRepresentacaoCamaraMunicipalRJ2124 as oficio_representacao_2124,
    # 17-20
    ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ1720 as proj_emendas_1720,
    ProjetosDeLeiCamaraMunicipalRJ1720 as proj_leis_1720,
    ProjetosDeLeiComplementarCamaraMunicipalRJ1720 as proj_comp_1720,
    ProjetosDeDecretoCamaraMunicipalRJ1720 as proj_decretos_1720,
    ProjetosResolucaoCamaraMunicipalRJ1720 as proj_res_1720,
    IndicacoesCamaraMunicipalRJ1720 as ind_1720,
    MocoesCamaraMunicipalRJ1720 as mocoes_1720,
    RequerimentoInformacaoCamaraMunicipalRJ1720 as reqinf_1720,
    RequerimentoCamaraMunicipalRJ1720 as req_1720,
    OficioCamaraMunicipalRJ1720 as oficio_1720,
    OficioDenunciaCamaraMunicipalRJ1720 as oficio_denuncia_1720,
    OficioOutrosCamaraMunicipalRJ1720 as oficio_outros_1720,
    OficioEditalCamaraMunicipalRJ1720 as oficio_edital_1720,
    OficioQuestaoOrdemCamaraMunicipalRJ1720 as oficio_ordem_1720,
    OficioParecerNormativoCJRCamaraMunicipalRJ1720 as oficio_cjr_1720,
    OficioRecursoCamaraMunicipalRJ1720 as oficio_recurso_1720,
    OficioRepresentacaoCamaraMunicipalRJ1720 as oficio_representacao_1720,
    # 13-16
    ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ1316 as proj_emendas_1316,
    ProjetosDeLeiCamaraMunicipalRJ1316 as proj_leis_1316,
    ProjetosDeLeiComplementarCamaraMunicipalRJ1316 as proj_comp_1316,
    ProjetosDeDecretoCamaraMunicipalRJ1316 as proj_decretos_1316,
    # 09-12
    ProjetosDeEmendasLeiOrganicaCamaraMunicipalRJ0912 as proj_emendas_0912,
    ProjetosDeLeiCamaraMunicipalRJ0912 as proj_leis_0912,
    ProjetosDeLeiComplementarCamaraMunicipalRJ0912 as proj_comp_0912,
    ProjetosDeDecretoCamaraMunicipalRJ0912 as proj_decretos_0912
)

output_folder = 'raw_data_cmrj'

lista_documentos = [
    # emendas(f'{output_folder}/emendas.csv'),
    # decretos(f'{output_folder}/decretos.csv'),
    # leis(f'{output_folder}/leis.csv'),
    # comp(f'{output_folder}/leis_complementares.csv'),
    # res(f'{output_folder}/resolucoes.csv'),
    proj_emendas_2124(f'{output_folder}/proj_emendas_2124.csv'),
    proj_leis_2124(f'{output_folder}/proj_leis_2124.csv'),
    proj_comp_2124(f'{output_folder}/proj_leis_complementares_2124.csv'),
    proj_decretos_2124(f'{output_folder}/proj_decretos_2124.csv'),
    proj_res_2124(f'{output_folder}/proj_res_2124.csv'),
    ind_2124(f'{output_folder}/indicacoes_2124.csv'),
    mocoes_2124(f'{output_folder}/mocoes_2124.csv', False),
    reqinf_2124(f'{output_folder}/requerimentos_informacao_2124.csv'),
    req_2124(f'{output_folder}/requerimentos_2124.csv'),
    oficio_2124(f'{output_folder}/oficios_2124.csv'),
    oficio_denuncia_2124(f'{output_folder}/oficios_denuncia_2124.csv'),
    oficio_outros_2124(f'{output_folder}/oficios_outros_2124.csv'),
    oficio_edital_2124(f'{output_folder}/oficios_edital_2124.csv'),
    oficio_ordem_2124(f'{output_folder}/oficios_ordem_2124.csv'),
    oficio_cjr_2124(f'{output_folder}/oficios_cjr_2124.csv'),
    oficio_recurso_2124(f'{output_folder}/oficios_recurso_2124.csv'),
    oficio_representacao_2124(f'{output_folder}/oficios_representacao_2124.csv'),
]

for d in lista_documentos:
    print(d)
    d.download()
