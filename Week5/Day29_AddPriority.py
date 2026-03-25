# Day 29 - To add priority to tasks

import json
from pathlib import Path

# Path to the folder where the tasks will be saved
FILE = Path("tasks.json")
# Priorities accepted by the system
VALID_PRIORITIES = ("low", "medium", "high")


def normalize_priority(value):
# Converts the value to a string, removes spaces, and converts it to lowercase
    value = str(value).strip().lower()
# If the priority is valid, return it
    if value in VALID_PRIORITIES:
        return value
# If is invalid, use "medium" as the default
    return "medium"


def normalize_tasks(data):
# Ensures that the loaded JSON content is a list
    if not isinstance(data, list):
        return []

    normalized = []
# Go through each item on the list to standardize the format
    for item in data:
# If the item is just a string, convert it to a standard task
        if isinstance(item, str):
            title = item.strip()
            if title:
                normalized.append({
                    "title": title,
                    "done": False,
                    "priority": "medium",
                })
            continue
# If the item is already a dictionary, extract and normalize the fields
        if isinstance(item, dict):
            title = str(item.get("title", "")).strip()
            done = bool(item.get("done", False))
            priority = normalize_priority(item.get("priority", "medium"))
# Only add tasks w/ a non-empty title
            if title:
                normalized.append({
                    "title": title,
                    "done": done,
                    "priority": priority,
                })
            continue

    return normalized


def load_tasks():
# If the file does not yet exist, start with an empty list
    if not FILE.exists():
        return []
    try:
#  Reads the contents of the JSON file
        raw = FILE.read_text(encoding="utf-8")
        data = json.loads(raw)
# Normalize the data before returning it to the program
        return normalize_tasks(data)
    except (json.JSONDecodeError, OSError):
# If an error occurs while reading or parsing the file, it returns an empty list
        return []


def save_tasks(tasks):
# Save the to-do list to a JSON file with indentation to make it readable
    FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def show_menu():
# Displays the program's main menu
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
# Displays the priority in uppercase letters to visually highlight it
    return priority.upper()


def format_task_line(i, task):
# Displays “x” if the task has been completed, or a blank space if it hasn't
    mark = "x" if task["done"] else " "
# Set the display priority
    priority = format_priority(task["priority"])
# Build the string that will be displayed to the user
    return f"{i}) [{mark}] ({priority}) {task['title']}"


def build_view(tasks, predicate=None):
# Creates a filtered “view” of the task list
# Each item stores:
# - the task's original index in the main list
# - the task itself
    view = []
    for idx, task in enumerate(tasks):
# If there is no filter, include everything
# If there is a filter, include only what meets the condition
        if predicate is None or predicate(task):
            view.append((idx, task))
    return view


def list_view(view, header="Tasks"):
# Displays the title of the current view
    print(f"\n{header}:")
# If there are no tasks in this view, display a message and exit
    if not view:
        print("No tasks found.")
        print("Total: 0 tasks\n")
        return
# Displays tasks numbered starting from 1 to make it easier for users to navigate
    for i, (_orig_idx, task) in enumerate(view, start=1):
        print(format_task_line(i, task))
    print(f"Total: {len(view)} tasks\n")


def read_view_number(prompt, max_value):
# Reads the number entered by the user
    raw = input(prompt).strip()
# Rejects any input that is not a number
    if not raw.isdigit():
        return None
    n = int(raw)
# Ensures that the number is within the valid range of the displayed list
    if not (1 <= n <= max_value):
        return None
    return n


def read_priority(prompt="Priority [low/medium/high]: "):
# Reads the priority specified by the user
    raw = input(prompt).strip().lower()
# Returns the priority only if it is valid
    if raw in VALID_PRIORITIES:
        return raw
    return None


def add_task(tasks):
# Enter the title of the new task
    title = input("Enter a new task: ").strip()
# Does not allow adding an empty task
    if not title:
        print("Empty task. Nothing added.\n")
        return

# Creates a set of existing titles in lowercase
# To prevent duplicates by ignoring case differences
    existing = {t["title"].strip().lower() for t in tasks}
    if title.lower() in existing:
        print("This task already exists.\n")
        return

# Read the priority of the new task
    priority = read_priority()
    if priority is None:
        print("Invalid priority. Use: low, medium, or high.\n")
        return

# Add the new task to the list
    tasks.append({
        "title": title,
        "done": False,
        "priority": priority,
    })
# Save immediately to the file
    save_tasks(tasks)
    print("Task added successfully.\n")


def clear_completed(tasks):
# Count how many completed tasks there are
    done_count = sum(1 for t in tasks if t["done"])
# If there are none, inform the user
    if done_count == 0:
        print("No completed tasks to clear.\n")
        return
#  Keep only the tasks that haven't been completed yet
    tasks[:] = [t for t in tasks if not t["done"]]
#  Save the updated list
    save_tasks(tasks)
    print(f"Cleared {done_count} completed task(s).\n")


def toggle_from_view(tasks, view):
# There is nothing to toggle if the view is empty
    if not view:
        print("No tasks to toggle.\n")
        return

# Reads the task number in the current view
    n = read_view_number("Task number to toggle: ", len(view))
    if n is None:
        print("Invalid number.\n")
        return
# Restores the task's original index in the main list
    orig_idx, _task = view[n - 1]
# Changes the status: from pending to completed, or vice versa
    tasks[orig_idx]["done"] = not tasks[orig_idx]["done"]
    save_tasks(tasks)

    state = "done" if tasks[orig_idx]["done"] else "not done"
    print(f"Updated: '{tasks[orig_idx]['title']}' is now {state}.\n")


def remove_from_view(tasks, view):
# There is nothing to remove if the view is empty
    if not view:
        print("No tasks to remove.\n")
        return
# Reads the task number in the current view
    n = read_view_number("Task number to remove: ", len(view))
    if n is None:
        print("Invalid number.\n")
        return
# Find the actual task ID and remove it from the main list
    orig_idx, _task = view[n - 1]
    removed = tasks.pop(orig_idx)
    save_tasks(tasks)
    print(f"Removed: {removed['title']}\n")


def edit_title_from_view(tasks, view):
# There is nothing to edit if the preview is empty
    if not view:
        print("No tasks to edit.\n")
        return
# Read the number of the task to be edited
    n = read_view_number("Task number to edit title: ", len(view))
    if n is None:
        print("Invalid number.\n")
        return
# Restores the task's original index
    orig_idx, _task = view[n - 1]
    current = tasks[orig_idx]["title"]
# Order the new title
    new_title = input(f"New title (current: {current}): ").strip()
    if not new_title:
        print("Empty title. Nothing changed.\n")
        return
# Avoid duplicating existing titles
    existing = {t["title"].strip().lower() for t in tasks}
    if new_title.lower() in existing and new_title.lower() != current.strip().lower():
        print("A task with this title already exists.\n")
        return
# Update the title and save
    tasks[orig_idx]["title"] = new_title
    save_tasks(tasks)
    print("Title updated.\n")


def edit_priority_from_view(tasks, view):
# There is nothing to edit if the preview is empty
    if not view:
        print("No tasks to edit.\n")
        return
# Read the task number whose priority will be changed
    n = read_view_number("Task number to edit priority: ", len(view))
    if n is None:
        print("Invalid number.\n")
        return
# Retrieves the original task and its current priority
    orig_idx, _task = view[n - 1]
    current = tasks[orig_idx]["priority"]
# Request the new priority
    new_priority = read_priority(
        prompt=f"New priority [low/medium/high] (current: {current}): "
    )
    if new_priority is None:
        print("Invalid priority.\n")
        return
# Update the priority and save
    tasks[orig_idx]["priority"] = new_priority
    save_tasks(tasks)
    print("Priority updated.\n")


def view_loop(tasks, header, predicate=None):
# Interaction loop for a specific view:
# all, pending, completed, search, high priority, etc.
    while True:
# Render the view on every iteration to reflect recent changes
        view = build_view(tasks, predicate=predicate)
        list_view(view, header=header)

        action = input(
            "Action [T]oggle [R]emove [E]dit title [P]riority [B]ack: "
        ).strip().lower()
# Back to the main menu
        if action in ("b", ""):
            print()
            return
# Mark/unmark task as completed
        elif action == "t":
            toggle_from_view(tasks, view)
# Remove task
        elif action == "r":
            remove_from_view(tasks, view)
# Edit title
        elif action == "e":
            edit_title_from_view(tasks, view)
# Edit priority
        elif action == "p":
            edit_priority_from_view(tasks, view)
        else:
            print("Invalid action.\n")


def main():
# Load saved tasks when the program starts
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choice: ").strip()
# Show all tasks
        if choice == "1":
            view_loop(tasks, header="All tasks")
# Add new task
        elif choice == "2":
            add_task(tasks)
# Show only pending tasks
        elif choice == "3":
            view_loop(tasks, header="Pending tasks", predicate=lambda t: not t["done"])
# Show only tasks completed
        elif choice == "4":
            view_loop(tasks, header="Done tasks", predicate=lambda t: t["done"])
# Search tasks by text in the title
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
# Remove all tasks completed
        elif choice == "6":
            clear_completed(tasks)
# Show only high-priority tasks
        elif choice == "7":
            view_loop(
                tasks,
                header="High priority tasks",
                predicate=lambda t: t["priority"] == "high",
            )
# The program ends
        elif choice == "0":
            save_tasks(tasks)
            print("Exiting...")
            break

        else:
            print("Invalid option.\n")

# Ensures that the program runs only if this file is executed directly

if __name__ == "__main__":
    main()
