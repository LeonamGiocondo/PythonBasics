# Day 5 - Password Check System

password = input("Enter your password: ")

has_number = False

for char in password:

    if char.isdigit():
       has_number = True


if len(password) >= 8 and has_number:
    print("Password strength: Strong")
else:
    print("Password strenght: Weak")