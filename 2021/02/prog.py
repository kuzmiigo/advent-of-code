import fileinput


def parse_input(lines):
    return [(cmd, int(x)) for s in lines for cmd, x in [s.strip().split()]]


def run1(commands):
    horizontal, depth = 0, 0
    for cmd, x in commands:
        if cmd == 'down':
            depth += x
        elif cmd == 'up':
            depth -= x
        else:
            horizontal += x
    print(horizontal * depth)


def run2(commands):
    horizontal, depth, aim = 0, 0, 0
    for cmd, x in commands:
        if cmd == 'down':
            aim += x
        elif cmd == 'up':
            aim -= x
        else:
            horizontal += x
            depth += aim * x
    print(horizontal * depth)


lines = list(fileinput.input())
commands = parse_input(lines)

run1(commands)
run2(commands)
