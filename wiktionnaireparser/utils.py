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
