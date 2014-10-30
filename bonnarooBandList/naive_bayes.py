import pandas as pd
import numpy as np
import sklearn.cross_validation as cross_val

def train_then_test(df, band_list):

    X, y = pandas_to_Xy(df, band_list)
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    prior, conditional_prob, min_prob = \
                train_probabilities(X_train, y_train, band_list)

    vclassify_map = np.vectorize(lambda x:
                    classify_map(x,
                                band_list,
                                min_prob,
                                prior,
                                conditional_prob,
                                )
                                )
    y_train_pred = vclassify_map(X_train)
    print 'Training Data: \n'
    calculate_accuracy(y_train_pred, y_train)

    y_test_pred = vclassify_map(X_test)
    print 'Test Data: \n'
    calculate_accuracy(y_test_pred, y_test)

    print 'Training Error by Artist: \n'
    for band in band_list:
        print '%s' % band
        calculate_accuracy(y_train_pred[ y_train==band ],
                    y_train[y_train==band]
                    )
    # return conditional_prob


def calculate_accuracy(y_pred, y_true):
    accuracy = float(np.sum(y_pred==y_true))/len(y_pred)

    print 'Accuracy: %.4f \n' % accuracy

def train_test_split(X, y):
    X_train, X_test, y_train, y_test \
             = cross_val.train_test_split(X,
    r                                      y,
                                          test_size=0.2,
                                          random_state=33)
    return X_train, X_test, y_train, y_test

def pandas_to_Xy(df, band_list):
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


def train_probabilities(X, y, band_list):

    prior = calculate_prior_probability(X, y, band_list)

    class_bag = make_class_documents(X, y, band_list)

    conditional_prob, min_prob = \
        calculate_conditional_probability(band_list, class_bag)
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


def calculate_prior_probability(X, y, band_list):
    # Calculate prior probability
    prior = {}
    total_docs = float(len(y))

    for band in band_list:
        prior[band] = float(len( y[ y==band ] ))/total_docs

    return prior

def calculate_conditional_probability(band_list, class_bag):
    # Calculate conditional probability
    conditional_prob = {}
    min_prob = {}
    alpha = 1.
    for band in band_list:
        tmp_prob = {}
        # Get total number of words for a given band
        total_class_word_count = float(np.sum(class_bag[band].values()))
        # For each word in the band class, find relative frequency
        # Use Laplace smoothing
        vocab_size = float(len(class_bag.keys()))
        for k, v in class_bag[band].iteritems():
            v = float(v)
            tmp_prob[k] = (v + alpha*1.)/(total_class_word_count +
                            alpha*vocab_size)
        conditional_prob[band] = tmp_prob
        min_prob[band] = alpha*1./(total_class_word_count + alpha*vocab_size)
    return conditional_prob, min_prob


def make_class_documents(X, y, band_list):
    """
    Create a bag of words and associated word counts for each band in band_list. The output is a dictionary with key for each band and the value is a dictionary containing words as keys and word counts as values for every tweet that mentioned that band.
    """
    class_bag = {}
    for band in band_list:
        class_bag[band] = word_count(X[y == band])
    return class_bag

def word_count(X):
    # Vectorize map function and apply to X
    vmapper = np.vectorize(lambda x: mapper(x))
    mapout = vmapper(X)

    global big_bag
    big_bag = {}

    # Vectorize reduce function and apply to mapout
    vreducer = np.vectorize(lambda x: reducer(x, big_bag))
    vreducer(mapout)

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