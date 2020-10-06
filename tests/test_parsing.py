import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch

from ..parsing import Page


wikitext = """== {{langue|fr}} ==\n=== {{S|étymologie}} ===\n: Du {{étyl|la|fr|mot=implico|dif=implicāre|sens=impliquer}}.\n\n=== {{S|verbe|fr}} ===\n'''employer''' {{pron|ɑ̃.plwa.je|fr}} {{t|fr}} {{conj|grp=1|fr}} {{lien pronominal|'}}\n# [[utiliser|Utiliser]] ; [[user]] ; se [[servir]] de.\n#* ''Le sucre était connu des anciens qui ne l’'''employaient''' qu'en très-petite quantité et comme médicament ; il y a 200 ans à peine, il se vendait seulement chez les pharmaciens, à un prix très-élevé.'' {{source|{{Citation/Edmond Nivoit/Notions élémentaires sur l’industrie dans le département des Ardennes/1869|119}}}}\n#* ''On sait que l’emploi du fer fut inconnu de toute l’Amérique avant l’arrivée de Colomb. […]. Parfois cependant le fer météorique '''est employé''' accidentellement.'' {{source|{{w|René Thévenin}} & {{w|Paul Coze}}, ''Mœurs et Histoire des Indiens Peaux-Rouges'', Payot, 1929, 2{{e}} éd., p.18}}\n#* ''Tant qu’il n’était pas appelé au loin par la guerre contre les Saxons, les Bretons, ou les Goths de la Septimanie, Chlother '''employait''' son temps à se promener d’un domaine à l’autre.'' {{source|{{w|Augustin Thierry}}, ''Récits des temps mérovingiens'', 1{{er}} récit : ''Les quatre fils de Chlother Ier — Leur caractère — Leurs mariages — Histoire de Galeswinthe (561-568)'', 1833–1837}}\n#* ''Ces cartouches sont destinées à remplacer les fortes charges de poudre-éclair qu'il serait nécessaire d’'''employer''' pour l’éclairage intensif d'intérieurs, de grottes, de mines, etc., […].'' {{source|''Agenda Lumière 1930'', Paris : Société Lumière & librairie Gauthier-Villars, page 413}}\n#* ''La Sandaraque impure des marchés arabes provient du Thuya et de divers Juniperus. On l’'''emploie''' en poudre pour arrêter les petites hémorragies de l’épistaxis.'' {{source|''Bulletin des sciences pharmacologiques'', 1921, vol. 28, page 23}}\n# {{spéc}} {{lexique|grammaire|fr}} S’en servir en parlant ou en écrivant, en parlant d'une phrase, d'un mot ou d'une locution.\n#* '''''Employer''' les termes propres, les tours les plus élégants.''\n# [[pourvoir|Pourvoir]] d’une [[occupation]] ou d’un [[travail]] pour son [[usage]] ou pour son [[profit]].\n#* ''Une seule usine, '''employant''' une vingtaine d'ouvriers, existe à Vatan et la main-d’œuvre masculine, hormis celle du bâtiment, se voit contrainte d'aller travailler dans les villes voisines.'' {{source|Marc Michon, ''Petite histoire de Vatan'', impr. Lecante, 1971, page 57}}\n#* ''On l’a employé dans de grandes affaires, à de grandes négociations.''\n#* ''C’est un homme qui mérite d’être employé.''\n#* ''Il est employé dans les bureaux de tel ministère.''\n\n==== {{S|apparentés}} ====\n{{(}}\n* [[désemployer]]\n* [[emploi]]\n* [[employé]]\n* [[employeur]]\n* [[réemploi]]\n* [[remploi]]\n* [[réemployer]]\n* [[s’employer]]\n* [[sous-employer]]\n* [[suremployer]]\n{{)}}\n\n==== {{S|traductions}} ====\n{{trad-début|Utiliser}}\n* {{T|af}} : {{trad+|af|gebruik}}, {{trad-|af|benut}}, {{trad-|af|benuttig}}\n* {{T|de}} : {{trad+|de|benutzen}}, {{trad+|de|anwenden}}, {{trad+|de|brauchen}}, <br />{{trad+|de|gebrauchen}}, {{trad+|de|verwenden}}, {{trad+|de|verwerten}}\n* {{T|en}} : {{trad+|en|employ}}, {{trad+|en|use}}, {{trad+|en|make use of}}, {{trad-|en|turn to account}}\n* {{T|ca}} : {{trad+|ca|emprar}}\n* {{T|co}} : {{trad-|co|impiicà}}, {{trad+|co|usà}}, {{trad-|co|servesi}}\n* {{T|da}} : {{trad+|da|benytte}}, {{trad+|da|bruge}}, {{trad-|da|tilbringe}}\n* {{T|es}} : {{trad+|es|usar}}, {{trad+|es|emplear}}\n* {{T|eo}} : {{trad+|eo|uzi}}\n* {{T|fo}} : {{trad-|fo|nýta}}\n* {{T|fi}} : {{trad+|fi|käyttää}}\n* {{T|fy}} : {{trad+|fy|brûke}}\n* {{T|gallo}} : {{trad--|gallo|alouer}}\n* {{T|hu}} : {{trad+|hu|alkalmaz}}, {{trad+|hu|használ}}\n* {{T|io}} : {{trad+|io|uzar}}, {{trad+|io|employar}}\n* {{T|is}} : {{trad-|is|brúka}}, {{trad+|is|nota}}\n* {{T|it}} : {{trad+|it|impiegare}}, {{trad+|it|usare}}\n* {{T|la}} : {{trad-|la|uti}}\n* {{T|ms}} : {{trad-|ms|gunakan}}, {{trad-|ms|menggunakan}}\n* {{T|nl}} : {{trad+|nl|aanwenden}}, {{trad+|nl|benutten}}, {{trad+|nl|gebruiken}}\n* {{T|oc}} : {{trad+|oc|emplegar}}\n* {{T|pap}} : {{trad--|pap|usa}}, {{trad--|pap|uza}}\n* {{T|pl}} : {{trad+|pl|używać}}\n* {{T|pt}} : {{trad+|pt|empregar}}, {{trad-|pt|servir-se de}}, {{trad+|pt|usar}}, {{trad+|pt|despender}}\n* {{T|ro}} : {{trad+|ro|folosi}}\n* {{T|ru}} : {{trad+|ru|использовать}}\n* {{T|sv}} : {{trad+|sv|använda}}, {{trad+|sv|begagna}}, {{trad+|sv|bruka}}\n* {{T|tl}} : {{trad-|tl|gamítin}}\n* {{T|cs}} : {{trad-|cs|zaměstnat}}\n* {{T|tr}} : {{trad+|tr|kullanmak}}\n* {{T|vi}} : {{trad+|vi|dùng}}\n* {{T|wa}} : {{trad+|wa|eployî}}\n* {{T|zu}} : {{trad-|zu|-sebenzisa}}\n{{trad-fin}}\n\n{{trad-début|Donner un métier}}\n* {{T|de}} : {{trad+|de|anstellen}}, {{trad+|de|einstellen}}\n* {{T|gallo}} : {{trad--|gallo|alouer}}\n* {{T|nl}} : {{trad+|nl|tewerkstellen}}\n* {{T|no}} : {{trad-|no|ansette}}, {{trad-|no|tilsette}}\n{{trad-fin}}\n\n=== {{S|prononciation}} ===\n* {{pron|ɑ̃.plwa.je|fr}}\n* {{écouter|lang=fr|France <!-- précisez svp la ville ou la région -->|ɑ̃.plwa.je|audio=Fr-employer.ogg}}\n* {{écouter|lang=fr|France (Toulouse)||audio=LL-Q150 (fra)-Lepticed7-employer.wav}}\n\n== {{langue|en}} ==\n=== {{S|étymologie}} ===\n: {{composé de|m=1|employ|-er|lang=en}}.\n\n=== {{S|nom|en}} ===\n{{en-nom-rég}}\n'''employer''' {{pron|ɛm.ˈplɔ.jər|en}}\n# [[employeur|Employeur]].\n\n==== {{S|antonymes}} ====\n* {{lien|employee|en}}\n\n=== {{S|voir aussi}} ===\n* {{WP|lang=en}}"""


class MockResponse:
    @staticmethod
    def json():
        return {'parse': {'wikitext': {'*': wikitext}}}


class TestParsing:
    @classmethod
    def setup_class(cls):
        cls.page = Page(wikitext)
        cls.monkeypatch = MonkeyPatch()

    @pytest.mark.parametrize(
        "lang,i,text_length",
        [('fr', 0, 5092),
        ('en', 1, 281)]
    )
    def test_get_language_section_text_length(self, lang, i, text_length):
        assert len(self.page.all_sections[i].section) == text_length

    @pytest.mark.parametrize(
        "lang,etymology,typ",
        [("fr", ": Du {{étyl|la|fr|mot=implico|dif=implicāre|sens=impliquer}}.\n\n", str),
        ("en", ": {{composé de|m=1|employ|-er|lang=en}}.\n\n", str),
        ("it", None, type(None)),
        (None, [": Du {{étyl|la|fr|mot=implico|dif=implicāre|sens=impliquer}}.\n\n", ": {{composé de|m=1|employ|-er|lang=en}}.\n\n"], list),]
    )
    def test_get_etymology(self, lang, etymology, typ):
        result = self.page.get_etymology(lang=lang)
        assert result == etymology
        assert isinstance(result, typ)

    def test_language_sections(self):
        assert len(self.page.all_sections) == 2
        assert str(self.page.all_sections[0]) == "_LanguageSection fr"
        assert str(self.page.all_sections[1]) == "_LanguageSection en"

    def test_query_from_api(self):
        def mock_get(*args, **kwargs):
            return MockResponse()

        self.monkeypatch.setattr(requests, "get", mock_get)

        page = Page.from_api("")
        assert page.get_etymology(lang="en") == ": {{composé de|m=1|employ|-er|lang=en}}.\n\n"
