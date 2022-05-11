from datasets import load_dataset
from SearchData import SearchData
from TextPreprocessor import TextPreprocessor
from scipy.sparse import csr_matrix, lil_matrix, find
from scipy.sparse.linalg import norm
import numpy as np
from nltk.downloader import download


class SearchEngine:
    def __init__(self, data_name, data_size):
        download('punkt')
        download('wordnet')
        download('omw-1.4')
        download('stopwords')
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

        q = lil_matrix((1, self.k), dtype=np.float32)
        for word in list_of_words:
            if word in self.search_data.terms:
                q[0, self.search_data.terms[word]] += 1

        q = q.tocsr()
        max_f = csr_matrix.max(q)
        if max_f == 0:
            return []

        # idf for query terms (https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
        rows, cols = q.nonzero()
        for row, col in zip(rows, cols):
            idf_value = self.search_data.idf_values[col]
            q[row, col] = (0.5 + 0.5 * q[row, col] / max_f) * idf_value

        q /= norm(q)

        print(q)

        # finding non-zero values in sparse result vector and sorting result by correlation desc
        result = find(q @ self.search_data.matrix)
        result = list(zip(result[2], result[1]))
        result.sort(reverse=True)
        # print(result)

        query_res = []
        for i, res in enumerate(result[:20]):
            query_res.append(self.search_data.entries[res[1]])

        return query_res
