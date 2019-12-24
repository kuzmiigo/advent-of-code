import argparse

verbose = False

deltas = {
    1: (0, -1),
    2: (0, 1),
    3: (-1, 0),
    4: (1, 0)
}


###############################################################################
# Util
###############################################################################

def read_file(name):
    with open(name, 'r') as f:
        return list(filter(None, map(str.strip, f.readlines())))


###############################################################################
# Part 1
###############################################################################

def parse1(input_data):
    grid = []
    for c in input_data:
        grid.append(1 if c == '#' else 0)
    return grid


def print_grid1(grid):
    for i, bit in enumerate(grid):
        print('#' if bit else '.', end='')
        if i % 5 == 4 and i > 0:
            print()
    print()


def check1(grid, i, bit):
    x = i % 5
    y = i // 5
    crowd = 0
    for dx, dy in deltas.values():
        nx = x + dx
        ny = y + dy
        if 0 <= nx and nx < 5 and 0 <= ny and ny < 5:
            crowd += grid[nx + ny * 5]
    if bit == 1:
        return 1 if crowd == 1 else 0
    return 1 if crowd in [1, 2] else 0


def step1(grid):
    next_grid = []
    for i, bit in enumerate(grid):
        next_grid.append(check1(grid, i, bit))
    return next_grid


def biodiversity(grid):
    return sum([bit * 2**power for power, bit in enumerate(grid)])


def find_duplicate(grid):
    seen = set()
    while True:
        bd = biodiversity(grid)
        if bd in seen:
            return bd, grid
        seen.add(bd)
        grid = step1(grid)


###############################################################################
# Part 2
###############################################################################

def parse2(lines):
    grid = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                grid[(0, x, y)] = 1
    return grid


def print_grid2(grid):
    min_level = min([level for level, _, _ in grid.keys()])
    max_level = max([level for level, _, _ in grid.keys()])
    for level in range(min_level, max_level + 1):
        print('Level', level)
        for y in range(5):
            for x in range(5):
                if x == 2 and y == 3:
                    c = '?'
                elif (level, x, y) in grid:
                    c = '#'
                else:
                    c = '.'
                print(c, end='')
            print()
        print()
    print('Total bugs:', len(grid.values()), '\n')


def find_borders(grid):
    ks = grid.keys()
    borders = {}
    min_level = min([level for level, _, _ in ks])
    max_level = max([level for level, _, _ in ks])
    for level in range(min_level, max_level + 1):
        level_coords = [(x, y) for lvl, x, y in ks if lvl == level]
        borders[(level, (0, -1))] = sum([1 for _, y in level_coords if y == 4])
        borders[(level, (0, +1))] = sum([1 for _, y in level_coords if y == 0])
        borders[(level, (-1, 0))] = sum([1 for x, _ in level_coords if x == 4])
        borders[(level, (+1, 0))] = sum([1 for x, _ in level_coords if x == 0])
    return min_level, max_level, borders


def get_neighbour(grid, borders, level, x, y, delta):
    dx, dy = delta
    nx = x + dx
    ny = y + dy
    if nx == -1:
        return grid.get((level - 1, 1, 2), 0)
    if nx == 5:
        return grid.get((level - 1, 3, 2), 0)
    if ny == -1:
        return grid.get((level - 1, 2, 1), 0)
    if ny == 5:
        return grid.get((level - 1, 2, 3), 0)
    if nx != 2 or ny != 2:
        return grid.get((level, nx, ny), 0)
    return borders.get((level + 1, delta), 0)


def check2(grid, borders, level, x, y):
    bug = grid.get((level, x, y), 0)
    crowd = 0
    for delta in deltas.values():
        crowd += get_neighbour(grid, borders, level, x, y, delta)
    if bug == 1 and crowd == 1:
        return True
    if bug == 0 and crowd in [1, 2]:
        return True
    return False


def step2(grid):
    next_grid = {}
    min_level, max_level, borders = find_borders(grid)
    for level in range(min_level - 1, max_level + 2):
        for x in range(5):
            for y in range(5):
                if x == 2 and y == 2:
                    continue
                if check2(grid, borders, level, x, y):
                    next_grid[(level, x, y)] = 1
    return next_grid


###############################################################################
# Main
###############################################################################

#
# Init
#

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='input filename')
parser.add_argument('steps', help='number of steps')
parser.add_argument('-v', dest='verbose', action='store_true', help='verbose')
args = parser.parse_args()
verbose = args.verbose

lines = read_file(args.filename)

#
# Part 1
#

grid1 = parse1(''.join(lines))
rating, grid1 = find_duplicate(grid1)
if verbose:
    print('Part 1: duplicate\n')
    print_grid1(grid1)
    print('Rating:', rating)

#
# Part 2
#

grid2 = parse2(lines)
for _ in range(int(args.steps)):
    grid2 = step2(grid2)
if verbose:
    print('\nPart 2: state after', args.steps, 'minutes\n')
    print_grid2(grid2)

#
# Final output
#

print(1, rating)
print(2, len(grid2.values()))
