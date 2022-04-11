import numpy as np
import matplotlib.pyplot as plt


class SimulatedAnnealing:
    def __init__(self, problem, T=100, T_min=2, n=100, alfa=0.99, restarts=1, stop=0):
        self.problem = problem
        self.T_0 = T
        self.T = T
        self.n = n
        self.alfa = alfa

        self.restarts = restarts
        self.stop = stop

        self.old_cost = self.problem.cost()
        self.T_min = T_min
        self.min_cost = np.inf
        self.best_state = problem.get_state()
        self.costs = []
        self.temperatures = []

    def P(self, new_cost):
        # return 1 if new_cost < self.old_cost else np.exp((self.old_cost - new_cost) / self.T)
        return 1 if new_cost <= self.old_cost else np.exp((self.old_cost - new_cost) / self.T)

    def optimize(self, save_animation=False, iterations_per_frame=20):
        i = 0
        while self.restarts > 0:
            while self.T > self.T_min:
                # print("T: ", self.T, " COST:", self.old_cost)

                for _ in range(self.n):
                    new_cost, mv = self.problem.random_move()

                    if np.random.random() < self.P(new_cost):
                        self.problem.make_move(mv)
                        self.old_cost = new_cost
                        if new_cost < self.min_cost:
                            self.min_cost = new_cost
                            self.best_state = self.problem.get_state()

                self.costs.append(self.old_cost)
                self.temperatures.append(self.T)
                self.T = self.alfa * self.T

                if save_animation and i % iterations_per_frame == 0:
                    self.problem.save_frame()
                i += 1

                if self.min_cost <= self.stop:
                    break

            self.restarts -= 1
            if self.restarts > 0:
                if self.min_cost <= self.stop:
                    break
                self.T = SimulatedAnnealing.init_temperature(self.problem, 10)

        self.plot()
        self.problem.plot(self.best_state)
        if save_animation:
            return self.problem.animation()

    def plot(self):
        fig, ax = plt.subplots(1, 2, figsize=(18, 7))
        steps = np.arange(1, len(self.costs) + 1)
        fig.suptitle(f"Number of moves: {len(self.temperatures) * self.n}")
        ax[0].set_xlabel("Steps")
        ax[0].set_ylabel("Cost")
        ax[0].plot(steps, self.costs)
        ax[1].set_xlabel("Steps")
        ax[1].set_ylabel("T")
        ax[1].plot(steps, self.temperatures)
        plt.show()

    @staticmethod
    def init_cost_variance(sample_size, cost_func, init_func):
        init_costs = []
        for _ in range(sample_size):
            init_func()
            init_costs.append(cost_func())
        return np.std(init_costs)

    @staticmethod
    def init_temperature(problem, sample_size):
        costs = []
        for _ in range(sample_size):
            new_cost, mv = problem.random_move()
            costs.append(new_cost)
            problem.make_move(mv)

        return np.std(costs)
