import fileinput


lines = list(fileinput.input())
nums = [int(line) for line in lines]

nums.append(0)
nums.append(max(nums) + 3)
nums.sort()

z = zip(nums[:-1], nums[1:])
diffs = [y - x for x, y in z]
d1 = [x for x in diffs if x == 1]
d3 = [x for x in diffs if x == 3]
print(len(d1) * len(d3))

counts = {}
counts.update([(x, 0) for x in nums])
counts[nums[-1]] = 1

for x in nums[:0:-1]:
    for d in range(x - 3, x):
        if d in counts:
            counts[d] += counts[x]

print(counts[0])

# Can move forward as well
#
# counts = {}
# counts.update([(x, 0) for x in nums])
# counts[0] = 1

# for x in nums[:-1]:
#     for d in range(x + 1, x + 4):
#         if d in counts:
#             counts[d] += counts[x]

# print(counts[nums[-1]])
