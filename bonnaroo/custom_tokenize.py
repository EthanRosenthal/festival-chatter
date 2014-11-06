from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re

def custom_tokenize(text, custom_words=None, clean_custom_words=False):
    """
    This routine takes an input "text" and strips punctuation (except apostrophes),
    converts each words to lowercase, removes standard english stopwords, removes
    a set of custom_words (optional), and returns a list of all of the leftover
    words.
    INPUTS:
    text = text string that one wants to tokenize
    custom_words = custom list or dictionary of wordse2461 to omit from the tokenization.
    clean_custom_world = Flag as True if you want to clean these words.
                         Flag as False if mapping this function to many keys. In
                         that case, pre-clean the words before running this function.
    OUTPUTS:
    words = This is a list of the tokenized version of each word that was in "text"
    """
    tokenizer = RegexpTokenizer(r"[\w']+")
    stop_url = re.compile(r'http[^\\s]+')
    stops = stopwords.words('english')

    if clean_custom_words:
        custom_words = tokenize_custom_words(custom_words)

    words = [w.lower().split("'")[0] for w in text.split() if not re.match(stop_url, w)]
    words = tokenizer.tokenize(' '.join(words))
    words = [w for w in words if w not in stops and w not in custom_words]

    return words

def tokenize_custom_words(custom_words):
    tokenizer = RegexpTokenizer(r"[\w']+")
    custom_tokens = []
    stops = stopwords.words('english')

    if type(custom_words) is dict: # Useful for alias_dict
        for k, v in custom_words.iteritems():
            k_tokens = [w.lower() for w in k.split() if w.lower() not in stops]
            k_tokens = tokenizer.tokenize(' '.join(k_tokens)) # Remove all punctuation
            k_tokens = [w.replace("'","") for w in k_tokens] # Remove apostrophes
            # Below takes care of nested lists, then tokenizes
            v_tokens = [word for listwords in v for word in listwords]
            v_tokens = tokenizer.tokenize(' '.join(v_tokens))
            v_tokens = [w.replace("'","") for w in v_tokens] # Remove apostrophes
            custom_tokens.extend(k_tokens)
            custom_tokens.extend(v_tokens)
            custom_tokens.append(''.join(k_tokens)) # For hashtags (e.g. kanyewest)
            custom_tokens.append(''.join(v_tokens))
    elif type(custom_words) is list:
        custom_tokens = [tokenizer.tokenize(words) for words in custom_words]
        custom_tokens = [words.replace("'","") for words in custom_tokens]

    custom_tokens = set(custom_tokens)
    return custom_tokens


