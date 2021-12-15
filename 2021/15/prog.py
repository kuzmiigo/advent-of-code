import fileinput
from queue import PriorityQueue


deltas = [
    (-1,  0),
    (0, -1),
    (0,  1),
    (1,  0),
]


def parse_input(lines):
    input = [line.strip() for line in lines]
    h = len(input)
    w = len(input[0])
    grid = dict([
        ((i, j), int(c))
        for i, s in enumerate(input)
        for j, c in enumerate(s)
    ])
    return grid, h, w


def scale(grid, h, w):
    res = {}
    for v, r in grid.items():
        for di in range(5):
            for dj in range(5):
                i, j = v
                i += di * h
                j += dj * w
                rr = r + di + dj
                if rr > 9:
                    rr -= 9
                res[(i, j)] = rr
    return res


def find(g, s, e):
    D = {v: float('inf') for v in g}
    D[s] = 0
    vis = set()
    pq = PriorityQueue()
    pq.put((0, s))
    while not pq.empty():
        (dist, current_vertex) = pq.get()
        if current_vertex == e:
            return dist
        vis.add(current_vertex)
        i, j = current_vertex
        for di, dj in deltas:
            v = (i + di, j + dj)
            if v in g and v not in vis:
                old_cost = D[v]
                new_cost = D[current_vertex] + g[v]
                if new_cost < old_cost:
                    pq.put((new_cost, v))
                    D[v] = new_cost
    return D[e]


def run1(grid, h, w):
    return find(grid, (0, 0), (h - 1, w - 1))


def run2(grid, h, w):
    grid = scale(grid, h, w)
    return find(grid, (0, 0), (5 * h - 1, 5 * w - 1))


lines = list(fileinput.input())
grid, h, w = parse_input(lines)

print(run1(grid, h, w))
print(run2(grid, h, w))
