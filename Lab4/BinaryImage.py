import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation


class BinaryImage:
    def __init__(self, n, delta, neighborhood_rules):
        self.n = n
        self.delta = delta
        self.init_state = None
        self.image = None
        self.random_init_state()
        self.frames = []

        self.neighborhood_rules = neighborhood_rules
        self.current_cost = self.cost()

    def random_init_state(self):
        k = int(self.n ** 2 * self.delta)
        arr = np.concatenate((np.ones(k, int), np.zeros(self.n ** 2 - k, int)))
        self.image = np.random.permutation(arr).reshape(self.n, -1)
        self.init_state = self.image.copy()

    def make_move(self, mv):
        row, col, row_2, col_2, new_cost = mv
        self.image[row, col], self.image[row_2, col_2] = self.image[row_2, col_2], self.image[row, col]
        self.current_cost = new_cost

    def random_move(self):
        index = np.random.randint(self.n ** 2)
        while self.image[index // self.n, index % self.n] == 0:
            index = np.random.randint(self.n ** 2)
        row, col = index // self.n, index % self.n

        index = np.random.randint(self.n ** 2)
        while self.image[index // self.n, index % self.n] == 1:
            index = np.random.randint(self.n ** 2)
        row_2, col_2 = index // self.n, index % self.n

        new_cost = self.current_cost + self.local_cost(row, col, row_2, col_2)
        return new_cost, (row, col, row_2, col_2, new_cost)

    def get_state(self):
        return self.image

    def neighborhood_cost(self, row, col):
        c = 0

        for i, j, x in self.neighborhood_rules:
            c += x * self.image[(row + i) % self.n, (col + j) % self.n]

        return c

    def local_cost(self, row, col, row_2, col_2):
        unique = set()

        for i, j, _ in self.neighborhood_rules:
            unique.add(((row + i) % self.n, (col + j) % self.n))
            unique.add(((row_2 + i) % self.n, (col_2 + j) % self.n))

        c = 0
        for i, j in unique:
            if self.image[i, j] == 1:
                c -= self.neighborhood_cost(i, j)

        self.image[row, col], self.image[row_2, col_2] = self.image[row_2, col_2], self.image[row, col]
        for i, j in unique:
            if self.image[i, j] == 1:
                c += self.neighborhood_cost(i, j)

        self.image[row, col], self.image[row_2, col_2] = self.image[row_2, col_2], self.image[row, col]
        return c

    def cost(self):
        c = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.image[i, j] == 1:
                    c += self.neighborhood_cost(i, j)

        return c

    def plot(self, image=None):
        if image is not None:
            self.image = image

        fig, ax = plt.subplots(1, 2, figsize=(16, 9))
        ax[0].matshow(self.init_state, cmap=ListedColormap(['w', 'k']))
        ax[0].set_title("Init state")
        ax[1].matshow(self.image, cmap=ListedColormap(['w', 'k']))
        ax[1].set_title("Best state")
        plt.show()

    def save_frame(self):
        self.frames.append(self.image.copy())

    def animation(self):
        fig, ax = plt.subplots(figsize=(18, 9))
        im = ax.matshow(self.image, cmap=ListedColormap(['w', 'k']))

        def init():
            im.set_data(self.image)
            return im

        def update(i):
            im.set_data(self.frames[i])
            return im

        animation = FuncAnimation(fig, update, init_func=init, frames=len(self.frames), interval=200)
        plt.close()
        return animation

    def __repr__(self):
        return f"BinaryImage: \n  n: {self.n}\n  delta: {self.delta}\n  image: \n{self.image}"

    def __str__(self):
        res = ""
        for i in range(self.n):
            for j in range(self.n):
                res += "■" if self.image[i, j] == 1 else " "
            res += "\n"

        return res
