import fileinput
from collections import Counter


def parse(lines):
    template = lines[0].strip()
    rules = dict([line.strip().split(' -> ') for line in lines[2:]])
    return template, rules


def step1(polymer, rules):
    res = ''
    for a, b in zip(polymer, polymer[1:]):
        res += a
        res += rules.get(a + b, '')
    res += b
    return res


def step2(pairs, rules):
    res = {}
    for p, count in pairs.items():
        a, b = p
        t = a
        if a + b in rules:
            c = rules[a + b]
            res[a + c] = res.get(a + c, 0) + count
            t = c
        res[t + b] = res.get(t + b, 0) + count
    return res


def run1(template, rules):
    polymer = template
    for _ in range(10):
        polymer = step1(polymer, rules)
    c = Counter(polymer).most_common()
    print(c[0][1] - c[-1][1])


def run2(template, rules):
    pairs = {}
    for a, b in zip(template, template[1:]):
        pairs[a + b] = pairs.get(a + b, 0) + 1
    for i in range(40):
        pairs = step2(pairs, rules)
    counts = {}
    for p, count in pairs.items():
        a, b = p
        counts[a] = counts.get(a, 0) + count
        counts[b] = counts.get(b, 0) + count
    vals = sorted(counts.values())
    # Elements are counted twice, as each belongs to two pairs,
    # except for the first and the last (these will have odd counts).
    print((vals[-1] + 1) // 2 - (vals[0] + 1) // 2)


lines = list(fileinput.input())
template, rules = parse(lines)
run1(template, rules)
run2(template, rules)
