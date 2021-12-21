import fileinput
from collections import defaultdict

bases = [
    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    ((1, 0, 0), (0, 0, 1), (0, -1, 0)),
    ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
    ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    ((0, 1, 0), (1, 0, 0), (0, 0, -1)),
    ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
    ((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
    ((0, 1, 0), (0, 0, -1), (-1, 0, 0)),
    ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
    ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
    ((0, 0, 1), (-1, 0, 0), (0, -1, 0)),
    ((0, 0, 1), (0, -1, 0), (1, 0, 0)),
    ((-1, 0, 0), (0, 1, 0), (0, 0, -1)),
    ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
    ((-1, 0, 0), (0, -1, 0), (0, 0, 1)),
    ((-1, 0, 0), (0, 0, -1), (0, -1, 0)),
    ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
    ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
    ((0, -1, 0), (-1, 0, 0), (0, 0, -1)),
    ((0, -1, 0), (0, 0, -1), (1, 0, 0)),
    ((0, 0, -1), (1, 0, 0), (0, -1, 0)),
    ((0, 0, -1), (0, 1, 0), (1, 0, 0)),
    ((0, 0, -1), (-1, 0, 0), (0, 1, 0)),
    ((0, 0, -1), (0, -1, 0), (-1, 0, 0))
]


def parse(lines):
    report = []
    scanner = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('--- '):
            scanner = []
            report.append(scanner)
        else:
            scanner.append(tuple([int(n) for n in line.split(',')]))
    return report


def dist(a, b):
    return sum([(i - j) ** 2 for i, j in zip(a, b)])


def scanner_dists(scanner):
    dists = defaultdict(set)
    for a in scanner:
        for b in scanner:
            if a == b:
                continue
            dists[a].add(dist(a, b))
    return dists


def all_dists(report):
    return [scanner_dists(scanner) for scanner in report]


def transform_point(p, base, offset):
    return tuple([
        x[0] * b[0] + x[1] * b[1] + x[2] * b[2] + o
        for x, b, o in zip([p] * len(p), base, offset)
    ])


def transform_scanner(scanner, base, offset):
    return [transform_point(s, base, offset) for s in scanner]


def find_overlap(dists1, dists2):
    for p1, d1 in dists1.items():
        for p2, d2 in dists2.items():
            common = len(d1.intersection(d2))
            if common >= 11:
                return (p1, p2)
    return None


def check_dists(d1, d2, base, offset):
    for p, ds in d1.items():
        if ds != d2[transform_point(p, base, offset)]:
            return False
    return True


def sub(a, b):
    return tuple([i - j for i, j in zip(a, b)])


def transform_and_combine(combined, d, p1, p2):
    for b in bases:
        pp2 = transform_point(p2, b, (0, 0, 0))
        offset = sub(p1, pp2)
        ts = transform_scanner(d.keys(), b, offset)
        if len(set(combined.keys()).intersection(set(ts))) < 12:
            continue
        if check_dists(d, scanner_dists(ts), b, offset):
            origin = transform_point((0, 0, 0), b, offset)
            return list(set(list(combined.keys()) + ts)), origin
    return combined.keys()


def max_manhattan(ps):
    m = 0
    for i in range(len(ps)):
        for j in range(i + 1, len(ps)):
            a, b = ps[i], ps[j]
            m = max(m, abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]))
    return m


def run(report):
    dists = all_dists(report)
    origins = {0: (0, 0, 0)}
    combined = dists[0].copy()
    curr_dists = list(enumerate(dists))[1:]
    next_dists = []
    while curr_dists:
        for idx, d in curr_dists:
            res = find_overlap(combined, d)
            if res:
                p1, p2 = res
                sc, origin = transform_and_combine(combined, d, p1, p2)
                origins[idx] = origin
                combined = scanner_dists(sc)
            else:
                next_dists.append((idx, d))
        curr_dists = next_dists
        next_dists = []
    print(len(combined))
    print(max_manhattan(origins))


lines = list(fileinput.input())
report = parse(lines)
run(report)
