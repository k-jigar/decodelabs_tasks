import json
import os

DATA_FILE = "expenses.json"


def load_expenses() -> list:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_expenses(expenses: list) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses: list, description: str, amount: float) -> dict:
    expense = {
        "id":          len(expenses) + 1,
        "description": description,
        "amount":      round(amount, 2)
    }
    expenses.append(expense)
    save_expenses(expenses)
    return expense


def get_total(expenses: list) -> float:
    total = 0
    for expense in expenses:
        total += expense["amount"]
    return round(total, 2)


def get_highest(expenses: list) -> dict:
    if not expenses:
        return None
    highest = expenses[0]
    for expense in expenses:
        if expense["amount"] > highest["amount"]:
            highest = expense
    return highest


def get_average(expenses: list) -> float:
    if not expenses:
        return 0.0
    return round(get_total(expenses) / len(expenses), 2)


def view_expenses(expenses: list) -> None:
    if not expenses:
        print("\n  No expenses recorded yet.\n")
        return

    print("\n" + "-" * 48)
    print(f"  {'#':<4} {'DESCRIPTION':<22} {'AMOUNT':>10}")
    print("-" * 48)

    for index, expense in enumerate(expenses, start=1):
        print(f"  {index:<4} {expense['description']:<22} Rs {expense['amount']:>8.2f}")

    print("-" * 48)
    print(f"  {'TOTAL':<26} Rs {get_total(expenses):>8.2f}")
    print(f"  {'AVERAGE':<26} Rs {get_average(expenses):>8.2f}")

    highest = get_highest(expenses)
    print(f"  {'HIGHEST':<26} {highest['description']} (Rs {highest['amount']:.2f})")
    print("-" * 48)
    print()


def delete_expense(expenses: list, expense_id: int) -> bool:
    original_len = len(expenses)
    expenses[:] = [e for e in expenses if e["id"] != expense_id]
    if len(expenses) < original_len:
        for i, expense in enumerate(expenses, start=1):
            expense["id"] = i
        save_expenses(expenses)
        return True
    return False


def print_menu() -> None:
    print("+" + "-" * 36 + "+")
    print("|  1. Add an expense                 |")
    print("|  2. View all expenses              |")
    print("|  3. Delete an expense              |")
    print("|  4. View total spent               |")
    print("|  5. Exit                           |")
    print("+" + "-" * 36 + "+")


def main() -> None:
    expenses = load_expenses()
    print("  Type 'quit' at any prompt to return to menu.\n")

    while True:
        print_menu()
        choice = input("  Enter choice (1-5): ").strip()

        if choice == "1":
            description = input("  Expense description: ").strip()
            if description.lower() == "quit" or not description:
                continue

            raw = input("  Amount (Rs): ").strip()

            if raw.lower() == "quit":
                continue

            try:
                amount = float(raw)
                if amount <= 0:
                    print("\n  Amount must be greater than zero.")
                    continue
                new_expense = add_expense(expenses, description, amount)
                print(f"\n  Added: {new_expense['description']} — Rs {new_expense['amount']:.2f}")
                print(f"  Running total: Rs {get_total(expenses):.2f}")
            except ValueError:
                print("\n  Invalid amount. Please enter a number.")

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            view_expenses(expenses)
            if expenses:
                raw = input("  Enter expense # to delete: ").strip()
                if raw.lower() == "quit":
                    continue
                try:
                    eid = int(raw)
                    if delete_expense(expenses, eid):
                        print(f"\n  Expense {eid} deleted.")
                        print(f"  Remaining total: Rs {get_total(expenses):.2f}")
                    else:
                        print(f"\n  Expense {eid} not found.")
                except ValueError:
                    print("\n  Invalid input. Please enter a number.")

        elif choice == "4":
            if not expenses:
                print("\n  No expenses recorded yet.")
            else:
                print(f"\n  Total expenses recorded : {len(expenses)}")
                print(f"  Total amount spent      : Rs {get_total(expenses):.2f}")
                print(f"  Average per expense     : Rs {get_average(expenses):.2f}")
                highest = get_highest(expenses)
                print(f"  Highest single expense  : {highest['description']} (Rs {highest['amount']:.2f})")

        elif choice == "5":
            print(f"\n  Session closed. Total spent: Rs {get_total(expenses):.2f}")
            print("  Data saved to expenses.json\n")
            break

        else:
            print("\n  Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()