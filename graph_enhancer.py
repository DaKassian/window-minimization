from enum import Enum

import networkx

import view
from graph_generator import get_bipartite_graph_modified
from view import is_parent_node, adapt_ga
from numpy import ceil
from networkx import min_weight_matching


class Metric(Enum):
    WINDOW_MAX = 1
    WINDOW_SUM = 2
    EDGE_MAX = 3
    EDGE_SUM = 4


def enhance_graph(graph, use_brute_force, metric):
    if use_brute_force:
        raise NotImplementedError("Brute Force is not implemented yet")
    else:
        if metric == Metric.WINDOW_SUM:
            return create_adapted_graph(graph, win_sum(graph))
        else:
            raise NotImplementedError("Currently only MinWinSumPar with Parallel Drawing is implemented.")


def create_adapted_graph(graph, new_positions):
    ga_new = adapt_ga(graph, new_positions)
    return get_bipartite_graph_modified(graph, ga_new)


def win_sum(graph):
    weighted_graph = create_window_graph(graph)
    edges = min_weight_matching(weighted_graph)
    new_positions = dict()
    for (p, t) in edges:
        if isinstance(p, int):
            new_positions[t] = p
        else:
            new_positions[p] = t
    return new_positions


def create_window_graph(graph):
    positions = set()
    parents = []
    edges = []
    n = graph.get_number_of_parents()
    for p in graph.get_g().nodes:
        if is_parent_node(graph.get_ga(), p):
            parents.append(p)
            [f_p, l_p] = graph.get_span(p)
            if l_p - f_p < n - 1:
                k = f_p - int(ceil((n - l_p + f_p - 1) / 2))
            else:
                k = f_p
            for t in range(k, k + n):
                positions.add(t)
                weight = max(l_p - t, l_p - f_p, t - f_p)
                edges.append((p, t, weight))
    return create_weighted_bip_graph(parents, positions, edges)


def create_weighted_bip_graph(parents: list, positions: set, edges: list):
    weighted_graph = networkx.Graph()
    weighted_graph.add_nodes_from(positions, bipartite=0)
    weighted_graph.add_nodes_from(parents, bipartite=1)
    for (p, t, weight) in edges:
        weighted_graph.add_weighted_edges_from([(p, t, weight)])
        if view.debug:
            print("Added edge " + str(p) + " / " + str(t) + " with weight " + str(weight))
    return weighted_graph


def brute_force(graph, metric):
    return graph
