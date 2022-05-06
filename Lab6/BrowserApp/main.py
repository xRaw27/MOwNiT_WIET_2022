from datasets import load_dataset
import nltk.downloader
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from unidecode import unidecode


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()
stop = set([re.sub(r'[^\w\s]', '', unidecode(stopword)) for stopword in stopwords.words()])


def text_to_list_of_words(text):
    # usunięcie znaków niealfanumerycznych
    text = re.sub(r'[^\w\s]', '', unidecode(text))

    # zamiana na lowercase, podział na tokeny i usunięcie stop words
    tokens = [token for token in nltk.tokenize.word_tokenize(text.lower(), language='english') if token not in stop]

    # sprowadzenie słów do rdzenia (PorterStemmer)
    words = [porter_stemmer.stem(token) for token in tokens]

    return words


def get_terms_from_dataset(dataset, n):
    terms = set()
    dataset = dataset[:n]

    for i in range(n):
        if i % 1000 == 0:
            print("Processed:", i)
        terms.update(text_to_list_of_words(dataset["text"][i]))
        terms.update(text_to_list_of_words(dataset["title"][i]))

    terms = {x for x in terms if len(x) < 25 and sum(c.isdigit() for c in x) <= 6}

    return terms


def main():
    dataset = load_dataset("wikipedia", "20220301.simple")["train"]

    terms = get_terms_from_dataset(dataset, 50000)
    print(terms)
    print(len(terms))
    #
    #
    # for term in terms:
    #     print(term)

    # print(dataset)
    # text = dataset[17]["text"]

    # print(text)
    # print(text_to_list_of_words(text))


if __name__ == "__main__":
    main()
