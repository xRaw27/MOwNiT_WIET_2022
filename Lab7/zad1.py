import numpy as np


def power_iterations(A, max_iters, epsilon):
    n = A.shape[0]

    x = np.ones(n)
    # print(x)

    for i in range(max_iters):
        prev_x = x
        x = x @ A
        x = x / np.linalg.norm(x)

        if np.linalg.norm(x - prev_x) < epsilon:
            print("break: ", i, np.linalg.norm(x - prev_x))
            break

    return x


A = np.random.randint(0, 1000, (100, 100))

u = power_iterations(A, 1000, 1e-16)
print(u)
# print((u @ A)[0] / u[0])

print(np.linalg.eig(A)[1])

# print(np.max(np.abs(np.linalg.eigvals(A))))
# print(np.linalg.eigvals(A))
