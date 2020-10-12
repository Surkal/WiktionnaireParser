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

    def test_language_setter(self):
        p = WiktionnaireParser(self.page.html, 'anglais')
        assert p.language == 'Anglais'
        p = WiktionnaireParser(self.page.html, 'Same du Nord')
        assert p.language == 'Same du Nord'

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
            'Nom commun 1': {0: {'definition': 'Denrée, marchandise, produit.'}, 'gender': 'commun', 'pronunciation': ['ˈvɑː.ˌra']},
            'Nom commun 2': {0: {'definition': '(Philosophie) Être, existence.'}, 'gender': 'neutre'},
            'Verbe 1': {0: {'definition': 'Être.'}, 'pronunciation': ['ˈvɑː.ˌra']},
            'Verbe 2': {0: {'definition': 'Durer.'}, 1: {'definition': 'Suppurer.'}, 'pronunciation': ['ˈvɑː.ˌra']}
        }
        assert self.page.get_parts_of_speech() == result

    def test_get_word_data(self):
        assert self.page.get_word_data['etymologies'] == self.page.get_etymology()


class TestHTMLFromSource:
    @pytest.mark.parametrize(
        'title,oldid,part_of_speech,definitions',
        [
            ('vafsi', 28592326, 'Nom commun', {0: {'definition': 'Langue iranienne parlée dans le village de Vafs et ses environs dans la province de Markazi en Iran.'}, 'gender': 'masculin', 'translations': {'Anglais': ['Vafsi'], 'Persan': ['وفسی'], 'Vafsi': ['ووسی']}}),
            ('maitresse de conférence', 28023166, 'Locution nominale', {0: {'definition': 'Variante orthographique de maitresse de conférences.'}, 'gender': 'féminin', 'pronunciation': ['mɛ.tʁɛs də kɔ̃.fe.ʁɑ̃s']}),
        ]
    )
    def test_get_definition(self, title, oldid, part_of_speech, definitions):
        page = WiktionnaireParser.from_source(title, oldid=oldid)
        data = page.get_parts_of_speech()
        assert data[part_of_speech] == definitions

    def test_random_page(self):
        assert WiktionnaireParser.random_page().get_title()

    def test_subsections(self):
        page = WiktionnaireParser.from_source('comète', oldid=28407934)
        assert len(page.sections_id) == 6
        assert len(page.sections_id['#Nom_commun']) == 9
        assert '#Synonymes' in page.sections_id['#Nom_commun']

    def test_messy_related_ords(self):
        page = WiktionnaireParser.from_source('merci', oldid=28604039)
        assert page.get_related_words('Synonymes') == {'Nom commun 1': ['grâce', 'miséricorde', 'pitié']}
        assert page.get_related_words('Dérivés') == {'Nom commun 1': ['sans merci', 'à la merci de'], 'Interjection': ['Dieu merci', 'grand merci', 'merci beaucoup', 'merci énormément', 'merci infiniment', 'mille mercis', 'non merci', 'remercier', 'remerciement', 'un grand merci']}
        # translations
        assert page.get_translations('#Traductions') == {'Allemand': ['Gnade'], 'Anglais': ['mercy'], 'Basque': ['eskerrik asko'], 'Bavarois': ['merci'], 'Bourguignon': ['marci'], 'Breton': ['trugarez'], 'Catalan': ['gràcia'], 'Danois': ['nåde'], 'Espagnol': ['gracia', 'merced'], 'Finnois': ['armo', 'sääli'], 'Grec': ['έλεος'], 'Italien': ['mercé'], 'Néerlandais': ['genade'], 'Occitan': ['mercés', 'mercé'], 'Picard': ['merchi'], 'Roumain': ['mersi'], 'Sarthois': ['marci'], 'Tourangeau': ['marci', 'marcit']}
        assert page.get_definitions('Nom commun') == {0: {'definition': 'Salaire, prix, récompense.', 'examples': {0: {'example': 'Dex te face pardon et si t’en rande merci et guerredon de cest courtois service. —\xa0(Jourdain de Blaive)'}}}, 1: {'definition': 'Faveur, grâce.', 'examples': {0: {'example': 'Au pié li vont la merci crïer\xa0: «\xa0Merci, frans quens, por Deu de majesté\xa0». —\xa0(Couronnement de Louis)'}}}, 2: {'definition': '(Par extension) Volonté, bon plaisir.', 'examples': {0: {'example': 'Erec l’anvoie a vos ci an prison, an vostre merci. —\xa0(Erec)'}}}, 3: {'definition': 'Pitié, miséricorde.', 'examples': {0: {'example': 'Par voz merciz un petit me soffrez. —\xa0(Charroi de Nîmes)'}}}, 4: {'definition': 'Remerciement.'}, 5: {'definition': 'Deu en rent graces et merci. (Béroul, Tristan).'}}

    def test_examples(self):
        page = WiktionnaireParser.from_source('föra', oldid=28301121)
        assert page.get_definitions('Verbe') == {0: {'definition': 'Conduire, mener, diriger, amener.', 'examples': {0: {'example': 'Föra en dam till bordet.', 'translation': 'Conduire une dame à table.'}, 1: {'example': 'Föra trupperna till seger.', 'translation': 'Conduire des troupes à la victoire.'}, 2: {'example': 'Föra i ledband.', 'translation': 'Mener en laisse.'}, 3: {'example': 'Föra ett land till branten av undergång.', 'translation': 'Mener un pays à sa perte.'}, 4: {'example': 'Detta brott förde honom till galgen.', 'translation': 'Ce crime le conduisit à la potence.'}, 5: {'example': 'En rymdfarkost inriktad på att föra en människa i omloppsbana runt jorden.', 'translation': 'Un vaisseau spatial ajusté pour amener un homme en orbite autour de la terre.'}}}}

    def test_pronunciation(self):
        page = WiktionnaireParser.from_source('moins', oldid=28516602)
        data = page.get_word_data
        assert data['partOfSpeech']['Adverbe']['pronunciation'] == ['mwɛ̃', 'mwɛ̃s']
        assert data['partOfSpeech']['Adverbe']['gender'] == 'invariable'
        assert data['partOfSpeech']['Conjonction']['pronunciation'] == ['mwɛ̃']
        assert data['partOfSpeech']['Conjonction']['gender'] == 'invariable'
