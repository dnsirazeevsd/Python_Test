test = [1,2,3,4,5,6,7,8,9]

def twoSum(nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, num in enumerate(nums):
            diff = target - num
            if diff in seen:
                  return [seen[diff], i]
            seen[num] = i

print(twoSum(test, 9))