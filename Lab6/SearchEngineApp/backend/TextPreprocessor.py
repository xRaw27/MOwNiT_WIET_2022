import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from unidecode import unidecode


class TextPreprocessor:
    def __init__(self):
        self.porter_stemmer = PorterStemmer()
        self.stop = set([re.sub(r'[^\w\s]', '', unidecode(stopword)) for stopword in stopwords.words()])

    def text_to_list_of_words(self, text):
        # non-alphanumeric characters removal
        text = re.sub(r'[^\w\s]', '', unidecode(text))

        # convert to lowercase, tokenization and stop words removal
        tokens = [token for token in word_tokenize(text.lower(), language='english')
                  if token not in self.stop and len(token) < 25 and sum(c.isdigit() for c in token) <= 6]

        # tokens stemming (PorterStemmer)
        words = [self.porter_stemmer.stem(token) for token in tokens]

        return words
