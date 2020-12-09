import fileinput


def is_valid(prefix, x):
    for y in prefix:
        if (x-y) != y and (x-y) in prefix:
            return True
    return False


def find(nums, preamble):
    for n in range(preamble, len(nums)):
        prefix = set(nums[n - preamble: n])
        x = nums[n]
        if not is_valid(prefix, x):
            return x
    return -1


def find_weakness(nums, x):
    seen = {}
    sum = 0
    for i, n in enumerate(nums):
        sum += n
        y = sum - x
        if y in seen:
            j = seen[y]
            if i - j >= 1:
                subset = nums[j: i + 1]
                return min(subset) + max(subset)
        seen[sum] = i
    return -1


lines = list(fileinput.input())
nums = [int(line) for line in lines]

# preamble = 5  # for test1
preamble = 25

invalid = find(nums, preamble)
print(invalid)

print(find_weakness(nums, invalid))
