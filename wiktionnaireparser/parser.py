import re
#from contextlib import suppress

import requests
from pyquery import PyQuery as pq

from .utils import beautify_section_name, etymology_cleaner, filter_sections_id


class WiktionnaireParser:
    """
    Main class to analyze the HTML code of a wiktionary page.
    """
    def __init__(self, html, language='Français'):
        self.html = html
        self._query = pq(html)
        self._language = language
        self.sections_id = []
        self._find_lang_sections_id()

    @classmethod
    def from_source(cls, title, language='Français', oldid=None):
        """
        Get a page by its title.
        Possibly an old version of the title you are looking for
        by entering its `oldid`.
        """
        if oldid:
            url = 'https://fr.wiktionary.org/w/index.php?title=%s&oldid=%s' % (title, str(oldid))
        else:
            url = 'https://fr.wiktionary.org/wiki/%s' % title
        response = requests.get(url)
        return cls(response.content, language)

    @classmethod
    def random_page(cls, language='Français'):
        """Get a random page."""
        # TODO: make it available for more languages
        url = 'http://tools.wmflabs.org/anagrimes/hasard.php?langue=fr'
        response = requests.get(url)
        return cls(response.content, language)

    @property
    def language(self):
        """The searched language."""
        return self._language

    @language.setter
    def language(self, language):
        self._language = language
        self._find_lang_sections_id()

    @property
    def get_word_data(self):
        """Returns a dictionary of all collected data."""
        return {
            'title'       : self.get_title(),
            'etymologies' : self.get_etymology(),
            'partOfSpeech': self.get_parts_of_speech(),
        }

    def _find_lang_sections_id(self):
        lang = None
        # No summary?
        if not self._query.find('.toc'):
            return self._find_sections_id_without_summary()

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

    def _find_sections_id_without_summary(self):
        if self._query.find('#Étymologie'):
            self.sections_id.append('#Étymologie')
        section_id = self._query.find('.titredef')[0].getparent().attrib['id']
        if section_id:
            self.sections_id.append('#' + section_id)

        return self.sections_id

    def get_title(self):
        """Get the current page title."""
        return self._query.find('h1').text()

    def get_parts_of_speech(self):
        parts_of_speech = {}
        useless_sections = (
            r'Étymologie', r'Prononciation', r'Références', r'Voir_aussi',
        )

        sections = filter_sections_id(self.sections_id, useless_sections)
        for section_name in sections:
            nice_section_name = beautify_section_name(section_name)
            parts_of_speech[nice_section_name] = self.get_definitions(section_name)
        return parts_of_speech

    def get_definitions(self, part_of_speech):
        """Get the definitions of the word."""
        definitions = []
        text = self._query.find(part_of_speech)[0]
        text = text.getparent()
        while text.tag != 'ol':
            text = text.getnext()
        for definition in text.getchildren():
            raw = definition.text_content()
            #examples = ''
            #with suppress(AttributeError):
                #examples = definition.find('ul').find('li').text_content()
            definitions.append(raw.split('\n')[0])
        return definitions

    def get_etymology(self):
        """
        Get the etymology of the word. On the French wiktionary,
        there is only one 'etymology' section per language.
        """
        id_ = list(filter(lambda x: re.search(r"Étymologie", x), self.sections_id))

        # If there is no etymology section, give up
        if not id_:
            return ''
        id_ = id_[0]

        etym = self._query.find(id_)[0].getparent().getnext().text_content()
        etym = etymology_cleaner(etym)

        return etym
