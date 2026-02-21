def calculate_sum(array):
    sum = 0
    for num in array:
        sum += num
    return sum
#Time complexity O(n)


def largest_two(array):
    largest = 0
    second = 0
    for num in array:
        if num > largest:
            second = largest
            largest = num
        elif num > second and num != largest:
            second = num
    return second
#Time complexity O(n)


def max_difference(array):
    min_val = array[0]
    max_val = array[0]
    for num in array:
        if num < min_val:
            min_val = num
        if num > max_val:
            max_val = num
    return max_val - min_val
#Time complexity O(n)





array1 = [6,5,2,4]
array2 = [4,7,2,1]
print(calculate_sum(array1))
print(calculate_sum(array2))
print(largest_two(array1))
print(largest_two(array2))
print(max_difference(array1))
print(max_difference(array2))


"""
Chatgpt prompt: 
given this code can you help me understand the time complexity of each function using the Big O notation. 
"""
