import csv
import sys
from datetime import datetime

try:
    import google.generativeai as genai
except ImportError:
    genai = None


def main():
    print("\n=== Personal Expenditure ===")

    while True:
        print("\nMenu:")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Analyze Expenses")
        print("4. Chat with your expenses")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            analyze_expenses()
        elif choice == "4":
            chat_with_expenses()
        elif choice == "5":
            print("Program exited.")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")


# Implementing AI chatbot
def chat_with_expenses():
    """Let the user ask natural-language questions about their spending."""
    if genai is None:
        print("\nThe 'google-generativeai' package is not installed.")
        print("Run:  pip install google-generativeai")
        return

    import os
    api_key = input("\nEnter your Gemini API key (or set GEMINI_API_KEY env var): ").strip()
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("No API key provided. Returning to menu.")
        return

    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses found. Add some expenses first.")
        return

    # Build a plain-text summary of all expenses to send as context
    lines = ["Date, Category, Amount, Description"]
    for e in expenses:
        lines.append(f"{e[0]}, {e[1]}, ${float(e[2]):.2f}, {e[3]}")
    expense_data = "\n".join(lines)

    system_prompt = (
        "You are a personal finance assistant. The user will ask questions about "
        "their spending. Answer using only the expense data provided — do not invent "
        "numbers. Be concise and helpful. If the data doesn't contain enough information "
        "to answer, say so clearly.\n\n"
        f"Here is the user's full expense history:\n\n{expense_data}"
    )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt,
    )
    chat = model.start_chat(history=[])

    print("\n=== AI Expense Chat ===")
    print("Ask anything about your spending. Type 'quit' to exit.\n")
    print("Example questions:")
    print("  - How much did I spend on food last month?")
    print("  - Which category is draining my budget most?")
    print("  - Where can I cut back?\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Exiting chat.")
            break

        try:
            response = chat.send_message(user_input)
            reply = response.text
            print(f"\nAssistant: {reply}\n")

        except Exception as e:
            print(f"\nSomething went wrong: {e}")
            break


def add_expense():
    categories = [
        "Food", "Transport", "Entertainment",
        "Bills", "Shopping", "Health", "Other",
    ]

    while True:
        try:
            amount = float(input("Enter amount: $"))
            if amount <= 0:
                print("Amount must be positive.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")

    print("\nCategories:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    while True:
        try:
            cat_choice = int(input("Choose category (1-7): "))
            if 1 <= cat_choice <= 7:
                category = categories[cat_choice - 1]
                break
            else:
                print("Invalid choice. Please choose 1-7.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    description = input("Enter description: ").strip()
    if not description:
        description = "No description"

    date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if date_input:
        if validate_date(date_input):
            date = date_input
        else:
            print("Invalid date format. Using today's date.")
            date = datetime.now().strftime("%Y-%m-%d")
    else:
        date = datetime.now().strftime("%Y-%m-%d")

    save_expense(amount, category, description, date)
    print(f"\n✓ Expense added successfully!")


def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses found.")
        return

    print(f"\n{'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
    print("-" * 60)
    for expense in expenses:
        date, category, amount, description = expense
        print(f"{date:<12} {category:<15} ${float(amount):<9.2f} {description}")
    print(f"\nTotal expenses: {len(expenses)}")


def analyze_expenses():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses to analyze.")
        return

    total = calculate_total(expenses)
    category_totals = calculate_by_category(expenses)
    most_expensive = find_most_expensive(expenses)

    print("\n=== Expense Analysis ===")
    print(f"\nTotal Spending: ${total:.2f}")
    print(f"Number of Expenses: {len(expenses)}")
    print(f"Average per Expense: ${total / len(expenses):.2f}")

    print("\nSpending by Category:")
    for category, amount in sorted(
        category_totals.items(), key=lambda x: x[1], reverse=True
    ):
        percentage = (amount / total) * 100
        print(f"  {category:<15} ${amount:>8.2f} ({percentage:>5.1f}%)")

    print(f"\nMost Expensive Purchase:")
    print(
        f"  ${most_expensive[2]} - {most_expensive[3]} ({most_expensive[1]}) on {most_expensive[0]}"
    )


def load_expenses():
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            return list(reader)
    except FileNotFoundError:
        return []


def save_expense(amount, category, description, date):
    with open("expenses.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])


def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def calculate_total(expenses):
    return sum(float(e[2]) for e in expenses)


def calculate_by_category(expenses):
    category_totals = {}
    for expense in expenses:
        category = expense[1]
        amount = float(expense[2])
        category_totals[category] = category_totals.get(category, 0) + amount
    return category_totals


def find_most_expensive(expenses):
    return max(expenses, key=lambda e: float(e[2]))


if __name__ == "__main__":
    main()
