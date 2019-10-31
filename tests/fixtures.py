# Fixtures clean_author_name

author_name_1 = 'Vereador  Dr.Fulâno '
expected_author_name_1 = 'DR. FULANO'

author_name_2 = 'Vereadora Coisinha'
expected_author_name_2 = 'COISINHA'

# Fixtures expand_results

names_dict = [
    {'col1': 1, 'col2': 'nome1,nome2'},
    {'col1': 2, 'col2': 'nome1'}
]
expected_expanded_names_dict = [
    {'col1': 1, 'col2': 'nome1'},
    {'col1': 1, 'col2': 'nome2'},
    {'col1': 2, 'col2': 'nome1'}
]

# Fixtures get_from_depara

depara = [
    {'nome_camara': 'DR. FULANO', 'nome_outro': 'FULANO'}
]

# Fixtures extract_projeto

string_projeto_lei_1 = 'Projeto de Lei nº 231A/2019'
string_projeto_lei_2 = 'Proj. Lei nº 231-A, de 2019'
string_projeto_leicomp_1 = 'Projeto de Lei Complementar 231 de 2019'
string_projeto_leicomp_2 = 'Proj. Lei Complementar 231/2019'
string_projeto_decreto_1 = 'Projeto de Decreto Legislativo 231 de 2019'
string_projeto_emenda_1 = 'Projeto de Emenda à Lei Orgânica 231 de 2019'
string_projeto_emenda_2 = 'Proposta de Emenda nº 231, de 2019'
string_no_projeto = 'Sem projeto'
