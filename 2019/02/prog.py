import fileinput


def run(programme, noun=None, verb=None, debug=False):
    state = {}

    for i, x in enumerate(p):
        state[i] = x

    if noun:
        state[1] = noun
    if verb:
        state[2] = verb

    if debug:
        print(f'START\n{state}')

    i = 0

    while True:
        if state[i] == 99:
            break
        elif state[i] == 1:
            state[state[i + 3]] = state[state[i + 1]] + state[state[i + 2]]
        elif state[i] == 2:
            state[state[i + 3]] = state[state[i + 1]] * state[state[i + 2]]
        else:
            return None, 'ERRCODE'
        i += 4

    if debug:
        print(f'STOP\n{state}')

    return state[0], None


p = [int(x) for x in fileinput.input()[0].split(',')]
result, err = run(p, 12, 2)
print(1, result)

for noun in range(100):
    for verb in range(100):
        result, err = run(p, noun, verb)
        if result == 19690720:
            print(2, 100 * noun + verb)
            exit()
