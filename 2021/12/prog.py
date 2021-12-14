import fileinput
from collections import defaultdict


def parse_input(lines):
    input = [line.strip() for line in lines]
    g = defaultdict(list)
    for line in input:
        u, v = line.split('-')
        if u != 'end' and v != 'start':
            g[u].append(v)
        if u != 'start' and v != 'end':
            g[v].append(u)
    return g


def find1(g, u, e, vis, path, paths):
    path.append(u)
    if u[0].islower():
        vis.add(u)
    if u == e:
        paths.add('-'.join(path))
    else:
        for v in g[u]:
            if v not in vis:
                find1(g, v, e, vis, path, paths)
    if u[0].islower():
        vis.remove(u)
    path.pop()
    return paths


def find2(g, u, e, vis, small, path, paths):
    path.append(u)
    if u[0].islower():
        vis.add(u)
    if u == e:
        paths.add('-'.join(path))
    else:
        for v in g[u]:
            if v not in vis:
                find2(g, v, e, vis, small, path, paths)
    if u[0].islower():
        vis.remove(u)
    if u[0].islower() and len(small) == 0:
        small.add(u)
        for v in g[u]:
            if v not in vis:
                find2(g, v, e, vis, small, path, paths)
        small.remove(u)
    path.pop()
    return paths


def run1(g):
    vis = set()
    path = []
    paths = set()
    find1(g, 'start', 'end', vis, path, paths)
    return len(paths)


def run2(g):
    vis = set()
    small = set()
    path = []
    paths = set()
    find2(g, 'start', 'end', vis, small, path, paths)
    return len(paths)


lines = list(fileinput.input())
g = parse_input(lines)

print(run1(g))
print(run2(g))
