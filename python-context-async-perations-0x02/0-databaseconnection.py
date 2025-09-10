#!/usr/bin/env python3
"""
0-databaseconnection.py

Task:
- Create a class-based context manager for database connections
- Use __enter__ and __exit__ to handle opening/closing automatically
"""

import sqlite3


class DatabaseConnection:
    """
    A custom context manager for managing SQLite database connections.
    Ensures the connection is opened on __enter__ and closed on __exit__.
    """

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection when entering the context."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection on exiting the context."""
        if self.conn:
            self.conn.close()
        # Returning False allows exceptions (if any) to propagate
        return False


# --- Example usage ---
if __name__ == "__main__":
    # Ensure a sample database with a users table exists
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)
    # Insert sample data if empty
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            [
                ("alice", "alice@example.com"),
                ("bob", "bob@example.com"),
                ("carol", "carol@example.com")
            ]
        )
        conn.commit()
    conn.close()

    # Use the custom context manager
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Users in database:")
        for row in results:
            print(row)
