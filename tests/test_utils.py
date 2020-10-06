import pytest

from ..utils import get_languages

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
