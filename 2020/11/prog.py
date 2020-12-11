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
    h = len(input)
    w = len(input[0])
    grid = dict([
        ((y, x), c)
        for y, s in enumerate(input)
        for x, c in enumerate(s)
        if c != '.'
    ])
    return grid, h, w


def find_neighbour_in_dir(grid, h, w, y, x, dy, dx):
    while True:
        y, x = y + dy, x + dx
        if y < 0 or y >= h or x < 0 or x >= w:
            return None
        if (y, x) in grid:
            return (y, x)


def find_neighbours1(grid):
    neighbours = {}
    for y, x in grid.keys():
        neighbours[(y, x)] = [
            (j, i)
            for j in range(y - 1, y + 2)
            for i in range(x - 1, x + 2)
            if (
                not (x == i and y == j)
                and (j, i) in grid
                and grid[(j, i)] != '.'
            )
        ]
    return neighbours


def find_neighbours2(grid, h, w):
    neighbours = {}
    for y, x in grid.keys():
        n = [
            find_neighbour_in_dir(grid, h, w, y, x, dy, dx)
            for dy, dx in deltas
        ]
        neighbours[(y, x)] = list(filter(None, n))
    return neighbours


def count_occupied(neighbours, grid, y, x):
    return [grid[(j, i)] for j, i in neighbours[(y, x)]].count('#')


def run(neighbours, grid, max_occupied):
    cur_grid = grid.copy()
    changed = True
    while changed:
        changed = False
        new_grid = {}
        for (y, x), c in cur_grid.items():
            occ = count_occupied(neighbours, cur_grid, y, x)
            if c == 'L' and occ == 0:
                c = '#'
                changed = True
            elif c == '#' and occ > max_occupied:
                c = 'L'
                changed = True
            new_grid[(y, x)] = c
        cur_grid = new_grid
    return list(cur_grid.values()).count('#')


lines = list(fileinput.input())
grid, h, w = parse_input(lines)

neighbours = find_neighbours1(grid)
print(run(neighbours, grid, 3))

neighbours = find_neighbours2(grid, h, w)
print(run(neighbours, grid, 4))
