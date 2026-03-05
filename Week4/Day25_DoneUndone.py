# Day 25 - Done & Undone 

import json
from pathlib import Path

FILE = Path("tasks.json")


def normalize_tasks(data):
    """
    Accepts:
      - [] (empty)
      - list of strings (old format)
      - list of dicts: {"title": str, "done": bool} (new format)

    Returns:
      - list of dicts in the new format
    """
    if not isinstance(data, list):
        return []

    normalized = []
    for item in data:
        # Old format: "Buy milk"
        if isinstance(item, str):
            title = item.strip()
            if title:
                normalized.append({"title": title, "done": False})
            continue

        # New format: {"title": "...", "done": ...}
        if isinstance(item, dict):
            title = str(item.get("title", "")).strip()
            done = bool(item.get("done", False))
            if title:
                normalized.append({"title": title, "done": done})
            continue

        # Ignore unknown item types
    return normalized


def load_tasks():
    if not FILE.exists():
        return []
    try:
        raw = FILE.read_text(encoding="utf-8")
        data = json.loads(raw)
        return normalize_tasks(data)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def show_menu():
    print("=== TO-DO ===")
    print("1) List tasks")
    print("2) Add task")
    print("3) Remove task")
    print("4) Toggle done")
    print("0) Exit")


def list_tasks(tasks):
    if not tasks:
        print("\nNo tasks registered.")
        print("Total: 0 tasks\n")
        return

    print("\nTasks:")
    for i, t in enumerate(tasks, start=1):
        mark = "x" if t["done"] else " "
        print(f"{i}) [{mark}] {t['title']}")
    print(f"Total: {len(tasks)} tasks\n")


def add_task(tasks):
    title = input("Enter a new task: ").strip()
    if not title:
        print("Empty task. Nothing added.\n")
        return

    # Avoid duplicates (case-insensitive)
    existing = {t["title"].strip().lower() for t in tasks}
    if title.lower() in existing:
        print("This task already exists.\n")
        return

    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print("Task added successfully.\n")


def read_task_number(prompt, max_value):
    raw = input(prompt).strip()
    if not raw.isdigit():
        return None
    n = int(raw)
    if not (1 <= n <= max_value):
        return None
    return n


def remove_task(tasks):
    if not tasks:
        print("There are no tasks to remove.\n")
        return

    list_tasks(tasks)
    n = read_task_number("Enter the task number to remove: ", len(tasks))
    if n is None:
        print("Invalid number.\n")
        return

    removed = tasks.pop(n - 1)
    save_tasks(tasks)
    print(f"Task removed successfully: {removed['title']}\n")


def toggle_done(tasks):
    if not tasks:
        print("There are no tasks to update.\n")
        return

    list_tasks(tasks)
    n = read_task_number("Enter the task number to toggle done: ", len(tasks))
    if n is None:
        print("Invalid number.\n")
        return

    task = tasks[n - 1]
    task["done"] = not task["done"]
    save_tasks(tasks)
    state = "done" if task["done"] else "not done"
    print(f"Updated: '{task['title']}' is now {state}.\n")


def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choice: ").strip()

        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            toggle_done(tasks)
        elif choice == "0":
            save_tasks(tasks)
            print("Exiting...")
            break
        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()
