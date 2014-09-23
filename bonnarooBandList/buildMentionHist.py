import pandas as pd
from pandas import DataFrame, Series
import string
import re
from nltk.corpus import stopwords



# To be used for removing punctuation
regex = re.compile('[%s]' % re.escape(string.punctuation))

def clean_sentence(sentence):
    """
    Converts each sentence to lowercase and removes
    punctuation.
    """
    sentence = sentence.lower().replace(' &amp;', '') # Remove ampersands
    sentence = regex.sub('', sentence) # Remove punctuation
    # sentence_words = [w for w in sentence.split() if w not in stopwords.words('english')]
    return sentence

def find_mention(sentence, phrase_list):
    """
    Takes a phase_list, which is a list of phrases where
    each phrase corresponds to a list of the words in the phrase, and
    checks to see whether all the words of any of the phrases are
    present in "sentence".
    """
    for words in phrase_list:
        words = set(words)
        if words.issubset(sentence):
            return True
    return False # None of the word lists were subsets

def check_each_alias(sentence, alias_dict):
    """
    Checks to see whether any of the aliases for
    each band mentioned in alias_dict are mentioned
    in "sentence".

    band_bool is a dictionary that contains all band
    names as keys and True or False as values corresponding
    to whether or not the band was mentioned in the sentence.
    """
    band_bool={}
    sentence = set(clean_sentence(sentence).split())
    for k, v in alias_dict.iteritems():
        band_bool[k] = find_mention(sentence, v)
    return pd.Series(band_bool)

def build_apply_fun(alias_dict):
    """
    Turn check_each_alias into an anonymous function.
    """
    apply_fun = lambda x : check_each_alias(x, alias_dict)
    return apply_fun



def get_bandPop(df, alias_dict):
    """
    For tweet DataFrame input "df", build histogram of of mentions
    for each band in alias_dict.
    """
    bandPop = df['text'].apply(build_apply_fun(alias_dict), alias_dict)
    bandPop = bandPop.sum(axis=0)
    bandPop.sort(ascending=False)
    return bandPop



# test2 = pd.concate([organics, df_bandpop], axis=1)
# test2[test2['Kanye West']==True]['text']
