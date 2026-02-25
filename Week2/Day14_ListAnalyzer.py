# Day 14 — List Analyzer

numbers = []

for i in range(5):
    num = int(input("Enter a number: "))
    numbers.append(num)

largest = numbers[0]
smallest = numbers[0]

for num in numbers:
    
    if num > largest:
        largest = num
        
    if num < smallest:
        smallest = num

print("\nNumbers:", numbers)
print("Largest:", largest)
print("Smallest:", smallest)