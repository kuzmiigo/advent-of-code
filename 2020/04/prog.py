import fileinput
from re import fullmatch


fields = {
    'byr': lambda s: is_valid_year(s, 1920, 2002),
    'iyr': lambda s: is_valid_year(s, 2010, 2020),
    'eyr': lambda s: is_valid_year(s, 2020, 2030),
    'hgt': lambda s: is_valid_height(s),
    'hcl': lambda s: fullmatch('#[0-9a-f]{6}', s) is not None,
    'ecl': lambda s: fullmatch('amb|blu|brn|gry|grn|hzl|oth', s) is not None,
    'pid': lambda s: fullmatch(r'\d{9}', s) is not None
}

keys = set(fields.keys())


def is_valid_year(s, mn, mx):
    m = fullmatch(r'\d{4}', s)
    if not m:
        return False
    y = int(m.string)
    return mn <= y and y <= mx


def is_valid_height(s):
    m = fullmatch(r'(\d+)(cm|in)', s)
    if not m:
        return False
    hs, m = m.groups()
    h = int(hs)
    if m == 'cm':
        mn, mx = 150, 193
    else:
        mn, mx = 59, 76
    return mn <= h and h <= mx


def is_valid1(passport):
    return keys.issubset(set(passport.keys()))


def is_valid2(passport):
    for k, f in fields.items():
        val = passport.get(k)
        if not val or not f(val):
            return False
    return True


lines = list(fileinput.input())

valid1 = 0
valid2 = 0
passport = {}
for line in lines:
    if line.strip():
        passport.update([p.split(':') for p in line.split()])
    else:
        if is_valid1(passport):
            valid1 += 1
        if is_valid2(passport):
            valid2 += 1
        passport = {}

if is_valid1(passport):
    valid1 += 1
if is_valid2(passport):
    valid2 += 1
print(valid1)
print(valid2)
