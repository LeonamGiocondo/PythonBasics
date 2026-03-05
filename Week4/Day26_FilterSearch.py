# Day 26 - Filter & Search & UX

import json
from pathlib import Path

FILE = Path("tasks.json")


def normalize_tasks(data):
    if not isinstance(data, list):
        return []

    normalized = []
    for item in data:
        if isinstance(item, str):
            title = item.strip()
            if title:
                normalized.append({"title": title, "done": False})
            continue

        if isinstance(item, dict):
            title = str(item.get("title", "")).strip()
            done = bool(item.get("done", False))
            if title:
                normalized.append({"title": title, "done": done})
            continue

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
    print("5) List pending")
    print("6) List done")
    print("7) Search tasks")
    print("8) Clear completed")
    print("0) Exit")


def list_tasks_view(view, header="Tasks"):
    """
    Prints a list of tasks (a 'view' can be filtered/search results).
    This function does NOT modify the original tasks list.
    """
    if not view:
        print(f"\n{header}:")
        print("No tasks found.")
        print("Total: 0 tasks\n")
        return

    print(f"\n{header}:")
    for i, t in enumerate(view, start=1):
        mark = "x" if t["done"] else " "
        print(f"{i}) [{mark}] {t['title']}")
    print(f"Total: {len(view)} tasks\n")


def list_tasks(tasks):
    # Keep your original behavior, but reuse list_tasks_view
    list_tasks_view(tasks, header="Tasks")


def add_task(tasks):
    title = input("Enter a new task: ").strip()
    if not title:
        print("Empty task. Nothing added.\n")
        return

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


def filter_tasks(tasks, mode="all"):
    """
    Returns a NEW list (filtered view).
    mode:
      - "all": everything
      - "pending": done == False
      - "done": done == True
    """
    if mode == "all":
        return list(tasks)  # copy
    if mode == "pending":
        return [t for t in tasks if not t["done"]]
    if mode == "done":
        return [t for t in tasks if t["done"]]
    return list(tasks)


def search_tasks(tasks, query):
    """
    Returns a NEW list containing tasks where query is in title (case-insensitive).
    """
    q = query.strip().lower()
    if not q:
        return []

    return [t for t in tasks if q in t["title"].lower()]


def clear_completed(tasks):
    """
    Removes all tasks with done=True from the ORIGINAL list (mutates it),
    then saves.
    """
    done_count = sum(1 for t in tasks if t["done"])
    if done_count == 0:
        print("No completed tasks to clear.\n")
        return

    # mutate original list so references stay valid
    tasks[:] = [t for t in tasks if not t["done"]]
    save_tasks(tasks)
    print(f"Cleared {done_count} completed task(s).\n")


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

        elif choice == "5":
            pending = filter_tasks(tasks, "pending")
            list_tasks_view(pending, header="Pending tasks")

        elif choice == "6":
            done = filter_tasks(tasks, "done")
            list_tasks_view(done, header="Done tasks")

        elif choice == "7":
            query = input("Search: ")
            results = search_tasks(tasks, query)
            list_tasks_view(results, header=f"Search results for: {query.strip()}")

        elif choice == "8":
            clear_completed(tasks)

        elif choice == "0":
            save_tasks(tasks)
            print("Exiting...")
            break

        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()

