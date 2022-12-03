import fileinput


def parse_input(lines):
    return [p.strip() for p in lines]


def get_priority(c):
    p = 0
    o = ord(c)
    if o >= 97:  # 'a'
        o -= 32  # 'a' -> 'A'
    else:
        p += 26
    p += o - 65 + 1  # 'A'
    return p


def run1(bags):
    priority = 0
    for bag in bags:
        size = len(bag) // 2
        a, b = bag[:size], bag[size:]
        same = set(a).intersection(set(b)).pop()
        priority += get_priority(same)
    print(priority)


def run2(bags):
    priority = 0
    for i in range(0, len(bags), 3):
        a, b, c = bags[i:i + 3]
        same = set(a).intersection(set(b)).intersection(set(c)).pop()
        priority += get_priority(same)
    print(priority)


lines = list(fileinput.input())
data = parse_input(lines)

run1(data)
run2(data)
