import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect("budget.db")
cursor = conn.cursor()

# Create expenses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    amount REAL,
    date TEXT
)
""")

conn.commit()


# Add expense
def add_expense():
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))
    date = input("Enter date (YYYY-MM-DD): ")

    cursor.execute(
        "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
        (category, amount, date)
    )

    conn.commit()
    print("Expense added successfully!")


# Display expenses
def view_expenses():
    df = pd.read_sql_query("SELECT * FROM expenses", conn)

    if df.empty:
        print("No expenses found.")
    else:
        print("\nYour Expenses:")
        print(df)


# Category-wise report
def category_report():
    df = pd.read_sql_query("SELECT category, amount FROM expenses", conn)

    if df.empty:
        print("No data available.")
        return

    report = df.groupby("category")["amount"].sum()

    print("\nCategory-wise Expenses:")
    print(report)

    # Create chart
    report.plot(kind="bar")

    plt.title("Category-wise Expense Report")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.show()


# Main menu
while True:

    print("\n===== SMART BUDGET ANALYZER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Category-wise Report")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        category_report()

    elif choice == "4":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")

conn.close()