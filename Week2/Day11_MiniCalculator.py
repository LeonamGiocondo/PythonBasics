# Day 11 - Mini Calculator

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
operation = input("Choose operation (+, -, *, /): ")

if operation == "+":
    result = add(num1, num2)

elif operation == "-":
    result = subtract(num1, num2)

elif operation == "*":
    result = multiply(num1, num2)

elif operation == "/":
    result = divide(num1, num2)

else:
    print("Invalid operation")
    result = None

if result is not None:
    print("Result:", result)