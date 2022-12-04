import fileinput


def parse_input(lines):
    data = []
    for line in lines:
        line = line.strip()
        data.append([[int(n) for n in x.split('-')] for x in line.split(',')])
    return data


def run1(pairs):
    overlaps = 0
    for a, b in pairs:
        if (a[0] <= b[0] and a[1] >= b[1]) or (a[0] >= b[0] and a[1] <= b[1]):
            overlaps += 1
    print(overlaps)


def run2(pairs):
    overlaps = 0
    for a, b in pairs:
        if (a[0] <= b[1] and a[1] >= b[0]) or (b[0] <= a[1] and b[1] >= a[0]):
            overlaps += 1
    print(overlaps)


lines = list(fileinput.input())
data = parse_input(lines)

run1(data)
run2(data)
