import fileinput


def apply(op, x, y):
    if op == '+':
        return x + y
    if op == '*':
        return x * y
    return None


# Version with in-place list modification
def evaluate(expr, precedence):
    e = expr.copy()
    for ops in precedence:
        if len(e) < 3:
            continue
        i = 1
        while i < len(e):
            op = e[i]
            if op in ops:
                e[i-1:i+2] = [apply(op, e[i-1], e[i+1])]
            else:
                i += 2
    return e[0]


# Version without in-place list modification
def evaluate2(expr, precedence):
    e = expr.copy()
    for ops in precedence:
        ne = []
        x = e[0]
        i = 1
        while i < len(e):
            while i < len(e) and e[i] in ops:
                x = apply(e[i], x, e[i+1])
                i += 2
            if i < len(e) - 1:
                ne += [x, e[i]]
                x = e[i+1]
            i += 2
        ne.append(x)
        e = ne
    return e[0]


def run(line, precedence):
    stack = [[]]
    for c in line:
        s = stack[-1]
        if c in '+*':
            s.append(c)
        elif c in '0123456789':
            s.append(int(c))
        elif c == '(':
            stack.append([])
        elif c == ')':
            t = stack.pop()
            s = stack[-1]
            s.append(evaluate2(t, precedence))
    return evaluate2(stack[0], precedence)


lines = list(fileinput.input())

precedence = ['+*']
s = 0
for line in lines:
    x = run(line, precedence)
    # print(x)
    s += x
print(s)

precedence = ['+', '*']
s = 0
for line in lines:
    x = run(line, precedence)
    # print(x)
    s += x
print(s)
