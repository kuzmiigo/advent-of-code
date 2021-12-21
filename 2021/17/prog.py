import fileinput


def parse_input(lines):
    xs, ys = lines[0].strip().removeprefix('target area: ').split(', ')
    x_min, x_max = [int(n) for n in xs.split('=')[1].split('..')]
    y_min, y_max = [int(n) for n in ys.split('=')[1].split('..')]
    # [int(i) for i in re.findall(r'-?\d+', f.read().strip())]
    return x_min, x_max, y_min, y_max


def test(vx, vy, x_min, x_max, y_min, y_max):
    x, y = 0, 0
    my = -1
    while x <= x_max and y >= y_min:
        my = max(my, y)
        if x_min <= x and x <= x_max and y_min <= y and y <= y_max:
            return my
        x += vx
        y += vy
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1
    return None


def run(x_min, x_max, y_min, y_max):
    y = -1
    res = set()
    for vx in range(1, x_max + 1):
        for vy in range(y_min, 500):
            t = test(vx, vy, x_min, x_max, y_min, y_max)
            if t is not None:
                y = max(y, t)
                res.add((vx, vy))
    print(y)
    print(len(res))


lines = list(fileinput.input())
x_min, x_max, y_min, y_max = parse_input(lines)

run(x_min, x_max, y_min, y_max)
