# Day 30 - To add sorting tasks


import json
from pathlib import Path

# Path to the JSON file where tasks are stored
FILE = Path("tasks.json")

# Allowed priority values
VALID_PRIORITIES = ("low", "medium", "high")

# Priority ranking used for sorting
PRIORITY_RANK = {
    "high": 0,
    "medium": 1,
    "low": 2,
}


def normalize_priority(value):
    # Convert any input to a valid priority string
    value = str(value).strip().lower()
    if value in VALID_PRIORITIES:
        return value
    return "medium"


def normalize_tasks(data):
    # Normalize loaded JSON data into the expected task structure
    if not isinstance(data, list):
        return []

    normalized = []
    for item in data:
        if isinstance(item, str):
            title = item.strip()
            if title:
                normalized.append({
                    "title": title,
                    "done": False,
                    "priority": "medium",
                })
            continue

        if isinstance(item, dict):
            title = str(item.get("title", "")).strip()
            done = bool(item.get("done", False))
            priority = normalize_priority(item.get("priority", "medium"))

            if title:
                normalized.append({
                    "title": title,
                    "done": done,
                    "priority": priority,
                })

    return normalized


def load_tasks():
    # Load tasks from the JSON file
    if not FILE.exists():
        return []

    try:
        raw = FILE.read_text(encoding="utf-8")
        data = json.loads(raw)
        return normalize_tasks(data)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    # Save tasks to the JSON file
    FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def show_menu():
    # Display the main menu
    print("=== TO-DO ===")
    print("1) View: All tasks")
    print("2) Add task")
    print("3) View: Pending tasks")
    print("4) View: Done tasks")
    print("5) View: Search")
    print("6) Clear completed")
    print("7) View: High priority")
    print("0) Exit")


def format_priority(priority):
    # Convert priority to uppercase for display
    return priority.upper()


def format_task_line(i, task):
    # Format one task line for printing
    mark = "x" if task["done"] else " "
    priority = format_priority(task["priority"])
    return f"{i}) [{mark}] ({priority}) {task['title']}"


def build_view(tasks, predicate=None, sort_key=None, reverse=False):
    # Build a filtered view of tasks, preserving original indices
    view = []
    for idx, task in enumerate(tasks):
        if predicate is None or predicate(task):
            view.append((idx, task))

    # Apply sorting only to the view, not to the original tasks list
    if sort_key is not None:
        view.sort(key=lambda item: sort_key(item[1]), reverse=reverse)

    return view


def list_view(view, header="Tasks"):
    # Print a task view
    print(f"\n{header}:")
    if not view:
        print("No tasks found.")
        print("Total: 0 tasks\n")
        return

    for i, (_orig_idx, task) in enumerate(view, start=1):
        print(format_task_line(i, task))

    print(f"Total: {len(view)} tasks\n")


def read_view_number(prompt, max_value):
    # Read a valid task number from the current view
    raw = input(prompt).strip()
    if not raw.isdigit():
        return None

    n = int(raw)
    if not (1 <= n <= max_value):
        return None

    return n


def read_priority(prompt="Priority [low/medium/high]: "):
    # Read and validate a priority from user input
    raw = input(prompt).strip().lower()
    if raw in VALID_PRIORITIES:
        return raw
    return None


def read_sort_option():
    # Ask the user how to sort the current view
    print("Sort options:")
    print("1) Default order")
    print("2) Title (A-Z)")
    print("3) Priority (high -> low)")
    print("4) Pending first")
    choice = input("Choose sort: ").strip()

    if choice == "1":
        return None, False, "Default order"
    elif choice == "2":
        return lambda t: t["title"].lower(), False, "Title (A-Z)"
    elif choice == "3":
        return lambda t: PRIORITY_RANK[t["priority"]], False, "Priority (high -> low)"
    elif choice == "4":
        return lambda t: t["done"], False, "Pending first"

    print("Invalid sort option. Using default order.\n")
    return None, False, "Default order"


def add_task(tasks):
    # Add a new task to the list
    title = input("Enter a new task: ").strip()
    if not title:
        print("Empty task. Nothing added.\n")
        return

    existing = {t["title"].strip().lower() for t in tasks}
    if title.lower() in existing:
        print("This task already exists.\n")
        return

    priority = read_priority()
    if priority is None:
        print("Invalid priority. Use: low, medium, or high.\n")
        return

    tasks.append({
        "title": title,
        "done": False,
        "priority": priority,
    })
    save_tasks(tasks)
    print("Task added successfully.\n")


def clear_completed(tasks):
    # Remove all completed tasks
    done_count = sum(1 for t in tasks if t["done"])
    if done_count == 0:
        print("No completed tasks to clear.\n")
        return

    tasks[:] = [t for t in tasks if not t["done"]]
    save_tasks(tasks)
    print(f"Cleared {done_count} completed task(s).\n")


def toggle_from_view(tasks, view):
    # Toggle the done status of a task selected from the current view
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
    # Remove a task selected from the current view
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
    # Edit the title of a task selected from the current view
    if not view:
        print("No tasks to edit.\n")
        return

    n = read_view_number("Task number to edit title: ", len(view))
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
    if new_title.lower() in existing and new_title.lower() != current.strip().lower():
        print("A task with this title already exists.\n")
        return

    tasks[orig_idx]["title"] = new_title
    save_tasks(tasks)
    print("Title updated.\n")


def edit_priority_from_view(tasks, view):
    # Edit the priority of a task selected from the current view
    if not view:
        print("No tasks to edit.\n")
        return

    n = read_view_number("Task number to edit priority: ", len(view))
    if n is None:
        print("Invalid number.\n")
        return

    orig_idx, _task = view[n - 1]
    current = tasks[orig_idx]["priority"]

    new_priority = read_priority(
        prompt=f"New priority [low/medium/high] (current: {current}): "
    )
    if new_priority is None:
        print("Invalid priority.\n")
        return

    tasks[orig_idx]["priority"] = new_priority
    save_tasks(tasks)
    print("Priority updated.\n")


def view_loop(tasks, header, predicate=None):
    # Loop inside a specific task view with sorting and actions
    sort_key = None
    reverse = False
    sort_label = "Default order"

    while True:
        full_header = f"{header} | Sort: {sort_label}"
        view = build_view(tasks, predicate=predicate, sort_key=sort_key, reverse=reverse)
        list_view(view, header=full_header)

        action = input(
            "Action [S]ort [T]oggle [R]emove [E]dit title [P]riority [B]ack: "
        ).strip().lower()

        if action in ("b", ""):
            print()
            return
        elif action == "s":
            sort_key, reverse, sort_label = read_sort_option()
        elif action == "t":
            toggle_from_view(tasks, view)
        elif action == "r":
            remove_from_view(tasks, view)
        elif action == "e":
            edit_title_from_view(tasks, view)
        elif action == "p":
            edit_priority_from_view(tasks, view)
        else:
            print("Invalid action.\n")


def main():
    # Main application loop
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

        elif choice == "7":
            view_loop(
                tasks,
                header="High priority tasks",
                predicate=lambda t: t["priority"] == "high",
            )

        elif choice == "0":
            save_tasks(tasks)
            print("Exiting...")
            break

        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()
