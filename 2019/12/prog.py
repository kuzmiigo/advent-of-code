import copy
import math
import re
import sys
from functools import reduce
from itertools import combinations, count
from operator import mul


class ProgressTicker():
    chars = '.oOo'

    def __init__(self, step=1):
        self._counter = 0
        self._step = step
        self._index = 0

    def tick(self):
        self._counter += 1
        if self._counter % self._step == 0:
            c = ProgressTicker.chars[self._index % len(ProgressTicker.chars)]
            self._index = (self._index + 1) % len(ProgressTicker.chars)
            print(f'\r{c}', end='', flush=True)

    def stop(self):
        self._counter = 0
        print('\r', end='', flush=True)


def read_file(name):
    with open(name, 'r') as f:
        return list(filter(None, map(str.strip, f.readlines())))


def print_moons(moons):
    format_string = 'pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>'
    for m in moons:
        print(format_string.format(*m['p'], *m['v']))


def sign(x):
    return (x > 0) - (x < 0)


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def energy(moon):
    return sum(map(abs, moon['p'])) * sum(map(abs, moon['v']))


def step(moons):
    for a, b in combinations(moons, 2):
        pos1, vel1 = a['p'], a['v']
        pos2, vel2 = b['p'], b['v']
        gravity = [sign(c2 - c1) for c1, c2 in zip(pos1, pos2)]
        a['v'] = [v + g for v, g in zip(vel1, gravity)]
        b['v'] = [v - g for v, g in zip(vel2, gravity)]
    for m in moons:
        m['p'] = [c + v for c, v in zip(m['p'], m['v'])]


def select_param(moons, key, index):
    return [m[key][index] for m in moons]


# Originally, I just ran this simple version separately for each dimension.
# res = 1
# for c in range(3):
#     linmoons = [{'p': [m['p'][c]], 'v': [0]} for m in moons]
#     res = lcm(res, orig_spin(linmoons))
# print(2, res)
def orig_spin(moons):
    cp = copy.deepcopy(moons)
    progress = ProgressTicker(10000)
    for i in count(1):
        progress.tick()
        step(moons)
        if moons == cp:
            progress.stop()
            return i


# But then I wrote a better version to find alignments in one pass.
def spin(moons, dims=3):
    orig_coords = [select_param(moons, 'p', i) for i in range(dims)]
    orig_vels = [0] * len(moons)
    alignments = [0] * dims
    progress = ProgressTicker(10000)
    for i in count(1):
        progress.tick()
        step(moons)
        for d in range(dims):
            if alignments[d] > 0:
                continue
            if select_param(moons, 'p', d) != orig_coords[d]:
                continue
            if select_param(moons, 'v', d) != orig_vels:
                continue
            alignments[d] = i
            # When all alignments found
            if reduce(mul, alignments) > 0:
                progress.stop()
                return reduce(lcm, alignments)


# Moon is represented as a dictionary (string to list of integers, length of
# lists is equal to the number of dimensions):
#   'p' -> position (list of 3 numbers)
#   'v' -> velocity (list of 3 numbers)
# pos=<x=16, y=-11, z=2>, vel=<x=2, y=4, z=8> ->
# {
#   'p': [16, -11, 2],
#   'v': [2, 4, 8]
# }

#
# Init
#

lines = read_file(sys.argv[1])
r = re.compile(r'[\-\d]+')
init_moons = []
for line in lines:
    init_moons.append({'p': list(map(int, r.findall(line))), 'v': [0, 0, 0]})
# print_moons(init_moons)

#
# Part 1
#

moons = copy.deepcopy(init_moons)
for i in range(1000):
    step(moons)
print(1, sum(map(energy, moons)))

#
# Part 2
#

moons = copy.deepcopy(init_moons)
print(2, spin(moons))
