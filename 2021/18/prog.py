import copy
import fileinput


class Node:
    def __init__(self, value=None, left=None, right=None):
        self.parent = None
        self.value = value
        self.left = left
        if left:
            left.parent = self
        self.right = right
        if right:
            right.parent = self

    def __repr__(self):
        if self.is_leaf():
            return "%d" % (self.value)
        return "[%s, %s]" % (self.left, self.right)

    def is_leaf(self):
        return self.value is not None

    def magnitude(self):
        if self.is_leaf():
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


def to_tree(number):
    if isinstance(number, list):
        return Node(left=to_tree(number[0]), right=to_tree(number[1]))
    return Node(value=number)


def parse_number(s):
    res = []
    stack = [[]]
    for c in s:
        if c == '[':
            stack[-1].append([])
            stack.append(stack[-1][-1])
        elif c == ']':
            res = stack.pop()
        elif c == ',':
            pass
        else:  # number
            stack[-1].append(int(c))
    return to_tree(res)


def parse_input(lines):
    return [parse_number(line.strip()) for line in lines]


def find_explode(n, level):
    if n.is_leaf():
        return None
    if level > 4 and n.left.is_leaf() and n.right.is_leaf():
        return n
    child = find_explode(n.left, level + 1)
    if child:
        return child
    return find_explode(n.right, level + 1)


def find_split(n):
    if n.is_leaf():
        return n if n.value > 9 else None
    child = find_split(n.left)
    if child:
        return child
    return find_split(n.right)


def find_prec(e):
    p = e.parent
    while p is not None and p.left == e:
        p = p.parent
        e = e.parent
    if p is None:
        return None
    r = p.left
    while r.right is not None:
        r = r.right
    return r


def find_succ(e):
    p = e.parent
    while p is not None and p.right == e:
        p = p.parent
        e = e.parent
    if p is None:
        return None
    r = p.right
    while r.left is not None:
        r = r.left
    return r


def add_left(e):
    p = find_prec(e)
    if p:
        p.value += e.value


def add_right(e):
    p = find_succ(e)
    if p:
        p.value += e.value


def explode_number(n):
    e = find_explode(n, 1)
    if not e:
        return False
    add_left(e.left)
    add_right(e.right)
    e.value = 0
    e.left = None
    e.right = None
    return True


def split_number(n):
    e = find_split(n)
    if not e:
        return False
    e.left = Node(e.value // 2)
    e.left.parent = e
    e.right = Node(e.value - e.left.value)
    e.right.parent = e
    e.value = None
    return True


def reduce_number(n):
    while True:
        if explode_number(n):
            continue
        if split_number(n):
            continue
        break


def run1(numbers):
    res = numbers[0]
    for n in numbers[1:]:
        res = Node(left=res, right=n)
        reduce_number(res)
    print(res.magnitude())


def run2(numbers):
    m = -1
    for i in numbers:
        for j in numbers:
            if i == j:
                continue
            res = Node(left=copy.deepcopy(i), right=copy.deepcopy(j))
            reduce_number(res)
            m = max(m, res.magnitude())
    print(m)


lines = list(fileinput.input())

numbers = parse_input(lines)
run1(numbers)

numbers = parse_input(lines)
run2(numbers)
