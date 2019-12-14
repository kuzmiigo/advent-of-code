import sys


def read_file(name):
    with open(name, 'r') as f:
        return list(filter(None, map(str.strip, f.readlines())))


def calc_dist(rules, dist, element):
    if element in dist:
        return dist[element]
    if element == 'ORE':
        dist['ORE'] = 0
        return 0
    sources = rules[element][1]
    d = 1 + max([calc_dist(rules, dist, e[1]) for e in sources])
    dist[element] = d
    return d


def replace(requirements, element, rules):
    if element == 'ORE':
        return
    rule_qty, rule_sources = rules[element]
    qty = requirements[element]
    factor = (qty-1) // int(rule_qty) + 1
    del requirements[element]
    for source_qty, source_element in rule_sources:
        q = requirements.get(source_element, 0)
        requirements[source_element] = q + factor * int(source_qty)


def parse_rules(lines):
    rules = {}
    for line in lines:
        lhs, rhs = line.split('=>')
        qty, element = rhs.split()
        sources = [s.split() for s in lhs.split(',')]
        rules[element] = (qty, sources)
    return rules


def calc_ore(rules, sorted_elements, fuel_qty):
    requirements = {'FUEL': fuel_qty}
    for e in sorted_elements:
        replace(requirements, e, rules)
    return requirements['ORE']


#
# Init
#

rules = parse_rules(read_file(sys.argv[1]))
dist = {}
calc_dist(rules, dist, 'FUEL')
sorted_elements = [k for k, v in sorted(dist.items(), key=lambda x: -x[1])]

#
# Part 1
#

print(1, calc_ore(rules, sorted_elements, 1))

#
# Part 2
#

cargo = 1000000000000
# Binary search
low = 1
high = cargo
mid = 0
while low < high:
    mid = low + (high-low) // 2
    r = calc_ore(rules, sorted_elements, mid)
    if mid == low:
        break
    if r > cargo:
        high = mid
    elif r < cargo:
        low = mid
    else:
        break
print(2, mid)
