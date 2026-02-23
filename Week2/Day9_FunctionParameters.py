# Day 9 — Function Parameters

def greet(name):
    print("Hello,", name)
    print("Welcome!")

def show_age(age):
    print("You are", age, "years old")


name = input("Enter your name: ")
age = input("How old are you? ")

greet(name)
show_age(age)