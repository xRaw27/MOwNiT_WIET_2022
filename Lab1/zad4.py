import numpy as np
import matplotlib.pyplot as plt


# a
def logistic(x, r):
    return r * x * (1 - x)


def logistic_float32(x, r):
    return r * x * (np.float32(1) - x)


def bifurcation_diagram(x_0, min_r, max_r, n, iterations, last, np_type, alpha_value=.05):
    r = np.linspace(min_r, max_r, n, dtype=np_type)
    x_n = np.full(n, x_0, dtype=np_type)

    for _ in range(iterations - last):
        x_n = logistic(x_n, r)

    for _ in range(last):
        x_n = logistic(x_n, r)
        plt.plot(r, x_n, ',k', alpha=alpha_value)

    plt.xlabel('r')
    plt.ylabel('x')
    plt.xlim(min_r, max_r)
    plt.ylim(0, 1)
    plt.title('Diagram bifurkacyjny:\n {0} <= r <= {1}\n x_0 = {2}\n na wykresie zaznaczono {3} ostatnich iteracji z {4}'.format(min_r, max_r, x_0, last, iterations))
    plt.show()


bifurcation_diagram(0.2, 1, 4, 1000, 200, 100, np.float64)
bifurcation_diagram(0.4, 1, 4, 1000, 200, 100, np.float64)
bifurcation_diagram(0.9888, 1, 4, 1000, 200, 100, np.float64)
bifurcation_diagram(0.0001, 1, 4, 1000, 200, 100, np.float64)
bifurcation_diagram(0.0001, 3.57, 4, 1000, 500, 400, np.float64)


# b
def trajectories_float32_float64(x_0, r, n):
    r_float32 = np.float32(r)
    r_float64 = np.float64(r)
    x_float32 = np.float32(x_0)
    x_float64 = np.float64(x_0)

    iterations = np.arange(0, n + 1)
    x_n_float32 = [x_float32]
    x_n_float64 = [x_float64]

    for _ in range(n):
        x_float32 = logistic_float32(x_float32, r_float32)
        x_float64 = logistic(x_float64, r_float64)
        x_n_float32.append(x_float32)
        x_n_float64.append(x_float64)

    plt.plot(iterations, x_n_float32, marker='.', color='r', label='float32')
    plt.plot(iterations, x_n_float64, marker='.', color='g', label='float64')

    plt.xlabel('iteracja')
    plt.ylabel('x')
    plt.xlim(0, n)
    plt.legend(loc='lower left')
    plt.title('Trajektorie:\nr = {0} \nx_0 = {1}'.format(r, x_0))
    plt.show()


trajectories_float32_float64(0.31233211, 3.75, 60)
trajectories_float32_float64(0.31233211, 3.7843123, 60)
trajectories_float32_float64(0.31233211, 3.8, 60)
trajectories_float32_float64(0.3, 3.75, 60)
trajectories_float32_float64(0.3, 3.7843123, 60)
trajectories_float32_float64(0.3, 3.8, 60)


# c
def iterations_to_zero(x_0, iterations_limit, r=np.float32(4)):
    x = np.array(x_0)
    iterations = np.full(x.shape[0], 0)
    zeros = np.full(x.shape[0], False)

    for i in range(iterations_limit):
        x = logistic(x, r)
        temp = (x == np.float32(0))
        iterations[zeros != temp] = i
        zeros = temp

    plt.plot(x_0[iterations != 0], iterations[iterations != 0], '.r')
    plt.xlabel('x_0')
    plt.ylabel('iteracje po których osiągnięto 0')
    plt.show()

    count = iterations[iterations != 0].shape[0]
    print("Osiągnęły zero: ", count)
    print("Nie osiągnęły zera: ", x.shape[0] - count)


iterations_to_zero(np.linspace(0.001, 0.999, 300, dtype=np.float32), 1000000)
