# Day 22 - Search for item in the list

# w/ in (more safe)

fruits = ["Banana", "Apple", "Grape", "Orange", "Mango"]

print("Apple" in fruits)   # True
print("Kiwi" in fruits)    # False

# ----

# w/ .index() (finds the position, but may give an error)

fruits = ["Banana", "Apple", "Grape"]

print(fruits.index("Apple"))  # 1
# fruits.index("Kiwi")        # ValueError (erro)

# ---- 

# w/ .index() (check before)

item = "Kiwi"
if item in fruits:
    pos = fruits.index(item)
    print("Posição:", pos)
else:
    print("Não encontrei:", item)
