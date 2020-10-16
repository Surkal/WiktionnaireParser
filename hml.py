from pprint import pprint

#from wiktionnaireparser.parser import WiktionnaireParser as wiktp

"""
page = wiktp.random_page()
#page = wiktp.from_source('coéternel')
print(page.get_title())
#page.find_lang_sections_id()
#sections_id = page.sections_id
#print(page.get_etymology())
pprint(page.get_word_data)
"""
from time import sleep
from wiktionnaireparser import WiktionnaireParser as wiktp

def loop(n):
    for i in range(n):
        page = wiktp.random_page()
        print(i, page.get_title())
        pprint(page.get_word_data)
        sleep(1)

#page = wiktp.from_source('föra', language='Suédois')
#page = wiktp.random_page()
loop(50)
print(page.get_title())
pprint(page.get_word_data)
#pprint(page.get_related_words('Synonymes'))
#pprint(len(page.get_word_data['partOfSpeech']['Verbe'][0]['subdefinitions'][2]['subdefinition']))
#loop(50)

#page = wiktp.from_source('vara', 'Suédois')
#page = wiktp.from_source('quote-part')
#page = wiktp.from_source('dödssynd', 'Suédois')
#page = wiktp(html)
#with open('/tmp/anglophone', 'r') as f:
    #html = f.read()
#page = wiktp(html)
"""
print(page.get_title())
print(page.get_etymology())
print('------------------')"""
#pprint(page.get_parts_of_speech())

#print(len(page.sections_id))
#print(len(page.sections_id['#Nom_commun']))
#print(page.sections_id['#Nom_commun'])
#print(page.sections_id)
#print('---------------------------------')
#print(page.get_related_words('Dérivés'))
#with open('/tmp/merci.html', 'w') as f:
    #f.write(page.html.decode('utf-8'))
#ids = page.get_related_words_ids('Traductions')
#print(page.sections_id)
#print(ids)
#print(page.get_translations('#Traductions'))
#page.get_definitions('Nom commun')
