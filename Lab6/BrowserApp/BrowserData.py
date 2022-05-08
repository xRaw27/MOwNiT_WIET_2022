import pickle
import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
from TextPreprocessor import TextPreprocessor


class BrowserData:
    def __init__(self):
        self.entries = None
        self.terms = None
        self.matrix = None

    def load_data(self, s):
        try:
            with open(f"./data/entries_{s}", "rb") as f1, open(f"./data/terms_{s}", "rb") as f2, open(f"./data/matrix_{s}", "rb") as f3:
                self.entries = pickle.load(f1)
                self.terms = pickle.load(f2)
                self.matrix = pickle.load(f3)
        finally:
            return self.entries is not None and self.terms is not None and self.matrix is not None


    def create_and_save(self, dataset, n, s):
        self.preprocess_dataset(dataset, n)
        self.build_matrix()

        with open(f"./data/entries_{s}", "wb") as f1, open(f"./data/terms_{s}", "wb") as f2, open(f"./data/matrix_{s}", "wb") as f3:
            pickle.dump(self.entries, f1)
            pickle.dump(self.terms, f2)
            pickle.dump(self.matrix, f3)

    def preprocess_dataset(self, dataset, n):
        text_preprocessor = TextPreprocessor()

        self.entries = []
        terms = set()

        for i in range(n):
            if i % 1000 == 0:
                print("Processed:", i)

            entry = {
                "id": i,
                "title": dataset["title"][i],
                "short_text": dataset["text"][i][:128],
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
        print(f"Terms len: {len(self.terms)}")
        print(self.terms)


    def build_matrix(self):
        matrix = lil_matrix((len(self.terms), len(self.entries)), dtype=np.float32)

        for i, entry in enumerate(self.entries):
            if i % 1000 == 0:
                print("Matrix processed:", i)

            v = np.array(list(entry["words"].values()), dtype=np.float32)
            v /= np.linalg.norm(v)
            indexes_in_matrix = np.array([self.terms[word] for word in entry["words"].keys()])
            matrix[indexes_in_matrix, i] = v
            entry["words"] = None

        self.matrix = matrix.tocsr()
        print(f"Matrix len: {self.matrix.count_nonzero()}")
        print(self.matrix)
