# Day 21 - Loop through a list using for and enumerate

fruits = ["Banana", "Apple", "Grape"]

for fruit in fruits:  # Browse items
    print(fruit)

# ----

# Browse items w/ index + item (enumerate)

fruits = ["Banana", "Apple", "Grape"]

for i, fruit in enumerate(fruits):
    print(i, fruit)

# if you want to start from 1

for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)
