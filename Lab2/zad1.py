from time import time
import numpy as np
import matplotlib.pyplot as plt


def gauss_jordan(A, B, partial_pivoting=True):
    n = A.shape[0]
    AB = np.hstack((A, B))

    # Scaling
    for i in range(n):
        AB[i] /= np.max(np.abs(A[i]))

    for i in range(n):
        if partial_pivoting:
            pivot = i + np.abs(AB[i:,i]).argmax()
            AB[[i, pivot]] = AB[[pivot, i]]

        AB[i] /= AB[i, i]

        for j in range(n):
            if i != j:
                AB[j] -= AB[j, i] * AB[i]

    return AB[:, n]


def random_a_b_float(n, _min=-100000, _max=100000):
    a = np.random.uniform(_min, _max, [n, n])
    b = np.random.uniform(_min, _max, [n, 1])
    return a, b


for i in range(3):
    np.random.seed(i)
    a, b = random_a_b_float(500)
    gauss_jordan_partial_pivoting = gauss_jordan(a, b).reshape(500, 1)
    gauss_jordan_no_partial_pivoting = gauss_jordan(a, b, partial_pivoting=False).reshape(500, 1)
    np_linalg_solve = np.linalg.solve(a, b)
    print("\nTest", i + 1)
    print("[partial pivoting] Tolerancja bezwzględna 1e-11, np.allclose:", np.allclose(gauss_jordan_partial_pivoting, np_linalg_solve, rtol=0, atol=10e-11))
    print("[partial pivoting] Tolerancja bezwzględna 1e-12, np.allclose:", np.allclose(gauss_jordan_partial_pivoting, np_linalg_solve, rtol=0, atol=10e-12))
    print("[partial pivoting] Tolerancja bezwzględna 1e-13, np.allclose:", np.allclose(gauss_jordan_partial_pivoting, np_linalg_solve, rtol=0, atol=10e-13))
    print("[partial pivoting] Tolerancja bezwzględna 1e-14, np.allclose:", np.allclose(gauss_jordan_partial_pivoting, np_linalg_solve, rtol=0, atol=10e-14))
    print("[no partial pivoting] Tolerancja bezwzględna 1e-10, np.allclose:", np.allclose(gauss_jordan_no_partial_pivoting, np_linalg_solve, rtol=0, atol=10e-10))
    print("[no partial pivoting] Tolerancja bezwzględna 1e-11, np.allclose:", np.allclose(gauss_jordan_no_partial_pivoting, np_linalg_solve, rtol=0, atol=10e-11))
    print("[no partial pivoting] Tolerancja bezwzględna 1e-12, np.allclose:", np.allclose(gauss_jordan_no_partial_pivoting, np_linalg_solve, rtol=0, atol=10e-12))


for n in range(550, 1001, 50):
    a, b = random_a_b_float(n)
    print(f"Macierz o rozmiarze {n}x{n}: ")

    start = time()
    gs = gauss_jordan(a, b)
    print("  Gauss-Jordan: ", round(time() - start, 6), "sekund")

    start = time()
    nls = np.linalg.solve(a, b)
    print("  np.linalg.solve: ", round(time() - start, 6), "sekund")

    print("  Weryfikacja poprawności z tolerancją bezwzględna 10e-10, np.allclose:", np.allclose(gs.reshape(n, 1), nls, rtol=0, atol=10e-10))


x = [n for n in range(100, 1001, 100)]
gs = []
nls = []
for n in x:
    a, b = random_a_b_float(n)
    start = time()
    gauss_jordan(a, b)
    gs.append(time() - start)
    start = time()
    np.linalg.solve(a, b)
    nls.append(time() - start)

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
for ax in axs:
    ax.plot(x, gs, marker='.', label='Gauss-Jordan partial pivoting')
    ax.plot(x, nls, marker='.', label='np.linalg.solve')
    ax.set_xlabel('Rozmiar macierzy n')
    ax.set_ylabel('Czas [s]')
    ax.legend()
axs[0].set_title('skala liniowa')
axs[1].set_title('skala logarytmiczna')
axs[1].set_yscale('log')
plt.show()