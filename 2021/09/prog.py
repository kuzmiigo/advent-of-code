import fileinput
import math


deltas = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0)
]


def parse_input(lines):
    input = [line.strip() for line in lines]
    grid = [[int(x) for x in line] for line in input]
    return grid


def get_neighbours(grid, x, y):
    w = len(grid[0])
    h = len(grid)
    ns = []
    for dx, dy in deltas:
        if x + dx >= 0 and x + dx < w and y + dy >= 0 and y + dy < h:
            ns.append((x + dx, y + dy))
    return ns


def get_mins(grid):
    w = len(grid[0])
    h = len(grid)
    mins = []
    for x in range(w):
        for y in range(h):
            level = grid[y][x]
            ns = get_neighbours(grid, x, y)
            if all([grid[ny][nx] > level for nx, ny in ns]):
                mins.append((x, y))
    return mins


def get_basin(grid, m):
    size = 0
    q = [m]
    seen = set([m])
    while q:
        x, y = q.pop()
        level = grid[y][x]
        size += 1
        for nx, ny in get_neighbours(grid, x, y):
            if (nx, ny) in seen:
                continue
            nl = grid[ny][nx]
            if nl != 9 and nl >= level:
                q.append((nx, ny))
                seen.add((nx, ny))
    return size


def run1(grid):
    mins = get_mins(grid)
    return sum([grid[y][x] + 1 for x, y in mins])


def run2(grid):
    mins = get_mins(grid)
    basins = sorted([get_basin(grid, m) for m in mins])
    return math.prod(basins[-3:])


lines = list(fileinput.input())
grid = parse_input(lines)

print(run1(grid))

print(run2(grid))
