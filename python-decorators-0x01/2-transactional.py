#!/usr/bin/env python3
"""
2-transactional.py

Implements:
 - with_db_connection: decorator that manages opening/closing sqlite3 connection.
 - transactional: decorator that wraps a function call in a transaction (commit/rollback).

Usage:
    update_user_email(user_id=1, new_email="someone@example.com")
"""

import sqlite3
import functools
from typing import Any, Callable, Optional, Tuple

# ------------------------------
# Decorator 1: with_db_connection
# ------------------------------


def with_db_connection(func: Callable) -> Callable:
    """
    Ensures that the wrapped function has a sqlite3 connection.
    If caller passes conn=..., uses it (caller must close).
    Otherwise opens 'users.db', injects conn as first argument, and closes it automatically.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "conn" in kwargs and kwargs["conn"] is not None:
            # Use provided connection
            return func(*args, **kwargs)

        conn: Optional[sqlite3.Connection] = None
        try:
            conn = sqlite3.connect("users.db")
            return func(conn, *args, **kwargs)
        finally:
            if conn:
                conn.close()
    return wrapper


# ------------------------------
# Decorator 2: transactional
# ------------------------------
def transactional(func: Callable) -> Callable:
    """
    Wraps a DB operation in a transaction:
    - Calls the wrapped function with a conn.
    - If it completes without error, commits the transaction.
    - If it raises an exception, rolls back before re-raising.
    """
    @functools.wraps(func)
    def wrapper(conn: sqlite3.Connection, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
    return wrapper


# ------------------------------
# Example usage
# ------------------------------
@with_db_connection
@transactional
def update_user_email(conn: sqlite3.Connection, user_id: int, new_email: str) -> None:
    """
    Update a user's email address by ID.
    The decorators ensure connection + transaction safety.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )


# --- helper to create a sample DB for local testing ---
def _ensure_sample_db():
    """Create users.db and a users table with sample rows if they don't exist."""
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """)
    # Add sample data if table empty
    cur.execute("SELECT COUNT(*) FROM users;")
    count = cur.fetchone()[0]
    if count == 0:
        sample = [
            ("alice", "alice@example.com"),
            ("bob", "bob@example.com"),
            ("carol", "carol@example.com"),
        ]
        cur.executemany(
            "INSERT INTO users (username, email) VALUES (?, ?);", sample)
        conn.commit()
    conn.close()


if __name__ == "__main__":
    _ensure_sample_db()

    # Update a user's email safely (commit if success, rollback if error)
    update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")

    # Show result
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = 1;")
    print("Updated row ->", cur.fetchone())
    conn.close()
