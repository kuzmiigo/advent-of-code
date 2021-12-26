import fileinput


digits = {
    'abcefg': '0',
    'cf': '1',
    'acdeg': '2',
    'acdfg': '3',
    'bcdf': '4',
    'abdfg': '5',
    'abdefg': '6',
    'acf': '7',
    'abcdefg': '8',
    'abcdfg': '9'
}


def add_counts(counts, code):
    for c in code:
        counts[c] = counts.get(c, 0) + 1


def find_count(counts, n):
    res = set()
    for k, v in counts.items():
        if v == n:
            res.add(k)
    return res


def solve(input):
    codes = input.split()
    one = set()
    four = set()
    seven = set()
    eight = set()
    counts5 = {}
    counts56 = {}
    for c in codes:
        s = len(c)
        if s == 2:
            one = set(c)
        elif s == 3:
            seven = set(c)
        elif s == 4:
            four = set(c)
        elif s == 5:
            add_counts(counts5, c)
            add_counts(counts56, c)
        elif s == 6:
            add_counts(counts56, c)
        elif s == 7:
            eight = set(c)

    m = {}
    m['a'] = (seven - one).pop()
    m['e'] = find_count(counts56, 3).pop()
    m['g'] = (eight - four - seven - set(m['e'])).pop()
    m['d'] = (find_count(counts5, 3) - set(m['a'] + m['g'])).pop()
    m['b'] = (four - one - set(m['d'])).pop()
    m['c'] = (find_count(counts56, 4) - set(m['b'])).pop()
    m['f'] = (one - set(m['c'])).pop()

    return {v: k for k, v in m.items()}


def to_digit(mapping, code):
    enc = ''.join(sorted([mapping[c] for c in code]))
    return digits[enc]


def decode1(line):
    _, output = line.split(' | ')
    return sum([len(c) != 5 and len(c) != 6 for c in output.split()])


def decode2(line):
    input, output = line.split(' | ')
    mapping = solve(input)
    codes = output.split()
    return int(''.join([to_digit(mapping, c) for c in codes]))


lines = list(fileinput.input())
print(sum([decode1(line.strip()) for line in lines]))
print(sum([decode2(line.strip()) for line in lines]))
