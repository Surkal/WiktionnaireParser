import re


def etymology_cleaner(etymology):
    """
    Cleans up the etymology of the text prompting
    site visitors to contribute.
    """
    ignore_etym = [
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


def extract_related_words(section):
    related = []
    while section.tag != 'h3' and section.tag != 'h4':
        for link in section.cssselect('a'):
            if 'Annexe:' in link.attrib.get('href'):
                continue
            related.append(link.text_content())
        section = section.getnext()
    return related
