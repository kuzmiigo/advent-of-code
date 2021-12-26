import fileinput


def fuel2(n):
    return n * (n + 1) // 2


lines = list(fileinput.input())

pos = [int(x) for x in lines[0].split(',')]
a, b = min(pos), max(pos)

print(min([sum([abs(x - p) for p in pos]) for x in range(a, b + 1)]))
print(min([sum([fuel2(abs(x - p)) for p in pos]) for x in range(a, b + 1)]))
