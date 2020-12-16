import fileinput
from collections import defaultdict


def parse(lines):
    rules = {}
    ticket = []
    nearby = []
    mode = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if mode == 0:
            if line == 'your ticket:':
                mode += 1
            else:
                field, rest = line.split(': ')
                ranges = [
                    tuple(map(int, r.split('-')))
                    for r in rest.split(' or ')
                ]
                rules[field] = ranges
        elif mode == 1:
            if line == 'nearby tickets:':
                mode += 1
            else:
                ticket = [int(x) for x in line.split(',')]
        else:
            nearby.append([int(x) for x in line.split(',')])
    return rules, ticket, nearby


def is_valid(ranges, x):
    for a, b in ranges:
        if a <= x and x <= b:
            return True
    return False


def rules_to_map(rules):
    res = defaultdict(set)
    for name, ranges in rules.items():
        for a, b in ranges:
            for x in range(a, b + 1):
                res[x].add(name)
    return res


def detect(rules, tickets):
    rulesmap = rules_to_map(rules)
    candidates = []
    for i, col in enumerate(zip(*tickets)):
        fields = set(rules.keys())
        for x in col:
            fields.intersection_update(rulesmap[x])
        candidates.append((i, fields))
    mapping = len(rules) * ['']
    seen = set()
    for i, col in sorted(candidates, key=lambda x: len(x[1])):
        f = col.difference(seen)
        if len(f) != 1:
            print('cannot detect field for column', i)
            continue
        seen.update(f)
        mapping[i] = list(f)[0]
    return mapping


# Init

lines = list(fileinput.input())
rules, ticket, nearby = parse(lines)
ranges = [item for r in rules.values() for item in r]


# Part 1

vals = [item for r in nearby for item in r]
sum_invalid = sum(filter(lambda x: not is_valid(ranges, x), vals))
print(sum_invalid)


# Part 2

valid = list(filter(lambda t: all([is_valid(ranges, f) for f in t]), nearby))
mapping = detect(rules, valid)
prod = 1
for name, val in zip(mapping, ticket):
    if name.startswith('departure'):
        prod *= val
print(prod)
