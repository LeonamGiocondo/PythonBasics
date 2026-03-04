# Day 19 - Exercices Loops w/ List w/ for and enumerate

# Print each fruit on a separate line

fruits = ["Banana","Apple","Grape","Orange","Mango"]

for fruit in fruits:
    print(fruit)

# ----

# print index: fruit using enumerate

fruits = ["Banana", "Apple", "Grape", "Orange", "Mango"]

for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")


# ----


# Using enumerate(start=1), print 1) Banana, 2) Apple ... 

fruits = ["Banana", "Apple", "Grape", "Orange", "Mango"]

for index, fruit in enumerate(fruits, start=1):
    print(f"{index}) {fruit}")

