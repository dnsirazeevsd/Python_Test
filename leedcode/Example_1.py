test = [1,2,3,4,5,6,7,8,9]

def twoSum(nums: list[int], target: int) -> list[int]:
        result = []
        for index_1 in range(len(nums)):
            for index_2 in range(index_1 + 1 ,len(nums)):
                  if nums[index_1] + nums[index_2] == target:
                        result.append(index_1)
                        result.append(index_2)
                        return result

print(twoSum(test, 9))