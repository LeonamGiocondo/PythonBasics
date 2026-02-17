# Day 6 - To-Do List System

tasks = []

while True:
    print("\n=== To-Do List ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Remove Task")
    print("5. Exit")
    
    choice = input("Choose an option: ")

    if choice == "1":
        task = input("Enter the task: ")
        tasks.append({"task": task, "completed": False})
        print(f"Task '{task}' added.")
    
    elif choice == "2":
        if not tasks:
            print("No tasks found.")
        for i, t in enumerate(tasks):
            status = "✅" if t["completed"] else "❌"
            print(f"{i + 1}. {t['task']} [{status}]")
    
    elif choice == "3":
        task_num = int(input("Enter task number to complete: ")) - 1
        if 0 <= task_num < len(tasks):
            tasks[task_num]["completed"] = True
            print(f"Task '{tasks[task_num]['task']}' marked as completed.")
        else:
            print("Invalid task number.")
    
    elif choice == "4":
        task_num = int(input("Enter task number to remove: ")) - 1
        if 0 <= task_num < len(tasks):
            removed = tasks.pop(task_num)
            print(f"Task '{removed['task']}' removed.")
        else:
            print("Invalid task number.")
    
    elif choice == "5":
        print("Exiting To-Do List. Goodbye!")
        break
    
    else:
        print("Invalid choice. Try again.")
