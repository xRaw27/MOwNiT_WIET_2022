from datasets import load_dataset
from SearchData import SearchData
from TextPreprocessor import TextPreprocessor
from scipy.sparse import csr_matrix, lil_matrix, find
from scipy.sparse.linalg import norm
import numpy as np


class SearchEngine:
    def __init__(self, data_name, data_size):
        self.dataset = load_dataset("wikipedia", "20220301.simple")["train"]
        self.search_data = SearchData()
        self.load_data(data_name, data_size)
        self.k = len(self.search_data.terms)
        self.text_preprocessor = TextPreprocessor()

    def load_data(self, data_name, data_size):
        if not self.search_data.load_data(data_name):
            self.search_data.create_and_save(self.dataset[:data_size], data_size, data_name)

    def query(self, text):
        list_of_words = self.text_preprocessor.text_to_list_of_words(text)
        # print(list_of_words)

        q = lil_matrix((1, self.k), dtype=np.float32)
        for word in list_of_words:
            if word in self.search_data.terms:
                q[0, self.search_data.terms[word]] += 1

        q /= norm(q)

        result = find(q @ self.search_data.matrix)
        result = list(zip(result[2], result[1]))
        result.sort(reverse=True)
        # print(result)

        query_res = []
        for i, res in enumerate(result[:20]):
            # print(f"Correlation: ", res[0])
            # print(self.search_data.entries[res[1]])
            # query_res[i] = self.search_data.entries[res[1]]
            query_res.append(self.search_data.entries[res[1]])

        return query_res
