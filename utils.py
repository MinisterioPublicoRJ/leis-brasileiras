import re
from unidecode import unidecode

def clean_author_name(x):
    x = unidecode(x)
    x = x.upper()
    x = re.sub(r'VEREADORA?', '', x)
    x = x.replace('.', '. ')
    x = re.sub('\s+', ' ', x)
    return x.strip()