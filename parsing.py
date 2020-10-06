import re
import json

import requests
import wikitextparser as wtp

from utils import get_languages


API_QUERY = "https://fr.wiktionary.org/w/api.php?\
             action=parse&prop=wikitext&format=json&page="


class Page:
    all_sections = []

    def __init__(self, wikitext):
        self.wikitext = wikitext
        self._parse()

    def _parse(self):
        self.parsed = wtp.parse(self.wikitext)
        self.langs = get_languages(self.wikitext)
        self._language_sections()

    def _language_sections(self):
        for lang in self.langs:
            _LanguageSection(self.wikitext, self.parsed, lang)

    def get_etymology(self, lang=None):
        if lang:
            for section in self.all_sections:
                if section.lang == lang and section.etymology:
                    return section.etymology.contents
            return
        return [section.etymology.contents for section in self.all_sections]

    @classmethod
    def from_api(cls, title):
        query = API_QUERY + title
        response = requests.get(query)
        js = json.loads(response.text)
        wikitext = js['parse']['wikitext']['*']
        return cls(wikitext)


class _LanguageSection(Page):
    def __init__(self, wikitext, parsed, lang):
        self.parsed = parsed
        self.lang = lang
        self.section = self._extract_lang_section()
        if self.section:
            self.etymology = self.extract_etymology()
        Page.all_sections.append(self)

    def _extract_lang_section(self):
        regex = r"=* *\{\{langue\|%s\}\}" % self.lang

        for s in self.parsed.sections:
            if re.match(regex, s.string):
                self.section = s
                return s

    def extract_etymology(self):
        regex = r"=* *\{\{S\|étymologie\}\} *=*\n*"
        # TODO: DRY
        for s in self.section.sections:
            if re.match(regex, s.string):
                return s.sections[1]

    def extract_sources(self):
        pass

    def __repr__(self):
        return "%s %s" % (self.__class__.__name__, self.lang)


class _PartOfSpeech(_LanguageSection):
    pass


class Definition:
    pass


class Conjugation:
    pass
