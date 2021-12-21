import fileinput
import re
from collections import Counter
from functools import cache
from itertools import product


class Player:
    def __init__(self, pos):
        self.pos = pos
        self.score = 0

    def move(self, n):
        self.pos = (self.pos + n) % 10
        self.score += self.pos + 1


class DeterministicDice:
    def __init__(self):
        self.count = 0
        self.n = 0

    def roll(self):
        self.count += 1
        self.n += 1
        if self.n > 100:
            self.n = 1
        return self.n


def parse_input(lines):
    return [int(re.findall(r'\d+$', line.strip())[0]) - 1 for line in lines]


def run1(positions):
    dice = DeterministicDice()
    ps = [Player(pos) for pos in positions]
    idx = 0
    while True:
        n = sum([dice.roll() for _ in range(3)])
        ps[idx].move(n)
        s = ps[idx].score
        idx = (idx + 1) % 2
        if s >= 1000:
            break
    print(ps[idx].score * dice.count)


def roll_counts():
    triplets = product(range(1, 4), repeat=3)
    return Counter([sum(t) for t in triplets])


# moves = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
moves = roll_counts()


@cache
def quantum_run(idx, position0, position1, score0, score1):
    wins = [0, 0]
    for m in moves:
        positions = [position0, position1]
        positions[idx] = (positions[idx] + m) % 10
        scores = [score0, score1]
        scores[idx] += positions[idx] + 1
        if scores[idx] >= 21:
            wins[idx] += moves[m]
        else:
            wins2 = quantum_run((idx + 1) % 2, *positions, *scores)
            wins[0] += wins2[0] * moves[m]
            wins[1] += wins2[1] * moves[m]
    return wins


def run2(positions):
    wins = quantum_run(0, *positions, 0, 0)
    print(max(wins))


lines = list(fileinput.input())
positions = parse_input(lines)

run1(positions)
run2(positions)
