def binarysearch_iterative(nums: list[int], target: int) -> int:

    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Example usage:
nums = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target = 23
result = binarysearch_iterative(nums, target)
print(f'Target {target} found at index {result}')
if result == -1:
    print('Target not found in the list')