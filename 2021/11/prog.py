import fileinput


deltas = [
    (-1, -1),
    (-1,  0),
    (-1,  1),
    (0, -1),
    (0,  1),
    (1, -1),
    (1,  0),
    (1,  1)
]


def parse_input(lines):
    input = [line.strip() for line in lines]
    grid = dict([
        ((i, j), int(c))
        for i, s in enumerate(input)
        for j, c in enumerate(s)
    ])
    return grid


def step(grid):
    g = {k: v + 1 for k, v in grid.items()}
    q = [k for k, v in g.items() if v > 9]
    flashed = set()
    while q:
        o = q.pop()
        g[o] = 0
        flashed.add(o)
        i, j = o
        for di, dj in deltas:
            n = (i + di, j + dj)
            if n in g and n not in flashed and n not in q:
                c = g[n] + 1
                g[n] = c
                if c > 9:
                    q.append(n)
                    g[n] = 0
                    flashed.add(n)
    return g, len(flashed)


def run1(grid, n):
    g = grid
    flashed = 0
    for _ in range(n):
        g, f = step(g)
        flashed += f
    return flashed


def run2(grid):
    size = len(grid)
    g = grid
    i = 0
    while True:
        i += 1
        g, f = step(g)
        if f == size:
            return i


lines = list(fileinput.input())
grid = parse_input(lines)

print(run1(grid, 100))
print(run2(grid))
