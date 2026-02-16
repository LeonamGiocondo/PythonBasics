# Day 4 — Number Analyzer

number = int(input("Enter a number: "))

even_count = 0

print("\nNumbers from 1 to", number)

for i in range(1, number + 1):

    if i % 2 == 0:
        print(i, "- even")
        even_count = even_count + 1
    else:
        print(i, "- odd")

print("\nTotal even numbers:", even_count)
