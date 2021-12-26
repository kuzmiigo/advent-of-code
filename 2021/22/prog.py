import fileinput
import re
from collections import defaultdict


# Cuboids are stored in the hierarchical collection coll:
# - level 0 is the list of cuboids;
# - level 1 is the list of their overlaps;
# - level 2 is the list of the overlaps of the overlaps;
# - etc.
#
# Finding total volume has to consider different combinations of overlaps to
# count each area exactly one. The total volume is computed by:
# - adding volumes of the cuboids on level 0;
# - substracting volumes of their overlaps on level 1;
# - adding volumes of the overlaps of the overlaps;
# - etc. level by level switching between adding and substracting.
#
# Switching on a new cuboid means adding this cuboid to level 0 and computing
# all overlaps with existing cuboids and overlaps on other levels.
#
# Switching off a new cuboid means just computing all overlaps with existing
# cuboids and overlaps on other levels. Switching off means to remove overlaps
# with the existing collection, there is nothing to add on level 0.


def parse_input(lines):
    res = []
    for line in lines:
        operation, rest = line.strip().split()
        x0, x1, y0, y1, z0, z1 = [int(i) for i in re.findall(r'-?\d+', rest)]
        res.append((operation, (x0, x1, y0, y1, z0, z1)))
    return res


def overlap(cuboid1, cuboid2):
    x0, x1, y0, y1, z0, z1 = cuboid1
    i0, i1, j0, j1, k0, k1 = cuboid2
    if (i0 > x1 or j0 > y1 or k0 > z1 or
            x0 > i1 or y0 > j1 or z0 > k1 or
            i1 < x0 or j1 < y0 or k1 < z0 or
            x1 < i0 or y1 < j0 or z1 < k0):
        return None
    a0, a1 = max(x0, i0), min(x1, i1)
    b0, b1 = max(y0, j0), min(y1, j1)
    c0, c1 = max(z0, k0), min(z1, k1)
    return (a0, a1, b0, b1, c0, c1)


def volume(cuboid):
    x0, x1, y0, y1, z0, z1 = cuboid
    return (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)


def total_volume(coll):
    vol = 0
    for level, cuboids in coll.items():
        mul = (-1) ** level
        vol += mul * sum([volume(c) for c in cuboids])
    return vol


def add(coll, cuboid, operation):
    add_coll = {}
    for level, cuboids in coll.items():
        add_cuboids = []
        for c in cuboids:
            o = overlap(c, cuboid)
            if o:
                add_cuboids.append(o)
        add_coll[level + 1] = add_cuboids
    for level, cuboids in add_coll.items():
        coll[level] += cuboids
    if operation == 'on':
        coll[0].append(cuboid)


def cut(cuboid):
    """Cuts cuboid to the init region (each coordinate in [-50, 50])."""
    for i in range(0, len(cuboid), 2):
        if cuboid[i] > 50 or cuboid[i + 1] < -50:
            return None
    return tuple([max(-50, min(50, c)) for c in cuboid])


def run1(steps):
    coll = defaultdict(list)
    for operation, cuboid in steps:
        cuboid = cut(cuboid)
        if cuboid:
            add(coll, cuboid, operation)
    print(total_volume(coll))


def run2(steps):
    coll = defaultdict(list)
    for operation, cuboid in steps:
        add(coll, cuboid, operation)
    print(total_volume(coll))


lines = list(fileinput.input())
steps = parse_input(lines)

run1(steps)
run2(steps)
