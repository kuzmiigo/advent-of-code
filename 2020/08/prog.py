import fileinput


def parse(line):
    op, arg = line.split()
    return op, int(arg)


def run(prog):
    acc = 0
    pc = 0
    seen = set()
    while pc < len(prog):
        if pc in seen:
            return False, acc
        seen.add(pc)
        op, arg = prog[pc]
        if op == 'acc':
            acc += arg
            pc += 1
        elif op == 'jmp':
            pc += arg
        else:
            pc += 1
    return True, acc


def find(prog):
    pc = 0
    done = False
    acc = None
    while pc < len(prog):
        op, arg = prog[pc]
        if op == 'jmp':
            prog[pc] = ('nop', arg)
            done, acc = run(prog)
            prog[pc] = ('jmp', arg)
        elif op == 'nop':
            prog[pc] = ('jmp', arg)
            done, acc = run(prog)
            prog[pc] = ('nop', arg)
        if done:
            return acc
        pc += 1
    return None


lines = list(fileinput.input())
prog = [parse(line) for line in lines if line.strip()]

_, res = run(prog)
print(res)

print(find(prog))
