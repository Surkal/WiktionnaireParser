import re

def get_languages(wikitext):
    """Returns the code of the languages having a section in the wikitext input."""
    return re.findall(r"{{langue\|([^\}]+)}\}", wikitext)
