import re
import pandas as pd
from pandas import DataFrame, Series


def get_sentiment_dict():
    sent_file = open('AFINN-111.txt')
    sentiment_dict = {}
    for line in sent_file:  # Build sentiment dictionary
      term, score  = line.split("\t")  # The file is tab-delimited.
      sentiment_dict[term] = int(score)  # Convert the score to an integer.

    return sentiment_dict

def get_tweet_sentiment(tweet_df):
    re_search = re.compile(r"[\w']+|[.,;?!]") # Compile regex search for words avoiding punctuation
    sentiment_dict = get_sentiment_dict()

    apply_fun  =  lambda x: sentiment_count(x, sentiment_dict, re_search)
    tweet_sents = tweet_df['text'].apply(apply_fun, (sentiment_dict, re_search))

    return pd.Series(tweet_sents, name='text_sentiment')


def sentiment_count(text, sentiment_dict, re_search):
    tokens = re.findall(re_search,text) # Find all words
    sent_score = 0.
    word_count = 0.
    # new_terms_sublist = {}
    sent_buck = {}
    sent_buck['positive'] = 0.
    sent_buck['negative'] = 0.

    for word in tokens:
        if sentiment_dict.has_key(word):
            if sentiment_dict[word]>0:
                sent_buck['positive'] += float(sentiment_dict[word])
            elif sentiment_dict[word]<0:
                sent_buck['negative'] += float(sentiment_dict[word])
        # else:
        #     new_terms_sublist[word] = 0.
        word_count += 1.

    if word_count == 0:
        sent_score = 0
    else:
        sent_score = (sent_buck['positive']+sent_buck['negative'])

    # for word in new_terms_sublist:
    #     if new_terms.has_key(word):
    #         new_terms[word] = (new_terms[word] + sent_score)/2
    #     else:
    #         new_terms[word] = sent_score

    return sent_score