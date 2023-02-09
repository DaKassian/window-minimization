from graph_generator import create_random_bipartite_graph_with_seed
from bipartite_graph import BipartiteGraph
from graph_enhancer import enhance_graph, Metric
from view import print_graph, compare


def improve_graph(graph: BipartiteGraph, metric: Metric):
    print_graph(graph, "example")
    graph2 = enhance_graph(graph, False, metric)
    print_graph(graph2, "example-solution")
    compare(graph, graph2, metric)


if __name__ == '__main__':
    # Currently the only implemented algorithm solves MinWinSumPar in parallel drawing
    # The rest will be implemented until submission of the paper

    # This code generates random bipartite graphs with 5-15 parents and children and several edges
    # Then it minimizes the windows and compares the stats
    for number_of_parents in range(5, 15):
        for number_of_children in range(5, 15):
            for number_of_edges in range(int(number_of_children * number_of_parents * 0.2),
                                         int(number_of_children * number_of_parents * 0.8)):
                random_graph = create_random_bipartite_graph_with_seed(number_of_children, number_of_parents,
                                                                       number_of_edges, 0, False)
                improve_graph(random_graph, Metric.WINDOW_SUM)
