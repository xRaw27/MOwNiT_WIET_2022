import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


G = nx.grid_2d_graph(2, 2)

G = nx.convert_node_labels_to_integers(G)
G.add_edge(0, 3, SEM=True, i=0, R=0, I=0, spring_weight=0)

n = nx.number_of_nodes(G)
m = nx.number_of_edges(G)
E = 10
A = np.zeros((m, m))
b = np.zeros(m)
print(f"n = {n}, m = {m}")


G = nx.DiGraph(G)
[print(x) for x in G.edges.data()]


i = 1
for u, v in G.edges:
    if "SEM" not in G[u][v] and u > v:
        G[u][v]["SEM"] = G[v][u]["SEM"] = False
        G[u][v]["R"] = G[v][u]["R"] = 1
        G[u][v]["I"] = G[v][u]["I"] = 0
        G[u][v]["i"] = G[v][u]["i"] = i
        i += 1

for u in list(G.nodes)[:-1]:
    for v in nx.neighbors(G, u):
        if u < v:
            A[u, G[u][v]["i"]] = -1
        else:
            A[u, G[u][v]["i"]] = 1


print(nx.cycle_basis(G))

# cycle_generator = nx.simple_cycles(G)
# # next(cycle_generator)
#
# reversed_cycles = set()
# num_of_equations = n - 1
# while num_of_equations < m:
#     cycle = next(cycle_generator)
#     if len(cycle) > 2:
#         i = np.argmin(cycle)
#         temp = cycle[i + 1:] + cycle[:i]
#
#         if not tuple(cycle[i:i+1] + temp) in reversed_cycles:
#             temp.reverse()
#             reversed_cycles.add(tuple(cycle[i:i + 1] + temp))
#
#             print("\n\n", cycle)
#             u = cycle[-1]
#             for v in cycle:
#                 if G[u][v]["SEM"]:
#                     if u > v:
#                         # print(u, v, "minus E", E)
#                         b[num_of_equations] = E
#                     else:
#                         # print(u, v, "plus E", E)
#                         b[num_of_equations] = -E
#                 else:
#                     if u > v:
#                         print(u, v, "plus IR", )
#                         A[num_of_equations, G[u][v]["i"]] = G[u][v]["R"]
#                     else:
#                         print(u, v, "minus IR")
#                         A[num_of_equations, G[u][v]["i"]] = -G[u][v]["R"]
#                 u = v
#             num_of_equations += 1

exit()

x = np.linalg.solve(A, b)
print(A)
print(b)
print(x)

to_remove = []
for u, v in G.edges:
    G[u][v]["I"] = x[G[u][v]["i"]]
    if u < v:
        if G[u][v]["I"] < 0:
            to_remove.append((u, v))
    else:
        if G[u][v]["I"] < 0:
            G[u][v]["I"] = -G[u][v]["I"]
        else:
            to_remove.append((u, v))

for u, v in to_remove:
    G.remove_edge(u, v)


edge_colors = [d["I"] for u, v, d in G.edges(data=True)]
print(edge_colors)
print(G.edges.data())


cmap = plt.cm.plasma
pos = nx.spring_layout(G, weight="spring_weight", iterations=1000, seed=90)
nodes = nx.draw_networkx_nodes(G, pos, node_size=100)
labels = nx.draw_networkx_labels(G, pos)
edges = nx.draw_networkx_edges(
    G,
    pos,
    arrowstyle="->",
    connectionstyle='arc3, rad = 0.1',
    arrowsize=10,
    edge_color=edge_colors,
    edge_cmap=cmap,
    width=1
)

ax = plt.gca()
pc = mpl.collections.PatchCollection(edges, cmap=cmap)
pc.set_array(edge_colors)
plt.colorbar(pc, ax=ax)

plt.show()

