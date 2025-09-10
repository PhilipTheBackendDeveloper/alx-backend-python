#!/usr/bin/env python3
"""
1-with_db_connection.py

Provides a decorator `with_db_connection` that:
 - opens a sqlite3 connection to "users.db" if no connection is supplied,
 - injects the connection into the wrapped function as the first argument,
 - ensures the connection opened by the decorator is closed after the function finishes
   (even if the function raises).

If the caller passes an existing `conn=` keyword argument, the decorator will use that
connection and will NOT close it (caller is responsible for closing it).
"""

import sqlite3
import functools
from typing import Any, Callable, Optional, Tuple


def with_db_connection(func: Callable) -> Callable:
    """
    Decorator that manages a sqlite3 connection for the wrapped function.

    Behavior:
    - If caller passes conn=<sqlite3.Connection> in kwargs, the decorator will call the
      function using that connection and will NOT close it.
    - Otherwise the decorator will:
        * open a connection to 'users.db'
        * call the function with the connection injected as the first positional argument
          (i.e. func(conn, *args, **kwargs))
        * always close the connection (in a finally block)

    The decorator preserves the wrapped function's metadata using functools.wraps.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # If a connection was explicitly provided via keyword args, use it and don't close it.
        if 'conn' in kwargs and kwargs['conn'] is not None:
            return func(*args, **kwargs)

        conn: Optional[sqlite3.Connection] = None
        try:
            conn = sqlite3.connect("users.db")
            # Inject connection as the first positional argument
            return func(conn, *args, **kwargs)
        finally:
            if conn:
                conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn: sqlite3.Connection, user_id: int) -> Optional[Tuple[Any, ...]]:
    """
    Example function that expects a DB connection as first argument and an integer user_id
    as the second. Returns the fetched row or None.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


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
    # Prepare a small DB so you can run this script immediately
    _ensure_sample_db()

    # Call decorated function WITHOUT passing a connection (decorator opens & closes it)
    user = get_user_by_id(user_id=1)
    print("User id=1 ->", user)

    # Demonstrate calling with an existing connection (decorator won't close it)
    conn = sqlite3.connect("users.db")
    try:
        user2 = get_user_by_id(conn=conn, user_id=2)
        print("User id=2 (using provided conn) ->", user2)
    finally:
        conn.close()
