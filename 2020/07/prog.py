import fileinput
import re
from collections import defaultdict


def parse(line):
    result = []
    key, rest = line.split(' bags contain ')
    if not rest.startswith('no '):
        content = re.split(r' bags?[,|\.] ?', rest)[:-1]
        for item in content:
            n, bag = item.split(' ', 1)
            result.append((int(n), bag))
    return key, result


def find(index, key):
    s = set(index[key])
    for k in index[key]:
        s.update(find(index, k))
    return s


def count(index, key):
    return sum([n * (1 + count(index, bag)) for n, bag in index[key]])


index1 = defaultdict(list)
index2 = {}
lines = list(fileinput.input())
for line in lines:
    key, content = parse(line)
    index2[key] = content
    for n, bag in content:
        index1[bag].append(key)

enclosing = find(index1, 'shiny gold')
print(len(enclosing))

print(count(index2, 'shiny gold'))
