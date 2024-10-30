def quicksort_recursive(arr):

    # Base case: If the array has 1 or fewer elements, it is already sorted.
    if len(arr) <= 1:
        return arr

    # Select a pivot element from the array. Here we choose the middle element.
    pivot = arr[len(arr) // 2]

    # Divide the array into three lists: elements less than the pivot, equal to the pivot, and greater than the pivot.
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Recursively sort each list and combine them.
    return quicksort_recursive(left) + middle + quicksort_recursive(right)

# Example usage:
arr = [3, 6, 8, 10, 1, 2, 1]
print(quicksort_recursive(arr))