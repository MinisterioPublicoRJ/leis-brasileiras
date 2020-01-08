urls_decretos_planalto = {
    '2019': 'decretos1/2019-decretos',
    '2018': 'decretos1/2018-decretos/2018-decretos',
    '2017': 'decretos1/2017-decretos',
    '2016': 'decretos1/2016-decretos',
    '2015': 'decretos1/2015-decretos-1',
    '2014': 'decretos1/2014-decretos-1',
    '2013': 'decretos1/2013-decretos-2',
    '2012': 'decretos1/2012-decretos-2',
    '2011': 'decretos1/2011-decretos-2',
    '2010': 'decretos1/2010-decretos-1',
    '2009': 'decretos1/2009-decretos',
    '2008': 'decretos1/2008-decretos',
    '2007': 'decretos1/2007-decretos',
    '2006': 'decretos1/2006-decretos',
    '2005': 'decretos1/2005-decretos-1',
    '2004': 'decretos1/2004-decretos-1',
    '2003': 'decretos1/2003-decretos',
    '2002': 'decretos1/2002-decretos-1',
    '2001': 'decretos1/2001-decretos',
    '2000': 'decretos1/2000-decretos-1',
    '1999': 'decretos1/1999-decretos-2',
    '1998': 'decretos1/1998-decretos-1',
    '1997': 'decretos1/1997-decretos',
    '1996': 'decretos1/1996-decretos',
    '1995': 'decretos1/1995-decretos',
    '1994': 'decretos1/1994-decretos-1',
    '1993': 'decretos1/1993-decretos-1',
    '1992': 'decretos1/1992-decretos',
    '1991': 'decretos1/1991-decretos',
    '1990': 'decretos1/1990-decretos-1',
    '1989': 'decretos1/1989-decretos',
    '1988': 'decretos1/1988-decretos-1',
    '1987': 'decretos1/1987-decretos-1',
    '1986': 'decretos1/1986-decretos-1',
    '1985': 'decretos1/1985-decretos-1',
    '1984': 'decretos1/1984-decretos-1',
    '1983': 'decretos1/1983-decretos-1',
    '1982': 'decretos1/1982-decretos',
    '1981': 'decretos1/1981-decretos-1',
    '1980': 'decretos1/1980-decretos-1',
    '1970-1979': 'decretos1/1979-a-1970-decretos-1',
    '1960-1969': 'decretos1/1969-a-1960-decretos-1',
    'anterior-1960': 'decretos1/anteriores-a-1960-decretos'
}

urls_leis_ordinarias_planalto = {
    '2019': 'leis-ordinarias/2019-leis-ordinarias',
    '2018': 'leis-ordinarias/2018-leis-ordinarias',
    '2017': 'leis-ordinarias/2017-leis-ordinarias',
    '2016': 'leis-ordinarias/leis-ordinarias-2016',
    '2015': 'leis-ordinarias/leis-ordinarias-2015',
    '2014': 'leis-ordinarias/2014-leis-ordinarias',
    '2013': 'leis-ordinarias/2013-leis-ordinarias',
    '2012': 'leis-ordinarias/2012-leis-ordinarias-2',
    '2011': 'leis-ordinarias/2011-leis-ordinarias',
    '2010': 'leis-ordinarias/2010-leis-ordinarias-1',
    '2009': 'leis-ordinarias/2009-leis-ordinarias-1',
    '2008': 'leis-ordinarias/2008-leis-ordinarias-1',
    '2007': 'leis-ordinarias/2007-leis-ordinarias-1',
    '2006': 'leis-ordinarias/2006-leis-ordinarias-1',
    '2005': 'leis-ordinarias/2005',
    '2004': 'leis-ordinarias/2004',
    '2003': 'leis-ordinarias/2003',
    '2002': 'leis-ordinarias/2002-leis-ordinarias-1',
    '2001': 'leis-ordinarias/2001-leis-ordinarias-1',
    '2000': 'leis-ordinarias/2000-leis-ordinarias-1',
    '1999': 'leis-ordinarias/1999-leis-ordinarias-1',
    '1998': 'leis-ordinarias/1998-leis-ordinarias',
    '1997': 'leis-ordinarias/1997-leis-ordinarias-1',
    '1996': 'leis-ordinarias/1996',
    '1995': 'leis-ordinarias/1995',
    '1994': 'leis-ordinarias/1994',
    '1993': 'leis-ordinarias/1993',
    '1992': 'leis-ordinarias/1992',
    '1991': 'leis-ordinarias/1991',
    '1990': 'leis-ordinarias/1990',
    '1989': 'leis-ordinarias/1989',
    '1988': 'leis-ordinarias/1988',
    '1981-1987': 'leis-ordinarias/1987-a-1981-leis-ordinarias',
    '1960-1980': 'leis-ordinarias/1980-a-1960-leis-ordinarias',
    'anterior-1960': 'leis-ordinarias/anteriores-a-1960-leis-ordinarias'
}

urls_medidas_provisorias = {
    '2019-2022': 'medidas-provisorias/2019-a-2022',
    '2015-2018': 'medidas-provisorias/medidas-provisorias-2015-a-2018',
    '2011-2014': 'medidas-provisorias/2011-a-2014',
    '2007-2010': 'medidas-provisorias/2007-a-2010',
    '2003-2006': 'medidas-provisorias/2003-a-2006',
    '2001-2002': 'medidas-provisorias/2001-e-2002',
    '2000-2001': 'medidas-provisorias/2000-e-2001',
    '1996-1999': 'medidas-provisorias/1996-a-1999',
    '1992-1995': 'medidas-provisorias/1992-a-1995',
    '1988-1991': 'medidas-provisorias/1988-a-1991'
}

urls_projetos_leis_casa_civil = {
        **{2019: 'copy_of_pl-2019'},
        **{year: 'pl-{0}'.format(year) for year in range(2018, 1993, -1)}
}
urls_projetos_leis_complementares_casa_civil = {
    **{2019: 'plp-2019'},
    **{year: 'plp-{0}'.format(year) for year in range(2017, 1997, -1)}
}
urls_projetos_leis_congresso_casa_civil = {
    **{2019: 'pln-2019', 2018: 'pln-2018-1'},
    **{year: 'pln-{0}'.format(year) for year in range(2017, 2011, -1)}
}
