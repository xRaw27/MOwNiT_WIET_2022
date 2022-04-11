import numpy as np
import matplotlib.pyplot as plt


def draw_sphere(n):
    s = np.linspace(0, 2 * np.pi, n)
    t = np.linspace(0, np.pi, n)

    ss, tt = np.meshgrid(s, t)

    x = np.cos(ss) * np.sin(tt)
    y = np.sin(ss) * np.sin(tt)
    z = np.cos(tt)

    print(x.shape, y.shape, z.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(x, y, z, alpha=0.5, linewidth=0.3).set_edgecolor('k')
    plt.show()

    return x, y, z


def transform(x, y, z, A):
    n = x.shape[0]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(n):
        for j in range(n):
            vector = A @ np.array([x[i, j], y[i, j], z[i, j]])
            ax.plot([0, vector[0]], [0, vector[1]], [0, vector[2]], linewidth=3, zorder=3)
            x[i, j] = vector[0]
            y[i, j] = vector[1]
            z[i, j] = vector[2]

    ax.plot_surface(x, y, z, alpha=0.5, linewidth=0.3).set_edgecolor('k')
    plt.show()
    return x, y, z


x, y, z = draw_sphere(20)
A = np.random.rand(3, 3)

# elipsoida uzyskana przez mnożenie przez macierz A
transform(x.copy(), y.copy(), z.copy(), A)


# ta sama elipsoida uzyskana poprzez mnożenie przez kolejne macierze uzyskane z dekompozycji svd
u, s, vh = np.linalg.svd(A, full_matrices=True)

# rotacja
x, y, z = transform(x.copy(), y.copy(), z.copy(), vh)

# skalowanie
transform(x, y, z, np.diag(s))

# rotacja
transform(x, y, z, u)

