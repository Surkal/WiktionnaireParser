import pytest

from wiktionnaireparser.utils import (
    get_languages, remove_sortkey, etymology_cleaner, filter_sections_id,
)

@pytest.mark.parametrize(
    "langs",
    [(["fr"]),
    (["fr", "en"]),
    (["jicaque d’El Palmar"]),
    (["lala (Afrique du Sud)", "fr", "nanga ira’"])],
)
def test_get_languages(langs):
    wikitext = ""
    for lang in langs:
        wikitext +="test \n== {{langue|%s}} ==\ntest" % lang
    assert get_languages(wikitext) == langs

@pytest.mark.parametrize(
    "input,output",
    [
        ("{{S|nom|sv|clé=gz⿕ng|num=3}} ", "{{S|nom|sv|num=3}} "),
        (" {{S|nom|sv|num=3}} ", " {{S|nom|sv|num=3}} "),
        (" {{S|nom|sv|num=3|clé=gz⿕ng}}", " {{S|nom|sv|num=3}}"),
    ]
)
def test_remove_sortkey(input, output):
    assert remove_sortkey(input) == output

@pytest.mark.parametrize(
    "input,output",
    [
        ('(Siècle à préciser) Composé de maitresse, de et conférence.', 'Composé de maitresse, de et conférence.'),
        ('Étymologie manquante ou incomplète. Si vous la connaissez, vous pouvez l’ajouter en cliquant ici.', ''),
        ('(Nom commun 3) Étymologie manquante ou incomplète. Si vous la connaissez, vous pouvez l’ajouter en cliquant ici.', '(Nom commun 3) Étymologie manquante ou incomplète. Si vous la connaissez, vous pouvez l’ajouter en cliquant ici.')
    ]
)
def test_etymology_cleaner(input, output):
    assert etymology_cleaner(input) == output

def test_filter_sections_id():
    sections = ['#Étymologie_10', '#Nom_commun_1', '#Nom_commun_2_2', '#Verbe_1', '#Verbe_2', '#Prononciation']
    useless = (
        r'Étymologie', r'Prononciation', r'Références', r'Voir_aussi',
    )
    assert filter_sections_id(sections, useless) == ['#Nom_commun_1', '#Nom_commun_2_2', '#Verbe_1', '#Verbe_2']
