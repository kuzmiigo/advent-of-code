import fileinput
from copy import deepcopy


def parse_input(lines):
    draw = [int(x) for x in lines[0].split(',')]
    boards = []

    board = []
    for line in lines[1:]:
        line = line.strip()
        if line:
            board += [int(x) for x in line.split()]
        else:
            if board:
                boards.append(make_board(board))
            board = []
    boards.append(make_board(board))

    return draw, boards


def make_board(b):
    board = {}
    rows = [0] * 5
    cols = [0] * 5
    for i, x in enumerate(b):
        board[x] = (i // 5, i % 5)
    return (board, rows, cols)


def draw_ball(x, boards):
    res = -1
    bb = []
    for b, rows, cols in boards:
        won = False
        if x in b:
            r, c = b[x]
            rows[r] += 1
            cols[c] += 1
            del b[x]
            if rows[r] == 5 or cols[c] == 5:
                s = sum(b.keys())
                won = True
                res = s
        if not won:
            bb.append((b, rows, cols))
    return res, bb


def run(draw, boards, find_first):
    last = -1
    bb = deepcopy(boards)
    for x in draw:
        res, bb = draw_ball(x, bb)
        if res >= 0:
            last = res * x
            if find_first:
                break
            if not bb:
                break
    print(last)


lines = list(fileinput.input())
draw, boards = parse_input(lines)

run(draw, boards, True)
run(draw, boards, False)
