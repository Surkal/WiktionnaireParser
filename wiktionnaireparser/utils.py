import re

def get_languages(wikitext):
    """Returns the code of the languages having a section in the wikitext input."""
    return re.findall(r"{{langue\|([^\}]+)}\}", wikitext)

def remove_sortkey(title):
    sortkey_regex = r"\|clé=[^\|}]+"
    return re.sub(sortkey_regex, "", title)
