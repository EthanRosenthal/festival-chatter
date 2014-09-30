def custom_tokenize(text, custom_words=None):
    from nltk.tokenize import RegexpTokenizer
    from nltk.corpus import stopwords
    import re

    tokenizer = RegexpTokenizer(r'\w+')
    stop_url = re.compile(r'http[^\\s]+')
    stops = stopwords.words('english')


    words = [w.lower() for w in words if not re.match(stop_url, w)]
    words = tokenizer.tokenize(' '.join(words))
    words = [w for w in words if w not in stops or custom_words]

    return words