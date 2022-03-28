import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from time import time

# G = nx.grid_2d_graph(2, 2)
# G = nx.convert_node_labels_to_integers(G)
# G.add_edge(0, 3)
# G = nx.convert_node_labels_to_integers(G)
# G = nx.to_directed(G)
#
# # cycle_generator =
#
# print(list(nx.simple_cycles(G)))
#
# # print(next(cycle_generator))
# #
# # print(next(cycle_generator))
#
# # start = time()
# #
# # print(len(list(nx.simple_cycles(G))))
# #
# # print(time() - start)
#
# nx.draw(G)
# plt.show()


graph = nx.grid_2d_graph(50, 10)

graph = nx.convert_node_labels_to_integers(graph)

n = nx.number_of_nodes(graph)

print(list(nx.neighbors(graph, 0)))

# for i in range(n):
#     graph.nodes[i]["V"] = 10
#
# xd = [10 for _ in range(n)]
#
# start = time()
#
# for i in range(n):
#     graph.nodes[i]["V"] = 43
#
# print(time() - start)
#
# start = time()
#
# for i in range(n):
#     xd[i] = 43
#
# print(time() - start)


# graph.add_nodes_from([0, 1, 2, 3])
# graph.add_edges_from([(1, 3, {"R": 1}), (2, 3, {"R": 2}), (1, 2, {"R": 1}), (1, 0, {"R": 2}), (2, 0, {"R": 1})])





# from random import randint
# from time import time
#
# reversed_cycles = set()
#
#
# start = time()
#
# # for _ in range(20):
# #     reversed_cycles.add(tuple([randint(0, 10000000) for _ in range(2000000)]))
#
#
# cycle1 = [randint(0, 10000000) for _ in range(10000000)]
# cycle2 = list(reversed(cycle1))
#
# print(time() - start)
#
# # print(cycle1)
# # print(cycle2)
#
# # exit()
#
#
#
# cycle = cycle1
#
# start = time()
#
# i = np.argmin(cycle)
# temp = cycle[i + 1:] + cycle[:i]
#
# if not tuple(cycle[i:i+1] + temp) in reversed_cycles:
#     temp.reverse()
#     reversed_cycles.add(tuple(cycle[i:i + 1] + temp))
#
#     print("cycle")
# else:
#     print("reversed:")
#
# print(time() - start)
#
# cycle = cycle2
#
# start = time()
#
# i = np.argmin(cycle)
# temp = cycle[i + 1:] + cycle[:i]
#
# if not tuple(cycle[i:i+1] + temp) in reversed_cycles:
#     temp.reverse()
#     reversed_cycles.add(tuple(cycle[i:i + 1] + temp))
#
#     print("cycle")
# else:
#     print("reversed:")
#
# print(time() - start)
#
# start = time()
#
# for x in cycle:
#     if x == 0:
#         print("XD")
#
# print(time() - start)
