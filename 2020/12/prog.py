import fileinput


deltas = {
    'W': (-1, 0),
    'E': (1, 0),
    'N': (0, 1),
    'S': (0, -1)
}

dirs = ['E', 'N', 'W', 'S']


lines = list(fileinput.input())
prog = [(line[:1], int(line[1:])) for line in lines]

x, y = 0, 0
cur_dir = 0
for cmd, arg in prog:
    if cmd in ['L', 'R']:
        arg = arg // 90 * (1 if cmd == 'L' else -1)
        cur_dir = (cur_dir + arg) % 4
    else:
        if cmd == 'F':
            cmd = dirs[cur_dir]
        dx, dy = deltas[cmd]
        x += arg * dx
        y += arg * dy

print(abs(x) + abs(y))


x, y = 0, 0
wx, wy = 10, 1
for cmd, arg in prog:
    if cmd == 'L':
        for i in range(arg // 90):
            wx, wy = -wy, wx
    elif cmd == 'R':
        for i in range(arg // 90):
            wx, wy = wy, -wx
    elif cmd == 'F':
        x += arg * wx
        y += arg * wy
    else:
        dx, dy = deltas[cmd]
        wx += arg * dx
        wy += arg * dy

print(abs(x) + abs(y))
