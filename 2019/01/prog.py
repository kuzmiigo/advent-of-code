import fileinput

cache = {}


def fuel_simple(mass):
    return mass // 3 - 2


def fuel(mass):
    if mass in cache:
        return cache[mass]
    f = mass // 3 - 2
    if f <= 0:
        return 0
    ff = f + fuel(f)
    cache[mass] = ff
    return ff


input = list(fileinput.input())
print(1, sum([fuel_simple(int(x)) for x in input]))
print(2, sum([fuel(int(x)) for x in input]))
