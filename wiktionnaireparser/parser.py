import re
from contextlib import suppress

import requests
from pyquery import PyQuery as pq

from .utils import etymology_cleaner, filter_sections_id


class WiktionnaireParser:
    """
    Main class to analyze the HTML code of a wiktionary page.
    """
    def __init__(self, html, language='Français'):
        self.html = html
        self._query = pq(html)
        self._language = language
        self.sections_id = {}
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

        self.sections_id = {}
        for section in lang.getnext().getchildren():  # 'li'
            section_id = section.find('a').attrib['href']
            # Subsections?
            if section.find('ul') is None:
                self.sections_id[section_id] = []
                continue
            subsections = []
            for subsection in section.find('ul'):
                subsections.append(subsection.find('a').attrib['href'])
            self.sections_id[section_id] = subsections

        return self.sections_id

    def _find_sections_id_without_summary(self):
        if self._query.find('#Étymologie'):
            self.sections_id['#Étymologie'] = []
        section_id = self._query.find('.titredef')[0].getparent().attrib['id']
        if section_id:
            self.sections_id['#' + section_id] = []

        return self.sections_id

    def get_title(self):
        """Get the current page title."""
        return self._query.find('h1').text()

    def _real_section_name(self, section_name):
        """Get section name."""
        section = self._query.find(section_name)
        return section.text()

    def get_parts_of_speech(self):
        parts_of_speech = {}
        useless_sections = (
            r'Étymologie', r'Prononciation', r'Références', r'Voir_aussi',
            r'Anagrammes',
        )

        sections = filter_sections_id(self.sections_id.keys(), useless_sections)
        for section_name in sections:
            nice_section_name = self._real_section_name(section_name)
            parts_of_speech[nice_section_name] = self.get_definitions(section_name)
        return parts_of_speech

    def get_translation(self, example_line):
        """Get the example translation."""
        # better than a 'split('\n')'
        with suppress(AttributeError):
            translation = example_line.find('dl').find('dd')
            return translation.text_content().strip()

    def get_examples(self, definition_bloc):
        examples = {}
        try:
            example_line = definition_bloc.find('ul').find('li')
        except AttributeError:
            return

        count = 0
        while True:
            translation = None
            example = None
            try:
                example = example_line.text_content().strip()
                translation = self.get_translation(example_line)
                example_line = example_line.getnext()
            except AttributeError:
                break

            ex = {}
            if example:
                ex['example'] = example
                if translation:
                    ex['translation'] = translation
                examples[count] = ex
            count += 1

        return examples

    def get_definitions(self, part_of_speech):
        """Get the definitions of the word."""
        definitions = {}
        text = self._query.find(part_of_speech)[0]
        text = text.getparent()
        while text.tag != 'ol':
            text = text.getnext()
        for i, definition_bloc in enumerate(text.getchildren()):
            raw = definition_bloc.text_content()
            definition = raw.split('\n')[0]
            # Catching examples
            examples = self.get_examples(definition_bloc)

            if examples:
                definitions[i] = {'definition': definition, 'examples': examples}
            else:
                definitions[i] = {'definition': definition}
        return definitions

    def get_etymology(self):
        """
        Get the etymology of the word. On the French wiktionary,
        there is only one 'etymology' section per language.
        """
        id_ = list(filter(lambda x: re.search(r"Étymologie", x), self.sections_id.keys()))

        # If there is no etymology section, give up
        if not id_:
            return ''
        id_ = id_[0]

        etym = self._query.find(id_)[0].getparent().getnext().text_content()
        etym = etymology_cleaner(etym)

        return etym

    def get_related_words_ids(self, related_word):
        related_word = related_word.replace(' ', '_')
        regex = r'#%s(?:_\d+)?' % related_word
        ids = {}
        for key, values in self.sections_id.items():
            name = self._query.find(key).text()
            for value in values:
                if re.match(regex, value):
                    ids[name] = value
        return ids

    def get_related_words(self, related_word):
        """
        Get related words.
        Possible parameters: Apparentés étymologiques, Dérivés, Synonymes,
            Dérivés dans d’autres langues, Hyponymes, Hyperonymes,
            Variantes orthographiques, Abréviations, Homophones, Méronymes,
            Vocabulaire apparenté par le sens, etc.
        For translations, use `get_translations`.
        """
        ids = self.get_related_words_ids(related_word)
        related_words = {}
        for key, value in ids.items():
            related = []
            section = self._query.find(value)[0]
            section = section.getparent()
            while section.tag != 'ul':
                # 1 box
                if section.tag == 'div' and section.attrib.get('class') == 'boite':
                    section = section.getprevious().getprevious().find('div')
                    section = section.find('div').find('div').find('ul')
                    break
                section = section.getnext()
            for s in section:
                related.append(s.find('a').text_content())
            related_words[key] = related
        return related_words

    def get_translations(self, translation_id):
        result = {}
        section = self._query.find(translation_id)[0].getparent()
        lines = section.getnext().find('div').find('div').getnext().find('div')
        lines = lines.find('div').find('ul').find('li')

        while lines is not None:
            language = lines.find('span').text_content()
            transl = []
            links = lines.find('a')
            while links is not None:
                if links.attrib.get('class') != 'trad-exposant' and links.attrib:
                    transl.append(links.text_content())
                links = links.getnext()
            lines = lines.getnext()
            result[language] = transl
        return result
