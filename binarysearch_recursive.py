def binarysearch_recursive(nums: list[int], target: int) -> int:

    def helper(left: int, right: int) -> int:
        if left > right:
            return -1
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            return helper(mid + 1, right)
        else:
            return helper(left, mid - 1)
    return helper(0, len(nums) - 1)

# Example usage:
nums = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target = 23
result = binarysearch_recursive(nums, target)
print(f'Target {target} found at index {result}')
if result == -1:
    print('Target not found in the list')