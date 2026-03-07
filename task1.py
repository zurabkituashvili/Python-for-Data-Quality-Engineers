# importing random module for generating randomness
import random

numbers = []

# create list of 100 random numbers from 0 to 1000
for i in range(100):
    num = random.randint(0, 1000)
    numbers.append(num)

# with bubble sort, we order the list in ascending order
for i in range(len(numbers)):
    for j in range(0, len(numbers) - i - 1):
        if numbers[j] > numbers[j + 1]:
            numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

# vars for sum and count of even numbers
even_sum = 0
even_count = 0

# vars for sum and count of odd numbers
odd_sum = 0
odd_count = 0

# iterate to calculate sums and counts of even and odd numbers
for num in numbers:
    if num % 2 == 0:
        even_sum += num
        even_count += 1
    else:
        odd_sum += num
        odd_count += 1

# calculate average of even numbers
even_average = even_sum / even_count if even_count != 0 else 0

# calculate average of odd numbers
odd_average = odd_sum / odd_count if odd_count != 0 else 0
