import fileinput


def parse(line):
    start, end = line.split(' -> ')
    x1, y1 = map(int, start.split(','))
    x2, y2 = map(int, end.split(','))
    return (x1, y1, x2, y2)


def is_horver(line):
    x1, y1, x2, y2 = line
    return x1 == x2 or y1 == y2


def cmp(a, b):
    return (a > b) - (a < b)


def gen(line):
    x1, y1, x2, y2 = line
    dx = cmp(x2, x1)
    dy = cmp(y2, y1)
    n = max(abs(x2 - x1), abs(y2 - y1)) + 1
    return [(x1 + dx * i, y1 + dy * i) for i in range(n)]


def build_space(lines):
    space = {}
    for line in lines:
        for x, y in gen(line):
            count = space.get((x, y), 0)
            space[(x, y)] = count + 1
    return space


def run(vents):
    space = build_space(vents)
    dangerous = len([c for c in space.values() if c > 1])
    print(dangerous)


lines = list(fileinput.input())
vents = [parse(line) for line in lines if line.strip()]

horver = list(filter(is_horver, vents))
run(horver)

run(vents)
