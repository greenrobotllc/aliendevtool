def jump_search(arr, x):
    n = len(arr)
    step = int(n**0.5)

def binary_search(low, high, x):
        while low <= high and x >= arr[low] and x <= arr[high]:
            mid = (low + high) // 2
            if arr[mid] == x:
                return mid
            elif arr[mid] < x:
                low = mid + 1
            else:
                high = mid - 1
        return -1

def jump_search(arr, x):
    n = len(arr)
    step = int(n**0.5)
    if binary_search(0, n-1, x) != -1:
        print('Element found at index', end=' ')
        index = binary_search(0, n-1, x)
        while index < n and arr[index] <= x:
            print(index, end=' ')
            index += step
    else:
        print('Element not present in array')