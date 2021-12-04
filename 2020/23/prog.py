import fileinput


class Node():
    def __init__(self, num):
        self.label = num
        self.next = None


def parse(line):
    return [int(c) for c in line]


def next(cup, size):
    res = cup - 1
    if res == 0:
        res = size
    return res


def to_nodes(cups):
    index = {}
    root = None
    last = None
    for c in cups:
        n = Node(c)
        index[c] = n
        if last:
            last.next = n
        else:
            root = n
        last = n
    last.next = root
    return index, root


def shuffle_nodes(index, cur, size):
    moved_head = cur.next
    cur.next = moved_head.next.next.next
    moved = [
        moved_head.label,
        moved_head.next.label,
        moved_head.next.next.label
    ]
    dest = next(cur.label, size)
    while dest in moved:
        dest = next(dest, size)
    d = index[dest]
    moved_head.next.next.next = d.next
    d.next = moved_head
    return cur.next


def run(index, cur, reps):
    size = len(index)
    for i in range(reps):
        # if i % 1000000 == 0:
        #     print(' ', i)
        cur = shuffle_nodes(index, cur, size)
    cur = index[1]
    # print(cur.label, cur.next.label, cur.next.next.label)
    prod = cur.next.label * cur.next.next.label
    res = []
    for i in range(size - 1):
        cur = cur.next
        res.append(cur.label)
    return res, prod


# Init

lines = list(fileinput.input())
input = parse(lines[0].strip())


# Part 1

cups = input
index, root = to_nodes(cups)
res, _ = run(index, root, 100)
print(''.join([str(x) for x in res]))


# Part 2

cups = input + list(range(max(input) + 1, 1000001))
index, root = to_nodes(cups)
_, prod = run(index, root, 10000000)
print(prod)
