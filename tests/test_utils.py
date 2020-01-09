from unittest import TestCase

from leis_brasileiras.utils import (
    extract_projeto
)
from tests.fixtures import (
    string_projeto_lei_1, string_projeto_lei_2,
    string_projeto_leicomp_1, string_projeto_leicomp_2,
    string_projeto_decreto_1, string_projeto_emenda_1,
    string_projeto_emenda_2, string_no_projeto
)


class TestUtils(TestCase):
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
