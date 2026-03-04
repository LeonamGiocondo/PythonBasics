# Day 19 - Slicing 

fruits = ["Banana", "Apple", "Grape", "Orange", "Mango"]
# index:    0        1        2        3        4

print(fruits[0:2])  # ['Banana', 'Apple']
print(fruits[1:4])  # ['Apple', 'Grape', 'Orange']
print(fruits[:3])   # from the beginning up to 3 (does not include 3) -> ['Banana','Apple','Grape']
print(fruits[2:])   # from the 2 until the final -> ['Grape','Orange','Mango']

# ----
# step

nums = [0, 1, 2, 3, 4, 5, 6]

print(nums[::2])   # take  2 at a time [0, 2, 4, 6]
print(nums[1::2])  # take in pairs, starting with number 1  [1, 3, 5]

# ----

# inverter 

fruits = ["Banana", "Apple", "Grape", "Orange", "Mango"]
print(fruits[::-1])  # ['Mango', 'Orange', 'Grape', 'Apple', 'Banana']

# important: fruits[::-1] creates a new inverted list.
# to truly invert the list itself, there is fruits.reverse()

