from contextlib import contextmanager

import pytest

from wiktionnaireparser.utils import (
    etymology_cleaner, filter_sections_id, get_language_name
)


@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize(
    "input_,output",
    [
        ('(Siècle à préciser) Composé de maitresse, de et conférence.', 'Composé de maitresse, de et conférence.'),
        ('Étymologie manquante ou incomplète. Si vous la connaissez, vous pouvez l’ajouter en cliquant ici.', ''),
        ('(Nom commun 3) Étymologie manquante ou incomplète. Si vous la connaissez, vous pouvez l’ajouter en cliquant ici.', '(Nom commun 3) Étymologie manquante ou incomplète. Si vous la connaissez, vous pouvez l’ajouter en cliquant ici.')
    ]
)
def test_etymology_cleaner(input_, output):
    assert etymology_cleaner(input_) == output


def test_filter_sections_id():
    sections = ['#Étymologie_10', '#Nom_commun_1', '#Nom_commun_2_2', '#Verbe_1', '#Verbe_2', '#Prononciation']
    useless = (
        r'Étymologie', r'Prononciation', r'Références', r'Voir_aussi',
    )
    assert filter_sections_id(sections, useless) == ['#Nom_commun_1', '#Nom_commun_2_2', '#Verbe_1', '#Verbe_2']


@pytest.mark.parametrize(
    'code,lang,error',
    [
        ('fr', 'Français', does_not_raise()),
        ('sv', 'Suédois', does_not_raise()),
        ('azerty', '', pytest.raises(KeyError))
    ]
)
def test_get_language_name(code, lang, error):
    with error:
        assert get_language_name(code) == lang
