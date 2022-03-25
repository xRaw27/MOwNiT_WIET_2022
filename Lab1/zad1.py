from time import time
import numpy as np
import matplotlib.pyplot as plt

# 1
n = 10 ** 7
v = np.float32(0.53125)
exact_sum = 5312500
arr = [v for _ in range(n)]

print("v =", v, np.dtype(v))


def naive_sum(t, _sum, p, q):
    for i in range(p, q):
        _sum += t[i]

    return _sum


_naive_sum = naive_sum(arr, np.float32(0), 0, n)
print("Uzyskana suma: ", _naive_sum, np.dtype(_naive_sum))


# 2
print("Błąd bezwzględny: ", abs(_naive_sum - exact_sum))
print("Błąd względny: ", round(abs((_naive_sum - exact_sum) / exact_sum) * 100, 4), "%")


# 3
current_sum = np.float32(0)
current_exact_sum = 0
x = np.arange(0, 10**7 + 1, 25000)
y1 = [0]
y2 = [0]

for i in range(0, n, 25000):
    current_sum = naive_sum(arr, current_sum, i, i + 25000)
    current_exact_sum += 13281.25
    y1.append(abs((current_sum - current_exact_sum) / current_exact_sum) * 100)
    y2.append(current_exact_sum - current_sum)

plt.plot(x, y1, color='r', label='błąd względny (%)')
plt.legend()
plt.show()

plt.plot(x, y2, color='b', label='current_sum - exact_current_sum')
plt.legend()
plt.show()


# 4
def recursive_sum(t, p, q):
    if p == q:
        return t[p]

    if p + 1 == q:
        return t[p] + t[q]

    m = (p + q) // 2
    return recursive_sum(t, p, m) + recursive_sum(t, m + 1, q)


_recursive_sum = recursive_sum(arr, 0, n - 1)
print("Uzyskana suma: ", np.dtype(_recursive_sum), _recursive_sum)


# 5
print("Błąd bezwzględny: ", abs(_recursive_sum - exact_sum))
print("Błąd względny: ", round(abs((_recursive_sum - exact_sum) / exact_sum) * 100, 10), "%")


# 6
start = time()
naive_sum(arr, np.float32(0), 0, n)
print("Algorytm naiwny: ", time() - start, "sekund")
start = time()
recursive_sum(arr, 0, n - 1)
print("Algorytm rekurencyjny: ", time() - start, "sekund")


# 7
w = np.float32(0.53125125)
arr2 = [w for _ in range(n)]
recursive_sum_arr2 = recursive_sum(arr2, 0, n - 1)
exact_sum_arr2 = 5312512.5

print("w =", w, np.dtype(w))
print("Uzyskana suma: ", recursive_sum_arr2, np.dtype(recursive_sum_arr2))
print("Błąd bezwzględny: ", abs(recursive_sum_arr2 - exact_sum_arr2))
print("Błąd względny: ", round(abs((recursive_sum_arr2 - exact_sum_arr2) / exact_sum_arr2) * 100, 10), "%")