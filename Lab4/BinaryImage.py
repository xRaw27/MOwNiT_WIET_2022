import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation


class BinaryImage:
    def __init__(self, n, delta):
        self.n = n
        self.delta = delta
        self.image = None
        self.random_init_state()
        self.frames = []

    def random_init_state(self):
        k = int(self.n ** 2 * self.delta)
        arr = np.concatenate((np.ones(k, int), np.zeros(self.n ** 2 - k, int)))
        self.image = np.random.permutation(arr).reshape(self.n, -1)

    def plot(self):
        fig, ax = plt.subplots(figsize=(18, 9))
        ax.matshow(self.image, cmap=ListedColormap(['w', 'k']))
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


if __name__ == "__main__":
    bi = BinaryImage(5, 0.2)

    for _ in range(100):
        bi.random_init_state()
        bi.save_frame()


    # print()
    # print("im1")
    # print(bi)
    #
    #
    # bi.random_init_state()
    # bi.save_frame()
    # print()
    # print("im2")
    # print(bi)
    #
    # bi.random_init_state()
    # bi.save_frame()
    # print()
    # print("im3")
    # print(bi)

    anime = bi.animation()
    anime.save("dupa.gif")
