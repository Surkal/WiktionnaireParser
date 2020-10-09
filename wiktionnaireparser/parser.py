import re
from contextlib import suppress

import requests
from pyquery import PyQuery as pq


class WiktionnaireParser:
    def __init__(self, html, *args, **kwargs):
        self.html = html
        self._query = pq(html)
        self._language = kwargs.get('language') or 'Français'
        self._find_lang_sections_id()

    @classmethod
    def from_source(cls, title, *args, **kwargs):
        url = 'https://fr.wiktionary.org/wiki/%s' % title
        response = requests.get(url)
        return cls(response.content, *args, **kwargs)

    @classmethod
    def random_page(cls):
        url = 'http://tools.wmflabs.org/anagrimes/hasard.php?langue=fr'
        response = requests.get(url)
        return cls(response.content)

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, x):
        self._language = x
        self._find_lang_sections_id()

    @property
    def get_word_data(self):
        return {
            'title'       : self.get_title(),
            'etymologies' : self.get_etymology(),
            'partOfSpeech': self.get_parts_of_speech(),
        }

    def _find_lang_sections_id(self):
        # TODO: returns None when there is no summary
        lang = None
        # Find in summary
        for link in self._query.find('a'):
            try:
                if link.attrib['href'] == '#%s' % (self._language.replace(' ', '_')):
                    lang = link
                    break
            except KeyError:
                pass

        # Language not in the page
        if lang is None:
            return None

        self.sections_id = []
        for section in lang.getnext().getchildren():
            self.sections_id.append(section.find('a').attrib['href'])

        return self.sections_id

    def _filter_sections_id(self, sections, useless_sections):
        filtered_sections = []
        for sections_ in sections:
            if any(re.search(x, sections_) for x in useless_sections):
                continue
            filtered_sections.append(sections_)
        return filtered_sections

    def _beautify_section_name(self, section_name):
        replacements = {'#': '', '_': ' '}
        # TODO: to try in one line
        section_name = re.sub(r'(_\d*)_\d*$', '\g<1>', section_name)
        section_name = re.sub(r'_1$', '', section_name)
        for key, value in replacements.items():
            section_name = section_name.replace(key, value)
        return section_name

    def get_title(self):
        return self._query.find('h1').text()

    def get_parts_of_speech(self):
        parts_of_speech = {}
        useless_sections = (r'Étymologie', r'Prononciation', r'Références')
        sections = self._filter_sections_id(self.sections_id, useless_sections)
        for section_name in sections:
            nice_section_name = self._beautify_section_name(section_name)
            parts_of_speech[nice_section_name] = self.get_definitions(section_name)
        return parts_of_speech

    def get_definitions(self, part_of_speech):
        definitions = []
        text = self._query.find(part_of_speech)[0].getparent()
        while text.tag != 'ol':
            text = text.getnext()
        for definition in text.getchildren():
            raw = definition.text_content()
            examples = ''
            #with suppress(AttributeError):
                #examples = definition.find('ul').find('li').text_content()
            definitions.append(raw.split('\n')[0])
        return definitions

    def get_etymology(self):
        # TODO: supprimer '(Siècle à préciser) ' exemple : chalon
        ignore_etym = 'Étymologie manquante ou incomplète. Si vous la '\
                      'connaissez, vous pouvez l’ajouter en cliquant ici.'
        id_ = list(filter(lambda x: re.search(r"Étymologie", x), self.sections_id))

        # If there is no etymology section, give up
        if not id_:
            return ''
        id_ = id_[0]

        etym = self._query.find(id_)[0].getparent().getnext().text_content()
        if etym == ignore_etym:
            return ''
        return etym
