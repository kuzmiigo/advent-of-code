import fileinput


def parse_input(lines):
    input = [line.strip() for line in lines]
    h = len(input)
    w = len(input[0])
    grid = {}
    for i, line in enumerate(input):
        for j, c in enumerate(line):
            if c != '.':
                grid[(i, j)] = c
    return grid, h, w


def print_grid(grid, h, w):
    for i in range(h):
        for j in range(w):
            print(grid.get((i, j), '.'), end='')
        print()
    print()


def step(grid, h, w):
    moved = False
    new_grid = {}
    for coord, c in grid.items():
        if c != '>':
            continue
        i, j = coord
        nj = (j + 1) % w
        if (i, nj) in grid:
            new_grid[(i, j)] = c
        else:
            new_grid[(i, nj)] = c
            moved = True
    for coord, c in grid.items():
        if c != 'v':
            continue
        i, j = coord
        ni = (i + 1) % h
        if grid.get((ni, j), '.') == 'v' or (ni, j) in new_grid:
            new_grid[(i, j)] = c
        else:
            new_grid[(ni, j)] = c
            moved = True
    return moved, new_grid


def run(grid, h, w):
    count = 0
    while True:
        count += 1
        moved, grid = step(grid, h, w)
        if not moved:
            break
    print(count)


lines = list(fileinput.input())
grid, h, w = parse_input(lines)

run(grid, h, w)
