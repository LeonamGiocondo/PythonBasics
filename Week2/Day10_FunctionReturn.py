# Day 10 — Function Return

def add_numbers(a, b):
    return a + b
def square(number):
    return number * number

num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

num = int(input("Enter a number: "))
result = square(num)

result = add_numbers(num1, num2)

print("Result:", result)
print("Square:", result)