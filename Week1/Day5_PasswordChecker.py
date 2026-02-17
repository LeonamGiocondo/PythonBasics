# Day 5 - Password Check System

password = input("Enter your password: ")

has_number = False
has_uppercase = False

for char in password:

    if char.isdigit():
       has_number = True

    if char.isupper():
       has_uppercase = True


if len(password) >= 8 and has_number and has_uppercase:
    print("Password strength: Strong")

elif len(password) >= 8 and has_number:
    print("Password strength: Medium")

else:
    print("Password strenght: Weak")