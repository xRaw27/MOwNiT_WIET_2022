from time import time
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.linalg import norm
import numpy as np
from SearchEngine import SearchEngine


def main():
    search_engine = SearchEngine("150k", 150000)

    a = input("Kto pytal: ")
    search_engine.query(a)


    # dataset = load_dataset("wikipedia", "20220301.simple")["train"]


    # browser_data = BrowserData()

    # start = time()
    # browser_data.create_and_save(dataset[:1], 1, "1")
    # res = browser_data.load_data("10k")

    # print(res)

    # print(list(browser_data.terms.keys())[:10000])
    #
    # print(browser_data.matrix)
    # print(browser_data.matrix.count_nonzero())
    #
    # print(f"Execution time: {time() - start}")

    # A = np.array([1, 2])
    # B = [[5, 2],
    #      [1, 9]]
    #
    # A = lil_matrix((1, 2), dtype=np.float32)
    #
    # A[0, 0] = 1
    # A[0, 1] = 4
    # print(A.toarray())
    #
    #
    # A = A.tocsr()
    # B = csr_matrix(B)
    # C = (A @ B)
    #
    # D = C / norm(C)
    #
    # print(D.toarray())
    # print(norm(D))

    # for i in range(10):
    #     print(browser_data.entries[i]["title"])
    #     print(browser_data.entries[i]["short_text"])
    #     print(browser_data.entries[i]["words"])
    # print(len(browser_data.terms))


if __name__ == "__main__":
    main()
