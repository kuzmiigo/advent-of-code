import fileinput


def run(line, turns):
    nums = [int(x) for x in line.split(',')]
    seen = dict([(x, [i+1]) for i, x in enumerate(nums)])
    turn = len(nums)
    last = nums[-1]
    while turn < turns:
        turn += 1
        prev = seen.get(last, [])
        if len(prev) < 2:
            last = 0
        else:
            last = prev[-1] - prev[-2]
        prev = seen.get(last, [])
        prev.append(turn)
        seen[last] = prev
    print(last)


lines = list(fileinput.input())

for line in lines:
    run(line.strip(), 2020)

for line in lines:
    run(line.strip(), 30000000)
