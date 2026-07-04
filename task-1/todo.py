import json
import os

DATA_FILE = "tasks.json"


def load_tasks() -> list:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks: list) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(tasks: list, description: str) -> dict:
    task = {
        "id": len(tasks) + 1,
        "task": description.strip(),
        "done": False
    }
    tasks.append(task)
    save_tasks(tasks)
    return task


def view_tasks(tasks: list) -> None:
    if not tasks:
        print("\nNo tasks yet.\n")
        return

    print("\n" + "-" * 42)
    print(f"{'#':<4} {'STATUS':<8} TASK")
    print("-" * 42)

    for index, task in enumerate(tasks, start=1):
        status = "Done" if task["done"] else "Todo"
        print(f"{index:<4} {status:<8} {task['task']}")

    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    print("-" * 42)
    print(f"{done}/{total} tasks completed\n")


def complete_task(tasks: list, task_id: int) -> bool:
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            return True
    return False


def delete_task(tasks: list, task_id: int) -> bool:
    original_len = len(tasks)
    tasks[:] = [t for t in tasks if t["id"] != task_id]

    if len(tasks) < original_len:
        for i, task in enumerate(tasks, start=1):
            task["id"] = i
        save_tasks(tasks)
        return True
    return False


def print_menu() -> None:
    print("\n========================")
    print("      To-Do List")
    print("========================")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. Mark task as complete")
    print("4. Delete a task")
    print("5. Exit")


def main() -> None:
    tasks = load_tasks()

    print("\nWelcome!")

    while True:
        print_menu()
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            desc = input("Task description: ").strip()
            if desc:
                new_task = add_task(tasks, desc)
                print(f"\nAdded: [{new_task['id']}] {new_task['task']}")
            else:
                print("\nTask cannot be empty.")

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            view_tasks(tasks)
            if tasks:
                try:
                    tid = int(input("Enter task number to mark complete: "))
                    if complete_task(tasks, tid):
                        print(f"\nTask {tid} marked as done.")
                    else:
                        print(f"\nTask {tid} not found.")
                except ValueError:
                    print("\nPlease enter a valid number.")

        elif choice == "4":
            view_tasks(tasks)
            if tasks:
                try:
                    tid = int(input("Enter task number to delete: "))
                    if delete_task(tasks, tid):
                        print(f"\nTask {tid} deleted.")
                    else:
                        print(f"\nTask {tid} not found.")
                except ValueError:
                    print("\nPlease enter a valid number.")

        elif choice == "5":
            print("\nGoodbye.\n")
            break

        else:
            print("\nInvalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
