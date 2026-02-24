# Day 10 — Function Return

def add_numbers(a, b):
    return a + b

def square(number):
    return number * number

def double(number):
    return number + number


num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

num = int(input("Enter a number: "))

double_num = int(input("Enter a number again: "))


sum_result = add_numbers(num1, num2)
square_result = square(num)
double_result = double(double_num)


print("Result:", sum_result)
print("Square:", square_result)
print("Double:", double_result)