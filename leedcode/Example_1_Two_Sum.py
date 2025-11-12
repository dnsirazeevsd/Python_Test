test = [1,2,3,4,5,6,7,8,9]

def two_sum(nums : list[int], target : int) -> list[int]:
    seen = {}
    
    for index, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], index]
        seen[num] = index

print(two_sum(test, 9))