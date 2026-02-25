# Day 15 — User Manager

users = []

while True:
    
    name = input("Enter a username (or type 'exit'): ")
    
    if name == "exit":
        break
        
    users.append(name)
    
print("\nRegistered users:")
for user in users:
    print(user)

print("Total users:", len(users))