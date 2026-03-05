# Day 23 - CRUD of list

# To create (add)

tasks = []
tasks.append("To study Python")   # add at the end

# ----

# To read (show)

for i, task in enumerate(tasks, start=1):
    print(f"{i}) {task}")

# ----

# To update (edit)

tasks[0] = "To study Python 30 min"

# ----

# To delete (remove)

tasks.remove("To study Python")   # Error if does not exist

# ---- 

# To remove for index (very used)

removed = tasks.pop(0)           # remove and return the item


