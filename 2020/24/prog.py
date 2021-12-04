import fileinput


deltas = {
    'e': (2, 0),
    'se': (1, -1),
    'sw': (-1, -1),
    'w': (-2, 0),
    'nw': (-1, 1),
    'ne': (1, 1)
}


def parse_line(line):
    res = []
    i = 0
    while i < len(line):
        c = line[i]
        if c in ['n', 's']:
            i += 1
            c += line[i]
        res.append(c)
        i += 1
    return res


def parse(input):
    return [parse_line(line.strip()) for line in input]


def run1(input):
    turned = set()
    for seq in input:
        x, y = 0, 0
        for step in seq:
            dx, dy = deltas[step]
            x += dx
            y += dy
        if (x, y) in turned:
            turned.remove((x, y))
        else:
            turned.add((x, y))
    return turned


def run2(turned, reps):
    for i in range(reps):
        counts = {}
        for x, y in turned:
            for dx, dy in deltas.values():
                t = (x + dx, y + dy)
                counts[t] = counts.get(t, 0) + 1
        nt = [t for t, c in counts.items() if c == 2]
        nt += [t for t, c in counts.items() if c == 1 and t in turned]
        turned = set(nt)
    return turned


lines = list(fileinput.input())
input = parse(lines)

t = run1(input)
print(len(t))

t = run2(t, 100)
print(len(t))
