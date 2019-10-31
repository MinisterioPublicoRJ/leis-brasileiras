import pandas as pd
from unittest import TestCase
from pandas.testing import assert_frame_equal

from leis_brasileiras.utils import (
    clean_author_name,
    expand_results,
    extract_projeto,
    get_from_depara
)
from tests.fixtures import (
    author_name_1, expected_author_name_1,
    author_name_2, expected_author_name_2,
    names_dict, expected_expanded_names_dict,
    depara,
    string_projeto_lei_1, string_projeto_lei_2,
    string_projeto_leicomp_1, string_projeto_leicomp_2,
    string_projeto_decreto_1, string_projeto_emenda_1,
    string_projeto_emenda_2, string_no_projeto
)


class TestUtils(TestCase):
    def test_clean_author_name(self):
        output_1 = clean_author_name(author_name_1)
        output_2 = clean_author_name(author_name_2)

        assert expected_author_name_1 == output_1
        assert expected_author_name_2 == output_2

    def test_expand_results(self):
        df_input = pd.DataFrame(names_dict)
        df_expected = pd.DataFrame(expected_expanded_names_dict)

        output = expand_results(df_input, ['col2'])

        assert_frame_equal(output, df_expected)

    def test_get_from_depara(self):
        nome_1 = 'DR. FULANO'
        nome_2 = 'PESSOA'

        df_depara = pd.DataFrame(depara)

        output_1 = get_from_depara(nome_1, df_depara, 'nome_outro')
        output_2 = get_from_depara(nome_2, df_depara, 'nome_outro')

        assert output_1 == 'FULANO'
        assert output_2 is None

    def test_extract_projeto(self):
        expected = '0231/2019'

        output_1 = extract_projeto(string_projeto_lei_1, 'lei')
        output_2 = extract_projeto(string_projeto_lei_2, 'lei')
        output_3 = extract_projeto(string_projeto_leicomp_1, 'lei_comp')
        output_4 = extract_projeto(string_projeto_leicomp_2, 'lei_comp')
        output_5 = extract_projeto(string_projeto_decreto_1, 'decreto')
        output_6 = extract_projeto(string_projeto_emenda_1, 'emenda')
        output_7 = extract_projeto(string_projeto_emenda_2, 'emenda')
        output_8 = extract_projeto(string_no_projeto, 'lei')
        output_9 = extract_projeto(string_no_projeto, law_type=None)

        assert expected == output_1
        assert expected == output_2
        assert expected == output_3
        assert expected == output_4
        assert expected == output_5
        assert expected == output_6
        assert expected == output_7
        assert '' == output_8
        assert '' == output_9


    