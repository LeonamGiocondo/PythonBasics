# Day 35 To add a field due_date to tasks for managing deadlines


import json
from pathlib import Path
from datetime import datetime, date

# Constants
FILE = Path("tasks.json")           # Path to the JSON file used as persistent storage
VALID_PRIORITIES = ("low", "medium", "high")  # Accepted priority values
DATE_FORMAT = "%Y-%m-%d"            # ISO 8601 date format (e.g., 2026-03-30)

# Maps priority labels to numeric ranks for sorting (lower = higher priority)
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


def normalize_priority(value):
    """Convert any input to a valid priority (low/medium/high)."""
    value = str(value).strip().lower()
    return value if value in VALID_PRIORITIES else "medium"  # Fallback to "medium" if unrecognized


def normalize_date(value):
    """Parse and validate a date string (YYYY-MM-DD). Returns None if invalid."""
    if not value:
        return None

    try:
        parsed = datetime.strptime(value, DATE_FORMAT).date()
        return parsed if parsed >= date.today() else None  # Reject past dates
    except (ValueError, TypeError):
        return None  # Return None for any parsing error


def normalize_tasks(data):
    """Normalize raw JSON data into structured tasks with due_date."""
    if not isinstance(data, list):
        return []  # Reject anything that isn't a list

    normalized = []
    for item in data:
        # Support plain strings as minimal task definitions (title only)
        if isinstance(item, str):
            title = item.strip()
            if title:
                normalized.append({
                    "title": title,
                    "done": False,
                    "priority": "medium",  # Default priority for string tasks
                    "due_date": None,      # No due date for string tasks
                })
            continue

        # Full task object: extract and sanitize each field
        if isinstance(item, dict):
            title = str(item.get("title", "")).strip()
            done = bool(item.get("done", False))
            priority = normalize_priority(item.get("priority", "medium"))
            due_date = normalize_date(item.get("due_date"))

            if title:  # Skip tasks with empty or missing titles
                normalized.append({
                    "title": title,
                    "done": done,
                    "priority": priority,
                    "due_date": due_date.isoformat() if due_date else None,  # Store as string or null
                })

    return normalized


def load_tasks():
    """Load tasks from JSON file with due_date support."""
    if not FILE.exists():
        return []  # Return empty list if the file doesn't exist yet

    try:
        raw = FILE.read_text(encoding="utf-8")
        data = json.loads(raw)
        return normalize_tasks(data)  # Always normalize on load to ensure data integrity
    except (json.JSONDecodeError, OSError):
        return []  # Silently recover from corrupted or unreadable files


def save_tasks(tasks):
    """Save tasks to JSON file."""
    FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),  # Pretty-print with Unicode support
        encoding="utf-8",
    )


def show_menu():
    """Display the main menu with due_date options."""
    print("=== TO-DO ===")
    print("1) View: All tasks")
    print("2) Add task")
    print("3) View: Pending tasks")
    print("4) View: Done tasks")
    print("5) View: Overdue tasks")   # Tasks whose due_date is in the past
    print("6) View: Due today")       # Tasks due on the current date
    print("7) View: Upcoming tasks")  # Tasks with a future due date
    print("8) Clear completed")
    print("0) Exit")


def format_priority(priority):
    """Format priority for display (e.g., 'HIGH')."""
    return priority.upper()


def format_due_date(due_date):
    """Format due_date for display (e.g., '2026-03-30 (OVERDUE)')."""
    if not due_date:
        return "No due date"

    due = datetime.strptime(due_date, DATE_FORMAT).date()
    today = date.today()

    if due < today:
        return f"{due_date} (OVERDUE)"   # Past due date
    elif due == today:
        return f"{due_date} (TODAY)"     # Due on the current day
    else:
        return due_date                  # Future due date — no label needed


def format_task_line(i, task):
    """Format a task line with priority and due date."""
    mark = "x" if task["done"] else " "   # Checkbox: "x" = done, " " = pending
    priority = format_priority(task["priority"])
    due = format_due_date(task["due_date"])
    return f"{i}) [{mark}] ({priority}) {task['title']} | Due: {due}"


def build_view(tasks, predicate=None, sort_key=None, reverse=False):
    """Build a filtered and sorted view of tasks."""
    view = []
    for idx, task in enumerate(tasks):
        if predicate is None or predicate(task):
            view.append((idx, task))  # Preserve original index for in-place edits

    if sort_key is not None:
        view.sort(key=lambda item: sort_key(item[1]), reverse=reverse)

    return view


def list_view(view, header="Tasks"):
    """Display a list of tasks with a header."""
    print(f"\n{header}:")
    if not view:
        print("No tasks found.")
        print("Total: 0 tasks\n")
        return

    for i, (_orig_idx, task) in enumerate(view, start=1):
        print(format_task_line(i, task))  # Display number is view-relative, not original index

    print(f"Total: {len(view)} tasks\n")


def read_view_number(prompt, max_value):
    """Read a valid task number from the current view."""
    raw = input(prompt).strip()
    if not raw.isdigit():
        return None

    n = int(raw)
    if not (1 <= n <= max_value):
        return None  # Out of bounds

    return n


def read_priority(prompt="Priority [low/medium/high]: "):
    """Read and validate a priority."""
    raw = input(prompt).strip().lower()
    return raw if raw in VALID_PRIORITIES else None  # None signals invalid input to the caller


def read_date(prompt="Due date (YYYY-MM-DD): "):
    """Read and validate a due date."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            return None  # Empty input = no due date (optional field)

        parsed = normalize_date(raw)
        if parsed:
            return parsed.isoformat()

        print("Invalid date. Use YYYY-MM-DD (e.g., 2026-03-30).")  # Keep prompting until valid


def read_sort_option():
    """Ask the user how to sort the current view."""
    print("Sort options:")
    print("1) Default order")
    print("2) Title (A-Z)")
    print("3) Priority (high -> low)")
    print("4) Pending first")
    print("5) Due date (earliest first)")
    choice = input("Choose sort: ").strip()

    if choice == "1":
        return None, False, "Default order"
    elif choice == "2":
        return lambda t: t["title"].lower(), False, "Title (A-Z)"
    elif choice == "3":
        return lambda t: PRIORITY_RANK[t["priority"]], False, "Priority (high -> low)"
    elif choice == "4":
        return lambda t: t["done"], False, "Pending first"   # False sorts before True
    elif choice == "5":
        return lambda t: t["due_date"] or "9999-12-31", False, "Due date (earliest first)"  # Tasks without due date go last

    print("Invalid sort option. Using default order.\n")
    return None, False, "Default order"


def add_task(tasks):
    """Add a new task with optional due date."""
    title = input("Enter a new task: ").strip()
    if not title:
        print("Empty task. Nothing added.\n")
        return

    existing = {t["title"].strip().lower() for t in tasks}
    if title.lower() in existing:
        print("This task already exists.\n")  # Case-insensitive duplicate check
        return

    priority = read_priority()
    if priority is None:
        print("Invalid priority. Use: low, medium, or high.\n")
        return

    due_date = read_date()
    tasks.append({
        "title": title,
        "done": False,
        "priority": priority,
        "due_date": due_date,
    })
    save_tasks(tasks)
    print("Task added successfully.\n")


def clear_completed(tasks):
    """Remove all completed tasks."""
    done_count = sum(1 for t in tasks if t["done"])
    if done_count == 0:
        print("No completed tasks to clear.\n")
        return

    tasks[:] = [t for t in tasks if not t["done"]]  # In-place mutation to keep reference valid
    save_tasks(tasks)
    print(f"Cleared {done_count} completed task(s).\n")


def toggle_from_view(tasks, view):
    """Toggle the done status of a task."""
    if not view:
        print("No tasks to toggle.\n")
        return

    n = read_view_number("Task number to toggle: ", len(view))
    if n is None:
        print("Invalid number.\n")
        return

    orig_idx, _task = view[n - 1]  # Map view number back to original list index
    tasks[orig_idx]["done"] = not tasks[orig_idx]["done"]
    save_tasks(tasks)

    state = "done" if tasks[orig_idx]["done"] else "not done"
    print(f"Updated: '{tasks[orig_idx]['title']}' is now {state}.\n")


def remove_from_view(tasks, view):
    """Remove a task from the list."""
    if not view:
        print("No tasks to remove.\n")
        return

    n = read_view_number("Task number to remove: ", len(view))
    if n is None:
        print("Invalid number.\n")
        return

    orig_idx, _task = view[n - 1]
    removed = tasks.pop(orig_idx)  # pop() removes and returns the item at the original index
    save_tasks(tasks)
    print(f"Removed: {removed['title']}\n")


def edit_title_from_view(tasks, view):
    """Edit the title of a task."""
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
        print("A task with this title already exists.\n")  # Allow re-saving the same title
        return

    tasks[orig_idx]["title"] = new_title
    save_tasks(tasks)
    print("Title updated.\n")


def edit_priority_from_view(tasks, view):
    """Edit the priority of a task."""
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


def edit_due_date_from_view(tasks, view):
    """Edit the due date of a task."""
    if not view:
        print("No tasks to edit.\n")
        return

    n = read_view_number("Task number to edit due date: ", len(view))
    if n is None:
        print("Invalid number.\n")
        return

    orig_idx, _task = view[n - 1]
    current = tasks[orig_idx]["due_date"]

    new_due_date = read_date(
        prompt=f"New due date (YYYY-MM-DD) (current: {current}): "
    )
    tasks[orig_idx]["due_date"] = new_due_date  # None is valid — clears the due date
    save_tasks(tasks)
    print("Due date updated.\n")


def view_loop(tasks, header, predicate=None):
    """Loop inside a task view with sorting and actions."""
    sort_key = None
    reverse = False
    sort_label = "Default order"

    while True:
        full_header = f"{header} | Sort: {sort_label}"
        view = build_view(tasks, predicate=predicate, sort_key=sort_key, reverse=reverse)
        list_view(view, header=full_header)

        action = input(
            "Action [S]ort [T]oggle [R]emove [E]dit title [P]riority [D]ue date [B]ack: "
        ).strip().lower()

        if action in ("b", ""):
            print()
            return                               # Exit back to the main menu
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
        elif action == "d":
            edit_due_date_from_view(tasks, view)
        else:
            print("Invalid action.\n")


def main():
    """Main application loop."""
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
            today = date.today().isoformat()
            view_loop(
                tasks,
                header="Overdue tasks",
                predicate=lambda t: t["due_date"] and t["due_date"] < today,  # Strict past dates only
            )

        elif choice == "6":
            today = date.today().isoformat()
            view_loop(
                tasks,
                header="Due today",
                predicate=lambda t: t["due_date"] == today,  # Exact match on today's date
            )

        elif choice == "7":
            today = date.today().isoformat()
            view_loop(
                tasks,
                header="Upcoming tasks",
                predicate=lambda t: t["due_date"] and t["due_date"] > today,  # Strict future dates only
            )

        elif choice == "8":
            clear_completed(tasks)

        elif choice == "0":
            save_tasks(tasks)   # Final save before exit
            print("Exiting...")
            break

        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()
