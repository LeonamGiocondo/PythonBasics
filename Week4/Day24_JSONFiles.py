# Day 24 - JSON Files 

import json
from pathlib import Path

FILE = Path("tasks.json")


def load_tasks():
    if not FILE.exists():
        return []
    try:
        data = json.loads(FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def save_tasks(tasks):
    FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def list_tasks(tasks):
    if not tasks:
        print("\nNone task registered.\n")
        return

    print("\nTasks:")
    for i, t in enumerate(tasks, start=1):
        print(f"{i}. {t}")
    print()


def add_task(tasks):
    title = input("Enter a new task: ").strip()
    if not title:
        print("Empty task. Nothing has been added.\n")
        return
    if title in tasks:
        print("This task already exists.\n")
        return

    tasks.append(title)
    save_tasks(tasks)  # Save when to add w/ sucess 
    print("Task added w/ Success!\n")


def remove_task(tasks):
    if not tasks:
        print("There is no tasks to remove.\n")
        return

    list_tasks(tasks)
    raw = input("Enter a number of tasks to remove: ").strip()

    if not raw.isdigit():
        print("Invalid entry. Enter a number.\n")
        return

    idx = int(raw) - 1
    if idx < 0 or idx >= len(tasks):
        print("Number outside the range.\n")
        return

    removed = tasks.pop(idx)
    save_tasks(tasks)  # Save to remove w/ sucess
    print(f"Task removed w/ Success: {removed}\n")


def main():
    tasks = load_tasks()  # Integrate load_tasks() at beginning 

    while True:
        print("1) To list task")
        print("2) To add task")
        print("3) To remove task")
        print("0) To Leave")
        choice = input("Choice: ").strip()

        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "0":
            save_tasks(tasks)  # save to leave
            print("Leaving...")
            break
        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()

