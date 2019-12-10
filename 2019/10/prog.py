import math
import sys
from collections import defaultdict
from itertools import chain, zip_longest


def read_file(name):
    with open(name, 'r') as f:
        return filter(None, map(str.strip, f.readlines()))


def dist(x, y):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))


def angle(p1, p2):
    ang1 = math.atan2(-p1[1], p1[0])
    ang2 = math.atan2(-p2[1], p2[0])
    return math.degrees((ang1 - ang2) % (2 * math.pi))


def group(asteroids, station):
    slopes = defaultdict(list)
    for a in asteroids:
        if a == station:
            continue
        dx, dy = a[0] - station[0], a[1] - station[1]
        g = math.gcd(dx, dy)
        dx, dy = dx/g, dy/g
        slopes[(dx, dy)].append(a)
    return slopes


def order(groups, station):
    keys = sorted(groups.keys(), key=lambda x: angle((0, -1), x))
    cosmic_order = []
    for k in keys:
        asteroid_line = sorted(groups[k], key=lambda x: dist(station, x))
        cosmic_order.append(asteroid_line)
    return cosmic_order


# Quick and ugly. See more elegant version below.
def orig_kill(cosmic_order, target=200, verbose=False):
    i = 0
    killed = 0
    target_asteroid = None
    while cosmic_order:
        i = i % len(cosmic_order)
        asteroids = cosmic_order[i]
        a = asteroids.pop(0)
        killed += 1
        if verbose:
            print(killed, a)
        if killed == target:
            target_asteroid = a
        if asteroids:
            i += 1
        else:
            cosmic_order.pop(i)
    return target_asteroid


def kill(cosmic_order, target=200, verbose=False):
    destiny = list(filter(None, chain(*zip_longest(*cosmic_order))))
    if verbose:
        print('    Shooting asteroids:')
        print('\n'.join([f'    {i+1} {a}' for i, a in enumerate(destiny)]))
    return destiny[target - 1]


asteroids = []

lines = read_file(sys.argv[1])
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == '#':
            asteroids.append((x, y))

# Part 1

max_seen = 0
station = None

for i in range(len(asteroids)):
    seen = len(group(asteroids, asteroids[i]).keys())
    if seen > max_seen:
        max_seen = seen
        station = asteroids[i]

print(1, max_seen, station)

# Part 2

groups = group(asteroids, station)
cosmic_order = order(groups, station)
target_asteroid = kill(cosmic_order, 200, False)
print(2, target_asteroid[0] * 100 + target_asteroid[1], target_asteroid)
