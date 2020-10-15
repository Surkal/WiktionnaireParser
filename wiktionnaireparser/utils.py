import re

def get_languages(wikitext):
    """Returns the code of the languages having a section in the wikitext input."""
    return re.findall(r"{{langue\|([^\}]+)}\}", wikitext)

def remove_sortkey(title):
    sortkey_regex = r"\|clé=[^\|}]+"
    return re.sub(sortkey_regex, "", title)

def etymology_cleaner(etymology):
    """
    Cleans up the etymology of the text prompting
    site visitors to contribute.
    """
    ignore_etym =   [
        r'^Étymologie manquante ou incomplète. Si vous la connaissez, vous pouvez l’ajouter en cliquant ici\.$',
        r'\(Siècle à préciser\) ',
    ]
    for ignore in ignore_etym:
        etymology = re.sub(ignore, '', etymology)
    return etymology

def filter_sections_id(sections, useless_sections):
    """Filters interesting sections."""
    filtered_sections = []
    for sections_ in sections:
        if any(re.search(x, sections_) for x in useless_sections):
            continue
        filtered_sections.append(sections_)
    return filtered_sections

def aggregate_definitions(part_of_speech):
    return [y['definition'] for x in part_of_speech.values() for y in x.values()]

def filter_related_words(related_words):
    useless = [r'modifier le wikicode']
    related_words_copy = []
    for word in related_words:
        for regex in useless:
            if not re.fullmatch(regex, word):
                related_words_copy.append(word)
    return related_words_copy

def extract_related_words(section):
    related = []
    url = '/wiki/'
    while section.tag != 'h3' and section.tag != 'h4':
        for link in section.cssselect('a'):
            if 'Annexe:' in link.attrib.get('href'):
                continue
            related.append(link.text_content())
        section = section.getnext()
    return related
