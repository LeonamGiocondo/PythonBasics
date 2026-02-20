# Day 7 - Number Guessing Game

secret_number = 7

guess = 0
attempts = 0 # attempts count

while guess != secret_number:

    guess = int(input("Guess the number: "))
    attempts += 1 # Add 1 for each attempt

    if guess > secret_number:
        print("Too high")

    elif guess < secret_number:
        print("Too low")

    else:
        print("Correct! You guessed it.")
        print(f"You needed {attempts} attempts.")