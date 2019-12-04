import sys


def is_valid(n):
    if len(n) != 6:
        return False
    has_double = False
    for i in range(5):
        if n[i] > n[i + 1]:
            return False
        if n[i] == n[i + 1]:
            has_double = True
    return has_double


def is_valid2(n):
    if len(n) != 6:
        return False
    has_double = False
    reps = 1
    for i in range(5):
        if n[i] > n[i + 1]:
            return False
        if n[i] == n[i + 1]:
            reps += 1
        else:
            if reps == 2:
                has_double = True
            reps = 1
    if reps == 2:
        has_double = True
    return has_double


start = sys.argv[1] if len(sys.argv) > 2 else 254032
end = sys.argv[2] if len(sys.argv) > 2 else 789860

count = 0
for x in range(start, end + 1):
    if is_valid(str(x)):
        count += 1
print(1, count)

count = 0
for x in range(start, end + 1):
    if is_valid2(str(x)):
        count += 1
print(2, count)
