import sys


def read_file(name):
    with open(name, 'r') as f:
        return filter(None, map(str.strip, f.readlines()))


def to_chunks(s, size):
    return [s[i:i+size] for i in range(0, len(s), size)]


def num_chars(c, s):
    return len([i for i in s if i == c])


def combine_one(cs, i, layer):
    if layer >= len(cs):
        return '2'
    pixel = cs[layer][i]
    if pixel == '2':
        return combine_one(cs, i, layer + 1)
    return pixel


def combine(cs):
    return ''.join([combine_one(cs, i, 0) for i in range(len(cs[0]))])


def print_image(cs):
    print('\n'.join([c.replace('0', ' ').replace('1', '*') for c in cs]))


# Init
s = list(read_file(sys.argv[1]))[0]
cs = to_chunks(s, 25 * 6)

# Part 1
m = min(cs, key=lambda x: num_chars('0', x))
print(1, num_chars('1', m) * num_chars('2', m))

# Part 2
print(2)
print_image(to_chunks(combine(cs), 25))
