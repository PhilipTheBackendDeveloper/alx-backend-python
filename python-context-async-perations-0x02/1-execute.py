#!/usr/bin/env python3
"""
1-execute.py

Task:
- Implement a reusable query context manager ExecuteQuery
- Executes a given SQL query with parameters
- Automatically handles opening and closing the database connection
"""

import sqlite3


class ExecuteQuery:
    """
    A custom context manager for executing queries safely.
    Opens a connection, executes the given query with params,
    returns the result, and closes connection automatically.
    """

    def __init__(self, db_name: str, query: str, params: tuple = ()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, fetch results."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close cursor and connection safely."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Returning False means exceptions will propagate if any occur
        return False


# --- Example usage ---
if __name__ == "__main__":
    # Ensure sample data exists with an 'age' column
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER DEFAULT 30
    )
    """)
    # Insert sample users if table is empty
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
            [
                ("alice", "alice@example.com", 22),
                ("bob", "bob@example.com", 29),
                ("carol", "carol@example.com", 34),
                ("david", "david@example.com", 19),
            ]
        )
        conn.commit()
    conn.close()

    # Run query with context manager
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        print("Users older than 25:")
        for row in results:
            print(row)
