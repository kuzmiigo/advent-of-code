import fileinput


def to_bin(seq):
    x = 0
    for c in seq:
        x |= 1 << ord(c) - ord('a')
    return x


def count_ones(x):
    return bin(x).count('1')


def run1(lines):
    total = 0
    group = 0
    for line in lines:
        line = line.strip()
        if line:
            group |= to_bin(line)
        else:
            total += count_ones(group)
            group = 0
    total += count_ones(group)
    print(total)


def run2(lines):
    total = 0
    group = (1 << 26) - 1
    for line in lines:
        line = line.strip()
        if line:
            group &= to_bin(line)
        else:
            total += count_ones(group)
            group = (1 << 26) - 1
    total += count_ones(group)
    print(total)


lines = list(fileinput.input())
run1(lines)
run2(lines)
