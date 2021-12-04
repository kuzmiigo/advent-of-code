import fileinput


def pow(x, k, mod):
    y = 1
    for i in range(k):
        y = y * x % mod
    return y


def run(pubs, subject, mod):
    y = 1
    loop = 0
    while True:
        loop += 1
        y = y * subject % mod
        if y in pubs:
            other = pubs[0] if y == pubs[1] else pubs[1]
            return pow(other, loop, mod)


lines = list(fileinput.input())
pubs = [int(line) for line in lines]

print(run(pubs, 7, 20201227))
