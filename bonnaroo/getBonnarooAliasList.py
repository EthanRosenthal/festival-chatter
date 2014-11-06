"""
Created on Mon June 30 2014

@author: Ethan Rosenthal

This routine uses the musicbrainz API to get known aliases for a queried band name.
The results of the API GET request are returned as a dictionary.
The code below normalizes the dictionary results by removing punctuation and ampersands
and saves the results as a JSON file.
The JSON output file uses the original band name that was read in by the input band list
as the dict key and a list of aliases as the dict value
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
    This routine converts each alias to lowercase, removes
    punctuation, and removes stop words. The output is a
    list containing the remaining words.
    """
    alias = alias.lower().replace(' &amp;', '') # Remove ampersands
    alias = regex.sub('', alias) # Remove punctuation
    alias_words = [w for w in alias.split() if w not in stopwords.words('english')]
    return alias_words
################################

with open('bonnarooBandList.txt','r') as fin:
    with open('bonnarooAliasList.json','w') as fout:
    	aliasDict={} # Initialize alias dictionary
        for band in fin:
            band = band.rstrip('\n')
            band_query = band.lower().replace(' &amp;', '') # Remove ampersands
            band_query = regex.sub('', band_query) # Remove punctuation
            # Only grab first result
            result = mbrainz.search_artists(artist=band_query, limit=1)
            band_query = clean_aliases(band_query, regex) # Remove stopwords
            aliasList = [band_query] # Initialize with stripped version of name
                                     # listed on Bonnaroo website
            try:
            	for alias in result['artist-list'][0]['alias-list']:
                    alias = clean_aliases(alias['alias'], regex)
                    aliasList.append(alias) # Build alias List
            except: # Some artists do not return aliases
            	pass # So don't do anything!
            aliasDict[band] = aliasList
    	json.dump(aliasDict,fout)
    fout.close()
fin.close()