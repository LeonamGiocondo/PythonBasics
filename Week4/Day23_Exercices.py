# Day 23 - Exercices 

def show_menu():
    print("\n=== TO-DO ===")
    print("1) To add")
    print("2) To list")
    print("3) To Remove")
    print("0) To leave")

def list_tasks(tasks):
    if not tasks:
        print("No tasks.")
        print("Total: 0 tasks")
        return
    for i, task in enumerate(tasks, start=1):
        print(f"{i}) {task}")

    print(f"Total: {len(tasks)} tasks")

tasks = []

while True:
    show_menu()
    choice = input("Choice: ").strip()

    if choice == "1":
        task = input("Enter the task: ").strip()
        if task:
            if task in tasks:
                print("This task already exists")
            else:
                tasks.append(task)
                print("Added")
        else:
            print("Empty task cannot be entered.")
    elif choice == "2":
        list_tasks(tasks)
    elif choice == "3":
        list_tasks(tasks)
        if not tasks:
            continue
        raw = input("Task number to remove: ").strip()
        if raw.isdigit():
            n = int(raw)
            if 1 <= n <= len(tasks):
                removed = tasks.pop(n - 1)
                print("Removed:", removed)
            else:
                print("Number outside the range")
        else:
            print("Enter a valid number.")
    elif choice == "0":
        print("Leaving.")
        break
    else:
        print("Invalid option.")
