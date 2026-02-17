# Day 4 - Number Analyzer PRO

even_count = 0
odd_count = 0
total_sum = 0
largest = 0
smallest = 1

number = int(input("What's your number? "))

for i in range(1, number + 1):

    total_sum = total_sum + i

    if i % 2 == 0:
        print(i, "- even")
        even_count = even_count + 1
    else:
        print(i, "- odd")
        odd_count = odd_count + 1

    if i > largest:
        largest = i

    if i < smallest:
        smallest = i


print("\n--- RESULTS ---")
print("Even numbers:", even_count)
print("Odd numbers:", odd_count)
print("Sum:", total_sum)
print("Largest:", largest)
print("Smallest:", smallest)

