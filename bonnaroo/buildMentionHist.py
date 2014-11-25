"""
Check to see which artists were mentioned in tweet DataFrame.
"""

import pandas as pd
from pandas import DataFrame, Series
import string
import re


# To be used for removing punctuation
global regex
regex = re.compile('[%s]' % re.escape(string.punctuation))

def clean_sentence(sentence):
    """
    Convert each sentence to lowercase and remove
    punctuation.
    """
    sentence = sentence.lower().replace(' &amp;', '') # Remove ampersands
    sentence = regex.sub('', sentence) # Remove punctuation
    return sentence

def find_mention(sentence, nested_alias_list):
    """
    Find if there is an intersection between sentence and nested_alias_list.

    INPUTS
    sentence = list of word tokens
    nested_alias_list = list of tokenized aliases

    OUPUTS
    return True if, for any list in nested_alias_list, all word tokens appear in sentence.
    """
    for words in nested_alias_list:
        words = set(words)
        if words.issubset(sentence):
            return True
        if ''.join(words) in sentence: # Check for hashtags (e.g. #kanyewest)
            return True
    return False

def check_each_alias(sentence, alias_dict):
    """
    Check to see whether any of the aliases for
    each band in alias_dict are mentioned
    in "sentence".

    INPUTS
    sentence = string corresponding to tweet text
    alias_dict = dictionary with band names as keys and lists of tokenized "aliases" as values. Aliases come from getBonnarooAliasList.py

    OUTPUTS
    band_bool = Pandas series with each column a different band name from alias_dict keys, and boolean values indicating whether or not the band was mentioned.
    """
    band_bool={}
    band_bool['tokens'] = clean_sentence(sentence).split() # tokenize tweet
    sentence = set(clean_sentence(sentence).split())

    # See which bands are mentioned
    for k, v in alias_dict.iteritems():
        band_bool[k] = find_mention(sentence, v)

    # If band is mentioned, remove tokens that mention the band.
    for k in alias_dict.iterkeys():
        if band_bool[k] == True:
            for v in alias_dict[k]:
                band_bool['tokens'] = [w for w in band_bool['tokens'] if w not in v]

    return pd.Series(band_bool)

def get_bandPop(df, alias_dict):
    """
    For tweet DataFrame input "df", build histogram of mentions
    for each band in alias_dict.
    """
    bandPop = df['text'].apply(lambda x: check_each_alias(x, alias_dict))

    return bandPop
