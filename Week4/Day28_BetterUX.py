# Day 27 Submenu by list (All / Pending / Done / Search) with actions (toggle/remove/edit)

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
    print("1) View: All tasks")
    print("2) Add task")
    print("3) View: Pending tasks")
    print("4) View: Done tasks")
    print("5) View: Search")
    print("6) Clear completed")
    print("0) Exit")


def format_task_line(i, task):
    mark = "x" if task["done"] else " "
    return f"{i}) [{mark}] {task['title']}"


def build_view(tasks, predicate=None):
    view = []
    for idx, task in enumerate(tasks):
        if predicate is None or predicate(task):
            view.append((idx, task))
    return view


def list_view(view, header="Tasks"):
    print(f"\n{header}:")
    if not view:
        print("No tasks found.")
        print("Total: 0 tasks\n")
        return

    for i, (_orig_idx, task) in enumerate(view, start=1):
        print(format_task_line(i, task))
    print(f"Total: {len(view)} tasks\n")


def read_view_number(prompt, max_value):
    raw = input(prompt).strip()
    if not raw.isdigit():
        return None
    n = int(raw)
    if not (1 <= n <= max_value):
        return None
    return n


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


def clear_completed(tasks):
    done_count = sum(1 for t in tasks if t["done"])
    if done_count == 0:
        print("No completed tasks to clear.\n")
        return

    tasks[:] = [t for t in tasks if not t["done"]]
    save_tasks(tasks)
    print(f"Cleared {done_count} completed task(s).\n")


def toggle_from_view(tasks, view):
    if not view:
        print("No tasks to toggle.\n")
        return

    n = read_view_number("Task number to toggle: ", len(view))
    if n is None:
        print("Invalid number.\n")
        return

    orig_idx, _task = view[n - 1]
    tasks[orig_idx]["done"] = not tasks[orig_idx]["done"]
    save_tasks(tasks)

    state = "done" if tasks[orig_idx]["done"] else "not done"
    print(f"Updated: '{tasks[orig_idx]['title']}' is now {state}.\n")


def remove_from_view(tasks, view):
    if not view:
        print("No tasks to remove.\n")
        return

    n = read_view_number("Task number to remove: ", len(view))
    if n is None:
        print("Invalid number.\n")
        return

    orig_idx, _task = view[n - 1]
    removed = tasks.pop(orig_idx)
    save_tasks(tasks)
    print(f"Removed: {removed['title']}\n")


def edit_title_from_view(tasks, view):
    if not view:
        print("No tasks to edit.\n")
        return

    n = read_view_number("Task number to edit: ", len(view))
    if n is None:
        print("Invalid number.\n")
        return

    orig_idx, _task = view[n - 1]
    current = tasks[orig_idx]["title"]

    new_title = input(f"New title (current: {current}): ").strip()
    if not new_title:
        print("Empty title. Nothing changed.\n")
        return

    existing = {t["title"].strip().lower() for t in tasks}
    if new_title.lower() in existing and new_title.strip().lower() != current.strip().lower():
        print("A task with this title already exists.\n")
        return

    tasks[orig_idx]["title"] = new_title
    save_tasks(tasks)
    print("Title updated.\n")


def view_loop(tasks, header, predicate=None):
    """
    Shows a view and lets user perform actions on it:
      T = toggle, R = remove, E = edit, B = back
    Rebuilds the view after each action (because indices can change).
    """
    while True:
        view = build_view(tasks, predicate=predicate)
        list_view(view, header=header)

        action = input("Action [T]oggle [R]emove [E]dit [B]ack: ").strip().lower()
        if action in ("b", ""):
            print()
            return
        if action == "t":
            toggle_from_view(tasks, view)
        elif action == "r":
            remove_from_view(tasks, view)
        elif action == "e":
            edit_title_from_view(tasks, view)
        else:
            print("Invalid action.\n")


def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choice: ").strip()

        if choice == "1":
            view_loop(tasks, header="All tasks")

        elif choice == "2":
            add_task(tasks)

        elif choice == "3":
            view_loop(tasks, header="Pending tasks", predicate=lambda t: not t["done"])

        elif choice == "4":
            view_loop(tasks, header="Done tasks", predicate=lambda t: t["done"])

        elif choice == "5":
            query = input("Search query: ").strip().lower()
            if not query:
                print("Empty search.\n")
                continue
            view_loop(
                tasks,
                header=f"Search results for: {query}",
                predicate=lambda t, q=query: q in t["title"].lower(),
            )

        elif choice == "6":
            clear_completed(tasks)

        elif choice == "0":
            save_tasks(tasks)
            print("Exiting...")
            break

        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()
