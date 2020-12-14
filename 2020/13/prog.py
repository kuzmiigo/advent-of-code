import fileinput
import math


def find(ids, i, x, mod):
    if i < 0:
        return x
    n, a = ids[i]
    if x % n != a:
        return None
    nmod = n * mod
    while True:
        r = find(ids, i - 1, x, nmod)
        if r:
            return r
        x += nmod


# Init

lines = list(fileinput.input())
ts = int(lines[0])
ids = [int(x) for x in lines[1].split(',') if x.isnumeric()]


# Part 1

next, id = min([(i * math.ceil(ts / i), i) for i in ids])
print(id * (next-ts))


# Part 2

ids = [
    (int(x), i)
    for i, x in enumerate(lines[1].strip().split(',')) if x.isnumeric()
]
ids = [(x, (x-a) % x) for x, a in ids]
ids.sort()

r = find(ids, len(ids) - 1, ids[-1][1], 1)
print(r)
