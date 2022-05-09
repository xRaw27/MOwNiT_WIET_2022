from datasets import load_dataset
import nltk.downloader
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from unidecode import unidecode
import pickle
import numpy as np
from scipy.sparse import csr_matrix, lil_matrix



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
    terms = {word: idx for idx, word in enumerate(terms)}

    return terms


def save(data, filename):
    with open(filename, "wb") as file:
        pickle.dump(data, file)


def load(filename):
    with open(filename, "rb") as file:
        data = pickle.load(file)
    return data


def build_matrix(dataset, n, terms):
    matrix = lil_matrix((len(terms), n), dtype=np.float32)

    for i in range(n):
        if i % 1000 == 0:
            print("Processed:", i)
        v = np.zeros(len(terms))
        for word in text_to_list_of_words(dataset["text"][i]):
            if word in terms:
                v[terms[word]] += 1

        non_zero_indexes = np.argwhere(v != 0).reshape(-1)
        matrix[non_zero_indexes, i] = v[non_zero_indexes]


    # for word in text_to_list_of_words()



    # non_zero_indexes = np.argwhere(arr != 0).reshape(-1)
    # matrix[non_zero_indexes, 0] = arr[non_zero_indexes]

    # print(matrix.shape)
    matrix = matrix.tocsr()
    print(matrix.toarray())
    print(matrix)


def main():
    dataset = load_dataset("wikipedia", "20220301.simple")["train"]

    n = 10000

    # terms = get_terms_from_dataset(dataset, 50000)
    terms = get_terms_from_dataset(dataset, n)


    # terms = load("./data/wiki_terms")

    # for i, word in enumerate(terms):
    #     print(i, word)

    # terms = {idx: word for idx, word in enumerate(terms)}



    # print(terms)
    # print(len(terms))

    # matrix = csr_matrix((len(terms), n), dtype=np.float32)
    # matrix = csr_matrix((10, 15), dtype=np.float32)
    #
    # arr = np.array([0, 1, 2, 0, 0, 5, 1, 0, 0, 0])
    #
    # non_zero_indexes = np.argwhere(arr != 0).reshape(-1)
    # matrix[non_zero_indexes, 0] = arr[non_zero_indexes]


    print(terms)
    print(len(terms))

    build_matrix(dataset, n, terms)


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
