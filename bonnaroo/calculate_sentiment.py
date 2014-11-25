"""
Calculate tweet sentiment from tweet DataFrame
"""

import re
import pandas as pd
from pandas import DataFrame, Series


def get_sentiment_dict():
    """ Load in sentiment file AFINN-111 as dictionary """

    sent_file = open('AFINN-111.txt')
    sentiment_dict = {}
    for line in sent_file:
      term, score  = line.split("\t")
      sentiment_dict[term] = int(score)

    return sentiment_dict

def get_tweet_sentiment(tweet_df):
    """
    Calculate sentiment score for every tweet in DataFrame tweet_df
    """
    sentiment_dict = get_sentiment_dict()

    apply_fun  =  lambda x: sentiment_count(x, sentiment_dict)
    tweet_sents = tweet_df['tokens'].apply(apply_fun, sentiment_dict)

    return pd.Series(tweet_sents, name='text_sentiment')


def sentiment_count(tokens, sentiment_dict):
    """
    Calculate sentiment score for list of "tokens".
    """
    # Initialize
    sent_score = 0.
    word_count = 0.
    sent_buck = {}
    sent_buck['positive'] = 0.
    sent_buck['negative'] = 0.

    for word in tokens:
        if sentiment_dict.has_key(word):
            if sentiment_dict[word]>0:
                sent_buck['positive'] += float(sentiment_dict[word])
            elif sentiment_dict[word]<0:
                sent_buck['negative'] += float(sentiment_dict[word])
        word_count += 1.

    if word_count == 0:
        sent_score = 0
    else:
        sent_score = (sent_buck['positive']+sent_buck['negative'])

    return sent_score