from ogdf_python import ogdf
from colorama import Fore
from numpy import pi, ceil, cos, sin

import graph_enhancer

node_distance = 50
parent_nodes = 0
children_nodes = 2
horizontal = True
debug = False


def print_graph(graph, label):
    ga = graph.get_ga()
    ogdf.GraphIO.write(ga, label + ".svg")
    ogdf.GraphIO.write(ga, label + ".gml")
    if debug:
        print("Graph: " + label)
        print("(" + str(graph.get_number_of_parents()) + " parents, " + str(
            graph.get_number_of_children()) + " children, " + str(len(graph.get_g().edges)) + " edges)")
        print("Attributes:\n\tWindow Max: " + str(graph.get_win_max()))
        print("\tWindow Sum: " + str(graph.get_win_sum()))
        print("\tEdge Max:   " + str(graph.get_edge_max()))
        print("\tEdge Sum:   " + str(graph.get_edge_sum()))
        print("\tSpan Max:   " + str(graph.get_span_max()))
        print("\tSpan Sum:   " + str(graph.get_span_sum()))


def transform_graph_parallel(parents, children, edges):
    g = ogdf.Graph()
    ga = ogdf.GraphAttributes(g, ogdf.GraphAttributes.all)

    for pair in parents:
        n = g.newNode()
        ga.label[n] = pair[0]
        ga.y[n] = parent_nodes * node_distance
        ga.x[n] = pair[1] * node_distance

    for pair in children:
        n = g.newNode()
        ga.label[n] = pair[0]
        ga.y[n] = children_nodes * node_distance
        ga.x[n] = pair[1] * node_distance

    for pair in edges:
        parent = None
        child = None
        for n in g.nodes:
            if ga.label[n] == pair[0]:
                parent = n
            elif ga.label[n] == pair[1]:
                child = n
        if parent is not None and child is not None:
            e = g.newEdge(parent, child)
    return [g, ga]


def transform_graph_radial(parents: list, children: list, edges: set, fraction: int):
    g = ogdf.Graph()
    ga = ogdf.GraphAttributes(g, ogdf.GraphAttributes.all)

    for pair in parents:
        n = g.newNode()
        ga.label[n] = pair[0]
        [ga.x[n], ga.y[n]] = compute_coordinates(fraction, pair[1], True)

    for pair in children:
        n = g.newNode()
        ga.label[n] = pair[0]
        [ga.x[n], ga.y[n]] = compute_coordinates(fraction, pair[1], False)

    for pair in edges:
        parent = None
        child = None
        for n in g.nodes:
            if ga.label[n] == pair[0]:
                parent = n
            elif ga.label[n] == pair[1]:
                child = n
        if parent is not None and child is not None:
            e = g.newEdge(parent, child)
    return [g, ga]


def compute_radius(fraction: int, parent: bool):
    if parent:
        return int(ceil(fraction * node_distance / 2 / pi)) + node_distance
    else:
        return int(ceil(fraction * node_distance / 2 / pi))


def compute_coordinates(fraction: int, position: int, parent: bool):
    x_coord = cos(360 / fraction * position) * compute_radius(fraction, parent)
    y_coord = sin(360 / fraction * position) * compute_radius(fraction, parent)
    return [x_coord, y_coord]


def get_stats(g, ga):
    win_max = 0
    win_sum = 0
    edge_max = 0
    edge_sum = 0
    span_max = 0
    span_sum = 0

    for p in g.nodes:
        if is_parent_node(ga, p):
            f_p = None
            l_p = None
            for adj in p.adjEntries:
                if f_p is None:
                    f_p = get_position(ga, adj.twinNode())
                    l_p = get_position(ga, adj.twinNode())
                else:
                    f_p = min(f_p, get_position(ga, adj.twinNode()))
                    l_p = max(l_p, get_position(ga, adj.twinNode()))
                edge_max = max(edge_max, abs(get_position(ga, p) - get_position(ga, adj.twinNode())))
                edge_sum += abs(get_position(ga, p) - get_position(ga, adj.twinNode()))
            if l_p is not None:
                span_max = max(span_max, l_p - f_p)
                span_sum += l_p - f_p
                window = max(l_p - f_p, l_p - get_position(ga, p), get_position(ga, p) - f_p)
                if debug:
                    print("Parent " + ga.label(p) + " on position " + str(get_position(ga, p)) + " has f_p=" + str(
                        f_p) + ", l_p=" + str(l_p) + " window=" + str(window))
                win_max = max(win_max, window)
                win_sum += window

    return [win_max, win_sum, edge_max, edge_sum, span_max, span_sum]


def is_parent_node(ga, node):
    return ga.y(node) == (parent_nodes * node_distance)


def is_child_node(ga, node):
    return ga.y(node) == (children_nodes * node_distance)


def get_position(ga, node):
    return int(ga.x[node] / node_distance)


def adapt_ga(graph, new_positions):
    g = graph.get_g()
    ga = graph.get_ga()
    ga_new = ogdf.GraphAttributes(g, ogdf.GraphAttributes.all)

    for p in g.nodes:
        ga_new.y[p] = ga.y[p]
        ga_new.label[p] = ga.label[p]
        if is_parent_node(ga, p):
            ga_new.x[p] = new_positions.get(p) * node_distance
        else:
            ga_new.x[p] = ga.x[p]
    return ga_new


def compare(old_graph, new_graph, metric):
    if debug:
        print("Compare Stats:")
    stat_compare("Window Max", old_graph.get_win_max(), new_graph.get_win_max(),
                 metric == graph_enhancer.Metric.WINDOW_MAX)
    stat_compare("Window Sum", old_graph.get_win_sum(), new_graph.get_win_sum(),
                 metric == graph_enhancer.Metric.WINDOW_SUM)
    stat_compare("Edge Max  ", old_graph.get_edge_max(), new_graph.get_edge_max(),
                 metric == graph_enhancer.Metric.EDGE_MAX)
    stat_compare("Edge Sum  ", old_graph.get_edge_sum(), new_graph.get_edge_sum(),
                 metric == graph_enhancer.Metric.EDGE_SUM)


def stat_compare(label: str, old_value: int, new_value: int, expected_improvement: bool):
    if debug | expected_improvement:
        print(label + ": " + str(old_value) + " -> " + str(new_value))
        if new_value < old_value:
            print(Fore.GREEN + " -> improved by: " + str(old_value - new_value) + " (" +
                  str(int(100 * (1 - new_value / old_value))) + " %)" + Fore.RESET)
        elif new_value > old_value:
            if expected_improvement:
                raise Exception(label + " expected to improve got worse")
            print(Fore.RED + " -> degraded by: " + str(new_value - old_value) + " (" +
                  str(int(100 * ((old_value - new_value) / old_value))) + " %)" + Fore.RESET)
        else:
            print(Fore.YELLOW + " -> no change" + Fore.RESET)
