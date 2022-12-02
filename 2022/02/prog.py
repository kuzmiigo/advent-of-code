import fileinput


values = {
    'A': 1,
    'B': 2,
    'C': 3
}

wins = [['C', 'A'], ['B', 'C'], ['A', 'B']]
defeats = [[b, a] for a, b in wins]
draws = [[a, a] for a, _ in wins]

map1 = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C'
}

map2 = {
    'X': dict(defeats),
    'Y': dict(draws),
    'Z': dict(wins)
}


def parse_input(lines):
    return [p.split() for p in lines]


def get_score(pair):
    a, b = pair
    score = values[b]
    if a == b:
        score += 3
    elif pair in wins:
        score += 6
    return score


def run1(pairs):
    print(sum([get_score([a, map1[b]]) for a, b in pairs]))


def run2(pairs):
    print(sum([get_score([a, map2[b][a]]) for a, b in pairs]))


lines = list(fileinput.input())
data = parse_input(lines)

run1(data)
run2(data)
