import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def electric_circuit_kirchhoff_laws(G, s, t, E, show_node_labels=False, show_edge_labels=False, connection_style='arc3', current_round_digits=1, seed=None, spring_iterations=1000):
    G = nx.convert_node_labels_to_integers(G)
    G.add_edge(s, t, SEM=True, i=0, R=0, spring_weight=0)

    n = nx.number_of_nodes(G)
    m = nx.number_of_edges(G)
    A = np.zeros((m, m))
    b = np.zeros(m)
    print(f"n = {n}, m = {m}")

    i = 1
    for u, v in G.edges:
        if "SEM" not in G[u][v]:
            G[u][v]["SEM"] = False
            G[u][v]["i"] = i
            if "R" not in G[u][v]:
                G[u][v]["R"] = 1
            i += 1

    [print(x) for x in G.edges.data()]

    for u in list(G.nodes)[:-1]:
        for v in nx.neighbors(G, u):
            if u < v:
                A[u, G[u][v]["i"]] = -1
            else:
                A[u, G[u][v]["i"]] = 1

    print(A)
    print(len(nx.cycle_basis(G)))

    num_of_equations = n - 1
    for cycle in nx.cycle_basis(G):
        print("\n\n", cycle)
        u = cycle[-1]
        for v in cycle:
            if G[u][v]["SEM"]:
                if u > v:
                    b[num_of_equations] = E
                else:
                    b[num_of_equations] = -E
            else:
                if u > v:
                    A[num_of_equations, G[u][v]["i"]] = G[u][v]["R"]
                else:
                    A[num_of_equations, G[u][v]["i"]] = -G[u][v]["R"]
            u = v
        num_of_equations += 1

    x = np.linalg.solve(A, b)
    print(A)
    print(b)
    print(x)

    H = G.copy()
    G = nx.DiGraph()

    # [print(x) for x in G.edges.data()]
    [print(x) for x in H.edges.data()]

    for u, v in H.edges:
        I = x[H[u][v]["i"]]
        if I > 0:
            G.add_edge(min(u, v), max(u, v), I=I)
        else:
            G.add_edge(max(u, v), min(u, v), I=-I)

    edge_colors = [d["I"] for u, v, d in G.edges(data=True) if not H[u][v]["SEM"]]
    print(edge_colors)
    print(G.edges.data())

    plt.figure(figsize=(18, 9))

    plasma_modified = plt.cm.get_cmap('plasma_r', 256)
    cmap = mpl.colors.ListedColormap(np.vstack((plasma_modified(np.linspace(0.05, 0.8, 256)), plasma_modified(np.linspace(0.8, 1, 256)))))

    pos = nx.spring_layout(H, weight="spring_weight", iterations=spring_iterations, seed=seed)
    nodes = nx.draw_networkx_nodes(G, pos, node_size=20, node_color="black")
    sem_edge = nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[(u, v) for u, v in G.edges if H[u][v]["SEM"]],
        arrowstyle="->",
        arrowsize=20,
        width=2
    )
    edges = nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[(u, v) for u, v in G.edges if not H[u][v]["SEM"]],
        arrowstyle="->",
        connectionstyle=connection_style,
        arrowsize=20,
        edge_color=edge_colors,
        edge_cmap=cmap,
        width=1.2
    )

    # e_labels = dict([((u, v), f'{H[u][v]["spring_weight"]}')for u, v in G.edges if not H[u][v]["SEM"]])
    if show_node_labels:
        nx.draw_networkx_labels(G, pos, verticalalignment='bottom', horizontalalignment='right', font_size=10)

    edge_labels = {}
    if show_edge_labels:
        edge_labels = dict([((u, v), f'{H[u][v]["R"]}Ω\n{round(G[u][v]["I"], current_round_digits)}A') for u, v in G.edges if not H[u][v]["SEM"]])
    edge_labels[(s, t)] = "SEM"
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    ax = plt.gca()
    pc = mpl.collections.PatchCollection(edges, cmap=cmap)
    pc.set_array(edge_colors)
    plt.colorbar(pc, label=f'Natężenie prądu I[A]', ax=ax)

    ax.set_title(f'SEM ε = {E}V, I={round(G[s][t]["I"], current_round_digits)}A')
    ax.margins(0)
    plt.show()



def main():
    graph = nx.grid_2d_graph(5, 4)


    # 'arc3, rad = 0.03'

    # plt.clf()

    electric_circuit_kirchhoff_laws(graph, 0, 5, 100, connection_style='arc3', spring_iterations=1000, seed=123)


    graph = nx.watts_strogatz_graph(30, 4, 0.2)

    for u, v in graph.edges:
        graph[u][v]["spring_weight"] = 1
        if min(abs(u - v), 31 - abs(u - v)) > 2:
            graph[u][v]["spring_weight"] = 0

    electric_circuit_kirchhoff_laws(graph, 0, 15, 100, connection_style='arc3', spring_iterations=1000, seed=123)
    plt.show()


if __name__ == "__main__":
    main()
