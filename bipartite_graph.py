from ogdf_python import ogdf

from view import is_parent_node, get_position, transform_graph_radial, transform_graph_parallel, get_stats


class BipartiteGraph:
    g: ogdf.Graph()
    ga: ogdf.GraphAttributes()
    number_of_parents: int
    number_of_children: int
    win_max: int
    win_sum: int
    edge_max: int
    edge_sum: int
    span_max: int
    span_sum: int
    radial_drawing: bool
    fraction: int

    def __init__(self, g: ogdf.Graph, ga: ogdf.GraphAttributes, number_of_parents: int, number_of_children: int,
                 radial_drawing: bool, fraction: int):
        self.g = g
        self.ga = ga
        self.number_of_parents = number_of_parents
        self.number_of_children = number_of_children
        self.radial_drawing = radial_drawing
        if radial_drawing:
            self.fraction = fraction
        [self.win_max, self.win_sum, self.edge_max, self.edge_sum, self.span_max, self.span_sum] = get_stats(g, ga)

    def get_span(self, n):
        assert is_parent_node(self.ga, n)
        if len(n.adjEntries) == 0:
            return [get_position(self.ga, n), get_position(self.ga, n)]
        else:
            f_p = None
            l_p = None
            for adj in n.adjEntries:
                if f_p is None:
                    f_p = adj.twinNode()
                    l_p = adj.twinNode()
                else:
                    if get_position(self.ga, f_p) > get_position(self.ga, adj.twinNode()):
                        f_p = adj.twinNode()
                    elif get_position(self.ga, l_p) < get_position(self.ga, adj.twinNode()):
                        l_p = adj.twinNode()
            return [get_position(self.ga, f_p), get_position(self.ga, l_p)]

    def get_win_max(self):
        return self.win_max

    def get_win_sum(self):
        return self.win_sum

    def get_edge_max(self):
        return self.edge_max

    def get_edge_sum(self):
        return self.edge_sum

    def get_span_max(self):
        return self.span_max

    def get_span_sum(self):
        return self.span_sum

    def get_ga(self):
        return self.ga

    def get_g(self):
        return self.g

    def get_number_of_children(self):
        return self.number_of_children

    def get_number_of_parents(self):
        return self.number_of_parents

    def is_radial_drawing(self):
        return self.radial_drawing

    def get_fraction(self):
        return self.fraction


