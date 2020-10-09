import pytest

from wiktionnaireparser.utils import get_languages, remove_sortkey

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
