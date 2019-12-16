import sys
from itertools import chain, cycle, islice, repeat

BASE_PATTERN = [0, 1, 0, -1]


#
# Util
#

def read_file(name):
    with open(name, 'r') as f:
        return list(filter(None, map(str.strip, f.readlines())))


def to_numbers(s):
    return [int(x) for x in s]


def to_string(s):
    return ''.join([str(x) for x in s])


#
# Part 1
#

def pattern(n):
    c = cycle(chain.from_iterable([repeat(x, n) for x in BASE_PATTERN]))
    return islice(c, 1, None)


def process(seq, n):
    seq = to_numbers(seq)
    size = len(seq)
    for _ in range(n):
        res = []
        for pos in range(size):
            d = sum([a * b for a, b in zip(seq, pattern(pos + 1))])
            res.append(abs(d) % 10)
        seq = res
    return seq


#
# Part 2
#

def process_crazy(seq, n):
    skip = int(seq[:7])
    seq = to_numbers(seq)
    seq = seq * 10000
    seq = seq[skip:]
    seq.reverse()
    for _ in range(n):
        res = []
        d = 0
        for x in seq:
            d = (x + d) % 10
            res.append(d)
        seq = res
    seq.reverse()
    return seq


#
# Main
#

lines = read_file(sys.argv[1])

for seq in lines:
    if len(lines) > 1:
        print('Signal:', seq)

    res = process(seq, 100)
    print(1, to_string(res[:8]))

    res = process_crazy(seq, 100)
    print(2, to_string(res[:8]))
