import fileinput


def parse(lines):
    dots = set()
    folds = []
    mode = 0
    for line in lines:
        line = line.strip()
        if mode == 0:
            if not line:
                mode += 1
                continue
            x, y = line.split(',')
            dots.add((int(x), int(y)))
        elif mode == 1:
            f = line.split()
            if f[0] != 'fold':
                continue
            dir, n = f[-1].split('=')
            folds.append((dir, int(n)))
    return dots, folds


def print_dots(dots):
    min_x = min([x for x, y in dots])
    max_x = max([x for x, y in dots])
    min_y = min([y for x, y in dots])
    max_y = max([y for x, y in dots])

    for y in range(min_y, max_y - min_y + 1):
        for x in range(min_x, max_x - min_x + 1):
            print('#' if (x, y) in dots else ' ', end='')
        print()


def flip(d, fold):
    x, y = d
    dir, n = fold
    if dir == 'y':
        delta = y - n
        if delta > 0:
            y = n - delta
    else:  # x
        delta = x - n
        if delta > 0:
            x = n - delta
    return (x, y)


def fold(dots, fold):
    return set([flip(d, fold) for d in dots])


def run1(dots, folds):
    print(len(fold(dots, folds[0])))


def run2(dots, folds):
    d = dots
    for f in folds:
        d = fold(d, f)
    print_dots(d)


lines = list(fileinput.input())
dots, folds = parse(lines)
run1(dots, folds)
run2(dots, folds)
