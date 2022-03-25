from time import time
import numpy as np


def recursive_sum(t, p, q):
    if p == q:
        return t[p]

    if p + 1 == q:
        return t[p] + t[q]

    m = (p + q) // 2
    return recursive_sum(t, p, m) + recursive_sum(t, m + 1, q)


def kahan_sum(tab):
    _sum = np.float32(0)
    _err = np.float32(0)
    for i in range(len(tab)):
        y = tab[i] - _err
        temp = _sum + y
        _err = (temp - _sum) - y
        _sum = temp

    return _sum


# 1
n = 10 ** 7

v = np.float32(0.53125)
arr1 = [v for _ in range(n)]
exact_sum_v = 5312500

w = np.float32(0.53125125)
arr2 = [w for _ in range(n)]
exact_sum_w = 5312512.5

kahan_sum_v = kahan_sum(arr1)
kahan_sum_w = kahan_sum(arr2)

for s, e in [(kahan_sum_v, exact_sum_v), (kahan_sum_w, exact_sum_w)]:
    print("Uzyskana suma: ", s, np.dtype(s))
    print("Błąd bezwzględny: ", abs(s - e))
    print("Błąd względny: ", round(abs((s - e) / e) * 100, 10), "%\n")


# 3
start = time()
recursive_sum(arr1, 0, n - 1)
print("Algorytm rekurencyjny: ", time() - start, "sekund")
start = time()
kahan_sum(arr1)
print("Algorytm kahan: ", time() - start, "sekund")

