import random
from bipartite_graph import BipartiteGraph
from view import transform_graph_parallel, transform_graph_radial
from ogdf_python import ogdf


def create_random_bipartite_graph_with_seed(number_of_parents: int, number_of_children: int, number_of_edges: int,
                                            seed: int, radial_drawing: bool):
    if radial_drawing:
        raise NotImplementedError("Radial Drawing is not implemented yet")
    if number_of_edges > number_of_parents * number_of_children:
        raise AssertionError("Too many edges for this number of nodes")
    random.seed(seed)
    parents = []
    children = []
    edges = set()
    for i in range(0, number_of_parents):
        if number_of_parents <= 26:
            parents.append((chr(65 + i), i))
        else:
            parents.append(('p' + str(i), i))
    for i in range(0, number_of_children):
        if number_of_children <= 26:
            children.append((chr(97 + i), i))
        else:
            children.append(('c' + str(i), i))

    while len(edges) < number_of_edges:
        par = int(random.random() * number_of_parents)
        child = int(random.random() * number_of_children)
        edges.add((parents[par][0], children[child][0]))

    fraction = max(number_of_parents, number_of_children)

    return get_bipartite_graph_from_list(parents, children, edges, radial_drawing, fraction)


def create_random_bipartite_graph(number_of_parents: int, number_of_children: int, number_of_edges: int,
                                  radial_drawing: bool):
    return create_random_bipartite_graph_with_seed(number_of_parents, number_of_children, number_of_edges, 0,
                                                   radial_drawing)


def get_bipartite_graph_modified(graph: BipartiteGraph, new_ga: ogdf.GraphAttributes):
    return BipartiteGraph(graph.get_g(), new_ga, graph.get_number_of_parents(), graph.get_number_of_children(),
                          graph.is_radial_drawing(), graph.get_fraction())


def get_bipartite_graph_from_list(parents: list, children: list, edges: set, radial: bool, fraction: int):
    if radial:
        [g, ga] = transform_graph_radial(parents, children, edges, fraction)
    else:
        [g, ga] = transform_graph_parallel(parents, children, edges)
    number_of_parents = len(parents)
    number_of_children = len(children)
    return BipartiteGraph(g, ga, number_of_parents, number_of_children, radial, fraction)
