import fileinput


def parse_input(lines):
    return [p.strip() for p in lines]


def find_distinct(n, stream):
    for i in range(n, len(stream) + 1):
        if len(set(stream[i-n:i])) == n:
            return i
    return 0


lines = list(fileinput.input())
data = parse_input(lines)

for i, stream in enumerate(data):
    if i > 0:
        print()
    print(find_distinct(4, stream))
    print(find_distinct(14, stream))
