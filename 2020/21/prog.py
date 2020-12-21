import fileinput
from collections import defaultdict


def parse(lines):
    input = []
    for line in lines:
        line = line.strip()
        ingredients_str, allergens_str = line.split(' (contains ')
        ingredients = ingredients_str.split()
        allergens = allergens_str[:-1].split(', ')
        input.append((ingredients, allergens))
    return input


def process(input):
    candidates = {}
    counts = {}
    for ingredients, allergens in input:
        ings = set(ingredients)
        for a in allergens:
            if a in candidates:
                candidates[a].intersection_update(ings)
            else:
                candidates[a] = ings.copy()
        for i in ingredients:
            counts[i] = counts.get(i, 0) + 1
    return candidates, counts


def match(candidates, counts):
    mentions = defaultdict(list)
    mapping = {}
    ready = []
    to_process = {}
    for allergen, ings in candidates.items():
        if len(ings) == 1:
            ready.append((allergen, list(ings)[0]))
        else:
            to_process[allergen] = ings
        for i in ings:
            mentions[i].append(allergen)
    while ready:
        allergen, ingredient = ready.pop()
        mapping[allergen] = ingredient
        del counts[ingredient]
        for a in mentions[ingredient]:
            ings = to_process.get(a, set())
            if ingredient in ings:
                ings.remove(ingredient)
                if len(ings) == 1:
                    ready.append((a, list(ings)[0]))
                    del to_process[a]
    print(sum(counts.values()))
    print(','.join([v for k, v in sorted(mapping.items())]))


lines = list(fileinput.input())
input = parse(lines)
candidates, counts = process(input)
match(candidates, counts)
