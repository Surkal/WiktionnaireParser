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

def beautify_section_name(section_name):
    """Transforms id sections names into nice and readable names."""
    replacements = {'#': '', '_': ' '}
    # TODO: to try in one line
    section_name = re.sub(r'(_\d*)_\d*$', '\g<1>', section_name)
    section_name = re.sub(r'_1$', '', section_name)
    for key, value in replacements.items():
        section_name = section_name.replace(key, value)
    print(section_name)
    return section_name

def filter_sections_id(sections, useless_sections):
    """Filters interesting sections."""
    filtered_sections = []
    for sections_ in sections:
        if any(re.search(x, sections_) for x in useless_sections):
            continue
        filtered_sections.append(sections_)
    return filtered_sections
