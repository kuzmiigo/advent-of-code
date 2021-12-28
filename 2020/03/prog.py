import fileinput

deltas = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]


def count_trees(lines, dx, dy):
    m = len(lines)
    n = len(lines[0].strip())
    x = 0
    y = 0
    trees = 0
    while y < m:
        c = lines[y][x]
        # print(x, y, c)
        if c == '#':
            trees += 1
        x = (x + dx) % n
        y = y + dy
    return trees


def run1(lines):
    print(count_trees(lines, 3, 1))


def run2(lines):
    prod = 1
    for (dx, dy) in deltas:
        prod *= count_trees(lines, dx, dy)
    print(prod)


lines = list(fileinput.input())
run1(lines)
run2(lines)
