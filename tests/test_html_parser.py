import pytest
import requests
from unittest.mock import patch

from wiktionnaireparser import WiktionnaireParser



class TestWiktionnaireParser:
    @classmethod
    def setup_class(cls):
        with open('tests/vara.html', 'r') as f:
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
        'raw,clean',
        [
            ('Verbe_1', 'Verbe'),
            ('Verbe_2_2', 'Verbe 2'),
            ('Verbe_2', 'Verbe 2'),
            ('Nom_commun_1', 'Nom commun'),
            ('Nom_commun_2_2', 'Nom commun 2'),
        ]
    )
    def test_beautify_section_name(self, raw, clean):
        assert self.page._beautify_section_name(raw) == clean

    def test_filter_sections_id(self):
        sections = ['#Étymologie_10', '#Nom_commun_1', '#Nom_commun_2_2', '#Verbe_1', '#Verbe_2', '#Prononciation']
        useless  = ('Étymologie', 'Prononciation', 'Références')
        assert self.page._filter_sections_id(sections, useless) == ['#Nom_commun_1', '#Nom_commun_2_2', '#Verbe_1', '#Verbe_2']

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
            'Nom commun': ['Denrée, marchandise, produit.'],
            'Nom commun 2': ['(Philosophie) Être, existence.'],
            'Verbe': ['Être.'],
            'Verbe 2': ['Durer.', 'Suppurer.']
        }
        assert self.page.get_parts_of_speech() == result

    def test_get_word_data(self):
        assert self.page.get_word_data['etymologies'] == self.page.get_etymology()
