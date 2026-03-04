# Day 19 - Exercices 
# Objective: to take index numbers 1 through 3 (excluding index 3)

fruits = ["Banana", "Apple", "Grape", "Orange", "Mango"]

middle = fruits[1:3]
print(middle)

# ----

# the first 3 and the last 2

fruits = ["Banana", "Apple", "Grape", "Orange", "Mango"]

first3 = fruits[:3]
last2 = fruits[-2:]

print(first3)
print(last2)

# ----

# invert without changing the original

nums = [10, 3, 7, 2]
rev = nums[::-1]

print("Original:", nums)
print("Invertida:", rev)

