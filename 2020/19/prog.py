import fileinput
import re


def parse(lines):
    rules = {}
    messages = []
    mode = 0
    for line in lines:
        line = line.strip()
        if not line:
            mode += 1
            continue
        if mode == 0:
            i, rule = line.split(': ')
            if rule.startswith('"'):
                resolved, val = True, rule[1]
            else:
                resolved, val = False, rule
            rules[i] = (resolved, val)
        else:
            messages.append(line)
    return rules, messages


def resolve_rule(rules, i, modified):
    """Convert the given rule and its dependencies to regular expressions."""
    resolved, rule = rules[i]
    if resolved:
        return rule
    parts = [
        ''.join([resolve_rule(rules, r, modified) for r in p.split()])
        for p in rule.split(' | ')
    ]
    res = parts[0] if len(parts) == 1 else '(' + '|'.join(parts) + ')'
    if modified:
        if i == '8':
            res = res + '+'
        elif i == '11':
            # Emulate infinity with just a few expected repetitions
            p42 = rules['42'][1]
            p31 = rules['31'][1]
            res = '(' + '|'.join([
                f'({p42}{{{i}}}{p31}{{{i}}})'
                for i in range(1, 9)
            ]) + ')'
    rules[i] = (True, res)
    return res


def resolve(rules, modified):
    """Convert rules to a regular expression."""
    r = rules.copy()
    return resolve_rule(r, '0', modified)


lines = list(fileinput.input())
rules, messages = parse(lines)

expr = resolve(rules, False)
# print(expr)
print(len([m for m in messages if re.fullmatch(expr, m)]))

expr = resolve(rules, True)
# print(expr)
print(len([m for m in messages if re.fullmatch(expr, m)]))
