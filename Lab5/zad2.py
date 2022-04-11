import imageio
import numpy as np
import matplotlib.pyplot as plt

im = imageio.imread('Lenna2.png')

# matrix = np.arange(1, 10).reshape(3, 3)

u, s, vh = np.linalg.svd(im, full_matrices=True)

# print(matrix)
#
print(u.shape)

print(s.shape)

# print(vh)

# print(u * s @ vh)

# print(u[:, 0])
# print(vh[0, :])

# k = 100
k_values = []
diff_norms = []

for k in range(1, s.shape[0], 10):
    k_values.append(k)
    print("k:", k)

    sum_k = s[0] * np.outer(u[:, 0], vh[0, :])
    for i in range(1, k):
        sum_k += s[i] * np.outer(u[:, i], vh[i, :])

    diff_norms.append(np.linalg.norm(im - sum_k))

plt.plot(k_values, diff_norms)
plt.show()
# print(sum_k)
#
# imageio.imwrite("compressed.png", sum_k)
#
# np.linalg.norm(im - sum_k)

