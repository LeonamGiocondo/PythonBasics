# Day 16 — User Search System

users = ["Ana", "Pedro", "Carlos", "Maria"]

search = input("Enter name to search: ")

found = False

for user in users:
    
    if user == search:
        found = True
        break

if found:
    print("User found!")
else:
    print("User not found.")