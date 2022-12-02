import fileinput


def parse_input(lines):
    elves = []

    elf = 0
    for line in lines:
        line = line.strip()
        if line:
            elf += int(line)
        else:
            elves.append(elf)
            elf = 0
    elves.append(elf)

    return elves


def run1(elves):
    print(max(elves))


def run2(elves):
    print(sum(sorted(elves)[-3:]))


lines = list(fileinput.input())
elves = parse_input(lines)

run1(elves)
run2(elves)
