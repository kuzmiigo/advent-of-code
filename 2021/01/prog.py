import fileinput


def increases(numbers):
    return sum([x < y for x, y in zip(numbers, numbers[1:])])


report = [int(x) for x in fileinput.input()]
print(increases(report))

sliding = [sum(z) for z in zip(report, report[1:], report[2:])]
print(increases(sliding))
