def quicksort_iterative(arr):
    if len(arr) <= 1:
        return arr
    stack = [(0, len(arr) - 1)]
    while stack:
        start, end = stack.pop()
        if start < end:
            pivot_index = partition(arr, start, end)
            stack.append((start, pivot_index - 1))
            stack.append((pivot_index + 1, end))
    return arr

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
# Example usage:
arr = [3, 6, 8, 10, 1, 2, 1]
print(quicksort_iterative(arr))