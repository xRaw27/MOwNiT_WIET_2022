from time import time
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.linalg import norm
import numpy as np
from SearchEngine import SearchEngine


def main():
    search_engine = SearchEngine("150k", 150000)

    a = input("Kto pytal: ")
    res = search_engine.query(a)

    [print(x) for x in res]


if __name__ == "__main__":
    main()
