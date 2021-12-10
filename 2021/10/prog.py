import fileinput


pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

points_corr = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

points_ac = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}


def score(line):
    q = []
    for c in line:
        if c in pairs.keys():
            q.append(c)
        elif c in pairs.values():
            p = q.pop()
            if pairs[p] != c:
                return -points_corr[c]
    if not q:
        return 0

    s = 0
    while q:
        c = q.pop()
        s *= 5
        s += points_ac[c]

    return s


lines = list(fileinput.input())
input = [line.strip() for line in lines]
scores = [score(line) for line in input]

print(sum([-s for s in scores if s < 0]))
ac_scores = sorted([s for s in scores if s > 0])
print(ac_scores[len(ac_scores) // 2])
