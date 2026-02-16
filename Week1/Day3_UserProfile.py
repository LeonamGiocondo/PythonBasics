print("TESTE DE EXECUÇÃO")


# Day 3 - User Profile Mini Project

# Getting user input

name = input("What's your name?")
age = int(input("How old are you?"))
height = float(input("What is your height (in meters)?"))


# Condition to check if user is adult

if age >= 18:
   print("You are an adult")

else:
   print("You are not an adult")

# Printing formatted message

print("\n--- USER PROFILE ---")
print(f"My name is {name}, I'm {age} years old.")
print(f"My height is {height} meters.")
