from collections import defaultdict
import fileinput

deltas = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1)
}


def add_wire(board, wire, symbol):
    x, y = 0, 0
    min_dist = 0
    for s in wire:
        direction, count = s[0], int(s[1:])
        dx, dy = deltas[direction]
        for _ in range(count):
            x += dx
            y += dy
            c = board[x].get(y)
            if not c:
                board[x][y] = symbol
            elif c not in [symbol, 'X']:
                board[x][y] = 'X'
                dist = abs(x) + abs(y)
                if dist < min_dist or min_dist == 0:
                    min_dist = dist
    return min_dist


def add_wire2(board, wire, symbol):
    x, y = 0, 0
    min_steps = 0
    steps = 0
    for s in wire:
        direction, count = s[0], int(s[1:])
        dx, dy = deltas[direction]
        for _ in range(count):
            steps += 1
            x += dx
            y += dy
            c = board[x].get(y)
            if not c:
                board[x][y] = f'{symbol}:{steps}'
                continue
            symbol2, steps2 = c.split(':')
            if symbol2 not in [symbol, 'X']:
                sum_steps = steps + int(steps2)
                board[x][y] = f'X:{sum_steps}'
                if sum_steps < min_steps or min_steps == 0:
                    min_steps = sum_steps
    return min_steps


s1, s2, *_ = fileinput.input()
w1 = s1.strip().split(',')
w2 = s2.strip().split(',')

board1 = defaultdict(dict)
add_wire(board1, w1, '1')
print('1', add_wire(board1, w2, '2'))

board2 = defaultdict(dict)
add_wire2(board2, w1, '1')
print('2', add_wire2(board2, w2, '2'))
