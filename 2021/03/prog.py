import fileinput


def most(xs, idx):
    if len(xs) <= 1:
        return xs
    col = [x[idx] for x in xs]
    sel = '1' if col.count('1') >= (len(xs) + 1) // 2 else '0'
    return most([x for x in xs if x[idx] == sel], idx + 1)


def least(xs, idx):
    if len(xs) <= 1:
        return xs
    col = [x[idx] for x in xs]
    sel = '1' if col.count('1') < (len(xs) + 1) // 2 else '0'
    return least([x for x in xs if x[idx] == sel], idx + 1)


def run1(input):
    yy = ['1' if x.count('1') >= len(input) // 2 else '0' for x in zip(*input)]
    zz = ['1' if x == '0' else '0' for x in yy]
    print(int(''.join(yy), 2) * int(''.join(zz), 2))


def run2(input):
    print(int(''.join(most(input, 0)), 2) * int(''.join(least(input, 0)), 2))


input = [x.strip() for x in fileinput.input()]

run1(input)
run2(input)
