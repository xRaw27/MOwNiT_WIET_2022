import imageio
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import svds

# im = imageio.imread('Lenna2.png')

# matrix = np.arange(1, 37).reshape(6, 6)

np.set_printoptions(edgeitems=30, linewidth=100000)

matrix = lil_matrix((10, 10), dtype=np.float32)

xd = [
    ([1, 2], [4, 5]),
    ([2, 7], [2, 10]),
    ([1, 5, 9], [11, 2, 7]),
    ([2], [4]),
    ([2, 4, 8], [1, 2, 3]),
    ([1, 3], [6, 3]),
    ([0, 8], [7, 3]),
    ([0, 2], [11, 4]),
    ([0, 5], [2, 3]),
    ([4, 6], [6, 9])
]

for i in range(10):
    v = xd[i][1]
    # v /= np.linalg.norm(v)
    print(xd[i][0])
    print(v)
    matrix[np.array(xd[i][0]), i] = v

matrix = matrix.tocsr()

print(matrix.toarray())


# matrix = np.zeros((6, 6), dtype=np.int32)
# matrix[0, 3] = 4
# matrix[1, 2] = 2
# matrix[2, 4] = 1
# matrix[3, 5] = 6
# matrix[4, 1] = 4
# matrix[5, 3] = 3

u, s, vh = svds(matrix)
# u, s, vh = np.linalg.svd(matrix, full_matrices=False)

# print(matrix)
print(u)
print(s)
print(vh)

print(u * s @ vh)

#
# print(u.shape)
#
# print(s.shape)
#
# print(vh.shape)

# print(vh)

# print(u * s @ vh)

# print(u[:, 0])
# print(vh[0, :])

# k = 100
# k_values = []
# diff_norms = []

# for k in range(1, s.shape[0], 10):
#     k_values.append(k)
#     print("k:", k)
#
#     sum_k = s[0] * np.outer(u[:, 0], vh[0, :])
#     for i in range(1, k):
#         sum_k += s[i] * np.outer(u[:, i], vh[i, :])
#
#     diff_norms.append(np.linalg.norm(im - sum_k))

# plt.plot(k_values, diff_norms)
# plt.show()
# print(sum_k)
#
# imageio.imwrite("compressed.png", sum_k)
#
# np.linalg.norm(im - sum_k)




