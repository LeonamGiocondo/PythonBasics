# Day 19 - Sort and Reverse 

# sort change the list and ordered make a new

fruits = ["Banana", "Apple", "Grape", "Orange", "Mango"]

fruits.sort()          # change it's own list
print(fruits)

fruits2 = ["Banana", "Apple", "Grape", "Orange", "Mango"]
ordered = sorted(fruits2)  # dont change fruits2, make new list
print(fruits2)
print(ordered)

----

# reverse order 

numbers = [5, 2, 9, 1]
numbers.sort(reverse=True)
print(numbers)  # [9, 5, 2, 1]

----

# it reverses the current order, it doesn't "order" it

fruits = ["Banana", "Apple", "Grape"]
fruits.reverse()
print(fruits)  # ['Grape', 'Apple', 'Banana']

