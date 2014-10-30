import pandas as pd
import numpy as np

"""
NEED TO RE-DO FOR NON-PANDAS USAGE... OR JUST FIGURE OUT THE TRAIN-TEST SPLIT BETTER
"""

def make_train_test_split(df, band_list):
    X = np.empty(0)
    y = np.empty(0)
    for band in band_list:
        xtmp = np.array(df[ df[band]==True ]['tokens'])
        X = np.concatenate([X, xtmp])
        ytmp = []
        for i in range(len(xtmp)):
            ytmp.append(band)
        y = np.concatenate([y, np.array(ytmp)])
    return X, y



def train_probabilities(df, band_list):

    prior = calculate_prior_probability(df, band_list)

    class_bag = make_class_documents(df, band_list)

    conditional_prob, min_prob = \
        calculate_conditional_probability(df, band_list, class_bag)
    return prior, conditional_prob, min_prob

def classify_map(text, band_list, min_prob, prior, conditional_prob):
    score = {}
    for band in band_list:
        score[band] = np.log(prior[band])
        min_prob[band] = np.log(min_prob[band])
        for token in text:
            if conditional_prob[band].has_key(token):
                score[band] += np.log(conditional_prob[band][token])
            else:
                score[band] += min_prob[band]
    # Find maximum a posteriori (map)
    band_class = max(score.iterkeys(), key = (lambda key: score[key]))
    return band_class


def calculate_prior_probability(df, band_list):
    # Calculate prior probability
    prior = {}
    total_docs = float(0)
    for band in band_list:
        total_docs += df[band].value_counts()[True]

    for band in band_list:
        prior[band] = float(df[band].value_counts()[True])/total_docs

    return prior

def calculate_conditional_probability(df, band_list, class_bag):
    # Calculate conditional probability
    conditional_prob = {}
    min_prob = {}
    for band in band_list:
        tmp_prob = {}
        # Get total number of words for a given band
        total_class_word_count = float(np.sum(class_bag[band].values()))
        # For each word in the band class, find relative frequency
        # Use Laplace smoothing
        vocab_size = float(len(class_bag.keys()))
        for k, v in class_bag[band].iteritems():
            v = float(v)
            tmp_prob[k] = (v + 1.)/(total_class_word_count +
                            vocab_size)
        conditional_prob[band] = tmp_prob
        min_prob[band] = 1./(total_class_word_count + vocab_size)
    return conditional_prob, min_prob


def make_class_documents(df, band_list):
    """
    Create a bag of words and associated word counts for each band in band_list. The output is a dictionary with key for each band and the value is a dictionary containing words as keys and word counts as values for every tweet that mentioned that band.
    """
    class_bag = {}
    for band in band_list:
        class_bag[band] = word_count(df[df[band] == True])
    return class_bag

def word_count(df):
    # Map
    mapout = df['tokens'].apply(lambda x : mapper(x))
    global big_bag
    big_bag = {}
    # Reduce
    mapout.apply(lambda x : reducer(x, big_bag), big_bag)

    return big_bag


def mapper(tokens):
    small_bag = {}
    for word in tokens:
        if small_bag.has_key(word):
            small_bag[word] += 1
        else:
            small_bag[word] = 1

    return small_bag

def reducer(small_bag, big_bag):
    for k, v in small_bag.iteritems():
        if big_bag.has_key(k):
            big_bag[k] += v
        else:
            big_bag[k] = v