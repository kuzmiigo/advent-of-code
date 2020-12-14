import fileinput


def get_masks(pattern):
    q = [pattern.replace('0', '*').replace('1', '*')]
    res = []
    while q:
        p = q.pop()
        if p.count('X') == 0:
            mask_and = int(p.replace('*', '1'), 2)
            mask_or = int(p.replace('*', '0'), 2)
            res.append((mask_and, mask_or))
        else:
            q.append(p.replace('X', '0', 1))
            q.append(p.replace('X', '1', 1))
    return res


# Init

lines = list(fileinput.input())


# Part 1

mask0 = 0
mask1 = 1
mem = {}

for line in lines:
    var, num = line.strip().split(' = ')
    if var == 'mask':
        mask0 = int(num.replace('X', '1'), 2)
        mask1 = int(num.replace('X', '0'), 2)
    else:
        addr = int(var.removeprefix('mem[').removesuffix(']'))
        num = int(num)
        num |= mask1
        num &= mask0
        if num == 0:
            del mem[addr]
        else:
            mem[addr] = num

print(sum(mem.values()))


# Part 2

mask1 = 0
mem = {}

for line in lines:
    var, num = line.strip().split(' = ')
    if var == 'mask':
        mask1 = int(num.replace('X', '0'), 2)
        masks = get_masks(num)
    else:
        addr = int(var.removeprefix('mem[').removesuffix(']'))
        num = int(num)
        a = addr | mask1
        for ma, mo in masks:
            a &= ma
            a |= mo
            if num == 0:
                del mem[a]
            else:
                mem[a] = num

print(sum(mem.values()))
