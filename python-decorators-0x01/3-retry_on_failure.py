#!/usr/bin/env python3
"""
3-retry_on_failure.py

Implements:
 - with_db_connection: decorator to open/close sqlite3 connections.
 - retry_on_failure: decorator factory that retries a function on transient failures.

Usage:
    users = fetch_users_with_retry()
    print(users)
"""

import time
import sqlite3
import functools
from typing import Callable, Any, Optional


# ------------------------------
# Decorator 1: with_db_connection
# ------------------------------
def with_db_connection(func: Callable) -> Callable:
    """
    Ensures wrapped function has a sqlite3 connection.
    - If caller provides `conn=...`, use it (do not close).
    - Otherwise, open users.db, inject it, and close it automatically.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "conn" in kwargs and kwargs["conn"] is not None:
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
# Decorator 2: retry_on_failure
# ------------------------------
def retry_on_failure(retries: int = 3, delay: int = 2) -> Callable:
    """
    A decorator factory that retries a function if it raises an Exception.

    Args:
        retries (int): How many times to retry before giving up.
        delay (int): Seconds to wait between retries.

    Usage:
        @retry_on_failure(retries=3, delay=1)
        def some_function(...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception: Optional[Exception] = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(
                        f"[Retry {attempt}/{retries}] Error: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            # If all retries failed, raise the last exception
            raise last_exception
        return wrapper
    return decorator


# ------------------------------
# Example usage
# ------------------------------
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn: sqlite3.Connection):
    """
    Attempt to fetch all users.
    Will retry up to 3 times if a transient error occurs.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


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

    try:
        users = fetch_users_with_retry()
        print("Users fetched successfully:")
        for row in users:
            print(row)
    except Exception as e:
        print("Final failure:", e)
