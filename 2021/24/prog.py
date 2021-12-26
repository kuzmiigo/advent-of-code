import fileinput


# MONAD programme has 14 steps, one for each input digit w_i. Each step is the
# same, only two constants differ: a_i and c_i. Overall state is kept in z.
# For each step:
#     if z % 26 + a_i == w_i:
#         z //= 26
#     else:
#         z = 26 * z + w_i + c_i
# Thus, z is a numeric implementation of a stack, where multiplication and
# division by 26 act as push and pop operations.
#
# The check above can only be true if a_i < 0. So, we can extract constants
# a_i and c_i from each programme step and use sign(a_i) to decide whether we
# need push or pop operation.


def parse_input(lines):
    prog = []
    for i in range(0, len(lines), 18):
        a = int(lines[i + 5].split()[-1])
        c = int(lines[i + 15].split()[-1])
        prog.append((a, c))
    return prog


def fix(state, i, j):
    m = min(state[i], state[j])
    if m < 1:
        shift = 1 - m
        state[i] += shift
        state[j] += shift
    m = max(state[i], state[j])
    if m > 9:
        shift = m - 9
        state[i] -= shift
        state[j] -= shift


def run(prog, ideal_digit):
    size = len(prog)
    state = [ideal_digit] * size
    stack = []
    for i, p in enumerate(prog):
        a, c = p
        if a > 0:
            stack.append((i, c))
        else:
            j, d = stack.pop()
            state[i] = state[j] + d + a
            fix(state, i, j)
    print(''.join([str(d) for d in state]))


lines = list(fileinput.input())
prog = parse_input(lines)

run(prog, 9)
run(prog, 1)
