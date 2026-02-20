# Day 7 - Number Guessing Game

secret_number = 7

guess = 0

while guess != secret_number:

    guess = int(input("Guess the number: "))

    if guess > secret_number:
        print("Too high")

    elif guess < secret_number:
        print("Too low")

    else:
        print("Correct! You guessed it.")