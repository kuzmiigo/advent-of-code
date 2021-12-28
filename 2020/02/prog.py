import fileinput


def parse(line):
    mn, rest = line.split('-')
    mx, rest = rest.split(' ', 1)
    c, s = rest.split(': ')
    mn = int(mn)
    mx = int(mx)
    return mn, mx, c, s


def count_char(c, s):
    return len([x for x in s if x == c])


def is_valid1(mn, mx, c, s):
    count = count_char(c, s)
    return mn <= count and count <= mx


def is_valid2(mn, mx, c, s):
    return len([x for x in [s[mn-1], s[mx-1]] if x == c]) == 1


def run(input, validation_fun):
    valid = 0
    for line in input:
        mn, mx, c, s = parse(line)
        if validation_fun(mn, mx, c, s):
            valid += 1
    print(valid)


input = list(fileinput.input())

run(input, is_valid1)
run(input, is_valid2)
