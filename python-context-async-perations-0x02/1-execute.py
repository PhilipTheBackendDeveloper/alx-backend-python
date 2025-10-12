#!/usr/bin/python3
import sqlite3
import csv
import os


class ExecuteQuery:
    """Custom context manager that executes a query and returns results."""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, return results."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close resources cleanly."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


def seed_database_from_csv(db_name, csv_file):
    """Seed the database with data from a CSV file if table is empty."""
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        # Ensure table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)
        # Check if already populated
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0 and os.path.exists(csv_file):
            with open(csv_file, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                users = [(row["name"], row["email"], int(row["age"])) for row in reader]
                cursor.executemany(
                    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)", users
                )
                conn.commit()


# Example usage
if __name__ == "__main__":
    db_file = "users.db"
    csv_file = "user_data.csv"

    # Seed the database from CSV
    seed_database_from_csv(db_file, csv_file)

    # Use our context manager to query users older than 25
    with ExecuteQuery(db_file, "SELECT * FROM users WHERE age > ?", (25,)) as results:
        for row in results:
            print(row)
