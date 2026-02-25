# Day 12 — Password Checker

correct_password = "python123"

user_password = ""
attempts = 0

while user_password != correct_password:
    user_password = input("Enter the password: ")
    attempts = attempts + 1
    
    if user_password != correct_password:
        print("Wrong password. Try again.")
        
print(f"Access granted. Welcome! Attemps: {attempts}")