# Day 13 — Favorite Numbers

numbers = []

for i in range(3):
    num = int(input("Enter a number: "))
    numbers.append(num)

print("\nYour numbers are:")
for number in numbers:
    print(number)

print("\nTotal numbers:", len(numbers))
print("Sum:", sum(numbers))