import fileinput


def get_id(seq):
    id = 0
    for c in seq:
        id <<= 1
        if c in ['B', 'R']:
            id |= 1
    return id


lines = list(fileinput.input())

bm = 0
for line in lines:
    x = get_id(line.strip())
    bm |= (1 << x)

pos = 0
free = -1
while bm:
    w = bm & 7
    if w == 5:
        free = pos + 1
    pos += 1
    bm >>= 1

print(pos - 1)
print(free)
