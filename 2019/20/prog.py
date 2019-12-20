import argparse
import string
from collections import defaultdict
from queue import PriorityQueue

verbose = False
deltas = {
    1: (0, -1),
    2: (0, 1),
    3: (-1, 0),
    4: (1, 0)
}


def read_file(name):
    with open(name, 'r') as f:
        return f.readlines()


def in_bounds(bounds, x, y):
    min_x, min_y, max_x, max_y = bounds
    return min_x <= x and x <= max_x and min_y <= y and y <= max_y


def find_label(space, portals, bounds, x, y):
    label = None
    for dx, dy in deltas.values():
        c1 = space.get((x + dx, y + dy), '!')
        if c1 not in string.ascii_uppercase:
            continue
        c2 = space.get((x + 2*dx, y + 2*dy), '!')
        if c2 not in string.ascii_uppercase:
            continue
        # Check order of letters
        if dx + dy < 0:
            label = c2 + c1
        else:
            label = c1 + c2
        if label not in ['AA', 'ZZ']:
            if in_bounds(bounds, x + dx, y + dy):
                label += '-in'
            else:
                label += '-out'
        break
    return label


def parse_map(lines):
    space = {}
    min_x, min_y, max_x, max_y = -1, -1, -1, -1
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            space[(x, y)] = c
            if c == '#':
                if min_x < 0:
                    min_x = x
                if min_y < 0:
                    min_y = y
                if max_x < x:
                    max_x = x
                if max_y < y:
                    max_y = y
    bounds = (min_x, min_y, max_x, max_y)
    portals = {}
    coords = {}
    for (x, y), c in space.items():
        if c != '.':
            continue
        label = find_label(space, portals, bounds, x, y)
        if label:
            portals[label] = (x, y)
            coords[(x, y)] = label
    return space, portals, coords


def find_paths_for_portals(space, portals, coords):
    paths = {}
    for k in portals.keys():
        paths[k] = find_paths_for_portal(space, portals, coords, k)
    return paths


def find_paths_for_portal(space, portals, coords, portal):
    my_space = space.copy()
    x, y = portals[portal]
    # Find all possible destinations from the position of the given portal.
    # Each destination is a tuple (distance, x, y).
    paths = []
    stack = [(0, x, y)]
    while stack:
        distance, x, y = stack.pop(0)
        my_space[(x, y)] = '*'
        p = coords.get((x, y))
        if p and p != portal:
            paths.append((distance, p))
        for (dx, dy) in deltas.values():
            if my_space[(x + dx, y + dy)] == '.':
                stack.append((distance + 1, x + dx, y + dy))
    return paths


def get_paired(portals, p):
    if p.endswith('-in'):
        paired = p.replace('-in', '-out')
    elif p.endswith('-out'):
        paired = p.replace('-out', '-in')
    else:
        return None
    if paired in portals.keys():
        return paired
    return None


def find_reachable_portals(paths, portal, level):
    result = []
    paired = get_paired(portals, portal)
    if paired:
        result.append((1, paired, level))
    for d, p in paths[portal]:
        result.append((d, p, level))
    return result


def find_reachable_portals_deep(paths, portal, level):
    result = []
    paired = get_paired(portals, portal)
    if paired:
        new_level = level + (1 if portal.endswith('-in') else -1)
        result.append((1, paired, new_level))
    for d, p in paths[portal]:
        if p.endswith('-out') and level == 0:
            continue
        if p == 'AA':
            continue
        if p == 'ZZ' and level != 0:
            continue
        result.append((d, p, level))
    return result


def find_shortest(paths, find_reachable_portals_func):
    visited = defaultdict(set)
    stack = PriorityQueue()
    stack.put((0, 'AA', 0))
    while stack:
        distance, portal, level = stack.get()
        if portal == 'ZZ':
            return distance
        if portal not in visited[level]:
            visited[level].add(portal)
            for d, p, l in find_reachable_portals_func(paths, portal, level):
                stack.put((distance + d, p, l))
    return None


#
# Init
#

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='input filename')
parser.add_argument('-v', dest='verbose', action='store_true', help='verbose')
args = parser.parse_args()
verbose = args.verbose

#
# Main
#

space, portals, coords = parse_map(read_file(args.filename))
paths = find_paths_for_portals(space, portals, coords)
# print(paths)

print(1, find_shortest(paths, find_reachable_portals))
print(2, find_shortest(paths, find_reachable_portals_deep))
