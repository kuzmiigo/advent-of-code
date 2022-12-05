import fileinput


def parse_input(lines):
    header = 0
    for line in lines:
        if line.strip():
            header += 1
        else:
            break
    max_crate = int(lines[header - 1].split()[-1])

    crates = [[] for i in range(max_crate)]
    for line in lines[:header]:
        for i in range(max_crate):
            pos = 4 * i + 1
            if pos >= len(line):
                break
            c = line[pos]
            if c.isalpha():
                crates[i].insert(0, c)

    moves = [
        [int(x) for x in s.split() if x.isdigit()]
        for s in lines[header+1:]
    ]

    return crates, moves


def run1(crates, moves):
    # Make a copy
    cs = [row[:] for row in crates]

    for n, src, dst in moves:
        for _ in range(n):
            cs[dst - 1].append(cs[src - 1].pop())

    tops = ''.join([c[-1] for c in cs])
    print(tops)


def run2(crates, moves):
    # Make a copy
    cs = [row[:] for row in crates]

    for n, src, dst in moves:
        cs[dst - 1].extend(cs[src - 1][-n:])
        cs[src - 1] = cs[src - 1][:-n]

    tops = ''.join([c[-1] for c in cs])
    print(tops)


lines = list(fileinput.input())
crates, moves = parse_input(lines)

run1(crates, moves)
run2(crates, moves)
