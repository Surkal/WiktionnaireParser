# WiktionnaireParser

A library for parsing the [french wiktionary](https://fr.wiktionary.org).


## Installation

Supported Python versions : 3.6+

### With Pip

`pip install wiktionnaireparser`

### From source

`python setup.py install`


## Usage

```python
>>> from wiktionnaireparser import WiktionnaireParser as wiktp
>>> page = wiktp.from_source('nage PMT')
>>> page.get_etymology()
'Forme abrégée de nage avec palmes, masque et tuba.'
>>> page.get_parts_of_speech()
{'Locution nominale': ['(Plongée) Nage avec palmes, masque et tuba.']}
```

It is also possible to pick a word at random.

```python
>>> page.random_page()
>>> page.get_title()
'décrocher'
```
