import sys
from collections import defaultdict


def read_file(name):
    with open(name, 'r') as f:
        return filter(None, map(str.strip, f.readlines()))


lines = list(read_file(sys.argv[1]))


# Part 1


def tr(g, i, node):
    cs = g[node].keys()
    return i + sum(map(lambda x: tr(g, i + 1, x), cs))


g = defaultdict(dict)
for line in lines:
    o1, o2 = line.strip().split(')')
    g[o1][o2] = 0
# print(g)
print(1, tr(g, 0, 'COM'))


# Part 2

# Found find_path on https://www.python-course.eu/graphs_python.php
# It is easier to use networkx library (see below).
class Graph(object):
    def __init__(self):
        self._g = defaultdict(list)

    def add_edge(self, vertex1, vertex2):
        self._g[vertex1].append(vertex2)

    def find_path(self, start_vertex, end_vertex, path=None):
        if start_vertex not in self._g:
            return None
        if path is None:
            path = []
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        for vertex in self._g[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex, end_vertex, path)
                if extended_path:
                    return extended_path
        return None


gr = Graph()
for line in lines:
    o1, o2 = line.strip().split(')')
    gr.add_edge(o1, o2)
    gr.add_edge(o2, o1)
path = gr.find_path('YOU', 'SAN')
if path:
    print(2, len(path) - 3)

# import networkx as nx
# g = nx.Graph()
# g.add_edges_from([l.strip().split(')') for l in lines])
# print(2, len(nx.shortest_path(g, 'YOU', 'SAN')) - 3)
