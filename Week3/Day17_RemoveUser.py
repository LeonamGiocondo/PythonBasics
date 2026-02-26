# Day 17 — Remove User System

users = ["Ana", "Pedro", "Carlos", "Maria"]

name = input("Enter user to remove: ")

if name in users:
    users.remove(name)
    print("User removed.")
else:
    print("User not found.")

print("Current users:")
for user in users:
    print(user)