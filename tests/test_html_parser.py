import pytest
import requests
from unittest.mock import patch

from wiktionnaireparser import WiktionnaireParser


class TestWiktionnaireParser:
    @classmethod
    def setup_class(cls):
        with open('tests/vara.txt', 'r') as f:
            html = f.read()
        cls.page = WiktionnaireParser(html)

    def test_get_html_from_source(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value.content = self.page.html
            page_ = WiktionnaireParser.from_source('')
            assert page_.html == self.page.html

    def test_language_by_default(self):
        assert self.page.language == 'Français'

    @pytest.mark.parametrize(
        'language,etymology',
        [
            ('Français', 'De l’espagnol vara.'),
            ('Suédois', ''),
            ('Breton', ''),
            ('Portugais', 'Du latin vara.'),
            ('Same du Nord', ''),
            ('test', '')
        ]
    )
    def test_get_etymology(self, language, etymology):
        self.page.language = language
        assert self.page.get_etymology() == etymology

    def test_get_parts_of_speech(self):
        self.page.language = 'Suédois'
        result = {
            'Nom commun 1': {0: {'definition': 'Denrée, marchandise, produit.'}},
            'Nom commun 2': {0: {'definition': '(Philosophie) Être, existence.'}},
            'Verbe 1': {0: {'definition': 'Être.'}},
            'Verbe 2': {0: {'definition': 'Durer.'}, 1: {'definition': 'Suppurer.'}}
        }
        assert self.page.get_parts_of_speech() == result

    def test_get_word_data(self):
        assert self.page.get_word_data['etymologies'] == self.page.get_etymology()


class TestHTMLFromSource:
    @pytest.mark.parametrize(
        'title,oldid,part_of_speech,definitions',
        [
            ('vafsi', 28592326, 'Nom commun', {0: {'definition': 'Langue iranienne parlée dans le village de Vafs et ses environs dans la province de Markazi en Iran.'}}),
            ('maitresse de conférence', 28023166, 'Locution nominale', {0: {'definition': 'Variante orthographique de maitresse de conférences.'}}),
        ]
    )
    def test_get_definition(self, title, oldid, part_of_speech, definitions):
        page = WiktionnaireParser.from_source(title, oldid=oldid)
        data = page.get_parts_of_speech()
        assert data[part_of_speech] == definitions

    def test_random_page(self):
        assert WiktionnaireParser.random_page().get_title()
