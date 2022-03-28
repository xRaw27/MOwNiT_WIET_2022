import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from random import randint


def draw_solution(G, H, s, t, E, show_node_labels, show_edge_labels, edge_label_pos, pos, connection_style, current_round_digits):
    plt.figure(figsize=(18, 9))

    # Making a list of edge colors
    plasma_modified = plt.cm.get_cmap('plasma_r', 256)
    cmap = mpl.colors.ListedColormap(np.vstack((plasma_modified(np.linspace(0.05, 0.8, 256)), plasma_modified(np.linspace(0.8, 1, 256)))))
    edge_colors = [d["I"] for u, v, d in G.edges(data=True) if not H[u][v]["SEM"]]

    # Positioning graph nodes
    if pos is None:
        pos = nx.kamada_kawai_layout(H)
        # pos = nx.spring_layout(H, weight="spring_weight", iterations=spring_iterations, seed=seed)

    # Drawing graph nodes
    nx.draw_networkx_nodes(G, pos, node_size=20, node_color="black")

    # Drawing graph edges
    sem = [(u, v) for u, v in G.edges if H[u][v]["SEM"]]
    other = [(u, v) for u, v in G.edges if not H[u][v]["SEM"]]

    nx.draw_networkx_edges(G, pos, edgelist=sem, arrowstyle="->", arrowsize=20, width=2)
    edges = nx.draw_networkx_edges(
        G, pos, edgelist=other,
        arrowstyle="->", arrowsize=20,
        connectionstyle=connection_style,
        edge_color=edge_colors, edge_cmap=cmap,
        width=1.2
    )

    # Drawing node labels
    if show_node_labels:
        nx.draw_networkx_labels(G, pos, verticalalignment='bottom', horizontalalignment='right', font_size=10)

    # Drawing edge labels
    edge_labels = {}
    if show_edge_labels:
        edge_labels = dict([((u, v), f'{H[u][v]["R"]}Ω\n{round(G[u][v]["I"], current_round_digits)}A') for u, v in G.edges if not H[u][v]["SEM"]])
    edge_labels[(s, t)] = "SEM"
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=edge_label_pos)

    # Setting title, margins and color bar
    ax = plt.gca()
    pc = mpl.collections.PatchCollection(edges, cmap=cmap)
    pc.set_array(edge_colors)
    ax.set_title(f'SEM ε = {E}V, I={round(G[s][t]["I"], current_round_digits)}A')
    ax.margins(0)

    plt.colorbar(pc, label=f'Natężenie prądu I[A]', ax=ax)
    plt.show()


def electric_circuit_kirchhoff_laws(G, s, t, E, show_node_labels=False, show_edge_labels=False, edge_label_pos=0.5,
                                    pos=None, connection_style='arc3', current_round_digits=2):

    # Initialization of the graph and the matrix
    s, t = min(s, t), max(s, t)
    G.add_edge(s, t, SEM=True, i=0, R=0)

    n = nx.number_of_nodes(G)
    m = nx.number_of_edges(G)
    A = np.zeros((m, m))
    b = np.zeros(m)

    i = 1
    for u, v in G.edges:
        if "SEM" not in G[u][v]:
            G[u][v]["SEM"] = False
            G[u][v]["i"] = i
            if "R" not in G[u][v]:
                G[u][v]["R"] = 1
            i += 1

    # Kirchhoff's current law
    num_of_equations = 0
    for u in list(G.nodes)[:-1]:
        for v in nx.neighbors(G, u):
            if u < v:
                A[num_of_equations, G[u][v]["i"]] = -1
            else:
                A[num_of_equations, G[u][v]["i"]] = 1

        num_of_equations += 1

    # Kirchhoff's voltage law
    # num_of_equations = n - 1
    for cycle in nx.cycle_basis(G):
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

    # Solving a system of linear equations
    x = np.linalg.solve(A, b)

    # Creating a directed graph with a value of electric current on its edges
    H = nx.DiGraph()
    G, H = H, G
    for u, v in H.edges:
        I = x[H[u][v]["i"]]
        if I > 0:
            G.add_edge(min(u, v), max(u, v), I=I)
        else:
            G.add_edge(max(u, v), min(u, v), I=-I)

    # Drawing solution:
    # G is a directed graph that has information about current (I) on its edges
    # H is an undirected graph whose edges contain information about resistance (R) and is SEM edge
    draw_solution(G, H, s, t, E, show_node_labels, show_edge_labels, edge_label_pos, pos, connection_style, current_round_digits)
    return G, H


def electric_circuit_nodal_analysis(G, s, t, E, show_node_labels=False, show_edge_labels=False, edge_label_pos=0.5,
                                    pos=None, connection_style='arc3', current_round_digits=2):

    # Initialization of the graph and the matrix
    s, t = min(s, t), max(s, t)
    G.add_edge(s, t, SEM=True, R=0)

    G.nodes[s]["V"] = 0
    G.nodes[t]["V"] = E
    G.nodes[s]["v"] = G.nodes[t]["v"] = None

    for u, v in G.edges:
        if "SEM" not in G[u][v]:
            G[u][v]["SEM"] = False
        if "R" not in G[u][v]:
            G[u][v]["R"] = 1

    n = 0
    for u in G.nodes:
        if "v" not in G.nodes[u]:
            G.nodes[u]["v"] = n
            n += 1

    A = np.zeros((n, n))
    b = np.zeros(n)

    # Nodes voltages are unknowns and the current between two nodes is equal to a difference of voltages divided by
    # the resistance. For each unknown node voltage we form an equation based on Kirchhoff's current law.
    for node in G.nodes:
        node_v = G.nodes[node]["v"]
        if node_v is not None:
            for neighbor in nx.neighbors(G, node):
                R = G[node][neighbor]["R"]
                neighbor_v = G.nodes[neighbor]["v"]

                A[node_v, node_v] += 1 / R

                if neighbor_v is not None:
                    A[node_v, neighbor_v] = -1 / R

                elif G.nodes[neighbor]["V"] != 0:
                    b[node_v] = G.nodes[neighbor]["V"] / R

    # Solving a system of linear equations and assigning voltages to nodes
    x = np.linalg.solve(A, b)

    for node in G.nodes:
        node_v = G.nodes[node]["v"]
        if node_v is not None:
            G.nodes[node]["V"] = x[node_v]

    # Creating a directed graph with a value of electric current on its edges
    H = nx.DiGraph()
    G, H = H, G
    for node1, node2 in H.edges:
        if not H[node1][node2]["SEM"]:
            V1 = H.nodes[node1]["V"]
            V2 = H.nodes[node2]["V"]
            R = H[node1][node2]["R"]

            if V1 > V2:
                G.add_edge(node1, node2, I=(V1 - V2) / R)
            else:
                G.add_edge(node2, node1, I=(V2 - V1) / R)

    G.add_edge(s, t, I=sum([G[t][u]["I"] for u in nx.neighbors(G, t)]))

    # Drawing solution:
    # G is a directed graph that has information about current (I) on its edges
    # H is an undirected graph whose edges contain information about resistance (R), is SEM edge, spring weight of the edge for spring layout
    draw_solution(G, H, s, t, E, show_node_labels, show_edge_labels, edge_label_pos, pos, connection_style, current_round_digits)
    return G, H


def is_solution_correct(G, H, E):
    is_correct = True

    # check Kirchhoff's current law
    for u in G.nodes:
        in_I = out_I = 0
        for v in G.successors(u):
            out_I += G[u][v]["I"]
        for v in G.predecessors(u):
            in_I += G[v][u]["I"]

        is_correct = is_correct and np.isclose(in_I, out_I)

    # check Kirchhoff's voltage law
    for cycle in nx.cycle_basis(H):
        voltages_sum = 0

        u = cycle[-1]
        for v in cycle:
            if G.has_edge(u, v):
                voltages_sum -= G[u][v]["I"] * H[u][v]["R"] if not H[u][v]["SEM"] else -E
            else:
                voltages_sum += G[v][u]["I"] * H[u][v]["R"] if not H[u][v]["SEM"] else -E
            u = v

        is_correct = is_correct and np.isclose(voltages_sum, 0)

    return is_correct


def main():
    graph = nx.grid_2d_graph(2, 2)
    # electric_circuit_kirchhoff_laws(graph, 0, 5, 100, connection_style='arc3', show_edge_labels=True, spring_iterations=1, seed=123)

    # graph = nx.watts_strogatz_graph(30, 4, 0.2)
    #
    # # exit()
    #
    # for u, v in graph.edges:
    #     graph[u][v]["spring_weight"] = 1
    #     if min(abs(u - v), 31 - abs(u - v)) > 2:
    #         graph[u][v]["spring_weight"] = 0
    #
    # electric_circuit_kirchhoff_laws(graph, 0, 15, 100, connection_style='arc3', spring_iterations=1000, seed=123)

    # graph = nx.Graph()
    # graph.add_nodes_from([0, 1, 2, 3])
    # graph.add_edges_from([(1, 3, {"R": 1}), (2, 3, {"R": 2}), (1, 2, {"R": 1}), (1, 0, {"R": 2}), (2, 0, {"R": 1})])

    # graph = nx.grid_2d_grap(5, 5)
    # graph = nx.convert_node_labels_to_integers(graph)
    #
    # graph = nx.watts_strogatz_graph(30, 4, 0.1)
    # nx.write_edgelist(graph, path="small_world_30_nodes", data=["R", "spring_weight"])
    #
    #
    # graph = nx.random_regular_graph(3, 30)
    # for u, v in graph.edges:
    #     graph[u][v]["R"] = randint(1, 99)
    #
    # nx.write_edgelist(graph, path="essa/3-regular_30_nodes_random_R", data=["R", "spring_weight"])

    # graph = nx.read_edgelist(path="3-regular_100_nodes",  data=(('R', float), ('spring_weight', float),))
    # graph = nx.read_edgelist(path="3-regular_100_nodes", nodetype=int)
    # graph = nx.read_edgelist(path="essa/3-regular_30_nodes_random_R", nodetype=int, data=(('R', float),))
    # graph = nx.read_edgelist(path="3-regular_100_nodes")
    # graph = nx.read_edgelist(path="essa/3-regular_100_nodes", nodetype=int)

    # nx.write_edgelist(graph, path="essa/3-regular_100_nodes", data=["R", "spring_weight"])

    # print(graph.edges.data())
    # [print(x) for x in G.edges.data()]

    # electric_circuit_kirchhoff_laws(graph, 0, 10, 100, show_edge_labels=True, seed=10)
    # electric_circuit_kirchhoff_laws(graph, 0, 10, 100, seed=10)
    # graph = nx.convert_node_labels_to_integers(graph)
    # electric_circuit_kirchhoff_laws(graph, 0, 2, 100, seed=10)
    # electric_circuit_kirchhoff_laws(graph, 0, 40, 100, seed=10)
    # electric_circuit_kirchhoff_laws(graph, 0, 3, 14, spring_iterations=10000)

    # G, H = electric_circuit_nodal_analysis(graph, 0, 10, 100)
    # is_correct = is_solution_correct(G, H, 14)
    #
    # print("Czy poprawne: ", is_solution_correct(G, H, 14))

    # ESSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

    """ 3-regularny """

    # graph = nx.read_edgelist(path="./tests/3-regular_30_nodes_random_R", nodetype=int, data=(('R', float),))
    # pos = nx.kamada_kawai_layout(graph)
    # electric_circuit_kirchhoff_laws(graph.copy(), 12, 27, 100, show_node_labels=True, show_edge_labels=True, pos=pos)
    # electric_circuit_nodal_analysis(graph.copy(), 3, 12, 100, show_edge_labels=True, pos=pos)
    # electric_circuit_kirchhoff_laws(graph.copy(), 2, 18, 100, show_edge_labels=True, pos=pos)
    # electric_circuit_nodal_analysis(graph.copy(), 10, 25, 100, show_edge_labels=True, pos=pos)

    # graph = nx.read_edgelist(path="./tests/3-regular_100_nodes", nodetype=int)
    # pos = nx.kamada_kawai_layout(graph)
    # electric_circuit_kirchhoff_laws(graph.copy(), 52, 68, 100, pos=pos)
    # electric_circuit_nodal_analysis(graph.copy(), 40, 67, 100, pos=pos)
    # electric_circuit_kirchhoff_laws(graph.copy(), 60, 80, 100, pos=pos)
    # electric_circuit_nodal_analysis(graph.copy(), 12, 24, 100, pos=pos)

    """ Z mostem """

    G = nx.random_regular_graph(3, 10, seed=10)
    H = nx.random_regular_graph(3, 10, seed=30)
    map = {x - 10: x for x in range(10, 20)}
    nx.relabel_nodes(H, mapping=map, copy=False)

    print(G.nodes)
    print(H.nodes)
    print(G.edges.data())
    print(H.edges.data())

    F = nx.compose(G, H)

    nx.draw(F, pos=nx.kamada_kawai_layout(F))
    plt.show()


    """ Siatka 2D """

    # graph = nx.read_edgelist(path="./tests/grid_5x5_random_R", nodetype=int, data=(('R', float),))
    # pos = nx.kamada_kawai_layout(graph)
    # electric_circuit_nodal_analysis(graph.copy(), 0, 6, 100, show_edge_labels=True, pos=pos)
    # electric_circuit_nodal_analysis(graph.copy(), 8, 12, 100, show_edge_labels=True, pos=pos)
    # electric_circuit_nodal_analysis(graph.copy(), 3, 20, 100, show_edge_labels=True, pos=pos)
    # electric_circuit_nodal_analysis(graph.copy(), 4, 23, 100, show_edge_labels=True, pos=pos)
    #
    # graph = nx.read_edgelist(path="./tests/grid_16x10", nodetype=int)
    # pos = nx.kamada_kawai_layout(graph)
    # electric_circuit_nodal_analysis(graph.copy(), 2, 43, 100, pos=pos)
    # electric_circuit_nodal_analysis(graph.copy(), 38, 121, 100, pos=pos)

    """ Small world """

    # graph = nx.read_edgelist(path="./tests/small_world_40_nodes", nodetype=int)
    # pos = nx.circular_layout(graph)
    # electric_circuit_kirchhoff_laws(graph.copy(), 11, 21, 100, pos=pos, connection_style='arc3,rad=0.3')
    # electric_circuit_nodal_analysis(graph.copy(), 25, 37, 100, pos=pos, connection_style='arc3,rad=0.3')
    # electric_circuit_kirchhoff_laws(graph.copy(), 26, 30, 100, pos=pos, connection_style='arc3,rad=0.3')
    # electric_circuit_nodal_analysis(graph.copy(), 10, 30, 100, pos=pos, connection_style='arc3,rad=0.3')





    # graph = nx.grid_2d_graph(16, 10)
    # graph = nx.convert_node_labels_to_integers(graph)
    # # for u, v in graph.edges:
    # #     graph[u][v]["R"] = randint(1, 99)
    #
    # nx.write_edgelist(graph, path="essa/grid_20x10", data=["R"])


if __name__ == "__main__":
    main()


