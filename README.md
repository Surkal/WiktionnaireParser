# WiktionnaireParser
[![Code Quality](https://www.code-inspector.com/project/14939/score/svg)](https://frontend.code-inspector.com/public/project/14939/WiktionnaireParser/dashboard)
[![Code Grade](https://www.code-inspector.com/project/14939/status/svg)](https://frontend.code-inspector.com/public/project/14939/WiktionnaireParser/dashboard)

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

Use `get_word_data` to extract and display all data

```python
>>> from wiktionnaireparser import WiktionnaireParser as wtp
>>> page = wtp.from_source('anglophone')
>>> page.get_word_data
{
    'title': 'anglophone',
    'etymologies': 'Composé du préfixe latin anglo pour anglais et du suffixe -phone.',
    'partOfSpeech': {
        'Nom commun': {
            0: {
                'definition': 'Personne parlant la langue anglaise.',
                'examples': {
                    0: {
                        'example': 'La minorité anglaise avait également reçu, de façon encore plus discrète, une autre «\xa0protection\xa0»: le trésorier du Québec serait un anglophone, un anglophone choisi par les financiers. —\xa0(Laurent Laplante, Paul Berryman, 2000)'
                    }
                }
            },
            'translations': {
                'Allemand': ['Englischsprachige'],
                'Anglais': ['English-speaker', 'anglophone'],
                'Breton': ['saozneger'],
                'Catalan': ['anglòfon', 'anglòfona', 'angloparlant'],
                'Espagnol': ['anglófono', 'anglófona', 'anglohablante'],
                'Espéranto': ['anglalingvano'],
                'Italien': ['anglofono'],
                'Néerlandais': ['Engelstalige'],
                'Portugais': ['anglófono', 'anglofalante', 'angloparlante'],
                'Roumain': ['anglofon']
            },
            'pronunciation': ['ɑ̃.ɡlɔ.fɔn'],
            'gender': 'masculin et féminin identiques',
            'Dérivés': ['Anglo-Bami', 'anglo-fou', 'angryphone'],
            'Apparentés étymologiques': ['Angleterre', 'anglais', '-phone']
        },
        'Adjectif': {
            0: {
                'definition': 'De langue anglaise.',
                'examples': {
                    0: {
                        'example': "Selon plusieurs penseurs de l'époque, l'État québécois est le seul qui puisse rivaliser avec les grandes entreprises anglophones d'Amérique du Nord. —\xa0(Mathieu Bureau Meunier, Wake up mes bons amis!, Québec, Septentrion, 2019, p. 133.)"
                    }
                }
            },
            'translations': {
                'Allemand': ['englischsprachig'],
                'Anglais': ['anglophone'],
                'Espagnol': ['anglófono', 'anglohablante'],
                'Espéranto': ['anglalingva'],
                'Italien': ['anglofono'],
                'Kazakh': ['ағылшынтілді'],
                'Néerlandais': ['Engelstalig'],
                'Norvégien (bokmål)': ['engelskspråklig'],
                'Portugais': ['anglófono', 'anglofalante', 'angloparlante'],
                'Roumain': ['anglofon']
            },
            'pronunciation': ['ɑ̃.ɡlɔ.fɔn'],
            'gender': 'masculin et féminin identiques',
            'Dérivés': ['anglo-fou']
        }
    }
}
```

## How to contribute

Contributions are more than welcome.

If you're new to Python and would like to contribute, get inspiration from the TODOs.
