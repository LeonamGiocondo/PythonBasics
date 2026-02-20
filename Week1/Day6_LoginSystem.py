# Day 6 - Mini Login System

correct_password = "Python123"
attempts = 0
max_attempts = 3

while attempts < max_attempts:

    password = input("Enter password: ")

    if password == correct_password:
        print("Access granted")
        break
    else:
        print("Wrong password")
        attempts = attempts + 1

if attempts == max_attempts:
    print("Account locked")