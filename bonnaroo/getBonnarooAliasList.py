"""
Use the musicbrainz API to get known aliases for a queried band name.

INPUTS
bonarooBandList.txt = Read in automatically below. Outputted from
    getBonnarooBandList.py Each band in file is used as a query to
    the musicbrainz API

OUTPUTS
bonnarooAliasList.josn = Outputted automatically below. Consists of keys
    corresponding to each band in input file. Values are a list of aliases
    returned from the API GET request. Alias lists are tokenized and
    stripped of stopwords.
"""

import musicbrainzngs as mbrainz
import json
import string
import re
import nltk
from nltk.corpus import stopwords


mbrainz.auth('rosentep','testing') # Omitted for github
mbrainz.set_useragent('Btest/0.0','x@gmail.com') # Omitted for github
# To be used for removing punctuation
regex = re.compile('[%s]' % re.escape(string.punctuation))


################################
def clean_aliases(alias, regex):
    """
    Convert each alias to lowercase, remove punctuation,
    and remove stop words. The output is a list containing
    the remaining words.
    """
    alias = alias.lower().replace(' &amp;', '') # Remove ampersands
    alias = regex.sub('', alias) # Remove punctuation
    alias_words = [w for w in alias.split() if w not in stopwords.words('english')]
    return alias_words
################################


# MAIN CODE
with open('bonnarooBandList.txt','r') as fin:
    with open('bonnarooAliasList.json','w') as fout:

    	aliasDict={}
        for band in fin:
            band = band.rstrip('\n')
            band_query = band.lower().replace(' &amp;', '') # Remove ampersands
            band_query = regex.sub('', band_query) # Remove punctuation
            # Only grab first result
            result = mbrainz.search_artists(artist=band_query, limit=1)
            band_query = clean_aliases(band_query, regex) # Remove stopwords
            aliasList = [band_query] # Initialize with stripped version of name
                                     # listed on Bonnaroo website

            # result is large JSON file. Extract alias list
            try:
            	for alias in result['artist-list'][0]['alias-list']:
                    alias = clean_aliases(alias['alias'], regex)
                    aliasList.append(alias) # Build alias List
            except:
                # Some artists do not return aliases
            	pass
            aliasDict[band] = aliasList

    	json.dump(aliasDict,fout)

    fout.close()
fin.close()