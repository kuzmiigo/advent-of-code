import fileinput


def parse_input(lines):
    input = [line.strip() for line in lines]
    grid = set([
        (x, y, 0, 0)
        for y, s in enumerate(input)
        for x, c in enumerate(s)
        if c == '#'
    ])
    return grid


def get_dims(grid):
    return [(min(coords), max(coords)) for coords in zip(*list(grid))]


def count_occupied_3d(grid, x, y, z):
    return len([
        (a, b, c, 0)
        for a in range(x - 1, x + 2)
        for b in range(y - 1, y + 2)
        for c in range(z - 1, z + 2)
        if (a, b, c, 0) in grid and (a, b, c) != (x, y, z)
    ])


def count_occupied_4d(grid, x, y, z, w):
    return len([
        (a, b, c, d)
        for a in range(x - 1, x + 2)
        for b in range(y - 1, y + 2)
        for c in range(z - 1, z + 2)
        for d in range(w - 1, w + 2)
        if (a, b, c, d) in grid and (a, b, c, d) != (x, y, z, w)
    ])


def run_3d(grid, cycles):
    cur_grid = grid.copy()
    for c in range(cycles):
        new_grid = set()
        dims = get_dims(cur_grid)
        for x in range(dims[0][0] - 1, dims[0][1] + 2):
            for y in range(dims[1][0] - 1, dims[1][1] + 2):
                for z in range(dims[2][0] - 1, dims[2][1] + 2):
                    occ = count_occupied_3d(cur_grid, x, y, z)
                    if (x, y, z, 0) in cur_grid:
                        if occ in [2, 3]:
                            new_grid.add((x, y, z, 0))
                    else:
                        if occ == 3:
                            new_grid.add((x, y, z, 0))
        cur_grid = new_grid
    return len(cur_grid)


def run_4d(grid, cycles):
    cur_grid = grid.copy()
    for c in range(cycles):
        new_grid = set()
        dims = get_dims(cur_grid)
        for x in range(dims[0][0] - 1, dims[0][1] + 2):
            for y in range(dims[1][0] - 1, dims[1][1] + 2):
                for z in range(dims[2][0] - 1, dims[2][1] + 2):
                    for w in range(dims[3][0] - 1, dims[3][1] + 2):
                        occ = count_occupied_4d(cur_grid, x, y, z, w)
                        if (x, y, z, w) in cur_grid:
                            if occ in [2, 3]:
                                new_grid.add((x, y, z, w))
                        else:
                            if occ == 3:
                                new_grid.add((x, y, z, w))
        cur_grid = new_grid
    return len(cur_grid)


lines = list(fileinput.input())
grid = parse_input(lines)

print(run_3d(grid, 6))

print(run_4d(grid, 6))
