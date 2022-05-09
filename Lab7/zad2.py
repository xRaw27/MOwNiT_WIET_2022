import numpy as np

def lu_factorization(A):
    n = A.shape[0]

    for i in range(n):
        for j in range(i + 1, n):
            A[j, i + 1:] -= (A[j, i] / A[i, i]) * A[i, i + 1:]
            A[j, i] = (A[j, i] / A[i, i])

    L = np.zeros((n, n))
    U = np.zeros((n, n))
    for i in range(n):
        U[i, i:] = A[i, i:]
        L[i, :i] = A[i, :i]
        L[i, i] = 1

    return L, U


def inverse_power_iter(matrix, sigma, max_iters):
    print(matrix)
    A = matrix.copy()
    n = A.shape[0]

    A = A - sigma * np.identity(n)

    # L, U = lu_factorization(A.copy())

    x = np.ones(n)

    for i in range(max_iters):
        x = np.linalg.solve(A, x)
        x = x / np.linalg.norm(x)

    print(x)


A = np.random.randint(0, 100, (4, 4))
A = np.array(A, dtype=np.float64)

inverse_power_iter(A, 100, 100)

print("\n")
[print(np.linalg.eig(A)[1][:, x]) for x in range(np.linalg.eig(A)[1].shape[1])]



