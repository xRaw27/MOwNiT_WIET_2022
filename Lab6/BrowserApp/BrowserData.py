import pickle
import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
from TextPreprocessor import TextPreprocessor


class BrowserData:
    def __init__(self):
        self.entries = []
        self.terms = None
        self.matrix = None

    def load_data(self):
        with open("./data/entries", "rb") as f1, open("./data/terms", "rb") as f2:
            self.entries = pickle.load(f1)
            self.terms = pickle.load(f2)

    def create_and_save(self, dataset, n):
        # print(dataset)
        self.preprocess_dataset(dataset, n)
        self.build_matrix()

        with open("./data/entries", "wb") as f1, open("./data/terms", "wb") as f2:
            pickle.dump(self.entries, f1)
            pickle.dump(self.terms, f2)

    def preprocess_dataset(self, dataset, n):
        text_preprocessor = TextPreprocessor()

        terms = set()

        for i in range(n):
            if i % 1000 == 0:
                print("Processed:", i)

            entry = {
                "id": i,
                "title": dataset["title"][i],
                "short_text": dataset["text"][i][:200],
                "url": dataset["url"][i],
                "words": dict()
            }

            list_of_words = text_preprocessor.text_to_list_of_words(dataset["text"][i]) + text_preprocessor.text_to_list_of_words(dataset["title"][i])

            terms.update(list_of_words)
            for w in list_of_words:
                if w in entry["words"]:
                    entry["words"][w] += 1
                else:
                    entry["words"][w] = 1

            self.entries.append(entry)

        self.terms = {word: idx for idx, word in enumerate(terms)}

    def build_matrix(self):
        matrix = lil_matrix((len(self.terms), len(self.entries)), dtype=np.float32)

        for i, entry in enumerate(self.entries):
            if i % 1000 == 0:
                print("Matrix processed:", i)
            for word, count in entry["words"].items():
                matrix[self.terms[word], i] = count

        self.matrix = matrix.tocsr()
