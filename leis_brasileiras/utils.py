import re


def extract_projeto(s, law_type=None):
    clean_s = s.replace('.', '').replace("//", "/")
    clean_s = re.sub(r'\s', '', clean_s)
    if law_type == 'lei':
        m = re.search(
            r'(ProjetodeLei|ProjLei)'
            r'(nº)?(\d+)\-?\w?(/|,de|de)(\d+)',
            clean_s)
    elif law_type == 'lei_comp':
        m = re.search(
            r'(ProjetodeLei|ProjLei)Complementar'
            r'(nº)?(\d+)\-?\w?(/|,de|de|)(\d+)',
            clean_s)
    elif law_type == 'decreto':
        m = re.search(
            r'(ProjetodeDecretoLegislativo|ProjDecretoLegislativo)'
            r'(nº)?(\d+)\-?\w?(/|,de|de|)(\d+)',
            clean_s)
    elif law_type == 'emenda':
        m = re.search(
            r'(ProjetodeEmendaàLeiOrgânica|PropostadeEmenda)'
            r'(nº)?(\d+)\-?\w?(/|,de|de|)(\d+)',
            clean_s)
    else:
        m = None
    if m:
        nr = m.group(3).zfill(4)
        ano = m.group(5)
        return '{}/{}'.format(nr, ano)
    return ''
