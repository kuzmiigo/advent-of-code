import argparse

verbose = False


###############################################################################
# Util
###############################################################################

def read_file(name):
    with open(name, 'r') as f:
        return list(filter(None, map(str.strip, f.readlines())))


###############################################################################
# Part 1
###############################################################################

def deal_new(deck):
    return deck[::-1]


def cut(deck, n):
    return deck[n:] + deck[:n]


def deal(deck, n):
    size = len(deck)
    res = [0] * size
    for i, x in enumerate(deck):
        res[i*n % size] = x
    return res


def parse1(lines, size):
    deck = list(range(size))
    for line in lines:
        split = line.split()
        if line == 'deal into new stack':
            deck = deal_new(deck)
        elif split[0] == 'cut':
            deck = cut(deck, int(split[1]))
        elif line.startswith('deal with increment'):
            deck = deal(deck, int(split[3]))
        else:
            print('Unknown technique!')
            exit(1)
    return deck


###############################################################################
# Part 2
###############################################################################

def modInverse(a, m):
    m0 = m
    y = 0
    x = 1

    if (m == 1):
        return 0

    while (a > 1):
        # q is quotient
        q = a // m

        t = m

        # m is remainder now, process
        # same as Euclid's algo
        m = a % m
        a = t
        t = y

        # Update x and y
        y = x - q * y
        x = t

    # Make x positive
    if (x < 0):
        x = x + m0

    return x


# All card-shuffling techniques are actually linear functions in the ring of
# integers modulo size of the deck, i.e. f(x) = a*x + b mod s, where x is the
# initial card position, f(x) is the resulting card position, s is the deck
# size, a and b are some constants. All operations are done modulo s.
#
# deal_new(x) = -x - 1
# cut_n(x) = x - n
# deal_n(x) = n * x
#
# Input is a sequence (chain) of shuffling functions. This sequence can be
# combined into a single linear function.

def parse2(lines, modulus):
    """Combine input into a linear function, return its constants."""
    a, b = 1, 0
    for line in lines:
        split = line.split()
        if line == 'deal into new stack':
            a = -a % modulus
            b = (-b - 1) % modulus
        elif split[0] == 'cut':
            b = (b - int(split[1])) % modulus
        elif line.startswith('deal with increment'):
            a = a * int(split[3]) % modulus
            b = b * int(split[3]) % modulus
        else:
            print('Unknown technique!')
            exit(1)
    return a, b


def sgs(a, r, n, modulus):
    """Find the sum of the first n terms in a geometric series."""
    f1 = (1 - pow(r, n, modulus)) % modulus
    f2 = modInverse((1 - r) % modulus, modulus)
    return a * f1 * f2 % modulus


# Let's consider function f(x) = a*x + b and assume that r is the result of n
# chained invocations. Then:
#
# f^n(x) = r
# f^{n-1}(x) = (r - b) / a
# f^{n-1}(x) = r/a - b/a
# f^{n-2}(x) = r/a^2 - b/a - b/a^2
# x = r/a^n - \sum_{i=1}^{n} b/a^i
#
# The sum on the right is the sum of the first n terms in a geometric series
# with start term b/a and common ratio 1/a.
#
# As we deal with a ring of integers modulo n (a finite field, actually) here,
# we'll replace 1/a with a^{-1} (inverse of a). All operations are modulo s
# (size of the deck), which happen to be prime.

def inv_fun(a, b, modulus, n, result):
    """Find z such that f^n(z) = result and f(x) = a*x + b (mod modulus)."""
    inv_a = modInverse(a, modulus)
    p1 = result * pow(inv_a, n, modulus) % modulus
    p2 = sgs(b * inv_a % modulus, inv_a, n, modulus)
    return (p1 - p2) % modulus


###############################################################################
# Main
###############################################################################

#
# Init
#

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='input filename')
parser.add_argument('-v', dest='verbose', action='store_true', help='verbose')
args = parser.parse_args()
verbose = args.verbose

lines = read_file(args.filename)
# print(parse1(lines, 10))  # Test

#
# Part 1
#

deck = parse1(lines, 10007)
for i, x in enumerate(deck):
    if x == 2019:
        print(1, i)
        break

#
# Part 2
#

modulus = 119315717514047
repetitions = 101741582076661

a, b = parse2(lines, modulus)
z = inv_fun(a, b, modulus, repetitions, 2020)
print(2, z)

# Originally, I used sympy to simplify expressions:
#
# from sympy import simplify
#
# def parse3(line, x, modulus):
#     x = f'({x})'
#     split = line.split()
#     if line == 'deal into new stack':
#         eq = f'-{x} - 1'
#     elif split[0] == 'cut':
#         eq = f'{x} - {split[1]}'
#     elif line.startswith('deal with increment'):
#         eq = f'{x} * {int(split[3])}'
#     else:
#         print('Unknown technique!')
#         exit(1)
#     seq = str(simplify(eq).expand(modulus=modulus))
#     return seq
#
# s = 'x'
# for line in lines:
#     s = parse3(line, s, modulus)
# print('sym(1)', s)
