import fileinput


def parse(lines):
    input = []
    deck = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('Player '):
            deck = []
            input.append(deck)
        else:
            deck.append(int(line))
    return input


def score(deck):
    return sum([(i+1) * x for i, x in enumerate(deck[::-1])])


def index_max(values):
    return max(range(len(values)), key=values.__getitem__)


def play1(input):
    deck1, deck2 = input
    while len(deck1) > 0 and len(deck2) > 0:
        card1, card2 = deck1.pop(0), deck2.pop(0)
        if card1 > card2:
            deck1 += [card1, card2]
        else:
            deck2 += [card2, card1]
    return deck1 if len(deck1) > 0 else deck2


def play2(decks):
    seen = set()
    winner = -1

    while all([len(d) > 0 for d in decks]):
        # Check if we have seen the same configuration (decks)
        cfg = tuple([tuple(d) for d in decks])
        if cfg in seen:
            winner = 0
            break
        else:
            seen.add(cfg)

        # Find round winner
        cards = [d.pop(0) for d in decks]
        zip_dc = list(zip(decks, cards))
        if all([len(d) >= c for d, c in zip_dc]):
            round_winner, _ = play2([d[:c] for d, c in zip_dc])
        else:
            round_winner = index_max(cards)

        # Append cards (works for two players only)
        decks[round_winner].append(cards[round_winner])
        decks[round_winner].append(cards[(round_winner + 1) % 2])

    if winner == -1:
        winner = index_max([len(d) for d in decks])
    return winner, decks[winner]


def play2_old(deck1, deck2, level):
    seen = set()
    winner = 0
    while len(deck1) > 0 and len(deck2) > 0:
        cfg = (tuple(deck1), tuple(deck2))
        if cfg in seen:
            winner = 1
            break
        else:
            seen.add(cfg)
        card1, card2 = deck1.pop(0), deck2.pop(0)
        if len(deck1) >= card1 and len(deck2) >= card2:
            round_winner = play2_old(deck1[:card1], deck2[:card2], level + 1)
        else:
            round_winner = 1 if card1 > card2 else 2
        if round_winner == 1:
            deck1 += [card1, card2]
        else:
            deck2 += [card2, card1]
    if winner == 0:
        winner = 1 if len(deck1) > len(deck2) else 2
    if level == 0:
        if winner == 1:
            print(sum([(i+1) * x for i, x in enumerate(deck1[::-1])]))
        else:
            print(sum([(i+1) * x for i, x in enumerate(deck2[::-1])]))
    return winner


lines = list(fileinput.input())

input = parse(lines)
winning_deck = play1(input)
print(score(winning_deck))

input = parse(lines)
_, winning_deck = play2(input)
print(score(winning_deck))

# input = parse(lines)
# play2_old(input[0], input[1], 0)
