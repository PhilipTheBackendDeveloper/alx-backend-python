#!/usr/bin/python3
import sqlite3
import functools
import os


def with_db_connection(func):
    """Decorator to handle DB connection automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def _create_sample_db_if_missing():
    if not os.path.exists("users.db"):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        cursor.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            [
                ("Alice", "alice@example.com"),
                ("Bob", "bob@example.com"),
                ("Charlie", "charlie@example.com")
            ]
        )
        conn.commit()
        conn.close()
        print("users.db created with sample data")


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == "__main__":
    _create_sample_db_if_missing()
    user = get_user_by_id(user_id=1)
    print("Fetched user:", user)
