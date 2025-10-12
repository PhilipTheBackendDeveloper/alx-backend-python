#!/usr/bin/python3
import sqlite3


class DatabaseConnection:
    """Custom context manager for handling SQLite database connections."""

    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open database connection and return it."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close database connection safely, even if an error occurs."""
        if self.conn:
            self.conn.close()


# Example usage
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()

        # Ensure table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

        # Insert multiple rows if table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 1:
            sample_users = [
                ("Eric Hackman", "eric@example.com"),
                ("Faith Okoth", "faith@example.com"),
                ("John Doe", "john@example.com"),
                ("Jane Smith", "jane@example.com"),
                ("Michael Brown", "michael@example.com"),
                ("Alice Johnson", "alice@example.com"),
                ("Bob Williams", "bob@example.com"),
            ]
            cursor.executemany(
                "INSERT INTO users (name, email) VALUES (?, ?)", sample_users
            )
            conn.commit()

        # Fetch and print results
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
