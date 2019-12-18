import argparse
import string

verbose = False
deltas = {
    1: (0, -1),
    2: (0, 1),
    3: (-1, 0),
    4: (1, 0)
}


def read_file(name):
    with open(name, 'r') as f:
        return list(filter(None, map(str.strip, f.readlines())))


def print_map(space):
    max_x = max([x for x, y in space.keys()])
    max_y = max([y for x, y in space.keys()])

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(space.get((x, y), ' '), end='')
        print()


def parse_map(lines):
    space = {}
    coords = {}
    robots = 0
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '@':
                if robots > 9:
                    print('Error: cannot have more than 10 robots.')
                    exit(1)
                c = str(robots)
                robots += 1
            space[(x, y)] = c
            if c not in ['.', '#']:
                coords[c] = (x, y)
    start_keys = [str(k) for k in range(robots)]
    return space, coords, start_keys


def can_visit(c):
    return c in string.ascii_lowercase + string.digits + '.'


def can_visit_potentially(c):
    return c in string.ascii_letters + string.digits + '.'


def is_key(c):
    return c in string.ascii_lowercase


def is_door(c):
    return c in string.ascii_uppercase


def is_target(c):
    return c in string.ascii_lowercase + string.digits


def find_paths_for_keys(space, coords):
    paths = {}
    keys = set([k for k in coords.keys() if is_target(k)])
    for k in keys:
        paths[k] = find_paths_for_key(space, coords, k)
    return paths


def find_paths_for_key(space, coords, key):
    my_space = space.copy()
    x, y = coords[key]
    # Find all possible destinations from the position of the given key.
    # Each destination is a tuple (distance, doors_to_pass, x, y).
    stack = [(0, set(), x, y)]
    keys = []
    while stack:
        distance, doors, x, y = stack.pop(0)
        c = my_space[(x, y)]
        my_space[(x, y)] = '*'
        if is_key(c) and c != key:
            keys.append((c, distance, doors))
        if is_door(c):
            doors = doors | set([c])
        for (dx, dy) in deltas.values():
            if can_visit_potentially(my_space[(x + dx, y + dy)]):
                stack.append((distance + 1, doors, x + dx, y + dy))
    return keys


def find_reachable_keys(paths, cur_keys, keys_in_pocket):
    open_doors = set([k.upper() for k in keys_in_pocket])
    result = []
    for vault, key in enumerate(cur_keys):
        for k, distance, doors in paths[key]:
            if k not in keys_in_pocket and doors <= open_doors:
                result.append((vault, k, distance))
    return result


def run(paths, cur_keys, keys_in_pocket='', cache=None):
    # if len(keys_in_pocket) < 3:
    #     print(keys_in_pocket)
    if len(keys_in_pocket) == len([k for k in paths.keys() if is_key(k)]):
        return (0, keys_in_pocket)
    if cache is None:
        cache = {}
    cache_key = (''.join(cur_keys), ''.join(sorted(keys_in_pocket)))
    if cache_key in cache:
        return cache[cache_key]
    results = []
    reachable_keys = find_reachable_keys(paths, cur_keys, keys_in_pocket)
    # print('run', cur_keys, keys_in_pocket, reachable)
    for vault, k, distance in reachable_keys:
        next_keys = cur_keys.copy()
        next_keys[vault] = k
        res = run(paths, next_keys, keys_in_pocket + k, cache)
        if res:
            results.append((res[0] + distance, res[1]))
    if results:
        min_result = min(results, key=lambda x: x[0])
        cache[cache_key] = min_result
        # if len(keys_in_pocket) < 3:
        #     print(keys_in_pocket, min_result)
        return min_result
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

space, coords, start_keys = parse_map(read_file(args.filename))
if verbose:
    print_map(space)
paths = find_paths_for_keys(space, coords)
# print(paths)
distance, keys = run(paths, start_keys)
print(distance, keys)
