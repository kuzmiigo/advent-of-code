import fileinput


def parse_input(lines):
    timers = [int(x) for x in lines[0].split(',')]
    counts = {}

    for t in timers:
        c = counts.get(t, 0)
        counts[t] = c + 1

    return counts


def step(counts):
    next_counts = {}
    for t, c in counts.items():
        if t == 0:
            next_counts[6] = next_counts.get(6, 0) + c
            next_counts[8] = c
        else:
            next_counts[t - 1] = next_counts.get(t - 1, 0) + c
    return next_counts


def run(counts, n):
    c = counts
    for i in range(n):
        c = step(c)
    print(sum(c.values()))


lines = list(fileinput.input())
counts = parse_input(lines)

run(counts, 80)
run(counts, 256)
