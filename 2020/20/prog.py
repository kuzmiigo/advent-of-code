import fileinput
import math


DRAGON = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   '
]

NUM_TRANSFORMS = 8


def to_bin(seq):
    res = 0
    for x in seq:
        res <<= 1
        res |= (1 if x == '#' else 0)
    return res


def get_borders(tile):
    size = len(tile)
    rng = range(size)
    return (
        to_bin([tile[0][i] for i in rng]),
        to_bin([tile[i][0] for i in rng]),
        to_bin([tile[i][size - 1] for i in rng]),
        to_bin([tile[size - 1][i] for i in rng])
    )


def parse(lines):
    tiles = {}
    borders = {}
    cur_tile_no = 0
    cur_tile = []
    for line in lines:
        line = line.strip()
        if not line:
            borders[cur_tile_no] = get_borders(cur_tile)
            continue
        if line.startswith('Tile '):
            cur_tile_no = int(line.removeprefix('Tile ').removesuffix(':'))
            cur_tile = []
            tiles[cur_tile_no] = cur_tile
        else:
            cur_tile.append(line)
    borders[cur_tile_no] = get_borders(cur_tile)
    size = len(cur_tile)
    tiles_per_size = round(math.sqrt(len(tiles)))
    return tiles, borders, size, tiles_per_size


def reverse(x, size):
    bx = bin(x)[2:]
    y = int(bx[::-1], 2)
    return y << (size - len(bx))


def rotate_borders(borders, size):
    return (
        reverse(borders[1], size),
        borders[3],
        borders[0],
        reverse(borders[2], size)
    )


def flip_border(borders, size):
    return (
        reverse(borders[0], size),
        borders[2],
        borders[1],
        reverse(borders[3], size)
    )


def tile_variants(borders, size):
    b = borders
    seen = set([b])
    flips = 0
    rotations = 0
    res = [(b, (flips, rotations))]
    for i in range(NUM_TRANSFORMS - 1):
        rotations += 1
        b = rotate_borders(b, size)
        if i == 3:
            flips += 1
            rotations = 0
            b = flip_border(b, size)
        if b not in seen:
            seen.add(b)
            res.append((b, (flips, rotations)))
    return res


def find(found, remaining_borders, to_find, tiles_per_size):
    if to_find == 0:
        return found
    i, j = len(found) // tiles_per_size, len(found) % tiles_per_size
    rb = remaining_borders.copy()
    if i > 0:
        rb = [
            (b, tile, ops) for b, tile, ops in rb
            if b[0] == found[-tiles_per_size][0][3]
        ]
    if j > 0:
        rb = [
            (b, tile, ops) for b, tile, ops in rb
            if b[1] == found[-1][0][2]
        ]
    for border, tile, ops in rb:
        found.append((border, tile, ops))
        rb1 = [(b, t, o) for b, t, o in remaining_borders if t != tile]
        res = find(found, rb1, to_find - 1, tiles_per_size)
        if res:
            return res
        found.pop()
    return None


def tile_text_to_bin_str(tile):
    # Remove borders
    return [s[1:-1].replace('#', '1').replace('.', '0') for s in tile[1:-1]]


def tile_to_num(tile):
    return int(''.join(tile), 2)


def count_ones_or_hashes(tile):
    s = ''.join(tile)
    return s.count('1') + s.count('#')


def flip(tile):
    return [x[::-1] for x in tile]


def rotate(tile):
    size = len(tile)
    return [
        ''.join([tile[row][col] for row in range(size - 1, -1, -1)])
        for col in range(size)
    ]


def transform(tile, ops):
    flips, rotations = ops
    if flips > 0:
        tile = flip(tile)
    for i in range(rotations):
        tile = rotate(tile)
    return tile


def combine_tiles(tiles, solution, tiles_per_size):
    # for border, tile, ops in solution:
    #     print(tile, ops, [bin(b)[2:] for b in border])
    res = []
    for border, tile, ops in solution:
        t = tile_text_to_bin_str(tiles[tile])
        t = transform(t, ops)
        res.append(t)

    size = len(res[0])
    tt = []
    for i in range(0, len(tiles), tiles_per_size):
        for j in range(size):
            tt.append(''.join([t[j] for t in res[i:i + tiles_per_size]]))
            # print(*[t[j] for t in res[i:i + tiles_per_size]])
        # print()
    return tt


def count_dragons(tile, d):
    t = tile_to_num(tile)
    res = 0
    while t:
        if t & d == d:
            res += 1
        t >>= 1
    return res


def find_dragons(tile):
    line_len = len(tile)
    padding = ' ' * (line_len - len(DRAGON[0]))
    dragon_ones = count_ones_or_hashes(DRAGON)
    dragon_bin = padding.join(DRAGON).replace('#', '1').replace(' ', '0')
    dragon_int = int(dragon_bin, 2)

    for i in range(NUM_TRANSFORMS):
        nd = count_dragons(tile, dragon_int)
        if nd > 0:
            return count_ones_or_hashes(tile) - nd * dragon_ones
        tile = rotate(tile)
        if i == 3:
            tile = flip(tile)


def solve(tiles, borders, size, tiles_per_size):
    all_borders = [
        (b, tile, ops)
        for tile, border in borders.items()
        for b, ops in tile_variants(border, size)
    ]
    res = find([], all_borders, len(borders), tiles_per_size)
    prod = 1
    for x in [res[i][1] for i in [0, tiles_per_size - 1, -tiles_per_size, -1]]:
        prod *= x
    print(prod)
    tile = combine_tiles(tiles, res, tiles_per_size)
    print(find_dragons(tile))


lines = list(fileinput.input())
tiles, borders, size, tiles_per_size = parse(lines)
solve(tiles, borders, size, tiles_per_size)
