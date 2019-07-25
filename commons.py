import re


def striphtml(html):
    p = re.compile(r'<.*?>')
    return p.sub('', html)
