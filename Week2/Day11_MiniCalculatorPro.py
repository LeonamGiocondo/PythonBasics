# Day 12 — Mini Calculator PRO

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b


while True:

    num1 = float(input("\nEnter first number: "))
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
        continue


    print("Result:", result)


    choice = input("\nContinue? (y/n): ")

    if choice.lower() == "n":
        print("Goodbye!")
        break