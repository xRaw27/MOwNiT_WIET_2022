from datasets import load_dataset
from BrowserData import BrowserData
from TextPreprocessor import TextPreprocessor
from scipy.sparse import csr_matrix, lil_matrix, find
from scipy.sparse.linalg import norm
import numpy as np

class Browser:
    def __init__(self):
        self.dataset = load_dataset("wikipedia", "20220301.simple")["train"]
        self.browser_data = BrowserData()
        self.load_data()
        self.k = len(self.browser_data.terms)
        self.text_preprocessor = TextPreprocessor()

    def load_data(self):
        if not self.browser_data.load_data("10k"):
            self.browser_data.create_and_save(self.dataset[:10000], 10000, "10k")

    def query(self, text):
        list_of_words = self.text_preprocessor.text_to_list_of_words(text)
        # print(list_of_words)

        q = lil_matrix((1, self.k), dtype=np.float32)
        for word in list_of_words:
            if word in self.browser_data.terms:
                q[0, self.browser_data.terms[word]] += 1

        q /= norm(q)

        result = find(q @ self.browser_data.matrix)
        result = list(zip(result[2], result[1]))
        result.sort(reverse=True)
        print(result)

        for res in result[:5]:
            print(f"Correlation: ", res[0])
            print(self.browser_data.entries[res[1]])

