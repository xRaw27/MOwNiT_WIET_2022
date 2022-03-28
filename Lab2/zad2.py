import numpy as np


def lu_factorization(A):
    n = A.shape[0]

    for i in range(n):
        for j in range(i + 1, n):
            A[j, i + 1:] -= (A[j, i] / A[i, i]) * A[i, i + 1:]
            A[j, i] = (A[j, i] / A[i, i])

    return A


def random_a_b_float(n, _min=-100000, _max=100000):
    a = np.random.uniform(_min, _max, [n, n])
    b = np.random.uniform(_min, _max, [n, 1])
    return a, b


def is_lu_factorization_correct(A, LU):
    n = LU.shape[0]
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    for i in range(n):
        U[i, i:] = LU[i, i:]
        L[i, :i] = LU[i, :i]
        L[i, i] = 1

    is_close = np.allclose(A, np.matmul(L, U), rtol=0, atol=10e-6)
    norm = np.linalg.norm(A - np.matmul(L, U))
    return is_close, norm


for i in range(1, 6):
    a, _ = random_a_b_float(100 * i)

    lu = lu_factorization(a.copy())
    is_close, norm = is_lu_factorization_correct(a, lu)

    print(f"Macierz o rozmiarze {100 * i}x{100 * i}:")
    print(f"  Norma Frobieniusa ||A - LU|| = ", norm)
    print(f"  Weryfikacja poprawności z tolerancją bezwzględną 10e-6, np.allclose:", is_close)