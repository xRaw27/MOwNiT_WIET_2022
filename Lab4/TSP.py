import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class TSP:
    def __init__(self, n, list_of_points=None):
        self.n = n
        self.x_range = None
        self.y_range = None

        if list_of_points is not None:
            if len(list_of_points) != self.n:
                raise Exception('Wrong number of points')
            self.points = np.array(list_of_points).reshape(n, 2)
        else:
            self.points = np.zeros((n, 2), int)

        self.set_range()
        self.permutation = np.random.permutation(n)
        self.frames = []

    def random_init_state(self):
        self.permutation = np.random.permutation(self.n)

    def set_range(self):
        min_x, min_y = tuple(np.min(self.points, axis=0))
        max_x, max_y = tuple(np.max(self.points, axis=0))
        self.x_range = (min_x, max_x)
        self.y_range = (min_y, max_y)

    def points_from_uniform_distribution(self, _min=-100, _max=100):
        self.points = np.random.uniform(_min, _max, (self.n, 2))
        self.set_range()

    def points_from_normal_distribution(self, mean=np.array([0, 0]), cov=np.array([[1, 0], [0, 1]])):
        self.points = np.random.multivariate_normal(mean, cov, (self.n, 2))
        self.set_range()

    def make_move(self, mv):
        a, b = mv
        self.permutation[a], self.permutation[b] = self.permutation[b], self.permutation[a]

    def random_move(self):
        a = np.random.randint(0, self.n)
        b = np.random.randint(0, self.n)
        while a == b:
            b = np.random.randint(0, self.n)

        self.permutation[a], self.permutation[b] = self.permutation[b], self.permutation[a]
        new_cost = self.cost()
        self.permutation[a], self.permutation[b] = self.permutation[b], self.permutation[a]

        return new_cost, (a, b)

    def get_state(self):
        return self.permutation.copy()

    def cost(self):
        cycle = self.points[self.permutation, :]
        cycle = np.vstack((cycle, cycle[0]))

        return np.sum(np.sqrt(np.sum(np.diff(cycle, axis=0) ** 2, axis=1)))

    def plot(self, permutation=None):
        if permutation is not None:
            self.permutation = permutation

        cycle = self.points[self.permutation, :]
        cycle = np.vstack((cycle, cycle[0]))

        fig, ax = plt.subplots(figsize=(18, 9))
        ax.plot(*cycle.T)
        for i in range(self.n):
            ax.annotate(i, tuple(self.points[i]))

        ax.plot(*cycle.T, 'o')
        ax.set_title(f"Best state:\n permutation = {np.array2string(self.permutation, max_line_width=np.inf)}\n cost = {self.cost()}")
        plt.show()

    def save_frame(self):
        self.frames.append(self.permutation.copy())

    def animation(self):
        fig, ax = plt.subplots(figsize=(18, 9))
        ax.set_xlim(self.x_range)
        ax.set_ylim(self.y_range)
        lines, = ax.plot([], [])
        points, = ax.plot([], [], 'o')

        def init():
            lines.set_data([], [])
            points.set_data([], [])
            return lines, points,

        def update(i):
            cycle = self.points[self.frames[i], :]
            cycle = np.vstack((cycle, cycle[0]))
            lines.set_data(*cycle.T)
            points.set_data(*cycle.T)
            return lines, points,

        animation = FuncAnimation(fig, update, init_func=init, frames=len(self.frames), interval=200)
        plt.close()
        return animation

    def __repr__(self):
        return f"TSP: \n  n: {self.n}\n  x_range: {self.x_range}\n  y_range: {self.y_range}\n  points: \n{str(self.points)}"

    def __str__(self):
        return self.__repr__()
