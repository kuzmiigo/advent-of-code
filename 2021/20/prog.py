import fileinput


deltas = [
    (-1, -1),
    (-1,  0),
    (-1,  1),
    (0, -1),
    (0,  0),
    (0,  1),
    (1, -1),
    (1,  0),
    (1,  1)
]


def parse_input(lines):
    input = [line.strip() for line in lines]
    algo = input[0]
    points = set()
    for i, line in enumerate(input[2:]):
        for j, c in enumerate(line):
            if c == '#':
                points.add((i, j))
    return algo, points


def print_points(points):
    top, bottom, left, right = bounds(points)
    for i in range(top, bottom + 1):
        for j in range(left, right + 1):
            print('#' if (i, j) in points else '.', end='')
        print()
    print()


def bounds(points):
    rows = [i for i, _ in points]
    cols = [j for _, j in points]
    top, bottom, left, right = min(rows), max(rows), min(cols), max(cols)
    return top, bottom, left, right


def step(algo, points, toggle):
    top, bottom, left, right = bounds(points)

    def is_on(r, c):
        if (r, c) in points:
            return True
        if r < top or r > bottom or c < left or c > right:
            return algo[0] == '#' and toggle
        return False

    new_points = set()
    for i in range(top - 1, bottom + 2):
        for j in range(left - 1, right + 2):
            idxs = ''
            for di, dj in deltas:
                idxs += '1' if is_on(i + di, j + dj) else '0'
            idx = int(idxs, 2)
            if algo[idx] == '#':
                new_points.add((i, j))
    return new_points, not toggle


def run(algo, points, n):
    # print_points(points)
    toggle = False
    for _ in range(n):
        points, toggle = step(algo, points, toggle)
    return len(points)


lines = list(fileinput.input())
algo, points = parse_input(lines)

print(run(algo, points, 2))
print(run(algo, points, 50))
