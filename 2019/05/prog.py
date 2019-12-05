import fileinput


def val(state, mode, index):
    if mode == 0:
        return state[state[index]]
    return state[index]


def run(programme, debug=False):
    state = {}

    for i, x in enumerate(programme):
        state[i] = x

    if debug:
        print(f'START\n{state}')

    i = 0

    while True:
        instruction = state[i]
        opcode = instruction % 100
        mode1 = instruction // 100 % 10
        mode2 = instruction // 1000 % 10
        # mode3 = instruction // 10000 % 10

        if opcode == 99:
            break
        elif opcode == 1:
            p1 = val(state, mode1, i + 1)
            p2 = val(state, mode2, i + 2)
            state[state[i + 3]] = p1 + p2
            i += 4
        elif opcode == 2:
            p1 = val(state, mode1, i + 1)
            p2 = val(state, mode2, i + 2)
            state[state[i + 3]] = p1 * p2
            i += 4
        elif opcode == 3:
            x = int(input("Enter a number: "))
            state[state[i + 1]] = x
            i += 2
        elif opcode == 4:
            print(val(state, mode1, i + 1))
            i += 2
        elif opcode == 5:
            p1 = val(state, mode1, i + 1)
            p2 = val(state, mode2, i + 2)
            if p1 != 0:
                i = p2
            else:
                i += 3
        elif opcode == 6:
            p1 = val(state, mode1, i + 1)
            p2 = val(state, mode2, i + 2)
            if p1 == 0:
                i = p2
            else:
                i += 3
        elif opcode == 7:
            p1 = val(state, mode1, i + 1)
            p2 = val(state, mode2, i + 2)
            state[state[i + 3]] = (1 if p1 < p2 else 0)
            i += 4
        elif opcode == 8:
            p1 = val(state, mode1, i + 1)
            p2 = val(state, mode2, i + 2)
            state[state[i + 3]] = (1 if p1 == p2 else 0)
            i += 4
        else:
            return None, 'ERRCODE'
        if debug:
            print(i, state)

    if debug:
        print(f'STOP\n{state}')

    return state[0], None


for line in fileinput.input():
    print(f'Running programme:')
    print(line)
    p = [int(x) for x in line.split(',')]
    run(p)
    print('')
