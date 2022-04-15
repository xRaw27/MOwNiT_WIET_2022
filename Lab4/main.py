import numpy as np
from TSP import TSP
from SimulatedAnnealing import SimulatedAnnealing
from Sudoku import Sudoku


def main():
    print(" s t a r t ")
    # tsp = TSP(3, [(0, 5), (3, 10), (-7, 14)])
    # tsp = TSP(10)
    # tsp.points_from_uniform_distribution()

    tsp = TSP(10)

    tsp = TSP(10)
    t_0 = 3 * SimulatedAnnealing.init_cost_variance(200, lambda: tsp.cost(), lambda: tsp.points_from_uniform_distribution())
    sa = SimulatedAnnealing(tsp, T=t_0, T_min=1, n=1000, alfa=0.99)
    animation = sa.optimize(save_animation=True, iterations_per_frame=50)
    animation.save("essasito.gif")

    # tsp.plot()


def sudoku():
    names = ["very_easy1", "very_easy2", "easy1", "easy2", "moderate1", "moderate2", "hard1", "hard2", "very_hard1", "very_hard2"]

    sud = Sudoku("./sudoku_data/" + "most_difficult")
    t_0 = SimulatedAnnealing.init_temperature(sud, 50)
    sa = SimulatedAnnealing(sud, T=t_0, T_min=0.1, n=100, alfa=0.99, restarts=30)
    sa.optimize()


def sudoku_translate(sud):
    res = ""
    for x in sud:
        if x == "x":
            res += "0"
        else:
            res += x

    print(res)


def init_t_test():
    tsp = TSP(50)
    t_1 = 3 * SimulatedAnnealing.init_cost_variance(200, lambda: tsp.cost(), lambda: tsp.points_from_uniform_distribution())
    print(t_1)
    t_0 = 3 * SimulatedAnnealing.init_temperature(tsp, 200)
    print(t_0)


if __name__ == "__main__":
    # main()
    # sudoku_translate("070000043040009610800634900094052000358460020000800530080070091902100005007040802")
    # sudoku_translate("x25xxxxx3x6x32xxxxxxx5xx1xxx47x58xxxxx6xxx2xxxxx24x89xxx8xx7xxxxxxx95x3x9xxxxx51x")
    sudoku()
    # init_t_test()
