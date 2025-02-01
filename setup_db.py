import sqlite3
import random
from faker import Faker

fake = Faker()

DB_PATH = "data/company.db"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Departments Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Departments (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT UNIQUE NOT NULL,
            Manager TEXT NOT NULL
        )
    """)

    # Create Employees Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employees (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Department TEXT NOT NULL,
            Salary REAL NOT NULL,
            Hire_Date TEXT NOT NULL,
            FOREIGN KEY (Department) REFERENCES Departments(Name)
        )
    """)

    conn.commit()
    conn.close()
    print("Database created successfully!")

def populate_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    departments = [
        "Engineering", "HR", "Finance", "Marketing", "Sales",
        "Support", "Product", "Operations", "Legal", "IT"
    ]
    
    # Insert Departments with Fake Managers
    for dept in departments:
        cursor.execute("INSERT OR IGNORE INTO Departments (Name, Manager) VALUES (?, ?)", 
                       (dept, fake.name()))

    # Insert 500+ Employees with Random Salaries and Hire Dates
    for _ in range(500):
        name = fake.name()
        department = random.choice(departments)
        salary = round(random.uniform(40000, 150000), 2)
        hire_date = fake.date_between(start_date="-10y", end_date="today").strftime('%Y-%m-%d')

        cursor.execute("INSERT INTO Employees (Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?)", 
                       (name, department, salary, hire_date))

    conn.commit()
    conn.close()
    print("Database populated with sample employees and departments!")

if __name__ == "__main__":
    create_database()
    populate_database()
