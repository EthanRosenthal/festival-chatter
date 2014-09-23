import nltk
from nltk.corpus import stopwords
import json
import re

path = 'bonnarooAliasList.json'
dirty_aliases = [json.loads(line) for line in open(path)][0]

clean_aliases = {}

with open('bonnarooCleanAliasList.json','w') as fout:
    for k, v in dirty_aliases.iteritems():
        clean_list = []
        for alias in v:
            clean = [w for w in alias.split() if w not in stopwords.words('english')]
            clean_list.append(clean)
        clean_aliases[k] = clean_list
    json.dump(clean_aliases,fout)
fout.close()


