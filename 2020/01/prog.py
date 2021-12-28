import fileinput


def exists(nums, s):
    for n in nums:
        m = s - n
        if m in nums:
            return m * n
    return None


def run1(nums):
    res = exists(nums, 2020)
    print(res)


def run2(nums):
    for n in nums:
        x = exists(nums - set([n]), 2020 - n)
        if x:
            print(x * n)
            break


input = list(fileinput.input())
nums = set([int(x) for x in input])

run1(nums)
run2(nums)
