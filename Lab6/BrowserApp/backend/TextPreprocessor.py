import nltk.downloader
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from unidecode import unidecode


class TextPreprocessor:
    def __init__(self):
        # nltk.download('punkt')
        # nltk.download('wordnet')
        # nltk.download('omw-1.4')
        # nltk.download('stopwords')
        self.porter_stemmer = PorterStemmer()
        self.stop = set([re.sub(r'[^\w\s]', '', unidecode(stopword)) for stopword in stopwords.words()])

    def text_to_list_of_words(self, text):
        # usunięcie znaków niealfanumerycznych
        text = re.sub(r'[^\w\s]', '', unidecode(text))

        # zamiana na lowercase, podział na tokeny i usunięcie stop words
        tokens = [token for token in nltk.tokenize.word_tokenize(text.lower(), language='english')
                  if token not in self.stop and len(token) < 25 and sum(c.isdigit() for c in token) <= 6]

        # sprowadzenie słów do rdzenia (PorterStemmer)
        words = [self.porter_stemmer.stem(token) for token in tokens]

        return words
